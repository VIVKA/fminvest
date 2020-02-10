import time
import requests
from datetime import datetime
from lxml import html
from app import db
from app.models.sector import ru_stock_sector
from app.models.asset import AssetModel
from app.models.asset_data import AssetDataModel
from sqlalchemy.exc import IntegrityError


def get_dividend_data(ticker):
    url = 'https://dohod.ru/ik/analytics/dividend/{}'.format(ticker.lower())

    page = None
    try:
        page = requests.get(url, timeout=1.0)
    except requests.exceptions.Timeout:
        print('Timeout on dividend data for {}'.format(ticker))
        return {}

    if page.status_code != 200:
        print('No dividend data found for {}'.format(ticker))
        return {}

    tree = html.fromstring(page.content)
    datatable = tree.xpath('//table[@class="content-table"][last()]')[0]
    trs = datatable.xpath('tr[position()>1]')

    out = {}
    for tr in trs:
        tds = tr.xpath('td')
        try:
            date = datetime.strptime(
                    tds[0].text.strip(), '%d.%m.%Y').strftime('%Y-%m-%d')
            amount = float(tds[2].text)
            if not out.get(date):
                out[date] = 0
            out[date] += amount
        except Exception:
            continue

    return out


def get_stock_data(symbol, date_from=None):
    dividend_data = get_dividend_data(symbol)

    data = []
    columns = None
    start = 0
    while True:
        query_data = run_stock_query(symbol, start, date_from)
        data += query_data['data']

        if not columns:
            columns = query_data['columns']

        if(len(query_data['data']) != 100):
            break

        start += 100
        time.sleep(1)

    def pf(xs):
        if(not(
            xs[columns.index('OPEN')] and
            xs[columns.index('LOW')] and
            xs[columns.index('HIGH')] and
            xs[columns.index('LEGALCLOSEPRICE')]
        )):
            return None

        dividend = 0
        if dividend_data.get(xs[columns.index('TRADEDATE')]):
            dividend = float(dividend_data.get(xs[columns.index('TRADEDATE')]))

        return [
            xs[columns.index('TRADEDATE')],
            xs[columns.index('OPEN')],
            xs[columns.index('HIGH')],
            xs[columns.index('LOW')],
            xs[columns.index('LEGALCLOSEPRICE')],  # TODO factor in splits?
            xs[columns.index('VOLUME')],
            dividend,
            1.0,  # TODO split coeff.
        ]

    parsed_data = list(map(pf, data))
    parsed_data = [i for i in parsed_data if i is not None]
    return parsed_data


def get_stock_full_name(symbol):
    q = 'https://iss.moex.com/iss/securities/{security}.{fmt}'.format(security=symbol, fmt='json')
    d = requests.get(q).json()
    d = d['description']['data']
    name = list(filter(lambda i: i[0] == 'NAME', d))[0][2]
    return name


def run_stock_query(symbol, start, date_from=None):
    if not date_from:
        date_from = '2010-01-01'
    else:
        date_from = date_from.date().isoformat()

    # https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/TQBR/securities/aflt?limit=1&sort_order_desc=desc
    base_url = (
        'https://iss.moex.com/iss/history/engines/'
        '{engine}/markets/{market}/boards/{board}/securities/{security}.{fmt}'
    ).format(
        engine='stock',
        market='shares',
        board='TQBR',
        security=symbol,
        fmt='json'
    )

    query = 'from={date_from}&start={start}'.format(
        date_from=date_from,
        start=start,
    )

    url_query = '{}?{}'.format(base_url, query)
    response_json = requests.get(url_query).json()

    return response_json['history']


def save_stock_data_daily_db(ticker, date_from=None):
    asset = touch_stock_db(ticker)
    asset_data = get_stock_data(ticker, date_from)

    for d in asset_data:
        ad = AssetDataModel(
            asset_id=asset.id,
            trade_date=d[0],
            open_price=d[1],
            high_price=d[2],
            low_price=d[3],
            close_price=d[4],
            adjusted_close_price=d[4],
            trade_volume=d[5],
            dividend_amount=d[6],
            split_coefficient=d[7],
        )
        try:
            db.session.add(ad)
            db.session.commit()
        except IntegrityError:
            print('{} already exists'.format(d[0]))
            db.session.rollback()

    asset.updated_at = 'now()'
    db.session.add(asset)
    db.session.commit()
    print('{} done!'.format(ticker))


def run_index_query(symbol, start, date_from=None):
    if not date_from:
        date_from = '2010-01-01'
    else:
        date_from = date_from.date().isoformat()

    # https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/TQBR/securities/aflt?limit=1&sort_order_desc=desc
    base_url = (
        'https://iss.moex.com/iss/history/engines/'
        '{engine}/markets/{market}/boards/{board}/securities/{security}.{fmt}'
    ).format(
        engine='stock',
        market='index',
        board='SNDX',
        security=symbol,
        fmt='json'
    )

    query = 'from={date_from}&start={start}'.format(
        date_from=date_from,
        start=start,
    )

    url_query = '{}?{}'.format(base_url, query)
    response_json = requests.get(url_query).json()

    return response_json['history']


def get_index_data(symbol, date_from=None):
    data = []
    columns = None
    start = 0
    while True:
        query_data = run_index_query(symbol, start, date_from)
        data += query_data['data']

        if not columns:
            columns = query_data['columns']

        if(len(query_data['data']) != 100):
            break

        start += 100
        time.sleep(1)

    def pf(xs):
        if(not(
            xs[columns.index('OPEN')] and
            xs[columns.index('LOW')] and
            xs[columns.index('HIGH')] and
            xs[columns.index('CLOSE')]
        )):
            return None

        return [
            xs[columns.index('TRADEDATE')],
            xs[columns.index('OPEN')],
            xs[columns.index('HIGH')],
            xs[columns.index('LOW')],
            xs[columns.index('CLOSE')],
        ]

    parsed_data = list(map(pf, data))
    parsed_data = [i for i in parsed_data if i is not None]

    return parsed_data


def save_index_data_daily_db(ticker, date_from=None):
    asset_id = None
    ticker = ticker.upper()

    asset = db.session.query(
        AssetModel
    ).filter(
        AssetModel.ticker == ticker,
    ).first()

    if asset:
        asset_id = asset.id
    else:
        asset = AssetModel(
            ticker=ticker.upper(),
            asset_type='index',
            name='',
            country='RU',
            sector='',
            currency='RUB',
        )
        db.session.add(asset)
        db.session.commit()
        asset_id = asset.id

    asset_data = get_index_data(ticker, date_from)

    for d in asset_data:
        ad = AssetDataModel(
            asset_id=asset_id,
            trade_date=d[0],
            open_price=d[1],
            high_price=d[2],
            low_price=d[3],
            close_price=d[4],
            adjusted_close_price=d[4],
            trade_volume=0.0,
            dividend_amount=0.0,
            split_coefficient=1.0,
        )
        try:
            db.session.add(ad)
            db.session.commit()
        except IntegrityError:
            print('{} already exists'.format(d[0]))
            db.session.rollback()

    asset.updated_at = 'now()'
    db.session.add(asset)
    db.session.commit()
    print('{} done!'.format(ticker))


def run_bond_query(symbol, start, date_from=None):
    if not date_from:
        date_from = '2010-01-01'
    else:
        date_from = date_from.date().isoformat()

    board = 'EQOB'
    if symbol[:2] == 'SU':
        board = 'TQOB'

    base_url = (
        'https://iss.moex.com/iss/history/engines/'
        '{engine}/markets/{market}/boards/{board}/securities/{security}.{fmt}'
    ).format(
        engine='stock',
        market='bonds',
        board=board,
        security=symbol,
        fmt='json'
    )

    query = 'from={date_from}&start={start}'.format(
        date_from=date_from,
        start=start,
    )

    url_query = '{}?{}'.format(base_url, query)
    response_json = requests.get(url_query).json()

    return response_json['history']


def get_bond_data(symbol, date_from=None):
    data = []
    columns = None
    start = 0
    while True:
        query_data = run_bond_query(symbol, start, date_from)
        data += query_data['data']

        if not columns:
            columns = query_data['columns']

        if(len(query_data['data']) != 100):
            break

        start += 100
        time.sleep(1)

    def pf(xs):
        if(not(
            xs[columns.index('OPEN')] and
            xs[columns.index('LOW')] and
            xs[columns.index('HIGH')] and
            xs[columns.index('LEGALCLOSEPRICE')]
        )):
            return None

        return [
            xs[columns.index('TRADEDATE')],
            xs[columns.index('FACEVALUE')],  # ??
            xs[columns.index('OPEN')],
            xs[columns.index('HIGH')],
            xs[columns.index('LOW')],
            xs[columns.index('LEGALCLOSEPRICE')],  # TODO factor in splits?
            xs[columns.index('VOLUME')],
            xs[columns.index('YIELDCLOSE')],
            xs[columns.index('MATDATE')],
            xs[columns.index('COUPONPERCENT')],
            xs[columns.index('COUPONVALUE')],
            xs[columns.index('ACCINT')],
        ]

    parsed_data = list(map(pf, data))
    parsed_data = [i for i in parsed_data if i is not None]

    return parsed_data


def save_bond_data_daily_db(ticker, date_from=None):
    asset_id = None
    ticker = ticker.upper()

    asset = db.session.query(
        AssetModel
    ).filter(
        AssetModel.ticker == ticker,
    ).first()

    if asset:
        asset_id = asset.id
    else:
        asset = AssetModel(
            ticker=ticker.upper(),
            asset_type='bond',
            name='',
            country='RU',
            sector='',
            currency='RUB',
        )
        db.session.add(asset)
        db.session.commit()
        asset_id = asset.id

    asset_data = get_bond_data(ticker, date_from)

    last_coupon = None
    for d in asset_data:
        acc = float(d[11])
        coupon_value = d[10]

        # order important
        dividend_amount = 0
        if acc == 0:
            if last_coupon:
                dividend_amount = last_coupon
            else:
                dividend_amount = coupon_value

        last_coupon = coupon_value
        #

        ad = AssetDataModel(
            asset_id=asset_id,
            trade_date=d[0],
            open_price=acc + (float(d[1]) * float(d[2]) / 100),
            high_price=acc + (float(d[1]) * float(d[3]) / 100),
            low_price=acc + (float(d[1]) * float(d[4]) / 100),
            close_price=acc + (float(d[1]) * float(d[5]) / 100),
            adjusted_close_price=acc + (float(d[1]) * float(d[5]) / 100),
            trade_volume=d[6],
            maturity_date=d[8],
            coupon_percent=d[9],
            coupon_value=d[10],
            yield_amount=d[7],
            dividend_amount=dividend_amount,
            split_coefficient=1.0,
            accrued_interest=d[11],
        )
        try:
            db.session.add(ad)
            db.session.commit()
        except IntegrityError:
            print('{} already exists'.format(d[0]))
            db.session.rollback()

    asset.updated_at = 'now()'
    db.session.add(asset)
    db.session.commit()
    print('{} done!'.format(ticker))


def touch_stock_db(ticker):
    ticker = ticker.upper()

    asset = db.session.query(
        AssetModel
    ).filter(
        AssetModel.ticker == ticker,
    ).first()

    if not asset:
        name = get_stock_full_name(ticker)
        sector = ru_stock_sector(ticker)
        asset = AssetModel(
            ticker=ticker.upper(),
            asset_type='stock',
            name=name,
            country='RU',
            sector=sector,
            currency='RUB',
        )
        db.session.add(asset)
        db.session.commit()

    return asset


def repair_stock_data_daily_db(ticker, date_from=None):
    asset = touch_stock_db(ticker)
    asset_data = get_stock_data(ticker, date_from)

    dividends = filter(lambda x: (x[6] > 0), asset_data)

    for item in dividends:
        try:
            ad = db.session.query(AssetDataModel).filter_by(trade_date=item[0], asset_id=asset.id).first()

            if item[6] != ad.dividend_amount:
                print('{} dividend new: {}, old: {}'.format(ad.trade_date, item[6], ad.dividend_amount))
                ad.dividend_amount = item[6]

            db.session.add(ad)
            db.session.commit()
        except IntegrityError as e:
            print(e)
            db.session.rollback()

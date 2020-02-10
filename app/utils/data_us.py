import json
import requests
from datetime import datetime
from app import db
from app.models.sector import get_gics_from_iax_sector
from app.models.asset import AssetModel
from app.models.asset_data import AssetDataModel
from app.models.currency_pair import CurrencyPairModel
from app.models.currency_pair_data import CurrencyPairDataModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_


def run_currency_query(symbol_from, symbol_to, **kwargs):
    ALPHAVANTAGE_API_KEY = '1UH8FHIQ1YCSALSS'
    base_url = 'https://www.alphavantage.co/query'
    function = kwargs.get('function', 'FX_DAILY')
    outputsize = kwargs.get('outputsize', 'compact')
    datatype = kwargs.get('datatype', 'json')

    query = (
        '{}?function={}&from_symbol={}&to_symbol={}&outputsize={}'
        '&datatype={}&apikey={}'
    ).format(
        base_url, function, symbol_from, symbol_to, outputsize,
        datatype, ALPHAVANTAGE_API_KEY
    )

    return requests.get(query).text


def get_currency_data(symbol_from, symbol_to, date_from=None):
    outputsize = 'full'

    if date_from and (datetime.today().date() - date_from.date()).days < 100:
        outputsize = 'compact'

    response = run_currency_query(
        symbol_from, symbol_to,
        function='FX_DAILY',
        outputsize=outputsize
    )

    json_data = json.loads(response)

    try:
        series_data = json_data['Time Series FX (Daily)']
    except Exception:
        print(json_data)

    ds = [
        [
            d,
            float(v['1. open']),
            float(v['2. high']),
            float(v['3. low']),
            float(v['4. close']),
        ]
        for (d, v) in series_data.items()
        if datetime.strptime(d, '%Y-%m-%d') >= date_from
    ]

    ds = list(reversed(ds))
    return ds


def save_currency_pair_data_daily_db(symbol_from, symbol_to, date_from=None):
    currency_pair_id = None
    symbol_from = symbol_from.upper()
    symbol_to = symbol_to.upper()

    currency_pair = db.session.query(
        CurrencyPairModel
    ).filter(
        and_(
            CurrencyPairModel.symbol_from == symbol_from,
            CurrencyPairModel.symbol_to == symbol_to,
        )
    ).first()

    if currency_pair:
        currency_pair_id = currency_pair.id
    else:
        currency_pair = CurrencyPairModel(
            currency_type="fiat",
            symbol_from=symbol_from.upper(),
            symbol_to=symbol_to.upper(),
        )
        db.session.add(currency_pair)
        db.session.commit()
        currency_pair_id = currency_pair.id

    currency_pair_data = get_currency_data(symbol_from, symbol_to, date_from)

    for d in currency_pair_data:
        ad = CurrencyPairDataModel(
            currency_pair_id=currency_pair_id,
            trade_date=d[0],
            open_price=d[1],
            high_price=d[2],
            low_price=d[3],
            close_price=d[4],
        )
        try:
            db.session.add(ad)
            db.session.commit()
        except IntegrityError:
            print('{} already exists'.format(d[0]))
            db.session.rollback()

    currency_pair.updated_at = 'now()'
    db.session.add(currency_pair)
    db.session.commit()
    print('{}/{} done!'.format(symbol_from, symbol_to))


def run_crypto_query(symbol_from, symbol_to, **kwargs):
    ALPHAVANTAGE_API_KEY = '1UH8FHIQ1YCSALSS'
    base_url = 'https://www.alphavantage.co/query'
    function = kwargs.get('function', 'DIGITAL_CURRENCY_DAILY')
    outputsize = kwargs.get('outputsize', 'compact')
    datatype = kwargs.get('datatype', 'json')

    query = (
        '{}?function={}&symbol={}&market={}&outputsize={}'
        '&datatype={}&apikey={}'
    ).format(
        base_url, function, symbol_from, symbol_to, outputsize,
        datatype, ALPHAVANTAGE_API_KEY
    )

    return requests.get(query).text


def get_crypto_data(symbol_from, symbol_to, date_from=None):
    outputsize = 'full'

    if date_from and (datetime.today().date() - date_from.date()).days < 100:
        outputsize = 'compact'

    response = run_crypto_query(
        symbol_from, symbol_to,
        function='DIGITAL_CURRENCY_DAILY',
        outputsize=outputsize
    )

    json_data = json.loads(response)

    try:
        series_data = json_data['Time Series (Digital Currency Daily)']
    except Exception:
        print(json_data)

    ds = [
        [
            d,
            float(v['1a. open ({})'.format(symbol_to)]),
            float(v['2a. high ({})'.format(symbol_to)]),
            float(v['3a. low ({})'.format(symbol_to)]),
            float(v['4a. close ({})'.format(symbol_to)]),
        ]
        for (d, v) in series_data.items()
        if datetime.strptime(d, '%Y-%m-%d') >= date_from
    ]

    ds = list(reversed(ds))
    return ds


def save_crypto_currency_pair_data_daily_db(symbol_from, symbol_to, date_from=None):
    currency_pair_id = None
    symbol_from = symbol_from.upper()
    symbol_to = symbol_to.upper()

    currency_pair = db.session.query(
        CurrencyPairModel
    ).filter(
        and_(
            CurrencyPairModel.symbol_from == symbol_from,
            CurrencyPairModel.symbol_to == symbol_to,
        )
    ).first()

    if currency_pair:
        currency_pair_id = currency_pair.id
    else:
        currency_pair = CurrencyPairModel(
            currency_type="crypto",
            symbol_from=symbol_from.upper(),
            symbol_to=symbol_to.upper(),
        )
        db.session.add(currency_pair)
        db.session.commit()
        currency_pair_id = currency_pair.id

    currency_pair_data = get_crypto_data(symbol_from, symbol_to, date_from)

    for d in currency_pair_data:
        ad = CurrencyPairDataModel(
            currency_pair_id=currency_pair_id,
            trade_date=d[0],
            open_price=d[1],
            high_price=d[2],
            low_price=d[3],
            close_price=d[4],
        )
        try:
            db.session.add(ad)
            db.session.commit()
        except IntegrityError:
            print('{} already exists'.format(d[0]))
            db.session.rollback()

    currency_pair.updated_at = 'now()'
    db.session.add(currency_pair)
    db.session.commit()
    print('{}/{} done!'.format(symbol_from, symbol_to))


def run_stock_query(ticker, **kwargs):
    ALPHAVANTAGE_API_KEY = '1UH8FHIQ1YCSALSS'
    base_url = 'https://www.alphavantage.co/query'
    function = kwargs.get('function', 'TIME_SERIES_DAILY_ADJUSTED')
    outputsize = kwargs.get('outputsize', 'compact')
    datatype = kwargs.get('datatype', 'json')

    query = (
        '{}?function={}&symbol={}&outputsize={}'
        '&datatype={}&apikey={}'
    ).format(
        base_url, function, ticker,
        outputsize, datatype, ALPHAVANTAGE_API_KEY
    )

    return requests.get(query).text


def get_iex_company_data(ticker, **kwargs):
    ticker = ticker.strip()
    query = 'https://api.iextrading.com/1.0/stock/{}/company'.format(ticker)
    response = requests.get(query).text
    return json.loads(response)


def get_stock_data(ticker, date_from=None):
    outputsize = 'full'

    if date_from and (datetime.today().date() - date_from.date()).days < 100:
        outputsize = 'compact'

    response = run_stock_query(
        ticker,
        function='TIME_SERIES_DAILY_ADJUSTED',
        outputsize=outputsize
    )

    json_data = json.loads(response)

    try:
        series_data = json_data['Time Series (Daily)']
    except Exception:
        print(json_data)

    ds = [
        [
            d,
            float(v['1. open']),
            float(v['2. high']),
            float(v['3. low']),
            float(v['4. close']),
            float(v['5. adjusted close']),
            float(v['6. volume']),
            float(v['7. dividend amount']),
            float(v['8. split coefficient']),
        ]
        for (d, v) in series_data.items()
        if datetime.strptime(d, '%Y-%m-%d') >= date_from
    ]

    ds = list(reversed(ds))

    return ds


def touch_stock_db(ticker):
    ticker = ticker.upper()

    asset = db.session.query(
        AssetModel
    ).filter(
        AssetModel.ticker == ticker,
    ).first()

    if not asset:
        asset_data = get_iex_company_data(ticker)
        sector = get_gics_from_iax_sector(asset_data['sector'])
        asset = AssetModel(
            ticker=ticker.upper(),
            asset_type='stock',
            name=asset_data['companyName'],
            country='US',
            sector=sector,
            currency='USD',
        )
        db.session.add(asset)
        db.session.commit()

    return asset


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
            adjusted_close_price=d[5],
            trade_volume=d[6],
            dividend_amount=d[7],
            split_coefficient=d[8],
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


def repair_stock_data_daily_db(ticker, date_from=None):
    asset = touch_stock_db(ticker)
    asset_data = get_stock_data(ticker, date_from)

    dividends_and_splits = filter(lambda x: (x[7] > 0 or x[8] != 1), asset_data)

    for item in dividends_and_splits:
        try:
            ad = db.session.query(AssetDataModel).filter_by(trade_date=item[0], asset_id=asset.id).first()

            if item[7] != ad.dividend_amount:
                print('{} dividend new: {}, old: {}'.format(ad.trade_date, item[7], ad.dividend_amount))
                ad.dividend_amount = item[7]

            if item[8] != ad.split_coefficient:
                print('{} split new: {}, old: {}'.format(ad.trade_date, item[8], ad.split_coefficient))
                ad.split_coefficient = item[8]

            db.session.add(ad)
            db.session.commit()
        except IntegrityError as e:
            print(e)
            db.session.rollback()

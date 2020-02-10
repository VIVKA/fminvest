import time
import pandas as pd
import numpy as np
import datetime
import requests
import random
import dateutil
from dateutil.relativedelta import relativedelta
from functools import wraps
from app import db
from app.utils import data_us
from app.utils import data_ru
from app.utils.asset import Asset
from app.models.asset import AssetModel
from app.models.portfolio import PortfolioModel
from app.models.currency_pair import CurrencyPairModel
from sqlalchemy.sql import text


def timeit(method):
    @wraps(method)
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('{}  {:2.2f} ms'.format(method.__name__, (te - ts) * 1000))
        return result
    return timed


def get_asset_return(asset):
    today_date = datetime.datetime.today()
    back_date = datetime.datetime.today() + relativedelta(years=-3)

    return asset.ry(back_date.year, today_date.year)


def get_asset_yield(asset):
    today_date = datetime.datetime.today()

    return asset.yy(today_date.year-3, today_date.year)


def current_values(assets):
    return np.array([asset.adjusted_close_price() for asset in assets])


def weights(assets, quantities):
    w = np.array(quantities)
    w = w * current_values(assets)
    tv = total_value(assets, quantities)
    if tv > 0:
        return w / tv

    return w


def current_returns(assets):
    return np.array([get_asset_return(asset) for asset in assets])


def current_yields(assets):
    return np.array([get_asset_yield(asset) for asset in assets])


def asset_values_at(assets, date):
    return np.array([asset.adjusted_close_price(date) for asset in assets])


def total_value_at(assets, quantities, date):
    return np.dot(asset_values_at(assets, date), quantities)


def total_value(assets, quantities):
    return np.dot(current_values(assets), quantities)


def total_return(assets, weights):
    return np.dot(current_returns(assets), weights)


def total_yield(assets, weights):
    return np.dot(current_yields(assets), weights)


def covariance(assets):
    today_date = datetime.datetime.today()
    back_date = datetime.datetime.today() + relativedelta(years=-3)

    data_frame = {}
    tickers = list(map(lambda a: a.ticker, assets))
    for asset in assets:
        data_frame[asset.ticker] = asset.adjusted_pct_change(back_date.year, today_date.year)
    df = pd.DataFrame(data_frame, columns=tickers)
    cov = df.cov()
    return cov * 252


def variance(assets, weights):
    cov = covariance(assets)
    weights = np.array(weights)
    return np.dot(weights.T, np.dot(cov, weights))


def stdev(assets, weights):
    return np.sqrt(variance(assets, weights))


def utility(assets, weights):
    # power utility function
    # U(µW, σ2W) = µW − σ2W * γ/2
    # return - variance * aversion_factor / 2

    tr = total_return(assets, weights) * 1
    ty = total_yield(assets, weights) * 1.1
    r = tr + ty
    v = variance(assets, weights)
    aversion = 2.5

    return r - v * (aversion / 2)


def sharpe(assets, weights):
    return total_return(assets, weights) / stdev(assets, weights)


def certainty_eq_value(assets, quantities):
    w = weights(assets, quantities)
    u = utility(assets, w)
    return total_value(assets, quantities) * (1 + u)


def certainty_eq_cost(assets, quantities_from, weights_to):
    weights_from = weights(assets, quantities_from)
    u_from = utility(assets, weights_from)
    u_to = utility(assets, weights_to)
    tv = total_value(assets, quantities_from)
    return tv * (u_to - u_from)


def generate_portfolio_weights(size, precision):
    lower_bound = 0.1/size  # 1/5x equal
    upper_bound = 2/size  # 2x equal

    total = 1.0
    ws = np.zeros(size)
    for i in range(size):
        w = np.random.uniform(lower_bound, upper_bound)

        if i == size-1:
            if total < upper_bound:
                ws[i] = total
                total = 0
            else:
                ws[i] = w
                total -= w
            continue

        if (total - w) < (lower_bound * (size - (i+1))):
            w = lower_bound
            total -= w
            ws[i] = w
            continue

        ws[i] = w
        total -= w

    while total > 0:
        ws = sorted(ws)
        for i in range(size):
            w = np.random.uniform(0, upper_bound - ws[i])
            if w < total:
                ws[i] += w
                total -= w
            else:
                ws[i] += total
                total = 0
                break

    np.random.shuffle(ws)
    ws = np.around(ws, precision)
    return ws


def fail_weight_bound(ws):
    lb = 0.005
    ub = 1.75 / len(ws)
    if next(filter(lambda w: w < lb or w > ub, ws), None):
        return True


def fail_lower_weight_bound(ws):
    b = 0.005
    if next(filter(lambda w: w < b, ws), None):
        return True


def fail_upper_weight_bound(ws):
    b = 1.5 / len(ws)

    if next(filter(lambda w: w > b, ws), None):
        return True


def allocate(assets, quantities_from, weights_to, amount):
    weights_from = np.array(weights(assets, quantities_from))
    weights_to = np.array(weights_to)
    # cv = current_values(assets)
    tv = total_value(assets, quantities_from)
    ntv = tv + amount
    cf = tv / ntv

    weights_from_new = weights_from * cf
    weight_difference = weights_to - weights_from_new
    quantities_diff = weight_difference * ntv

    enum_quantities_diff = list(enumerate(np.round(quantities_diff)))
    enum_quantities_diff_filtered = \
        list(filter(lambda v: v[1] > 0, enum_quantities_diff))

    sorted_orders = sorted(enum_quantities_diff_filtered, key=lambda p: -p[1])

    to_buy = []
    for (position, amount_limit) in sorted_orders:
        asset = assets[position]

        if amount_limit < amount:
            num_to_buy = np.floor(amount_limit / asset.close_price())
        else:
            num_to_buy = np.floor(amount / asset.close_price())

        if num_to_buy <= 0:
            continue

        num_to_buy = int(num_to_buy)

        cost = num_to_buy * asset.close_price() * 1.0035  # TODO assuming 0.035% fee
        to_buy.append([asset.ticker, num_to_buy, cost])
        amount -= cost

    return to_buy


def update_ru_asset_data(days_back=1):
    days_back = int(days_back)
    date_from = datetime.datetime.today() - datetime.timedelta(days=days_back)

    assets = db.session.query(
        AssetModel
    ).filter_by(
        country='RU',
    ).all()

    for i, a in enumerate(assets):
        print('RU {}/{}: {} {}'.format(i+1, len(assets), a.country, a.ticker))

        time.sleep(2)
        if a.asset_type == 'stock':
            time.sleep(2)
            data_ru.save_stock_data_daily_db(a.ticker, date_from)
        if a.asset_type == 'bond':
            data_ru.save_bond_data_daily_db(a.ticker, date_from)
        if a.asset_type == 'index':
            data_ru.save_index_data_daily_db(a.ticker, date_from)


def update_us_asset_data(days_back=1):
    days_back = int(days_back)
    date_from = datetime.datetime.today() - datetime.timedelta(days=days_back)

    assets = db.session.query(
        AssetModel
    ).filter_by(
        country='US',
    ).all()

    for i, a in enumerate(assets):
        print('US {}/{}: {} {}'.format(i+1, len(assets), a.country, a.ticker))

        time.sleep(15)
        data_us.save_stock_data_daily_db(a.ticker, date_from)


def repair_us_asset_data(days_back=1):
    days_back = int(days_back)
    date_from = datetime.datetime.today() - datetime.timedelta(days=days_back)

    assets = db.session.query(
        AssetModel
    ).filter_by(
        country='US',
    ).all()

    for i, a in enumerate(assets):
        print('US {}/{}: {} {}'.format(i+1, len(assets), a.country, a.ticker))

        time.sleep(15)
        data_us.repair_stock_data_daily_db(a.ticker, date_from)


def repair_ru_asset_data(days_back=1):
    days_back = int(days_back)
    date_from = datetime.datetime.today() - datetime.timedelta(days=days_back)

    assets = db.session.query(
        AssetModel
    ).filter_by(
        country='RU',
    ).all()

    for i, a in enumerate(assets):
        print('RU {}/{}: {} {}'.format(i+1, len(assets), a.country, a.ticker))

        time.sleep(2)
        if a.asset_type == 'stock':
            time.sleep(2)
            data_ru.repair_stock_data_daily_db(a.ticker, date_from)


def update_currencies_data(days_back=1):
    days_back = int(days_back)
    date_from = datetime.datetime.today() - datetime.timedelta(days=days_back)

    currency_pairs = db.session.query(
        CurrencyPairModel
    ).all()

    for i, a in enumerate(currency_pairs):
        print('{}/{}: {}/{}'.format(i+1, len(currency_pairs), a.symbol_from, a.symbol_to))

        time.sleep(3)
        if a.currency_type == 'fiat':
            data_us.save_currency_pair_data_daily_db(a.symbol_from, a.symbol_to, date_from)
        if a.currency_type == 'crypto':
            data_us.save_crypto_currency_pair_data_daily_db(a.symbol_from, a.symbol_to, date_from)


def alphavantage_query(function, **kwargs):
    ALPHAVANTAGE_API_KEY = '1UH8FHIQ1YCSALSS'

    function = function
    base_url = 'https://www.alphavantage.co/query'

    key_value_list = [
        '{}={}'.format(key, value)
        for (key, value) in kwargs.items()
    ]

    params = '&'.join(key_value_list)
    query = '{}?function={}&{}&apikey={}'.format(
        base_url, function, params, ALPHAVANTAGE_API_KEY
    )

    return requests.get(query).json()


def annuity(yearly_rate, months):
    rate = yearly_rate / 12
    g = (1 + rate) ** months
    ac = rate * g / (g-1)
    return ac


def get_weekly_asset_data(asset, f, t):
    today_date = datetime.datetime.today()
    today_date = today_date.year
    close_data = asset._data[str(f):str(t)]['close']

    if len(close_data) == 0:
        return []

    out = close_data.resample('D').mean().pct_change()

    _out = []
    acc = 1
    for tu in out.items():
        if not np.isnan(tu[1]):
            acc *= 1+float(tu[1])
        _out.append([tu[0].isoformat(), acc])

    return _out


@timeit
def get_weekly_portfolio_data(portfolio, f, t):
    today_date = datetime.datetime.today()
    today_date = today_date.year
    close_data = portfolio.close_data(f, t)

    if len(close_data) == 0:
        return []

    out = close_data.resample('D').last().pct_change()
    _out = []
    acc = 1
    for tu in out.iterrows():
        acc *= 1+float(np.sum(tu[1]*portfolio.w))
        _out.append([tu[0].isoformat(), acc])

    return _out


def warm_caches():
    print("warming caches...")
    assets = db.session.query(
        AssetModel
    ).filter(
        AssetModel.asset_type.in_(('bond', 'stock'))
    ).all()

    # select a log-proportional amount of all assets at random
    n = int(np.log(len(assets))*10)
    random.shuffle(assets)
    assets_to_cache = assets[:n]

    for i, a in enumerate(assets_to_cache):
        get_asset(a.ticker)
        print('{}/{}: {} {} {}'.format(i+1, len(assets_to_cache), a.country, a.asset_type, a.ticker))


def get_portfolio_data(account_id, portfolio_id):
    portfolio = db.session.query(
        PortfolioModel
    ).filter(
        PortfolioModel.id == portfolio_id
    ).first()

    return portfolio


def get_portfolio_actions(account_id, portfolio_id):
    q = (
        'SELECT assets.id, assets.ticker, portfolio_actions.amount, '
        'portfolio_actions.action_type, portfolio_actions.price, '
        'portfolio_actions.action_at '
        'FROM portfolio_actions '
        'JOIN assets ON portfolio_actions.asset_id = assets.id '
        'JOIN portfolios ON portfolio_actions.portfolio_id = portfolios.id '
        'WHERE portfolio_actions.portfolio_id = :portfolio_id '
        'AND portfolios.account_id = :account_id '
        'ORDER BY portfolio_actions.action_at ASC'
    )
    result = db.engine.execute(
        text(q), account_id=account_id, portfolio_id=portfolio_id)

    out = [
        {
            'action_type': action[3],
            'ticker': action[1],
            'amount': action[2],
            'price': action[4],
            'action_date': action[5].replace(tzinfo=None),  # TODO: timezones relevant?
        }
        for action in list(result)
    ]

    return out


def get_portfolio_grouped_actions(account_id, portfolio_id):
    portfolio_actions = get_portfolio_actions(account_id, portfolio_id)

    grouped_actions = {}
    for action in portfolio_actions:
        ticker = action['ticker']
        if ticker not in grouped_actions:
            grouped_actions[ticker] = []

        grouped_actions[ticker].append(action)

    return grouped_actions


def get_asset_split_actions(asset):
    split_actions = []
    for d, v in asset.splits:
        split = {
            'action_type': 'SPLIT',
            'ticker': asset.ticker,
            'split_factor': v,
            'action_date': d.to_pydatetime(),
        }
        split_actions.append(split)
    return split_actions


def get_asset_dividend_actions(asset):
    dividend_actions = []
    for d, v in asset.dividends:
        split = {
            'action_type': 'DIVIDEND',
            'ticker': asset.ticker,
            'dividend': v,
            'action_date': d.to_pydatetime(),
        }
        dividend_actions.append(split)
    return dividend_actions


def get_portfolio_asset_quantities(account_id, portfolio_id):
    portfolio_actions = get_portfolio_grouped_actions(account_id, portfolio_id)

    aggregates = {}
    for ticker, actions in portfolio_actions.items():
        a = get_asset(ticker)
        splits = get_asset_split_actions(a)

        queue = actions + splits
        sorted_action_queue = sorted(queue, key=lambda item: item['action_date'])

        aggregates[ticker] = 0

        for action in sorted_action_queue:
            if action['action_type'] == 'SPLIT':
                aggregates[ticker] *= action['split_factor']

            if action['action_type'] == 'BUY':
                aggregates[ticker] += action['amount']

            if action['action_type'] == 'SELL':
                aggregates[ticker] -= action['amount']

    assets = list(map(lambda a: get_asset(a), aggregates.keys()))
    quantities = list(aggregates.values())

    return assets, quantities


@timeit
def get_portfolio_history(account_id, portfolio_id, f=None, t=None):
    # GET ALL PORTFOLIO ACTIONS
    portfolio_actions = get_portfolio_actions(account_id, portfolio_id)

    # EARLY EXIT IF NO ACTIONS
    if len(portfolio_actions) == 0:
        return []

    # COLLECT SPLIT AND DIVIDEND ACTIONS
    asset_actions = []
    asset_lookup = {}
    for ticker in set([a['ticker'] for a in portfolio_actions]):
        asset = get_asset(ticker)
        asset_lookup[ticker] = asset
        asset_actions += get_asset_split_actions(asset)
        # asset_actions += get_asset_dividend_actions(asset)

    # GET HISTORY RANGE
    portfolio_actions = sorted(portfolio_actions, key=lambda item: item['action_date'])
    d0 = portfolio_actions[0]['action_date']  # first action date
    d1 = datetime.datetime.today()
    delta = d1 - d0

    # DROP OLDER ASSET ACTIONS
    filtered_asset_actions = list(filter(lambda item: item['action_date'] >= d0, asset_actions))

    # COMBINE AND SORT ALL ACTIONS
    sorted_portfolio_actions = sorted(portfolio_actions + filtered_asset_actions, key=lambda item: item['action_date'])

    # HELL LOOP
    portfolio = {}
    series = {}
    previous_value = None
    for i in range(delta.days + 1):
        d = d0 + datetime.timedelta(i)

        # MAIN
        assets = [asset_lookup[t] for t in portfolio.keys()]
        quantities = list(portfolio.values())
        current_date = d.date()

        current_total_value = None
        try:
            current_total_value = total_value_at(assets, quantities, current_date)
        except Exception as e:
            # TODO: is this all? just weekends/holidays?
            current_total_value = previous_value

        change = 1  # no change
        if previous_value:
            change = current_total_value / previous_value

        series[current_date] = (current_total_value, change)

        # PORTFOLIO EVENT LOOP
        need_update = False
        while len(sorted_portfolio_actions) > 0 and sorted_portfolio_actions[0]['action_date'] == d:
            need_update = True
            action = sorted_portfolio_actions.pop(0)
            ticker = action['ticker']

            if ticker not in portfolio:
                portfolio[ticker] = 0

            if action['action_type'] == 'SPLIT':
                if portfolio[ticker]:
                    portfolio[ticker] *= action['split_factor']

            if action['action_type'] == 'BUY':
                portfolio[ticker] += action['amount']

            if action['action_type'] == 'SELL':
                portfolio[ticker] -= action['amount']

        # POST LOOP
        if need_update:
            assets = [asset_lookup[t] for t in portfolio.keys()]
            quantities = list(portfolio.values())

            try:
                current_total_value = total_value_at(assets, quantities, current_date)
            except Exception as e:
                # TODO: is this all? just weekends/holidays?
                pass

        previous_value = current_total_value

    # PREPARE RESULTS
    _out = []
    acc = 1
    __f = datetime.datetime.strptime(f, '%Y-%m-%d').date()
    __series = [it for it in series.items() if it[0] >= __f]
    for item in __series:
        acc *= item[1][1]
        _out.append([item[0], acc, item[1][0]])

    return _out

    # today_date = datetime.datetime.today()
    # today_date = today_date.year
    # if not f:
    #     back_date = datetime.datetime.today() + relativedelta(years=-1)
    #     f = back_date
    # if not t:
    #     future_date = datetime.datetime.today() + relativedelta(years=+1)
    #     t = future_date

    # close_data = portfolio.close_data(f, t)

    # if len(close_data) == 0:
    #     return []

    # out = close_data.resample('D').last().pct_change()
    # _out = []
    # acc = 1
    # for tu in out.iterrows():
    #     acc *= 1+float(np.sum(tu[1]*portfolio.w))
    #     _out.append([tu[0].isoformat(), acc])

    # return _out


def get_portfolio_capital_gain(account_id, portfolio_id):
    portfolio_actions = get_portfolio_grouped_actions(account_id, portfolio_id)

    aggregates = {}
    for ticker, actions in portfolio_actions.items():
        a = get_asset(ticker)

        splits = get_asset_split_actions(a)

        queue = actions + splits
        sorted_queue = sorted(queue, key=lambda item: item['action_date'])

        positions = []  # [[amount, price], ...]
        for action in sorted_queue:
            if action['action_type'] == 'BUY':
                positions.append([action['amount'], action['price']])
            if action['action_type'] == 'SELL':
                # FIFO SELL
                sell_amount = action['amount']
                while sell_amount > 0:
                    if len(positions) == 0:
                        break

                    if positions[0][0] <= sell_amount:
                        sell_amount -= positions[0][0]
                        positions.pop(0)
                        continue

                    if positions[0][0] > sell_amount:
                        positions[0][0] -= sell_amount
                        sell_amount = 0
                        continue

            if action['action_type'] == 'SPLIT':
                # JNUG split example
                # ('SPLIT', datetime.datetime(2014, 12, 23, 0, 0), 0.1),
                # ('SPLIT', datetime.datetime(2015, 10, 1, 0, 0), 0.2),
                # ('SPLIT', datetime.datetime(2016, 8, 25, 0, 0), 10.0),
                # ('SPLIT', datetime.datetime(2017, 5, 1, 0, 0), 0.25)
                positions = [
                    [
                        p[0] * action['split_factor'],
                        p[1] / action['split_factor']
                    ] for p in positions
                ]

        if ticker not in aggregates:
            aggregates[ticker] = 0

        close_price = a.close_price()
        for position in positions:
            aggregates[ticker] += (close_price - position[1]) * position[0]

    return aggregates.values()


def get_portfolio_dividends(account_id, portfolio_id):
    portfolio_actions = get_portfolio_grouped_actions(account_id, portfolio_id)

    aggregates = {}
    dividends = {}
    for ticker, trades in portfolio_actions.items():
        a = get_asset(ticker)
        splits = get_asset_split_actions(a)
        divs = get_asset_dividend_actions(a)

        queue = trades + splits + divs
        sorted_action_queue = sorted(queue, key=lambda item: item['action_date'])

        aggregates[ticker] = 0
        dividends[ticker] = 0

        for action in sorted_action_queue:
            if action['action_type'] == 'SPLIT':
                aggregates[ticker] *= action['split_factor']

            if action['action_type'] == 'BUY':
                aggregates[ticker] += action['amount']

            if action['action_type'] == 'SELL':
                aggregates[ticker] -= action['amount']

            if action['action_type'] == 'DIVIDEND':
                if action['dividend'] > 0 and aggregates[ticker] > 0:
                    dividends[ticker] += action['dividend'] * aggregates[ticker]

    return dividends.values()

US_HOLIDAY_DATES = [
    '2019-01-01', '2019-01-21', '2019-02-18',
    '2019-04-19', '2019-05-27', '2019-07-04',
    '2019-09-02', '2019-11-28', '2019-12-25',
    # '2019-11-29', '2019-12-24', '2019-07-03', # half-days
]

RU_HOLIDAY_DATES = [
    '2019-01-01', '2019-01-02', '2019-01-05',
    '2019-01-06', '2019-01-07', '2019-02-23',
    '2019-02-24', '2019-03-08', '2019-03-09',
    '2019-03-10', '2019-05-01', '2019-05-09',
    '2019-06-12', '2019-11-04',
]

def get_tx_date(holidays, date, days_back):
    tdate = dateutil.parser.parse(date) - relativedelta(days=days_back)

    while True:
        # holidays
        if tdate.date().isoformat() in holidays:
            tdate = tdate - relativedelta(days=1)
            continue

        # weekends
        if tdate.weekday() > 4:
            tdate = tdate - relativedelta(days=1)
            continue

        break

    return tdate.date().isoformat()


__asset_cache = {}
def get_asset(ticker):
    global __asset_cache

    if ticker not in __asset_cache:
        __asset_cache[ticker] = Asset(ticker)

    return __asset_cache[ticker]


def get_asset_by_id(id):
    asset = db.session.query(
        AssetModel
    ).filter(
        AssetModel.id == id
    ).first()

    return get_asset(asset.ticker)

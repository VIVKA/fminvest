import io
import data
# import portfolio
import app.utils.asset
import time
import pandas as pd
import numpy as np
import csv
import random
import datetime

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('{}  {:2.2f} ms'.format(method.__name__, (te - ts) * 1000))
        return result
    return timed

target_portfolio_content_proportions = {
    'MO': 0.136,
    'AAPL': 0.033,
    'DIS': 0.027,
    'GM': 0.034,
    'VZ': 0.021,
    'MAIN': 0.012,
    'VOO': 0.051,
    'VO': 0.183,
    'VB': 0.023,
    'VEA': 0.085,
    'VWO': 0.021,
    'ORC': 0.089,
    'AWP': 0.003,
    'OHI': 0.054,
    'EXG': 0.091,
    'MPW': 0.002,
    'BND': 0.135,
}

target_portfolio = {
    'MO':   30.00,
    'AAPL': 15.00,
    'DIS':  10.00,
    'GM':   55.00,
    'VZ':   35.00,
    'MAIN': 60.00,
    'UNIT': 150.00,
    'NAT':  180.00,
    'ORC':  500.00,
    'AWP':  400.00,
    'OHI':  100.00,
    'MPW':  100.00,
    'XOM':  40.00,
    'JNUG': 75.00,
    'EXG': 0,
    'VOO': 0,
    'VO': 0,
    'VBK': 0,
    'VEA': 0,
    'VWO': 0,
    'BND': 0,
    'VCLT': 0,
    'SLIM': 0,
}


___stock_returns = {}
def get_stock_return(ticker):
    global ___stock_returns
    if ___stock_returns.get(ticker) == None:
        ___stock_returns[ticker] = asset.Asset(ticker).ry('2013', '2018')
    return ___stock_returns[ticker]

def get_stock_daily_data(ticker, date_from, date_to):
    _pd = data.get_pd(ticker)
    spd = _pd[date_from:date_to]
    return spd

def get_portfolio_daily_data(tickers, weights, date_from, date_to):
    data_frame = pd.DataFrame()
    for ticker in tickers:
        new_data_frame = get_stock_daily_data(ticker, date_from, date_to)['adjusted_close'].pct_change()
        new_data_frame = new_data_frame.rename(ticker)
        data_frame = data_frame.join(new_data_frame.to_frame(),how='outer')

    data_frame = data_frame[tickers]
    a = data_frame * weights
    a['my_sum'] = a.select_dtypes(float).sum(1)
    return(a)


__current_values = []
def current_values(tickers):
    global __current_values
    if len(__current_values) == 0:
        __current_values = np.array([asset.Asset(ticker).price() for ticker in tickers])
    return __current_values


def weights(tickers, quantities):
    w = np.array(quantities) * current_values(tickers)
    return w / total_value(tickers, quantities)


def current_returns(tickers):
    return np.array([get_stock_return(ticker) for ticker in tickers])


def total_value(tickers, quantities):
    return np.dot(current_values(tickers), quantities)


def total_return(tickers, weights):
    return np.dot(current_returns(tickers), weights)

# TODO
___stock_covariance = pd.DataFrame()
def covariance(tickers):
    global ___stock_covariance
    if ___stock_covariance.shape[0] != len(tickers):
        data_frame = {}
        for ticker in tickers:
            data_frame[ticker] = stock.Stock(ticker).adjusted_pct_change('2013', '2018')
        df = pd.DataFrame(data_frame, columns=tickers)
        cov = df.cov()
        ___stock_covariance = cov * 252
    return ___stock_covariance


def lpm(tickers):
    threshold = 0
    order = 2

    # data_frame = {}
    # for ticker in tickers:
    for ticker in ['AAPL']:
        # data_frame[ticker] = stock.Stock(ticker).adjusted_pct_change('2013', '2018')
        new_data_frame = get_stock_daily_data(ticker, '2016-04', '2018-05')['adjusted_close'].pct_change()
        diff = threshold - new_data_frame
        diff = diff.clip(lower=0)
        print(diff)
        print(len(diff))
        _lpm = np.sum(diff**order) / len(diff)
        print(_lpm)
        print(_lpm*1000)

    # df = pd.DataFrame(data_frame, columns=tickers)

    # Set the minimum of each to 0
    #     diff = diff.clip(min=0)
    # Return the sum of the different to the power of order
    #     return numpy.sum(diff ** order) / len(returns)


def variance(tickers, weights):
    cov = covariance(tickers)
    return np.dot(weights.T, np.dot(cov, weights))


def stdev(tickers, weights):
    return np.sqrt(variance(tickers, weights))


def utility(tickers, weights):
    return total_return(tickers, weights) - variance(tickers, weights)


def sharpe(tickers, weights):
    return total_return(tickers, weights) / stdev(tickers, weights)


def certainty_eq_value(tickers, quantities):
    w = weights(tickers, quantities)
    u = utility(tickers, w)
    return total_value(tickers, quantities) * (1 + u)


def certainty_eq_cost(tickers, quantities_from, weights_to):
    weights_from = weights(tickers, quantities_from)
    u_from = utility(tickers, weights_from)
    u_to = utility(tickers, weights_to)
    tv = total_value(tickers, quantities_from)
    return tv * (u_to - u_from)


def transaction_cost(tickers, quantities_from, weights_to):
    weights_from = np.array(weights(tickers, quantities_from))
    weights_to = np.array(weights_to)
    tv = total_value(tickers, quantities_from)
    cf = tv/(tv+1000)

    weights_from = weights_from*cf
    weight_difference = weights_to - weights_from
    weight_abs = np.abs(weight_difference)

    abv = weight_abs * tv
    cfun = lambda v: max(1, v*0.0025) # avanza mini
    total_cost = sum(map(cfun, abv))

    return total_cost

def weight_difference_sum(tickers, quantities_from, weights_to):
    weights_from = np.array(weights(tickers, quantities_from))
    weights_to = np.array(weights_to)

    weight_difference = weights_to - weights_from
    return np.sum(np.abs(weight_difference))


def aggs(tickers, weights):
    _aggs = {}
    for (ticker, weight) in list(zip(tickers, weights)):
        si = stock.INFO[ticker]

        agg_tokens = []
        for i in range(len(si)):
            agg_tokens.append(str(si[i]))

        agg_tokens = set(agg_tokens)

        for agg_token in agg_tokens:
            if agg_token not in _aggs:
                _aggs[agg_token] = 0
            _aggs[agg_token] += weight

    for (k, v) in _aggs.items():
        _aggs[k] = round(v * 100, 2)
    return _aggs


def generate_portfolio_weights(size):
    ws = random.choice([
        np.random.random(size=size),
        np.random.exponential(size=size),
        np.random.exponential(size=size),
    ])

    ws /= np.sum(ws)
    return ws


def fail_lower_weight_bound(ws, b = 0.005):
    if len(list(filter(lambda w: w < b, ws))) > 0:
        return True


def fail_upper_weight_bound(ws, b = 0.15):
    if len(list(filter(lambda w: w > b, ws))) > 0:
        return True


def fail_lower_utility_bound(tickers, ws, u):
    if utility(tickers, ws) < u:
        return True


def fail_diversification_bounds(tickers, ws):
    ag = aggs(tickers, ws)
    if ag['reit'] < 15:
        return True

    if ag['bond'] <= 5:
        return True

    # if a['international'] <= 5:
    #     return True

    # if a['etf'] <= 30:
    #     return True


def emulate():
    tickers = list(target_portfolio.keys())
    c = 300

    ps = []
    while len(ps) < c:
        w = generate_portfolio_weights(len(tickers))

        if fail_lower_weight_bound(w):
            continue

        if fail_upper_weight_bound(w):
            continue

        if fail_diversification_bounds(tickers, w):
            continue

        if fail_lower_utility_bound(tickers, w, 0.11):
            continue

        a = aggs(tickers, w)
        r = total_return(tickers, w)
        s = stdev(tickers, w)
        sh = sharpe(tickers, w)
        u = utility(tickers, w)
        cec = certainty_eq_cost(tickers, list(target_portfolio.values()),w)
        tc = transaction_cost(tickers, list(target_portfolio.values()),w)
        ww = list(zip(tickers, np.round(w,3)))
        wds = weight_difference_sum(tickers, list(target_portfolio.values()),w)

        ps.append((r, s, u, sh, a, cec, tc, ww, wds))

        dbg = '{:.1f}% u:{}'.format(len(ps)*100/c, u)
        print(dbg)

    ps = sorted(ps, key=lambda p: -p[2])
    # ps = sorted(ps, key=lambda p: p[5]-p[6] )

    with open('data/portfolio_model.csv', 'w') as f:
        writer = csv.writer(f)
        # writer.writerow(['R', 'STD', 'U', 'SHARPE', 'US', 'INTERNATIONAL', 'EQUITY', 'BOND', 'ETF', 'STOCK', 'REIT', 'CEC', 'TC', 'W'])
        writer.writerow(['R', 'STD', 'U', 'SHARPE', 'US', 'EQUITY', 'ETF', 'STOCK', 'REIT', 'CEC', 'TC', 'W'])
        for p in ps:
            writer.writerow(
                [
                    *np.round([
                        p[0], p[1], p[2], p[3],
                        p[4]['us'],
                        # p[4]['international'],
                        p[4]['equity'],
                        # p[4]['bond'],
                        p[4]['etf'],
                        p[4]['stock'],
                        p[4]['reit'],
                        p[5],
                        p[6],
                    ], 3),
                    p[7],
                    p[8],
                ]
            )

def allocate(tickers, quantities_from, weights_to, amount):
    weights_from = np.array(weights(tickers, quantities_from))
    weights_to = np.array(weights_to)
    cv = current_values(tickers)
    tv = total_value(tickers, quantities_from)
    ntv = tv + amount
    cf = tv / ntv

    weights_from_new = weights_from * cf
    weight_difference = weights_to - weights_from_new
    quantities_diff = weight_difference * ntv

    enum_quantities_diff = list(enumerate(np.round(quantities_diff)))
    enum_quantities_diff_filtered = list(filter(lambda v: v[1] > 0, enum_quantities_diff))

    sorted_orders = sorted(enum_quantities_diff_filtered, key=lambda p: -p[1] )

    to_buy = np.zeros(len(tickers))
    for (position, amount_limit) in sorted_orders:
        if amount < amount_limit:
            to_buy[position] = np.floor(amount / cv[position])
            break
        else:
            raise

    quantities_new = quantities_from + to_buy
    # new_weights = np.array(weights(tickers, quantities_new))
    # _t = total_return(tickers, new_weights)
    # _s = stdev(tickers, new_weights)
    # print("{:.4f} {:.4f}".format(_t, _s))
    return quantities_new


def allocaterandom(tickers, quantities_from, weights_to, amount):
    weights_from = np.array(weights(tickers, quantities_from))
    weights_to = np.array(weights_to)
    cv = current_values(tickers)
    tv = total_value(tickers, quantities_from)
    ntv = tv + amount
    cf = tv / ntv

    weights_from_new = weights_from * cf
    weight_difference = weights_to - weights_from_new
    quantities_diff = weight_difference * ntv

    enum_quantities_diff = list(enumerate(np.round(quantities_diff)))
    enum_quantities_diff_filtered = list(filter(lambda v: v[1] > 0, enum_quantities_diff))

    ######## picking heuristic #########
    selection = []
    for i in range(250):
        to_buy = np.zeros(len(tickers))

        # sorted_orders = sorted(enum_quantities_diff_filtered, key=lambda p: -p[1] )
        # for (position, amount_limit) in sorted_orders:
        #     if amount < amount_limit:
        #         to_buy[position] = np.floor(amount / cv[position])
        #         break
        #     else:
        #         raise
        position, amount_limit = random.choice(list(enum_quantities_diff_filtered))
        if amount < amount_limit:
            to_buy[position] = np.floor(amount / cv[position])

        quantities_new = quantities_from + to_buy
        new_weights = np.array(weights(tickers, quantities_new))
        u = utility(tickers, new_weights)
        selection.append((u, quantities_new))

    quantities_new = sorted(selection, key=lambda q: -q[0])
    quantities_new = quantities_new[0][1]


    # _t = total_return(tickers, new_weights)
    # _s = stdev(tickers, new_weights)
    # print("{:.4f} {:.4f}".format(_t, _s))
    return quantities_new

def stepthrough():
    ticks = list(target_portfolio.keys())
    vals = list(target_portfolio.values())
    _w = weights(
        list(target_portfolio.keys()),
        list(target_portfolio.values()),
    )

    ws = [('MO', 0.009), ('AAPL', 0.131), ('DIS', 0.149), ('GM', 0.019), ('VZ', 0.017), ('MAIN', 0.084), ('UNIT', 0.01), ('NAT', 0.032), ('ORC', 0.014), ('AWP', 0.025), ('OHI', 0.043), ('MPW', 0.032), ('XOM', 0.013), ('JNUG', 0.016), ('EXG', 0.051), ('VOO', 0.084), ('VO', 0.058), ('VBK', 0.022), ('VEA', 0.017), ('VWO', 0.019), ('BND', 0.027), ('VCLT', 0.028), ('SLIM', 0.1)]
    w = np.array([v[1] for v in ws])

    _t = total_return(ticks, w)
    _s = stdev(ticks, w)
    print("!!! {:.3f} {:.3f}".format(_t, _s))

    new_vals = vals
    tots = 0
    for i in range(50):
        tots += 1000
        new_vals = allocate(ticks, new_vals, w, 1000)
        # print(new_vals)
        print(i)
        time.sleep(0.05)

    # print(ticks)
    # print(vals)
    # print(new_vals)
    for t,v,nv in list(zip(ticks,vals,new_vals)):
        out = '{:<6} {:5d} {:5d}'.format(t,int(v),int(nv))
        print(out)


def annuity(yearly_rate, months):
    rate = yearly_rate / 12
    g = (1 + rate) ** months
    ac = rate * g / (g-1)
    return ac




if __name__ == "__main__":
    c = 1000
    n_in_ps = 36
    r = 0.12 # / n_in_ps
    print(c * annuity(r, n_in_ps))
    # print(c * annuity(r, n_in_ps) * n_in_ps)
    exit()
    tickers = list(target_portfolio.keys())
    quantities = list(target_portfolio.values())
    ws = weights(tickers, quantities)
    # u = utility(tickers, ws)
    # print(u)

    get_portfolio_daily_data(tickers, ws, '2018-04', '2018-04')

    # 'VOO': 0,
    # 'VO': 0,
    # 'VBK': 0,
    # 'VEA': 0,
    # 'VWO': 0,
    # 'BND': 0,
    # 'VCLT': 0,
    # 'SLIM': 0,

    # for ticker in target_portfolio.keys():
    #     tickers = [ticker]
    #     ws = np.array([1])

    #     tr = total_return(tickers, ws)
    #     st = stdev(tickers, ws)
    #     u = utility(tickers, ws)
    #     print('{:<6s} {:6.2f}  {:6.2f}  {:6.2f}'.format(ticker, tr, st, u))

    # tickers = ['VOO', 'VO', 'VBK', 'VEA', 'VWO', 'BND', 'VCLT', 'SLIM']
    tickers = ['VOO', 'VCLT', 'SLIM']
    # tickers = np.array(['VOO', 'VBK'])
    # ws = np.array([0.45, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.15])
    ws = np.array([0.6, 0.2, 0.2])
    # ws = np.array([0.0, 0.9, 0.])

    tr = total_return(tickers, ws)
    st = stdev(tickers, ws)
    u = utility(tickers, ws)
    print('\n{:<6s} {:6.2f}  {:6.2f}  {:6.2f}'.format('P!', tr, st, u))
    # ws = list()
    # stepthrough()
    # emulate()

    lpm(tickers)

    # COVARIANCE IMPLEMENTAION
    # np.random.seed(1)
    # N = 3
    # b1 = np.random.rand(N)
    # b2 = np.random.rand(N)
    # b3 = np.random.rand(N)
    # X = np.column_stack([b1, b2])

    # print(X)
    # X -= X.mean(axis=0)
    # print(X)

    # # print(X.mean(axis=0))
    # fact = N - 1
    # by_hand = np.dot(X.T, X.conj())
    # print(by_hand)
    # by_hand = np.dot(X.T, X) /fact
    # print(by_hand)

    # # [[ 0.04735338  0.01242557]
    # #  [ 0.01242557  0.07669083]]

    # using_cov = np.cov(b1, b2)
    # print(using_cov)
    # pp= pd.DataFrame(X)
    # print(pp.cov())
    # # print(by_hand)
    # # assert np.allclose(by_hand, using_cov)

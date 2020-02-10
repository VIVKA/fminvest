import io
import data
import pandas as pd
import numpy as np
import datetime
from functools import reduce
from stock import Stock
from stock import INFO as STOCK_INFO


# print now.year, now.month, now.day, now.hour, now.minute, now.second

class FPortfolio:
    def __init__(self, data):
        self._raw_data = data
        year = 2018
        data_frame = {}
        for ticker, quantity in data.items():
            data_frame[ticker] = Stock(ticker).adjuseted_pct_change(year-5, year)
            self._data_frame = pd.DataFrame(data_frame)




class RealPortfolio:
    def __init__(self, data):
        self._data = data
        self._data_frame = None
        self._dy = None
        self._covd = None

    def __repr__(self):
        return '{} {} {:.3f} {:.3f}'.format(
            self.value(), self.w, self.ry(), self.dy()
        )

    @property
    def data_frame(self):
        if self._data_frame is None:
            data_frame = {}
            for ticker, _ in self._data.items():
                data_frame[ticker] = Stock(ticker).adjusted_pct_change('2013', '2018')
            self._data_frame = pd.DataFrame(data_frame)
        return self._data_frame

    def value(self):
        value = 0
        for ticker, quantity in self._data.items():
            value += Stock(ticker).price() * quantity

        return value

    @property
    def w(self):
        total_value = self.value()
        w = []
        for ticker, quantity in self._data.items():
            value = Stock(ticker).price() * quantity
            value = round((value / total_value), 3)
            # w.append(
            #     (ticker, value)
            # )
            w.append(value)

        return np.array(w)

    def rd(self):
        return np.sum(self.data_frame.mean() * self.w)

    def ry(self):
        return self.rd() * 252

    def covd(self):
        if self._covd is None:
            self._covd = self.data_frame.cov()


        # print(self._covd)
        # print(self._covd.loc[['AAPL', 'MO'], ['AAPL', 'MO']])
        return self._covd

    def covy(self):
        return self.covd() * 252

    def dy(self):
        if self._dy is None:
            self._dy = np.sqrt(np.dot(self.w.T, np.dot(self.covy(), self.w)))
        return self._dy

    def u(self):
        variance = self.dy() ** 2
        risk_parameter = 7
        risk = risk_parameter / 2
        return self.ry() - (risk * variance)







class Portfolio:
    def __init__(self, tickers, weights):
        if len(tickers) != len(weights):
            raise
        self.tickers = tickers
        self.w = np.array(weights)
        self._stocks = {}
        self._data = None
        self._covd = None
        self._r = None
        self._d = None
        self._dd = None
        self._dy = None
        self.data

    def __repr__(self):
        return 'Portfolio r:{:.2f} d:{:.2f} s:{:.2f} k:{:.2f} y:{:.2f} u:{:.2f}\n {}'.format(
            self.ry(), self.dy(), self.s(), self.kc(), self.yy(),
            self.u(), self.aggs()
        )

    @property
    def data(self):
        if self._data is None:
            data_frame = {}
            for ticker in self.tickers:
                s = Stock(ticker)
                data_frame[ticker] = s.adjusted_pct_change('2013', '2018')
                self._stocks[ticker] = s
            self._data = pd.DataFrame(data_frame)
        return self._data

    def weights(self, weights):
        self._dy = None
        self._dd = None
        self.w = np.array(weights)

    def covd(self):
        if self._covd is None:
            self._covd = self._data.cov()
        return self._covd

    def covy(self):
        return self.covd() * 252

    def rd(self):
        return np.sum(self._data.mean() * self.w)

    def ry(self):
        return self.rd() * 252

    def dd(self):
        if self._dd is None:
            self._dd = np.sqrt(np.dot(self.w.T, np.dot(self.covd(), self.w)))
        return self._dd

    def dy(self):
        if self._dy is None:
            self._dy = np.sqrt(np.dot(self.w.T, np.dot(self.covy(), self.w)))
        return self._dy

    def s(self):
        return self.ry() / self.dy()

    def kc(self):
        return self.ry() / (self.dy() ** 2)

    def yy(self):
        yields = [s.yy() for s in self._stocks.values()]
        return np.sum(yields * self.w)

    def u(self):
        # U(w)=w′μ−λ2w′Σw
        variance = self.dy() ** 2
        return self.ry() - variance


    def aggs(self):
        _aggs = {}
        for (ticker, weight) in list(zip(self.tickers, self.w)):
            axi = STOCK_INFO[ticker]

            agg_tokens = []
            for i in range(len(axi)):
                agg_tokens.append(str(axi[i]))
                # agg_tokens.append('_'.join(axi[0:i+1]))

            agg_tokens = set(agg_tokens)

            for agg_token in agg_tokens:
                if agg_token not in _aggs:
                    _aggs[agg_token] = 0

                _aggs[agg_token] += weight

        # for k, v in _aggs.items():
        #     if k.count('_') <= 1:
        #         print(k, round(v, 2))

        for (k, v) in _aggs.items():
            _aggs[k] = round(v * 100, 2)
        return _aggs


_po = {
    'MO':   30.00,
    'AAPL': 15.00,
    'DIS':  10.00,
    'GM':   55.00,
    'VZ':   35.00,
    'MAIN': 60.00,
    'UNIT': 150.00,
    # 'NAT':  180.00,
    'ORC':  500.00,
    'AWP':  400.00,
    'OHI':  100.00,
    'MPW':  100.00,
    'XOM':  40.00,
    # 'JNUG': 75.00,
}

_bp = [
    ('MO', 0.136),
    ('AAPL', 0.033),
    ('DIS', 0.027),
    ('GM', 0.034),
    ('VZ', 0.021),
    ('MAIN', 0.012),
    ('VOO', 0.051),
    ('VO', 0.183),
    ('VB', 0.023),
    ('VEA', 0.085),
    ('VWO', 0.021),
    ('ORC', 0.089),
    ('AWP', 0.003),
    ('OHI', 0.054),
    ('EXG', 0.091),
    ('MPW', 0.002),
    ('BND', 0.135)
]
_bp = dict(_bp)

if __name__ == "__main__":
    data = [
        ('', 150),
        # ('EXG', 400)
    ]
    data = dict(data)
    data = _po

    p = RealPortfolio(data)
    print(p.u())



    print(p)

    p1 = Portfolio(
        list(_po.keys()),
        p.w
    )
    print(p1)

    p1 = Portfolio(
        list(_po.keys()),
        p.w * 0.5
    )
    print(p1)

    p1 = Portfolio(
        list(_bp.keys()),
        list(_bp.values())
    )
    print(p1)






































# print(STOCK_INFO)
# print(Portfolio(['AAPL', 'HYG', 'EXG'], [0.55, 0.25, 0.10]))
# Portfolio(['AAPL', 'BND', 'EXG'], [0.55, 0.25, 0.10]).aggs()
# _sum = 0
# for _ti, _v in _po.items():
#     s = Stock(_ti)
#     _sum += s.price() * _v

# w = []
# for _ti, _v in _po.items():
#     s = Stock(_ti)
#     w.append(
#         (
#             _ti,
#             round(((s.price() * _v) / _sum), 3)
#         )
#     )

# print(_sum)
# print(w)
# p =Portfolio(
#     list(_po.keys()),
#     np.array(list(_po.values())) / np.sum(np.array(list(_po.values())))
# )
# print(p)
# print(p.w)

# display_sector('large 8.3%', ['MO', 'AAPL', 'DIS', 'GM', 'VZ'], stock_data)
# display_sector('mid 8.3%', ['MAIN', 'UNIT'], stock_data)
# display_sector('small 8.3%', ['NAT'], stock_data)
# display_sector('us stocks 24.9%', ['MO', 'AAPL', 'DIS', 'GM', 'VZ']+['MAIN', 'UNIT']+['NAT'], stock_data)
# display_sector('n-us stocks 16.6%', [], stock_data)
# display_sector('stocks 41.5%', ['MO', 'AAPL', 'DIS', 'GM', 'VZ']+['MAIN', 'UNIT']+['NAT'], stock_data)
# display_sector('REIT 8.3%', ['ORC', 'AWP', 'OHI', 'MPW'], stock_data)
# display_sector('res 16.6%', ['XOM', 'JNUG'], stock_data)
# display_sector('bonds 24.9%', ['BOND'], stock_data)
# display_sector('cash 8.3%', ['CASH'], stock_data)
# display_sector('cash 8.3%', [], stock_data)
#
#
# [
#     0.41
#     'stock': {
#         'us-stock': {
#             'large': [
#                 MO, # 30
#                 AAPL, # 15
#                 DIS, # 10
#                 GM, # 55
#                 VZ, # 35
#             ],
#             'midcap': [
#                 MAIN, # 60
#                 UNIT, # 150
#             ],
#             'small': [
#                 NAT, # 180
#             ],
#         },
#         'non-us_stock': {
#             'developed': [
#                 # None
#             ]
#             'emerging': [
#                 # None
#             ]
#         },
#     }
#     0.833
#     'real_estate': {
#         'real-estate': [
#                 ORC, # 500
#                 AWP, # 400
#                 OHI, # 100
#                 MPW, # 100
#         ]
#     },
#     0.166
#     'resources': {
#         'natural_resources': [
#                 XOM, # 40
#                 JNUG, # 75
#         ],
#         'commodities': [
#                 # None
#         ],
#     },
#     0.166
#     'us-bonds': {
#         'us-bonds': [
#                 VCLT
#         ],
#         'inflation_protected_bonds': [
#                 VTIP
#         ],
#     },
#     0.833
#     'non-us_bonds': [
#                 VWOB
#     ],
#     0.8330
#     'cash': [
#                 0
#     ]
# ]

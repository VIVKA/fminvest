import pandas as pd
import numpy as np


class Portfolio:
    def __init__(self, assets, weights):
        if len(assets) != len(weights):
            raise
        self.assets = assets
        self.w = np.array(weights)
        self._covd = None
        self._r = None
        self._d = None
        self._dd = None
        self._dy = None

    def __repr__(self):
        msg = (
            'Portfolio r:{:.2f} d:{:.2f} s:{:.2f} k:{:.2f} '
            'y:{:.2f} u:{:.2f}\n {}'
        ).format(
            self.ry(), self.dy(), self.s(), self.kc(), self.yy(),
            self.u(), self.aggs()
        )

        return msg

    def data(self, f, t):
        data_frame = {}
        for asset in self.assets:
            data_frame[asset.ticker] = asset.adjusted_pct_change(f, t)
        return pd.DataFrame(data_frame)

    def close_data(self, f, t):
        data_frame = {}
        for asset in self.assets:
            data_frame[asset.ticker] = asset._data[str(f):str(t)]['close']
        return pd.DataFrame(data_frame)

    def weights(self, weights):
        self._dy = None
        self._dd = None
        self.w = np.array(weights)

    def covd(self, f, t):
        return self.data(f, t).cov()

    def covy(self, f, t):
        return self.covd(f, t) * 252

    def rd(self, f, t):
        return np.sum(self.data(f, t).mean() * self.w)

    def ry(self, f, t):
        return self.rd(f, t) * 252

    def dd(self, f, t):
        return np.sqrt(np.dot(self.w.T, np.dot(self.covd(f, t), self.w)))

    def dy(self, f, t):
        return np.sqrt(np.dot(self.w.T, np.dot(self.covy(f, t), self.w)))

    def s(self, f, t):
        return self.ry(f, t) / self.dy(f, t)

    def kc(self, f, t):
        return self.ry(f, t) / (self.dy(f, t) ** 2)

    def yy(self, f, t):
        yields = [s.yy(f, t) for s in self.assets]
        return np.sum(yields * self.w)

    def u(self):
        variance = self.dy() ** 2
        return self.ry() - variance

    def ch(self, t):
        if len(self.data(t, t)) > 0:
            return np.sum(self.data(t, t).iloc[-1] * self.w) * 100

        return 0

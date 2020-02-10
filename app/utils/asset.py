import numpy as np
import pandas as pd
from app.utils import data
from app.utils import system
import datetime


class Asset:
    def __init__(self, ticker):
        self.ticker = ticker
        self._data = None
        self._r = None
        self._d = None
        self._yy = None

        (asset, df, ddf) = data.load_asset_data(ticker)
        self._asset = asset
        self._asset_type = asset.asset_type
        self._data = df
        self._data_dict = ddf
        self.id = asset.id

    def __repr__(self):
        return '{} {}'.format(self.ticker, self._asset_type)

    @property
    def splits(self):
        selector = self._data['split_coefficient'].isin([1])
        return list(self._data.loc[~selector]['split_coefficient'].items())

    @property
    def dividends(self):
        selector = self._data['dividend_amount'].isin([0])
        return list(self._data.loc[~selector]['dividend_amount'].items())

    @property
    def data(self):
        return self._data

    @property
    def asset_type(self):
        return self._asset_type

    @property
    def sector(self):
        return self._asset.sector

    @property
    def country(self):
        return self._asset.country

    @property
    def updated_at(self):
        return self._asset.updated_at

    def adjusted_close_price(self, date=None):
        if date:
            if not type(date) is str:
                return self._data_dict[date.strftime('%Y-%m-%d')]['adjusted_close']
            else:
                return self._data_dict[date]['adjusted_close']
        else:
            return self._data.iloc[-1]['adjusted_close']

    def close_price(self, date=None):
        if date:
            if not type(date) is str:
                return self._data_dict[date.strftime('%Y-%m-%d')]['close']
            else:
                return self._data_dict[date]['close']
        else:
            return self._data.iloc[-1]['close']

    def ch(self, f, t):
        return self.adjusted_pct_change(f, t)[-1] * 100

    def rd(self, f, t):
        return self.adjusted_pct_change(f, t).mean()

    def ry(self, f, t):
        return self.rd(f, t) * 252

    def dd(self, f, t):
        return self.adjusted_pct_change(f, t).std()

    def dy(self, f, t):
        return self.dd(f, t) * np.sqrt(252)

    def s(self, f, t):
        return self.ry(f, t) / self.dy(f, t)

    def kc(self, f, t):
        return self.ry(f, t) / (self.dy(f, t) ** 2)

    @system.hourcacheassetmethod
    def yy(self, f, t):
        if self._asset_type == 'bond':
            return self._data[str(f):str(t)]['yield_amount'].mean()/100
        else:
            _div_slice = self._data[str(f):str(t-1)]['dividend_amount']
            _close_slice = self._data[str(f):str(t)]['close']

            _div_year_sample = _div_slice.resample('Y', closed='right').sum().mean()
            _close_year_sample = _close_slice.resample('Y', closed='right').mean().mean()

            return _div_year_sample / _close_year_sample

    @system.hourcacheassetmethod
    def adjusted_pct_change(self, f, t):
        if self._asset_type == 'bond':
            return self._data[str(f):str(t)]['close'].pct_change()
        else:
            return self._data[str(f):str(t)]['adjusted_close'].pct_change()

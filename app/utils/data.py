import pandas as pd
from app import db
from app.models.asset import AssetModel
from app.models.asset_data import AssetDataModel
from app.utils import system
import datetime


def load_asset_df(asset):
    asset_data = db.session.query(
        AssetDataModel
    ).filter_by(
        asset_id=asset.id
    ).all()

    parsed_data = [
        [
            data.trade_date,
            data.open_price,
            data.high_price,
            data.low_price,
            data.close_price,
            data.adjusted_close_price,
            data.trade_volume,
            data.dividend_amount,
            data.split_coefficient,
            data.yield_amount,
        ]
        for data in asset_data
    ]

    dataframe = pd.DataFrame(
        parsed_data,
        columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'adjusted_close',
            'volume', 'dividend_amount', 'split_coefficient', 'yield_amount'
        ]
    )

    dataframe.index = pd.to_datetime(dataframe['timestamp'])
    del dataframe['timestamp']
    dataframe.index = dataframe.index.normalize()
    # dataframe = dataframe.resample('D').ffill()
    dataframe.sort_index(ascending=True, inplace=True)

    _to = datetime.date.today().year
    _from = _to - 7
    dataframe = dataframe[str(_from):str(_to)]

    return dataframe


@system.daycache
def load_asset_data(ticker):
    asset = db.session.query(
        AssetModel
    ).filter_by(
        ticker=ticker,
    ).first()

    if not asset:
        raise 'Asset {} not found'.format(ticker)

    df = load_asset_df(asset)

    dt = df.copy()
    dt.index = dt.index.strftime('%Y-%m-%d')
    dt = dt.to_dict('index')

    return asset, df, dt

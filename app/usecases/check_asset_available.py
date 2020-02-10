from app import db
from app.models.asset import AssetModel


def check_asset_available(ticker):
    ticker = ticker.upper()

    asset = db.session.query(
      AssetModel
    ).filter(
      AssetModel.ticker == ticker,
    ).first()

    if asset:
        return {
            'id': asset.id,
        }

    return False

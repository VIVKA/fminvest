from app import db
from app.utils import utils
from app.models.portfolio_action import PortfolioActionModel
from datetime import datetime


def create_portfolio_action(account_id, portfolio_id, action_data):
    # TODO: check that portfolio_id belongs to account_id!!

    asset_id = action_data['asset_id']
    action_type = action_data['action_type']
    amount = action_data['amount']
    price = action_data.get('price', None)
    action_at = action_data['action_at']

    if action_type not in ['BUY', 'SELL']:
        raise 'unknown action type'

    if action_at:
        action_at = datetime.strptime(action_at, '%Y-%m-%dT%H:%M:%S.%fZ')
    else:
        action_at = datetime.today()

    if not price:
        asset = utils.get_asset_by_id(asset_id)
        price = asset.close_price(action_at)

    portfolio_asset = PortfolioActionModel(
        portfolio_id=portfolio_id,
        action_type=action_type,
        asset_id=asset_id,
        amount=amount,
        price=price,
        action_at=action_at,
    )

    db.session.add(portfolio_asset)
    db.session.commit()

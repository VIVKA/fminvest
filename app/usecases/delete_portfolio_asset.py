from app import db
from sqlalchemy.sql import text


def delete_portfolio_asset(account_id, portfolio_id, asset_id):
    sq = (
        'delete from portfolio_actions '
        'using portfolios '
        'where portfolio_actions.portfolio_id=:portfolio_id '
        'and portfolio_actions.asset_id=:asset_id '
        'and portfolios.account_id=:account_id')

    db.engine.execute(
        text(sq),
        account_id=account_id,
        portfolio_id=portfolio_id,
        asset_id=asset_id)

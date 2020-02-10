from app import db
from sqlalchemy.sql import text


def delete_portfolio(account_id, portfolio_id):
    sq_portfolio_actions = (
        'delete from portfolio_actions '
        'where portfolio_id=:portfolio_id'
    )

    sq_portolio = (
        'delete from portfolios '
        'where account_id=:account_id and id=:portfolio_id'
    )

    db.engine.execute(
        text(sq_portfolio_actions), portfolio_id=portfolio_id)
    db.engine.execute(
        text(sq_portolio), account_id=account_id, portfolio_id=portfolio_id)

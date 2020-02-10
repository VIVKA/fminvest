from sqlalchemy.sql import text
from app import db
from app.utils import utils


def extract_trades(t, asset_dict):
    asset = asset_dict[t[1]]

    action_type = t[2]
    amount = t[3]
    price = t[4]
    value = price * amount
    isodate = t[5].date().isoformat()

    return {
        'asset_id': t[0],
        'ticker': t[1],
        'action_type': action_type,
        'amount': amount,
        'price': price,
        'value': value,
        'traded_at': isodate,
        'action_at': isodate,
        'country': asset.country,
    }


def get_portfolio_trades(account_id, portfolio_id):
    aq = (
        'SELECT assets.id, assets.ticker, '
        'portfolio_actions.action_type, portfolio_actions.amount, '
        'portfolio_actions.price, portfolio_actions.action_at '
        'FROM portfolio_actions '
        'JOIN assets ON portfolio_actions.asset_id = assets.id '
        'JOIN portfolios ON portfolio_actions.portfolio_id = portfolios.id '
        'WHERE portfolio_actions.portfolio_id = :portfolio_id '
        'AND portfolios.account_id = :account_id '
        'ORDER BY portfolio_actions.action_at DESC'
    )

    asset_query_result = db.engine.execute(
        text(aq), portfolio_id=portfolio_id, account_id=account_id)

    portfolio_trades = list(asset_query_result)

    tickers = list(map(lambda t: t[1], portfolio_trades))
    asset_dict = {t: utils.get_asset(t) for t in tickers}

    trades = list(map(lambda t: extract_trades(t, asset_dict), portfolio_trades))

    response = {
        'trades': trades
    }

    return response

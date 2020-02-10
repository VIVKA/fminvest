from sqlalchemy.sql import text
from app import db
from app.models.portfolio import PortfolioModel


# def get_portfolio_assets(account_id, portfolio_id):
#     q = (
#         'SELECT assets.id, assets.ticker, '
#         'portfolio_assets.amount, portfolio_assets.traded_at '
#         'FROM portfolio_assets '
#         'JOIN assets ON portfolio_assets.asset_id = assets.id '
#         'JOIN portfolios ON portfolio_assets.portfolio_id = portfolios.id '
#         'WHERE portfolio_assets.portfolio_id = :portfolio_id '
#         'AND portfolios.account_id = :account_id '
#         'ORDER BY assets.id, portfolio_assets.traded_at ASC'
#     )
#     result = db.engine.execute(
#         text(q), account_id=account_id, portfolio_id=portfolio_id)
#     trades = list(result)

#     return trades


def duplicate_portfolio(account_id, portfolio_id):
    pass
    # trades = get_portfolio_assets(account_id, portfolio_id)
    # for t in trades:
    #     print(t)

    # portfolio = PortfolioModel(
    #     account_id=account_id
    # )
    # db.session.add(portfolio)
    # db.session.commit()

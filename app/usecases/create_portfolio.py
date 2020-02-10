from app import db
from app.models.portfolio import PortfolioModel


def create_portfolio(account_id):
    portfolio = PortfolioModel(
        account_id=account_id
    )
    db.session.add(portfolio)
    db.session.commit()

    return {
        'portfolio_id': portfolio.id
    }

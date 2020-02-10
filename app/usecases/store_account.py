from app import db
from app.models.account import AccountModel
from app.models.portfolio import PortfolioModel


def store_account(token):
    account = AccountModel(
        token=token
    )

    db.session.add(account)
    db.session.commit()

    portfolio = PortfolioModel(
        account_id=account.id
    )

    db.session.add(portfolio)
    db.session.commit()

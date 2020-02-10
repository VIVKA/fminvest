from app import db
from app.models.account import AccountModel


def get_account(token):
    account = db.session.query(
        AccountModel
    ).filter_by(
        token=token,
    ).first()

    return account

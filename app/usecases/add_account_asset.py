from app import db
from app.models.account_stock import AccountStock
from app.models.account_bond import AccountBond


def add_account_asset(account_id, asset_type, asset_id, amount):
    if asset_type == 'stock':
        account_stock = AccountStock(
            account_id=account_id,
            stock_id=asset_id,
            amount=amount
        )

        db.session.add(account_stock)
        db.session.commit()

    if asset_type == 'bond':
        account_bond = AccountBond(
            account_id=account_id,
            bond_id=asset_id,
            amount=amount
        )

        db.session.add(account_bond)
        db.session.commit()

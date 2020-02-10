from app import db
from sqlalchemy.sql import text


def update_account_asset(account_id, asset_type, asset_id, amount):
    if asset_type == 'stock':
        sq = (
            'update account_stocks set amount=:amount '
            'where account_id=:account_id and stock_id=:asset_id')
        db.engine.execute(
            text(sq), account_id=account_id, asset_id=asset_id, amount=amount)

    if asset_type == 'bond':
        bq = (
            'update account_bonds set amount=:amount '
            'where account_id=:account_id and bond_id=:asset_id')
        db.engine.execute(
            text(bq), account_id=account_id, asset_id=asset_id, amount=amount)

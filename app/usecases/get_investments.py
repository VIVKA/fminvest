from app import db
from sqlalchemy.sql import text


def get_portfolios(account_id):
    bq = (
        'select portfolios.id, portfolios.account_id, portfolios.name, count(distinct portfolio_actions.asset_id) as c '
        'from portfolios left join portfolio_actions on portfolios.id = portfolio_actions.portfolio_id '
        'where portfolios.account_id = :account_id '
        'group by portfolios.id '
        'order by portfolios.id asc')

    ports = db.engine.execute(text(bq), account_id=account_id)
    portfolio_data = list(ports)

    return portfolio_data


def get_investments(account_id):
    portfolio_data = get_portfolios(account_id)
    pd = [(p.id, p.name, p.c) for p in portfolio_data]

    return {
        'portfolio_data': pd,
    }

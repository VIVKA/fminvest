from sqlalchemy.sql import text
from app import db
from app.utils import utils


def get_asset_trades(account_id, portfolio_id):
    q = (
        'SELECT assets.id, assets.ticker, portfolio_actions.amount, '
        'portfolio_actions.action_type, portfolio_actions.action_at '
        'FROM portfolio_actions '
        'JOIN assets ON portfolio_actions.asset_id = assets.id '
        'JOIN portfolios ON portfolio_actions.portfolio_id = portfolios.id '
        'WHERE portfolio_actions.portfolio_id = :portfolio_id '
        'AND portfolios.account_id = :account_id '
        'ORDER BY assets.id, portfolio_actions.action_at ASC'
    )
    result = db.engine.execute(
        text(q), account_id=account_id, portfolio_id=portfolio_id)
    trades = list(result)

    # asset groups
    bunches = {}
    for trade in trades:
        ticker = trade[1]
        amount = trade[2]
        trade_type = trade[3]
        trade_date = trade[4].replace(tzinfo=None)  # TODO: timezones relevant?
        if ticker not in bunches:
            bunches[ticker] = []
        bunches[ticker].append(('TRADE', trade_date, trade_type, amount))

    return bunches


def get_portfolio_dividends(account_id, portfolio_id):
    bunches = get_asset_trades(account_id, portfolio_id)

    aggregates = {}
    dividends = []
    for key, values in bunches.items():
        a = utils.get_asset(key)

        # if key not in aggregates:
        aggregates[key] = 0
        # dividends[key = []

        splits = []
        if len(a.splits) > 0:
            for d, v in a.splits:
                split = ('SPLIT', d.to_pydatetime(), v)
                splits.append(split)

        divs = []
        if len(a.dividends) > 0:
            for d, v in a.dividends:
                split = ('DIVIDEND', d.to_pydatetime(), v)
                divs.append(split)

        queue = values + splits + divs
        sorted_queue = sorted(queue, key=lambda item: item[1])

        for item in sorted_queue:
            if item[0] == 'SPLIT':
                aggregates[key] *= item[2]

            if item[0] == 'TRADE':
                if item[2] == 'BUY':
                    aggregates[key] += item[3]

                if item[2] == 'SELL':
                    aggregates[key] -= item[3]

            if item[0] == 'DIVIDEND':
                dd = item[2] * aggregates[key]
                if dd > 0:
                    c = (
                        item[1], a.ticker, aggregates[key],
                        item[2], dd, a.country
                    )
                    dividends.append(c)

    # TODO: EX-DIVIDEND!

    dividends = list(reversed(sorted(dividends, key=lambda dd: dd[0])))

    response = {
        'dividends': dividends
    }

    return response

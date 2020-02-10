import time
import datetime
import numpy as np
from app.utils import utils
from app.utils.portfolio import Portfolio
from dateutil.relativedelta import relativedelta


def get_portfolio_history(account_id, portfolio_id, period):
    portfolio_actions = utils.get_portfolio_actions(account_id, portfolio_id)
    portfolio_actions = sorted(portfolio_actions, key=lambda item: item['action_date'])

    first_action_date = None
    if len(portfolio_actions) > 0:
            first_action_date = portfolio_actions[0]['action_date']  # first action date

    # f - from
    if period == 'YTD':
        f = datetime.datetime.today()
        f = f.replace(month=1, day=1)

        if first_action_date and first_action_date > f:
            f = first_action_date

        f = str(f.date())

    if period == 'ALL':
        f = datetime.datetime.today()
        f = f.replace(month=1, day=1)

        if first_action_date:
            f = first_action_date
        f = str(f.date())

    # t - to
    t = str(datetime.datetime.today().date())

    voo = utils.get_asset('VOO')
    vt = utils.get_asset('VT')
    imoex = utils.get_asset('IMOEX')
    benchmark = {
        'voo': utils.get_weekly_asset_data(voo, f, t),
        'vt': utils.get_weekly_asset_data(vt, f, t),
        'imoex': utils.get_weekly_asset_data(imoex, f, t),
        'portfolio': utils.get_portfolio_history(account_id, portfolio_id, f, t),
    }

    return {
        'benchmark': benchmark
    }

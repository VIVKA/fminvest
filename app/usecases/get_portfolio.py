import time
import datetime
import numpy as np
from app.utils import utils
from app.utils.portfolio import Portfolio
from app.usecases.get_recommended_weights import get_recommended_weights
from app.usecases.get_simulation_hull import get_simulation_hull
from app.models.sector import GICS_DATA
from dateutil.relativedelta import relativedelta


def portfolio_response(p, f=None, t=None):
    (asset, amount, weight, recommended_weight, capital_gain, dividends) = p

    today_date = datetime.datetime.today()
    today_year = today_date.year
    today_date = today_date.date().isoformat()
    back_date = datetime.datetime.today() + relativedelta(years=-3)
    back_year = back_date.year
    back_date = back_date.date().isoformat()

    return {
        'asset_id': int(asset.id),
        'asset_type': asset.asset_type,
        'ticker': asset.ticker,
        'amount': int(amount),
        'ch': asset.ch(today_year, today_year),
        'ry': [0, asset.ry(back_date, today_date), 0],
        'dy': [0, asset.dy(back_date, today_date), 0],
        'yy': asset.yy(back_year, today_year),
        'tv': int(amount) * asset.adjusted_close_price(),
        'p': asset.adjusted_close_price(),
        'cg': capital_gain,
        'divs': dividends,
        'tr': capital_gain + dividends,
        'country': asset.country,
        'sector': asset.sector,
        'weight': weight,
        'recommended_weight': recommended_weight,
        'updated_at': asset.updated_at,
    }


def get_portfolio(account_id, portfolio_id, f=None, t=None):
    assets, quantities = utils.get_portfolio_asset_quantities(account_id, portfolio_id)

    portfolio_data = utils.get_portfolio_data(account_id, portfolio_id)
    weights = utils.weights(assets, quantities)

    # gics
    gics = [asset.sector for asset in assets if asset._asset_type == 'stock']
    gics_aggs = {k: 0.0 for k in GICS_DATA.keys()}
    for (gics, weight) in list(zip(gics, weights)):
        if gics in GICS_DATA.keys():
            gics_aggs[gics] += weight

    # gics_aggs = sorted(gics_aggs.items(), key=lambda x: -x[1])
    gics_aggs = list(gics_aggs.items())

    # benchmarks
    voo = utils.get_asset('VOO')
    vt = utils.get_asset('VT')
    imoex = utils.get_asset('IMOEX')

    portfolio = Portfolio(assets, weights)

    recommended_weights = get_recommended_weights(assets)
    # target = Portfolio(assets, recommended_weights)

    portfolio_actions = utils.get_portfolio_actions(account_id, portfolio_id)
    portfolio_actions = sorted(portfolio_actions, key=lambda item: item['action_date'])

    capital_gain = utils.get_portfolio_capital_gain(account_id, portfolio_id)
    dividends = utils.get_portfolio_dividends(account_id, portfolio_id)

    assets_data = list(zip(
        assets, quantities, weights, recommended_weights, capital_gain, dividends
    ))
    assets_data_response = list(map(portfolio_response, assets_data))

    today_date = datetime.datetime.today()
    today_year = today_date.year
    today_date = today_date.date().isoformat()
    back_date = datetime.datetime.today() + relativedelta(years=-3)
    back_year = back_date.year
    back_date = back_date.date().isoformat()

    return {
        'portfolioData': {
            'name': portfolio_data.name,
            'ch': portfolio.ch(today_year),
            'r': portfolio.ry(back_date, today_date),
            'd': portfolio.dy(back_date, today_date),
            'y': portfolio.yy(back_year, today_year),
            'u': utils.utility(assets, weights),
            'or': utils.total_return(assets, recommended_weights),
            'od': utils.stdev(assets, recommended_weights),
            'oy': utils.total_yield(assets, recommended_weights),
            'ou': utils.utility(assets, recommended_weights),
            'tv': utils.total_value(assets, quantities),
            'tcg': int(np.sum(list(capital_gain))),
            'td': int(np.sum(list(dividends))),
            'gics_data': gics_aggs,  # TODO: maybe extract
            'simulation_hull': get_simulation_hull(assets),  # TODO: extract
        },
        'assetData': assets_data_response,
    }

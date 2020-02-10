import time
import math
from sqlalchemy.sql import text
from app import create_worker
from app import db
from app.utils import utils
from app.models.simulation import SimulationModel
from scipy.spatial import ConvexHull
import numpy as np

config = None
worker = create_worker(config)


def get_portfolio_assets(portfolio_id):
    aq = (
        'select assets.ticker '
        'from portfolio_actions '
        'join assets on portfolio_actions.asset_id = assets.id '
        'join portfolios on portfolio_actions.portfolio_id = portfolios.id '
        'where portfolio_actions.portfolio_id = :portfolio_id '
        'group by assets.id '
        'order by assets.ticker asc'
    )

    asset_query_result = db.engine.execute(text(aq), portfolio_id=portfolio_id)

    portfolio_assets = list(asset_query_result)
    tickers = list(map(lambda a: a[0], portfolio_assets))
    assets = list(map(lambda a: utils.get_asset(a), tickers))

    return assets


def simulate(assets, n=100):
    i = 0
    ws = []
    points = []
    while i < n:
        w = utils.generate_portfolio_weights(len(assets), 4)

        i += 1
        r = utils.total_return(assets, w)
        d = utils.stdev(assets, w)
        u = utils.utility(assets, w)
        points.append([r, d])
        ws.append((u, w))

    ps = sorted(ws, key=lambda p: -p[0])

    utility, weights = ps[0]

    # hull
    points = np.round(points, 3)
    _hull = ConvexHull(points)
    hull = [points[p] for p in _hull.vertices]

    return utility, weights, hull


def work_task():
    portfolio_results = \
        db.engine.execute('select portfolios.id from portfolios order by id asc')

    portfolio_ids = [r[0] for r in portfolio_results]

    portfolios = [
        get_portfolio_assets(portfolio_id) for portfolio_id in portfolio_ids
    ]

    portfolios = list(filter(lambda p: len(p) > 1, portfolios))

    # max_simulations = 1000000
    for assets in portfolios:
        time_last = time.time()
        asset_key = asset_key = ';'.join([a.ticker for a in assets])

        simulation = db.session.query(
            SimulationModel
        ).filter_by(
            asset_key=asset_key,
        ).first()

        time_quota = 10
        estimated_runtime = 1.0*math.exp(0.07*len(assets))  # per 100
        quota_coefficient = time_quota / estimated_runtime
        num_simulations = int(100 * quota_coefficient)
        try:
            utility, weights, hull = simulate(assets, num_simulations)
        except Exception as e:
            print('EXCEPTION', e)
            continue

        weight_key = ';'.join([str(w) for w in weights])
        hull_key = ';'.join([','.join(map(str, v)) for v in hull])

        if simulation:
            old_weights = [float(w) for w in simulation.weights.split(';')]
            old_utility = utils.utility(assets, old_weights)
            old_hull = [[float(h.split(',')[0]), float(h.split(',')[1])] for h in simulation.hull.split(';')]

            new_points = old_hull + hull
            _new_hull = ConvexHull(new_points)
            new_hull = [new_points[p] for p in _new_hull.vertices]
            hull_key = ';'.join([','.join(map(str, v)) for v in new_hull])

            new_weight_key = \
                weight_key if utility > old_utility else simulation.weights
            n = simulation.n + num_simulations

            sq = (
                'update simulations set weights = :weight_key, n = :n, hull = :hull '
                'where asset_key = :asset_key'
            )
            db.engine.execute(
                text(sq),
                asset_key=asset_key,
                weight_key=new_weight_key,
                hull=hull_key,
                n=n,
            )

        else:
            simulation = SimulationModel(
                asset_key=asset_key,
                weights=weight_key,
                hull=hull_key,
                n=num_simulations,
            )

            db.session.add(simulation)
            db.session.commit()

        time_elapsed = time.time() - time_last
        print("ran {} simulations in {:.2f}s at {:.2f}/s for {}".format(
            num_simulations,
            time_elapsed,
            num_simulations/time_elapsed,
            asset_key
        ))
        time_last = time.time()


with worker.app_context():
    while True:
        try:
            work_task()
        except (KeyboardInterrupt, SystemExit):
            exit()

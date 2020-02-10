from app import db
from app.models.simulation import SimulationModel


def get_recommended_weights(assets, cached=False):
    asset_key = ';'.join(sorted([a.ticker for a in assets]))

    simulation = db.session.query(
        SimulationModel
    ).filter_by(
        asset_key=asset_key,
    ).first()

    if not simulation:
        return [0.0 for a in assets]

    tickers = [t for t in simulation.asset_key.split(';')]
    weights = [float(w) for w in simulation.weights.split(';')]

    ticker_weights = dict(zip(tickers, weights))
    ordered_weights = [ticker_weights[a.ticker] for a in assets]
    return ordered_weights

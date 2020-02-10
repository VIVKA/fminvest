from app import db
from app.models.simulation import SimulationModel


def get_simulation_hull(assets, cached=False):
    asset_key = ';'.join(sorted([a.ticker for a in assets]))

    simulation = db.session.query(
        SimulationModel
    ).filter_by(
        asset_key=asset_key,
    ).first()

    if not simulation:
        return []

    hull = [
        [float(h.split(',')[1]), float(h.split(',')[0])] for h
        in simulation.hull.split(';')
    ]
    return hull

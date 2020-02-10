from app.utils import utils
from app.usecases.get_recommended_weights import get_recommended_weights


def get_recommendation(account_id, portfolio_id, amount):
    assets, quantities = utils.get_portfolio_asset_quantities(account_id, portfolio_id)

    recommended_weights = get_recommended_weights(assets)

    suggestions = utils.allocate(
      assets, quantities, recommended_weights, amount)

    return {
        'suggestions': suggestions[:3]
    }

from unittest.mock import patch
from create_portfolio_action import create_portfolio_action


@patch('app.usecases.create_portfolio_action.PortfolioActionModel')
def test_create_portfolio_action(PortfolioActionModel):
    # action_data = {
    #     'asset_id': 1,
    #     'action_type': 'BUY',
    #     'amount': 10,
    #     'action_at': '2019-02-01',
    #     'price': 20,
    # }
    # create_portfolio_action(1, 1, action_data)
    pass

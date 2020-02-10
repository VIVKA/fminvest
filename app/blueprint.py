from functools import wraps
from flask import (
    render_template, jsonify, request, make_response, Blueprint, redirect
)
import secrets

from app.utils import utils
from app.usecases.store_component import store_component
from app.usecases.store_account import store_account
from app.usecases.delete_component import delete_component
from app.usecases.get_account import get_account
from app.usecases.check_asset_available import check_asset_available
from app.usecases.get_components import get_all_components_for
from app.usecases.get_portfolio import get_portfolio
from app.usecases.get_portfolio_history import get_portfolio_history
from app.usecases.get_investments import get_investments
from app.usecases.get_stacked_data import get_all_stacked_data_for
from app.usecases.get_stats_data import get_stats_data_for
from app.usecases.get_recommendation import get_recommendation
from app.usecases.create_portfolio_action import create_portfolio_action
from app.usecases.create_portfolio import create_portfolio
from app.usecases.delete_portfolio import delete_portfolio
from app.usecases.duplicate_portfolio import duplicate_portfolio
from app.usecases.delete_portfolio_asset import delete_portfolio_asset
from app.usecases.get_portfolio_trades import get_portfolio_trades
from app.usecases.get_portfolio_dividends import get_portfolio_dividends


view = Blueprint(
    'public', __name__,
    template_folder='../../templates/public'
)


def get_account_from_cookies(cookies):
    account_token = cookies.get('account_token')
    if not account_token:
        raise 'no token'

    account = get_account(account_token)
    if not account:
        raise 'no account for given token'

    return account.id


def requires_authentication(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        account_id = get_account_from_cookies(request.cookies)
        return f(account_id, *args, **kwargs)
    return wrapped


# BUDGET

@view.route('/income', methods=['POST'])
@requires_authentication
def create_income_event(account_id):
    req = request.get_json()
    store_component(
        account_id,
        'income',
        req['frequency'],
        req['description'],
        req['quantity'],
    )
    return 'ok', 200


@view.route('/expense', methods=['POST'])
@requires_authentication
def create_expense_event(account_id):
    req = request.get_json()
    store_component(
        account_id,
        'expense',
        req['frequency'],
        req['description'],
        req['quantity'],
    )
    return 'ok', 200


@view.route('/stacked_data')
@requires_authentication
def get_stacked_data(account_id):
    out = get_all_stacked_data_for(account_id)
    return jsonify(out)


@view.route('/components')
@requires_authentication
def components(account_id):
    out = get_all_components_for(account_id)
    return jsonify(out)


@view.route('/stats')
@requires_authentication
def stats(account_id):
    out = get_stats_data_for(account_id)
    return jsonify(out)


# PORTFOLIO

@view.route('/asset/<symbol>', methods=['GET'])
@requires_authentication
def get_check_asset(account_id, symbol):
    result = check_asset_available(symbol)
    if result:
        return jsonify(result)

    return 'not_found', 404


@view.route('/components/<component_id>', methods=['DELETE'])
@requires_authentication
def delete_retular_event(account_id, component_id):
    delete_component(component_id)
    return 'ok', 200


@view.route('/investments', methods=['GET'])
@view.route('/portfolios', methods=['GET'])
@requires_authentication
def get_account_investments(account_id):
    out = get_investments(account_id)
    return jsonify(out)


@view.route('/portfolios', methods=['POST'])
@requires_authentication
def post_portfolios(account_id):
    out = create_portfolio(account_id)
    return jsonify(out)


@view.route('/portfolios/<int:portfolio_id>/duplicate', methods=['POST'])
@requires_authentication
def _duplicate_portfolio(account_id, portfolio_id):
    duplicate_portfolio(account_id, portfolio_id)
    return 'ok', 200


@view.route('/portfolios/<int:portfolio_id>', methods=['GET'])
@requires_authentication
@utils.timeit
def get_portfolios(account_id, portfolio_id):
    out = get_portfolio(account_id, portfolio_id)
    return jsonify(out)


@view.route('/portfolios/<int:portfolio_id>/history/<string:period>', methods=['GET'])
@requires_authentication
@utils.timeit
def _get_portfolio_history(account_id, portfolio_id, period):
    out = get_portfolio_history(account_id, portfolio_id, period)
    return jsonify(out)


@view.route('/portfolios/<int:portfolio_id>', methods=['DELETE'])
@requires_authentication
def delete_portfolios(account_id, portfolio_id):
    delete_portfolio(account_id, portfolio_id)
    return 'ok', 200


@view.route('/portfolios/<int:portfolio_id>/actions', methods=['POST'])
@requires_authentication
def post_portfolios_actions(account_id, portfolio_id):
    data = request.get_json()
    create_portfolio_action(account_id, portfolio_id, data)
    return 'ok', 200


@view.route('/portfolios/<int:portfolio_id>/recommendation/<int:amount>', methods=['GET'])
@requires_authentication
def _get_recommendation(account_id, portfolio_id, amount):
    out = get_recommendation(account_id, portfolio_id, amount)
    return jsonify(out)


@view.route('/portfolios/<int:portfolio_id>/assets', methods=['DELETE'])
@requires_authentication
def _delete_portfolio_asset(account_id, portfolio_id):
    req = request.get_json()
    delete_portfolio_asset(account_id, portfolio_id, req['asset_id'])
    return 'ok', 200


@view.route('/portfolios/<int:portfolio_id>/trades', methods=['GET'])
@requires_authentication
@utils.timeit
def _get_portfolio_trades(account_id, portfolio_id):
    out = get_portfolio_trades(account_id, portfolio_id)
    return jsonify(out)


@view.route('/portfolios/<int:portfolio_id>/dividends', methods=['GET'])
@requires_authentication
@utils.timeit
def _get_portfolio_dividends(account_id, portfolio_id):
    out = get_portfolio_dividends(account_id, portfolio_id)
    return jsonify(out)


# ROOT

@view.route('/')
def root():
    auth_attempt = request.args.get('auth')

    if auth_attempt:
        resp = make_response(redirect('/'))
        resp.set_cookie('account_token', auth_attempt)  # secure=True
        return resp

    account_token = request.cookies.get('account_token')
    resp = make_response(
        render_template('index.html', data={'token': account_token}))

    if not account_token:
        account_token = secrets.token_urlsafe(32)
        store_account(account_token)
        resp = make_response(
            render_template('index.html', data={'token': account_token}))
        resp.set_cookie('account_token', account_token)  # secure=True

    account = get_account(account_token)
    if not account:
        account_token = secrets.token_urlsafe(32)
        store_account(account_token)
        resp = make_response(
            render_template('index.html', data={'token': account_token}))
        resp.set_cookie('account_token', account_token)  # secure=True

    return resp


@view.route('/debug', methods=['GET', 'POST'])
def debug():
    print(request)
    print(request.args)
    print(request.form)
    print(request.data)
    return 'ok'

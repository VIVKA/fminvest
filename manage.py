from app import create_app
from app.utils import utils
from app.utils import data_us
from app.utils import data_ru
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.models.asset import AssetModel
import datetime
import time

from sqlalchemy.sql import text

from app.usecases.create_portfolio_action import create_portfolio_action

config = None
app = create_app(config)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def fix_asset_names():
    stocks = db.session.query(
        AssetModel
    ).filter(
        AssetModel.asset_type == 'stock'
    ).all()

    for s in stocks:
        time.sleep(2)
        if s.country == 'US':
            data = data_us.get_iex_company_data(s.ticker)
            sq = (
                'update assets set name = :name '
                'where ticker = :ticker'
            )
            db.engine.execute(
                text(sq),
                name=data['companyName'],
                ticker=s.ticker,
            )
            print(s.ticker, 'US!')

        if s.country == 'RU':
            name = data_ru.get_stock_full_name(s.ticker)
            sq = (
                'update assets set name = :name '
                'where ticker = :ticker'
            )
            db.engine.execute(
                text(sq),
                name=name,
                ticker=s.ticker,
            )
            print(s.ticker, 'RU!')


@manager.command
def repair_us_stock(ticker, days_back=None):
    date_from = None
    if days_back:
        date_from = \
            datetime.datetime.today() - datetime.timedelta(days=int(days_back))
    data_us.rapair_stock_data_daily_db(ticker, date_from)


@manager.command
def repair_ru_stock(ticker, days_back=None):
    date_from = None
    if days_back:
        date_from = \
            datetime.datetime.today() - datetime.timedelta(days=int(days_back))
    data_ru.rapair_stock_data_daily_db(ticker, date_from)


@manager.command
def load_us_stock(ticker, days_back=None):
    date_from = None
    if days_back:
        date_from = \
            datetime.datetime.today() - datetime.timedelta(days=int(days_back))
    data_us.save_stock_data_daily_db(ticker, date_from)


@manager.command
def load_ru_stock(ticker, days_back=None):
    date_from = None
    if days_back:
        date_from = \
            datetime.datetime.today() - datetime.timedelta(days=int(days_back))
    data_ru.save_stock_data_daily_db(ticker, date_from)


@manager.command
def load_ru_index(ticker, days_back=None):
    date_from = None
    if days_back:
        date_from = \
            datetime.datetime.today() - datetime.timedelta(days=int(days_back))
    data_ru.save_index_data_daily_db(ticker, date_from)


@manager.command
def load_ru_bond(ticker, days_back=None):
    date_from = None
    if days_back:
        date_from = \
            datetime.datetime.today() - datetime.timedelta(days=int(days_back))
    data_ru.save_bond_data_daily_db(ticker, date_from)


@manager.command
def load_crypto_currency_pair(symbol_from, symbol_to, days_back=None):
    date_from = None
    if days_back:
        date_from = \
            datetime.datetime.today() - datetime.timedelta(days=int(days_back))

    data_us.save_crypto_currency_pair_data_daily_db(symbol_from, symbol_to, date_from)


@manager.command
def load_currency_pair(symbol_from, symbol_to, days_back=None):
    date_from = None
    if days_back:
        date_from = \
            datetime.datetime.today() - datetime.timedelta(days=int(days_back))

    data_us.save_currency_pair_data_daily_db(symbol_from, symbol_to, date_from)


@manager.command
def load_all_ru():
    moex_stocks = [
        'ABRD', 'AFKS', 'AFLT', 'AGRO', 'AKRN', 'ALNU', 'ALRS',
        'AMEZ', 'APTK', 'AQUA', 'AVAN', 'AVAZ', 'AVAZP', 'BANE',
        'BANEP', 'BELU', 'BSPB', 'CBOM', 'CHEP', 'CHMF', 'CHMK',
        'CHZN', 'CNTLP', 'DIXY', 'DSKY', 'DVEC', 'ENPL', 'ENRU',
        'FEES', 'FESH', 'FIVE', 'FTRE', 'GAZA', 'GAZC', 'GAZP',
        'GAZT', 'GCHE', 'GMKN', 'HYDR', 'IRAO', 'IRGZ', 'IRKT',
        'KAZT', 'KAZTP', 'KBTK', 'KGKC', 'KMAZ', 'KRKNP', 'KZOS',
        'KZOSP', 'LKOH', 'LNTA', 'LNZL', 'LNZLP', 'LSNG', 'LSNGP',
        'LSRG', 'MAGN', 'MFGS', 'MFGSP', 'MFON', 'MGNT', 'MGTS',
        'MGTSP', 'MOEX', 'MRKC', 'MRKK', 'MRKP', 'MRKS', 'MRKU',
        'MRKV', 'MRKY', 'MRKZ', 'MSNG', 'MSRS', 'MSTT', 'MTLR',
        'MTLRP', 'MTSS', 'MVID', 'NKHP', 'NKNC', 'NKNCP', 'NLMK',
        'NMTP', 'NVTK', 'OBUV', 'OFCB', 'OGKB', 'OPIN', 'OTCP',
        'PHOR', 'PIKK', 'PLZL', 'POLY', 'PRTK', 'PSBR', 'QIWI',
        'RASP', 'RAVN', 'RBCM', 'RGSS', 'RNFT', 'ROSB', 'ROSN',
        'RSTI', 'RSTIP', 'RTKM', 'RTKMP', 'RUAL', 'SBER', 'SBERP',
        'SELG', 'SELGP', 'SFIN', 'SIBN', 'SNGS', 'SNGSP', 'SVAV',
        'TATN', 'TATNP', 'TGKA', 'TGKB', 'TGKD', 'TGKN', 'TNSE',
        'TRCN', 'TRMK', 'TRNFP', 'UNAC', 'UNKL', 'UPRO', 'URKA',
        'UTAR', 'UWGN', 'VSMO', 'VTBR', 'VZRZ', 'WTCM', 'WTCMP',
        'YNDX',
    ]
    moex_bonds = [
        'RU000A0JR8P0', 'RU000A0JVD17', 'RU000A0JWDN6', 'RU000A0JXQ93',
        'RU000A0JXRP9', 'RU000A0JXVY3', 'RU000A0ZYLB6', 'RU000A0ZZ0R3',
        'RU000A0ZZ547', 'RU000A0ZZFH2', 'SU25083RMFS5', 'SU26205RMFS3',
        'SU26207RMFS9', 'SU26212RMFS9', 'SU26215RMFS2', 'SU29006RMFS2',
        'SU29011RMFS2',
    ]
    moex_indices = [
        'IMOEX', 'MICEXTRN', 'MICEXCHM', 'MICEXCGS', 'MICEXFNL',
        'MICEXM&M', 'MICEXTLC', 'MICEXPWR', 'MICEXO&G',
    ]

    date_from = datetime.datetime(year=2010, month=1, day=1)
    for t in moex_stocks:
        data_ru.save_stock_data_daily_db(t, date_from)
        time.sleep(4)

    for t in moex_bonds:
        data_ru.save_bond_data_daily_db(t, date_from)
        time.sleep(3)

    for t in moex_indices:
        data_ru.save_index_data_daily_db(t, date_from)
        time.sleep(3)


@manager.command
def load_all_us():
    us_stocks = [
        'AAPL', 'AMZN', 'APD', 'AWK', 'AWP', 'BA', 'COST', 'DIS',
        'DUK', 'DWDP', 'ECL', 'EPR', 'EXG', 'GM', 'HTA', 'IRM',
        'JNJ', 'JNUG', 'JPM', 'LMT', 'MAIN', 'MO', 'MPW', 'NAT',
        'NEE', 'OHI', 'ORC', 'ROIC', 'STAG', 'TSLA', 'UNH', 'UNIT',
        'VZ', 'WPC', 'XOM',
    ]

    us_indices = [
        'BND', 'VAW', 'VCR', 'VDC', 'VDE', 'VFH', 'VGT',
        'VHT', 'VIS', 'VNQ', 'VOO', 'VOX', 'VPU', 'VT',
    ]

    date_from = datetime.datetime(year=2010, month=1, day=1)
    for t in us_stocks:
        data_us.save_stock_data_daily_db(t, date_from)
        time.sleep(15)

    for t in us_indices:
        data_us.save_stock_data_daily_db(t, date_from)
        time.sleep(15)


@manager.command
def update_all_asset_data(days_back):
    utils.update_currencies_data(days_back)
    utils.update_ru_asset_data(days_back)
    utils.update_us_asset_data(days_back)


@manager.command
def update_ru_asset_data(days_back):
    utils.update_ru_asset_data(days_back)


@manager.command
def update_us_asset_data(days_back):
    utils.update_us_asset_data(days_back)


@manager.command
def update_currencies_data(days_back):
    utils.update_currencies_data(days_back)


@manager.command
def repair_ru_asset_data(days_back):
    utils.repair_ru_asset_data(days_back)


@manager.command
def repair_us_asset_data(days_back):
    utils.repair_us_asset_data(days_back)


@manager.command
def alphavantage():
    result = utils.alphavantage_query(
        'CURRENCY_EXCHANGE_RATE',
        from_currency='RUB',
        to_currency='USD'
    )
    print(result)


@manager.command
def crypto(symbol):
    data_us.get_crypto_data(symbol, None)


@manager.command
def import_test_portfolio():
    trades = [
        ['2018-12-19', '6094854', 'BUY', 'UNH', '4'],
        ['2018-11-15', '6094854', 'BUY', 'AAPL', '5'],
        ['2018-10-30', '6094854', 'BUY', 'EPR', '15'],
        ['2017-09-27', '6094854', 'BUY', 'UNIT', '50'],
        ['2017-09-22', '6094854', 'BUY', 'UNIT', '100'],
        ['2017-08-25', '6094854', 'BUY', 'MO', '30'],
        ['2017-08-17', '6094854', 'BUY', 'AWP', '200'],
        ['2017-08-17', '6094854', 'BUY', 'ORC', '180'],
        ['2017-08-17', '6094854', 'BUY', 'OHI', '50'],
        ['2017-08-17', '6094854', 'BUY', 'XOM', '20'],
        ['2017-05-04', '6094854', 'BUY', 'AWP', '200'],
        ['2017-03-15', '6094854', 'BUY', 'OHI', '50'],
        ['2017-03-10', '6094854', 'BUY', 'ORC', '100'],
        ['2017-03-02', '6094854', 'BUY', 'JNUG', '300'],
        ['2017-02-06', '6094854', 'SELL', 'JNUG', '-125'],
        ['2017-01-19', '6094854', 'BUY', 'JNUG', '125'],
        ['2016-12-15', '6094854', 'BUY', 'NAT', '60'],
        ['2016-12-09', '6094854', 'BUY', 'MPW', '100'],
        ['2016-02-24', '6094854', 'BUY', 'MAIN', '20'],
        ['2016-02-24', '6094854', 'BUY', 'GM', '20'],
        ['2016-02-08', '6094854', 'BUY', 'NAT', '40'],
        ['2016-01-28', '6094854', 'BUY', 'MAIN', '40'],
        ['2016-01-28', '6094854', 'BUY', 'NAT', '80'],
        ['2016-01-28', '6094854', 'BUY', 'AAPL', '5'],
        ['2016-01-15', '6094854', 'BUY', 'ORC', '80'],
        ['2016-01-13', '6094854', 'BUY', 'GM', '35'],
        ['2016-01-06', '6094854', 'BUY', 'VZ', '10'],
        ['2016-01-06', '6094854', 'BUY', 'AAPL', '10'],
        ['2016-01-04', '6094854', 'BUY', 'VZ', '25'],
        ['2015-12-22', '6094854', 'BUY', 'XOM', '20'],
        ['2015-08-24', '6094854', 'BUY', 'ORC', '40'],
        ['2015-08-06', '6094854', 'BUY', 'ORC', '100'],
        ['2015-08-06', '6094854', 'BUY', 'DIS', '10'],
    ]

    for trade in trades:
        asset = utils.get_asset(trade[3])

        account_id = 1
        portfolio_id = 39
        action_data = {
            'asset_id': asset.id,
            'action_type': trade[2],
            'amount': int(trade[4]),
            'price': None,
            'action_at': trade[0],
        }

        create_portfolio_action(account_id, portfolio_id, action_data)


@manager.command
def simulate_debt_intress(principal, repay):
    principal = float(principal)
    repay = float(repay)
    p = 36
    ac = utils.annuity(0.08, p)
    a = principal*ac
    print(
      '{} x {:.2f} total: -{:.2f}'.format(
        p, a, a*p
      )
    )
    aa = (principal-repay)*ac
    print(
      '{} and {} x {:.2f} total: -{:.2f}'.format(
        repay, p-1, aa, repay+aa*(p-1)
      )
    )
    aaa = (principal-repay*2)*ac
    print(
      '{} and {} x {:.2f} total: -{:.2f}'.format(
        repay*2, p-1, aaa, repay*2+aaa*(p-1)
      )
    )
    it = repay*(1.15)**(p/12)
    itt = repay*2*(1.15)**(p/12)
    print('{:.2f} {:.2f} '.format(it, it-repay))
    print('{:.2f} {:.2f} '.format(itt, itt-repay*2))
    print('{} x {:.2f} total: -{:.2f}'.format(p, a, (a*p)-it))


if __name__ == '__main__':
    manager.run()

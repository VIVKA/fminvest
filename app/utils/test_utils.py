from app.utils import utils

def test_get_tx_date():
    t2_date_1 = utils.get_tx_date('US', '2019-01-17', 2)
    assert t2_date_1 == '2019-01-15'

    t2_date_2 = utils.get_tx_date('US', '2019-01-21', 2)
    assert t2_date_2 == '2019-01-18'

    t2_date_3 = utils.get_tx_date('US', '2019-02-20', 2)
    assert t2_date_3 == '2019-02-15'

    t2_date_4 = utils.get_tx_date('RU', '2019-02-23', 2)
    assert t2_date_4 == '2019-02-21'

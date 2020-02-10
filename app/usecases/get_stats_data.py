from app import db
from app.models.component import ComponentModel
from datetime import datetime
from dateutil import rrule


def get_stats_data_for(account_id):
    components = db.session.query(
        ComponentModel
    ).filter_by(
        account_id=account_id,
    ).all()

    date_from, date_to = datetime.now(), datetime(2019, 12, 30)  # TODO

    out = 0
    for component in components:
        if component.component_type != 'expense':
            continue

        rule = rrule.rrulestr(component.rrule)
        dates = rule.between(date_from, date_to)

        out += len(dates) * float(component.quantity)

    out = {
        'monthly': int(out / 15),
        'halfYear': int(out / 15) * 6,
    }

    return out

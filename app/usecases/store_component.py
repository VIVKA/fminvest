from app import db
from app.models.component import ComponentModel
from datetime import datetime
from dateutil import rrule


def _rule_quarterly():
    return rrule.rrule(
        rrule.MONTHLY,
        dtstart=datetime.now(),
        byweekday=rrule.MO,
        bysetpos=1,
        interval=3,
    )


def _rule_monthly():
    return rrule.rrule(
        rrule.MONTHLY,
        dtstart=datetime.now(),
        byweekday=rrule.MO,
        bysetpos=1,
        interval=1,
    )


def _rule_weekly():
    return rrule.rrule(
        rrule.WEEKLY,
        dtstart=datetime.now(),
        byweekday=rrule.MO,
    )


def _rule_once(when):
    return rrule.rrule(
        rrule.DAILY,
        dtstart=when,
        count=1
    )


def _annuity(yearly_rate, months, capital):
    rate = yearly_rate / 12
    g = (1 + rate) ** months
    ac = rate * g / (g-1)
    return capital * ac


def _rule_annuity(yearly_rate, months, capital):
    # pay = _annuity(yearly_rate, months, capital)
    return rrule.rrule(
        rrule.DAILY,
        dtstart=datetime.now(),
        count=months
    )


def store_component(
        account_id, component_type, frequency, description, quantity):
    freq_dict = {
        'monthly': _rule_monthly,
        'weekly': _rule_weekly,
        'quarterly': _rule_quarterly,
    }

    rrule_func = freq_dict[frequency]
    rule = str(rrule_func())
    comp = ComponentModel(
        account_id=account_id,
        component_type=component_type,
        frequency=frequency,
        rrule=rule,
        description=description,
        quantity=quantity,
    )

    db.session.add(comp)
    db.session.commit()

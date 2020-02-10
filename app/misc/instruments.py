import numpy as np
import pandas as pd
import data
import math
from functools import reduce
from datetime import datetime
from dateutil import (
    rrule,
    parser
)

rule_quarterly = rrule.rrulestr('''
    DTSTART:20161102T090000
    RRULE:FREQ=MONTHLY;BYSETPOS=1;BYDAY=MO;INTERVAL=3;UNTIL=20191224T000000
''')

rule_monthly = rrule.rrulestr('''
    DTSTART:20161102T090000
    RRULE:FREQ=MONTHLY;BYSETPOS=1;BYDAY=MO;UNTIL=20191224T000000
''')

rule_weekly = rrule.rrulestr('''
    DTSTART:20161102T090000
    RRULE:FREQ=WEEKLY;BYDAY=MO;UNTIL=20191224T000000
''')

freq_dict = {
    'monthly': rule_monthly,
    'weekly': rule_weekly,
    'quarterly': rule_quarterly,
}

def get_aggregate_between(rules, date_from, date_to):
    dfs = []
    for (event_type, name, rule, value) in rules:
        dates = rule.between(date_from, date_to)
        values = np.full(len(dates), value)
        df = pd.DataFrame(values, index=dates, columns=[event_type])
        dfs.append(df)

    print(dfs)
    product = reduce((lambda x, y: x.add(y, fill_value=0)), dfs)
    return product


def get_stacked_data():
    income_events = get_income_events()
    expense_events = get_expense_events()
    events = income_events + expense_events

    out = []
    agg = get_aggregate_between(events, datetime(2018, 5, 14), datetime(2018, 12, 1)).resample('W').mean().fillna(0)

    cap = 1000
    for d in agg.itertuples():
        cap += d.income
        cap += d.expense

        out.append({
            "datetime":d[0].strftime("%Y-%m-%d"),
            "expense":d.expense,
            "income":d.income,
            "capital": max(0, cap - d.income),
        })

    return out


def get_all_rules():
    events_data = data.get_events_data()
    events_data = events_data.strip().split('\n')

    rules = []
    for event_data in events_data:
        (event_type, freq, desc, q) = tuple(event_data.split(','))
        # if event_type != 'expense':
        #     continue
        # r = (event_type, desc, freq_dict[freq], -abs(float(q)))
        r = (event_type, desc, freq, float(q))
        rules.append(r)
    return rules


def get_expense():
    events = get_expense_events()

    out = []
    # agg = pd.date_range(datetime(2017, 1, 14), datetime(2018, 5, 14), freq='W')
    # for t in agg:
    #     k = np.random.random()*300
    #     out.append([t.strftime("%Y-%m-%d"), k])

    agg = get_aggregate_between(events, datetime(2018, 5, 14), datetime(2018, 12, 1)).resample('W').mean().fillna(0)

    for t, k in agg.itertuples():
        out.append([t.strftime("%Y-%m-%d"), k])

    return out

def get_income():
    events = get_income_events()

    out = []

    agg = get_aggregate_between(events, datetime(2018, 5, 14), datetime(2018, 12, 1)).resample('W').mean().fillna(0)
    for t, k in agg.itertuples():
        out.append([t.strftime("%Y-%m-%d"), k])

    return out

def get_expense_events():
    events_data = data.get_events_data()
    events_data = events_data.strip().split('\n')

    rules = []
    for event_data in events_data:
        (event_type, freq, desc, q) = tuple(event_data.split(','))
        if event_type != 'expense':
            continue
        r = (event_type, desc, freq_dict[freq], -abs(float(q)))
        rules.append(r)

    return rules


def get_income_events():
    events_data = data.get_events_data()
    events_data = events_data.strip().split('\n')

    rules = []
    for event_data in events_data:
        (event_type, freq, desc, q) = tuple(event_data.split(','))
        if event_type != 'income':
            continue
        r = (event_type, desc, freq_dict[freq], float(q))
        rules.append(r)

    return rules




def getdataspls():
    # print()
    rules_data = data.get_events_data()
    rules_data = rules_data.split('\n')

    if rules_data[-1] == '':
        rules_data = rules_data[:-1]

    rules = []
    for rule_data in rules_data:
        (freq, desc, q) = tuple(rule_data.split(','))
        freq = freq_dict[freq]
        q = float(q)
        r = (desc, freq, q)
        rules.append(r)
    # print(rules_data)
    print('111111111--------------')
    print(rules)
    # rules = [
    #     ('food', rule_weekly, 50),
    #     ('entertainment', rule_weekly, 25),
    #     ('fuel', rule_weekly, 20),
    #     ('haircut', rule_quarterly, 25),
    #     ('clothes', rule_quarterly, 50),
    #     ('misc', rule_monthly, 35),
    #     ('rent', rule_monthly, 400),
    # ]

    out = []

    agg = pd.date_range(datetime(2017, 1, 14), datetime(2018, 5, 14), freq='W')
    for t in agg:
        k = np.random.random()*300
        out.append([t.strftime("%Y-%m-%d"), k])

    print(rules)
    agg = get_aggregate_between(rules, datetime(2018, 5, 14), datetime(2018, 12, 1)).resample('W').mean().fillna(0)
    print(agg)
    for t, k in agg.itertuples():
        out.append([t.strftime("%Y-%m-%d"), k])

    return out

if __name__ == "__main__":
    pass
    # agg = getdataspls()
    # s = rrule.rruleset()

    # s.rrule(rrule.rrule(
    #     rrule.WEEKLY,
    #     byweekday=rrule.TU,
    #     dtstart=parser.parse("20021102T090000"),
    #     until=parser.parse("20031224T000000")
    # ))
    # s.exrule(rrule.rrule(
    #     rrule.WEEKLY,
    #     byweekday=rrule.TU,
    #     dtstart=parser.parse("20030124T000000")
    # ))

    # # k = list(rule)
    # k = s.between(datetime(2002, 11, 1), datetime(2003, 1, 1))

    # rr = rrule.rrule(
    #     rrule.MONTHLY,
    #     interval=3,
    #     byweekday=rrule.MO,
    #     bysetpos=1,
    #     dtstart=parser.parse("20161102T090000"),
    #     until=parser.parse("20181224T000000")
    # )

    # ds = list(rr)
    # print(ds)



    # ds = list(rule_weekly)
    # print(ds)

    # dsv = np.full(len(ds), 2)
    # _ds = list(zip(ds, dsv))

    # pdd = pd.DataFrame(dsv, index=ds, columns=['values'])
    # # pdd['dates'] = pd.to_datetime(pdd['dates'])
    # # pdd.index = pdd['dates']
    # # del pdd['dates']


    # pdd = pdd ** 2
    # print(pdd)
    # print()
    # print(pdd.resample('Y').sum())
    # print(dir(rr.rrule))
    # print()
    # print(dir(rule))
    # print()
    # print(k)

#     test_risk_metrics()
#     test_risk_adjusted_metrics()

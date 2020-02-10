import numpy as np
import pandas as pd
from app import db
from app.models.component import ComponentModel
from datetime import datetime
from functools import reduce
from dateutil import rrule


def get_all_stacked_data_for(account_id):
    components = db.session.query(
        ComponentModel
    ).filter_by(
        account_id=account_id,
    ).all()

    date_from, date_to = datetime.now(), datetime(2019, 12, 17)
    dfs = []
    for component in components:
        rule = rrule.rrulestr(component.rrule)
        dates = rule.between(date_from, date_to)
        q = float(component.quantity)
        if component.component_type == 'expense':
            q = -abs(q)
        values = np.full(len(dates), q)
        df = pd.DataFrame(
            values, index=dates, columns=[component.component_type])
        dfs.append(df)

    all_df = reduce((lambda x, y: x.add(y, fill_value=0)), dfs)
    all_df_adjusted = all_df.resample('W').sum().fillna(0)

    out = []
    cap = 0
    for d in all_df_adjusted.itertuples():
        cap += d.income
        cap += d.expense

        out.append({
            "datetime": d[0].strftime("%Y-%m-%d"),
            "expense": d.expense,
            "income": d.income,
            "capital": max(0, cap - d.income),
        })

    return out

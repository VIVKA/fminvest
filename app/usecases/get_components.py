from app import db
from app.models.component import ComponentModel


def get_all_components_for(account_id):
    components = db.session.query(
        ComponentModel
    ).filter_by(
        account_id=account_id,
    ).all()

    income = []
    expense = []
    other = []
    for component in components:
        c = (
            component.id,
            component.component_type,
            component.description,
            component.frequency,
            component.quantity,
        )

        if component.component_type == 'income':
            income.append(c)
        elif component.component_type == 'expense':
            expense.append(c)
        else:
            other.append(c)

    return {
        'income': income,
        'expense': expense,
        'other': other
    }

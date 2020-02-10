from app import db
from app.models.component import ComponentModel


def delete_component(component_id):
    db.session.query(
        ComponentModel
    ).filter(
        ComponentModel.id == component_id,
    ).delete()

    db.session.commit()

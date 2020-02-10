"""Simulations

Revision ID: 72ab2d9b7571
Revises: e01fbe058045
Create Date: 2018-10-08 02:01:19.865645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72ab2d9b7571'
down_revision = 'e01fbe058045'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'simulations',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('asset_key', sa.String, nullable=False),
        sa.Column('weights', sa.String, nullable=False),
        sa.Column('n', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint('asset_key'),
    )


def downgrade():
    op.drop_table('simulations')

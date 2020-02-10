"""create tables

Revision ID: e01fbe058045
Revises:
Create Date: 2018-06-19 00:02:28.473524

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e01fbe058045'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'accounts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('token', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )

    op.create_table(
        'components',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('account_id', sa.Integer, nullable=False),
        sa.Column('component_type', sa.String(50), nullable=False),
        sa.Column('frequency', sa.String(50), nullable=False),
        sa.Column('rrule', sa.String(100), nullable=False),
        sa.Column('description', sa.String(100), nullable=False),
        sa.Column('quantity', sa.Float(), nullable=False),
        sa.Column('end_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )

def downgrade():
    op.drop_table('components')
    op.drop_table('accounts')

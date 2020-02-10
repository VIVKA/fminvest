"""currencies

Revision ID: b28271228095
Revises: 7fad58f42594
Create Date: 2019-01-27 01:34:29.600156

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b28271228095'
down_revision = '7fad58f42594'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'currency_pairs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('currency_type', sa.String(10), nullable=False),
        sa.Column('symbol_from', sa.String(10), nullable=False),
        sa.Column('symbol_to', sa.String(10), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),

        sa.UniqueConstraint('symbol_from', 'symbol_to'),
    )

    op.create_table(
        'currency_pair_data',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('currency_pair_id', sa.Integer, nullable=False),
        sa.Column('trade_date', sa.Date, nullable=False),

        sa.Column('open_price', sa.Float, nullable=False),
        sa.Column('high_price', sa.Float, nullable=False),
        sa.Column('low_price', sa.Float, nullable=False),
        sa.Column('close_price', sa.Float, nullable=False),

        sa.ForeignKeyConstraint(['currency_pair_id'], ['currency_pairs.id']),
        sa.UniqueConstraint('currency_pair_id', 'trade_date'),
    )


def downgrade():
    op.drop_table('currency_pair_data')
    op.drop_table('currency_pairs')

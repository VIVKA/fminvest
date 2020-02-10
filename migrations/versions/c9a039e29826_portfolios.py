"""portfolios

Revision ID: c9a039e29826
Revises: 72ab2d9b7571
Create Date: 2018-11-13 03:28:46.169468

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9a039e29826'
down_revision = '72ab2d9b7571'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'portfolios',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('account_id', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id']),
    )

    op.create_table(
        'assets',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('asset_type', sa.String(50), nullable=False),
        sa.Column('ticker', sa.String(50), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('country', sa.String(10), nullable=False),
        sa.Column('sector', sa.String(50), nullable=False),
        sa.Column('currency', sa.String(10), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint('ticker', 'country'),
    )

    op.create_table(
        'asset_data',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('asset_id', sa.Integer, nullable=False),
        sa.Column('trade_date', sa.Date, nullable=False),

        sa.Column('open_price', sa.Float, nullable=False),
        sa.Column('high_price', sa.Float, nullable=False),
        sa.Column('low_price', sa.Float, nullable=False),
        sa.Column('close_price', sa.Float, nullable=False),
        sa.Column('adjusted_close_price', sa.Float, nullable=False),
        sa.Column('trade_volume', sa.Integer, nullable=False),

        sa.Column('dividend_amount', sa.Float, nullable=True),
        sa.Column('split_coefficient', sa.Float, nullable=True),
        sa.Column('maturity_date', sa.Date, nullable=True),
        sa.Column('coupon_percent', sa.Float, nullable=True),
        sa.Column('coupon_value', sa.Float, nullable=True),
        sa.Column('yield_amount', sa.Float, nullable=True),
        sa.Column('accrued_interest', sa.Float, nullable=True),

        sa.ForeignKeyConstraint(['asset_id'], ['assets.id']),
        sa.UniqueConstraint('asset_id', 'trade_date'),
    )

    op.create_table(
        'portfolio_assets',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('portfolio_id', sa.Integer, nullable=False),
        sa.Column('asset_id', sa.Integer, nullable=False),
        sa.Column('amount', sa.Integer, nullable=False),
        sa.Column('traded_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['portfolio_id'], ['portfolios.id']),
        sa.ForeignKeyConstraint(['asset_id'], ['assets.id']),
    )


def downgrade():
    op.drop_table('portfolio_assets')
    op.drop_table('asset_data')
    op.drop_table('assets')
    op.drop_table('portfolios')

"""misc fields

Revision ID: 446e6235ad36
Revises: b28271228095
Create Date: 2019-01-28 03:06:02.203171

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '446e6235ad36'
down_revision = 'b28271228095'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('simulations', sa.Column('hull', sa.String(), nullable=False, server_default=''))
    op.create_index('idx_assets_ticker', 'assets', ['ticker'])
    op.create_index('idx_asset_data_asset_id', 'asset_data', ['asset_id'])
    op.create_index('idx_portfolio_account_id', 'portfolios', ['account_id'])
    op.create_index('idx_portfolio_assets_portfolio_id', 'portfolio_assets', ['portfolio_id'])
    op.create_index('idx_portfolio_assets_asset_id', 'portfolio_assets', ['asset_id'])
    op.create_index('idx_currency_pair_data_currency_pair_id', 'currency_pair_data', ['currency_pair_id'])
    op.create_index('idx_simulations_asset_key', 'simulations', ['asset_key'])


def downgrade():
    op.drop_column('simulations', 'hull')
    op.drop_index('idx_assets_ticker')
    op.drop_index('idx_asset_data_asset_id')
    op.drop_index('idx_portfolio_account_id')
    op.drop_index('idx_portfolio_assets_portfolio_id')
    op.drop_index('idx_portfolio_assets_asset_id')
    op.drop_index('idx_currency_pair_data_currency_pair_id')
    op.drop_index('idx_simulations_asset_key')

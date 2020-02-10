"""portfolio actions

Revision ID: 39ddaf76545f
Revises: 446e6235ad36
Create Date: 2019-02-06 17:42:30.753035

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39ddaf76545f'
down_revision = '446e6235ad36'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'portfolio_actions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('action_type', sa.String(20), nullable=False),
        sa.Column('portfolio_id', sa.Integer, nullable=False),
        sa.Column('asset_id', sa.Integer, nullable=False),
        sa.Column('amount', sa.Integer, nullable=False),
        sa.Column('price', sa.Float, nullable=False),
        sa.Column('action_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['portfolio_id'], ['portfolios.id']),
        sa.ForeignKeyConstraint(['asset_id'], ['assets.id']),
    )
    op.create_index('idx_portfolio_actions_portfolio_id', 'portfolio_actions', ['portfolio_id'])
    op.create_index('idx_portfolio_actions_asset_id', 'portfolio_actions', ['asset_id'])


def downgrade():
    op.drop_index('idx_portfolio_actions_portfolio_id')
    op.drop_index('idx_portfolio_actions_asset_id')
    op.drop_table('portfolio_actions')

"""nuke portfolio assets

Revision ID: 477523436f77
Revises: 39ddaf76545f
Create Date: 2019-03-11 16:17:33.080548

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '477523436f77'
down_revision = '39ddaf76545f'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('portfolio_assets')


def downgrade():
    pass

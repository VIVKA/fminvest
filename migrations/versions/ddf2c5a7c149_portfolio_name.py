"""portfolio name

Revision ID: ddf2c5a7c149
Revises: 477523436f77
Create Date: 2019-03-28 17:34:10.903322

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ddf2c5a7c149'
down_revision = '477523436f77'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('portfolios', sa.Column('name', sa.String(50), nullable=True))


def downgrade():
    op.drop_column('portfolios', 'name')

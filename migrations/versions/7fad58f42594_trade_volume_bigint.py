"""trade_volume bigint

Revision ID: 7fad58f42594
Revises: c9a039e29826
Create Date: 2018-12-01 14:46:19.049931

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fad58f42594'
down_revision = 'c9a039e29826'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('asset_data', 'trade_volume', existing_type=sa.Integer(), type_=sa.BigInteger())


def downgrade():
    op.alter_column('asset_data', 'trade_volume', existing_type=sa.BigInteger(), type_=sa.Integer())

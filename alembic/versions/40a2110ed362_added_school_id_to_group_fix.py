"""added school_id to group (fix)

Revision ID: 40a2110ed362
Revises: 78f05d4e5203
Create Date: 2022-06-13 01:34:03.233529

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40a2110ed362'
down_revision = '78f05d4e5203'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('groups', schema=None) as batch_op:
        batch_op.add_column(sa.Column('school_id', sa.Integer()))


def downgrade() -> None:
    with op.batch_alter_table('groups', schema=None) as batch_op:
        batch_op.drop_column('id')

"""fix1

Revision ID: c1a872221cdb
Revises: 74d6f63aacd7
Create Date: 2022-06-15 13:11:49.461807

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1a872221cdb'
down_revision = '74d6f63aacd7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_table('_alembic_tmp_groups')


def downgrade() -> None:
    op.create_table('_alembic_tmp_groups',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('school_id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )

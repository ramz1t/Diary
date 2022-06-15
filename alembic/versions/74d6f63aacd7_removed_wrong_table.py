"""removed wrong table

Revision ID: 74d6f63aacd7
Revises: 40a2110ed362
Create Date: 2022-06-15 12:00:58.978858

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74d6f63aacd7'
down_revision = '40a2110ed362'
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

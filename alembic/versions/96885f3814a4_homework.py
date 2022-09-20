"""'homework'

Revision ID: 96885f3814a4
Revises: f702ddf59ed4
Create Date: 2022-09-19 16:46:42.297248

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96885f3814a4'
down_revision = 'f702ddf59ed4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('homework',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('class_date', sa.String(), nullable=True),
    sa.Column('time', sa.String(), nullable=True),
    sa.Column('exec_time', sa.Integer(), nullable=True),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.Column('db_group_id', sa.Integer(), nullable=True),
    sa.Column('body', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['db_group_id'], ['groups.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('homework')
    # ### end Alembic commands ###
"""changed login to email

Revision ID: 9b8f18615e4d
Revises: 4833b63f0ff4
Create Date: 2022-06-06 16:51:48.647049

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b8f18615e4d'
down_revision = '4833b63f0ff4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admins', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(), nullable=True))
        batch_op.drop_column('name')

    with op.batch_alter_table('students', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(), nullable=True))
        batch_op.drop_column('login')

    with op.batch_alter_table('teachers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(), nullable=True))
        batch_op.drop_column('login')

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('teachers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('login', sa.VARCHAR(), nullable=True))
        batch_op.drop_column('email')

    with op.batch_alter_table('students', schema=None) as batch_op:
        batch_op.add_column(sa.Column('login', sa.VARCHAR(), nullable=True))
        batch_op.drop_column('email')

    with op.batch_alter_table('admins', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(), nullable=True))
        batch_op.drop_column('email')

    # ### end Alembic commands ###

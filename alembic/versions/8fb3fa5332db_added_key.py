"""added key

Revision ID: 8fb3fa5332db
Revises: 9b8f18615e4d
Create Date: 2022-06-09 10:34:42.612758

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8fb3fa5332db'
down_revision = '9b8f18615e4d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('students', schema=None) as batch_op:
        batch_op.add_column(sa.Column('surname', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('students', schema=None) as batch_op:
        batch_op.drop_column('surname')

    # ### end Alembic commands ###

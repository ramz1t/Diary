"""fix

Revision ID: 78f05d4e5203
Revises: beebd8638b3a
Create Date: 2022-06-13 01:32:51.174229

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78f05d4e5203'
down_revision = 'beebd8638b3a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('groups')
    op.create_table('groups',
                    sa.Column('id', sa.Integer()),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )


    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('groups')
    op.create_table('groups',
                    sa.Column('name', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('name')
                    )

    # ### end Alembic commands ###
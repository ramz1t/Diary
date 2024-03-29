"""'initial'

Revision ID: b6b4e6d2ae22
Revises: 
Create Date: 2023-01-10 19:20:26.916903

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6b4e6d2ae22'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('school_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('keys',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('surname', sa.String(), nullable=True),
    sa.Column('group', sa.String(), nullable=True),
    sa.Column('school_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('schools',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teacher_keys',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('surname', sa.String(), nullable=True),
    sa.Column('school_id', sa.Integer(), nullable=True),
    sa.Column('value', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('telegram_autorizations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('diary_id', sa.Integer(), nullable=True),
    sa.Column('mark', sa.Boolean(), nullable=True),
    sa.Column('hw', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('classes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('subject_id', sa.Integer(), nullable=True),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.Column('school_db_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['school_db_id'], ['schools.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('school_db_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['school_db_id'], ['schools.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subjects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('school_db_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['school_db_id'], ['schools.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teachers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('surname', sa.String(), nullable=True),
    sa.Column('school_id', sa.Integer(), nullable=True),
    sa.Column('school_db_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['school_db_id'], ['schools.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('homework',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('class_date', sa.String(), nullable=True),
    sa.Column('time', sa.String(), nullable=True),
    sa.Column('exec_time', sa.Integer(), nullable=True),
    sa.Column('db_group_id', sa.Integer(), nullable=True),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.Column('body', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['db_group_id'], ['groups.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('scheduleclasses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('class_number', sa.Integer(), nullable=True),
    sa.Column('day_number', sa.Integer(), nullable=True),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('students',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('surname', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('school_id', sa.Integer(), nullable=True),
    sa.Column('group', sa.String(), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('marks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.Column('date', sa.String(), nullable=True),
    sa.Column('time', sa.String(), nullable=True),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.Column('final', sa.Boolean(), nullable=True),
    sa.Column('season', sa.Integer(), nullable=True),
    sa.Column('comment', sa.String(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('marks')
    op.drop_table('students')
    op.drop_table('scheduleclasses')
    op.drop_table('homework')
    op.drop_table('teachers')
    op.drop_table('subjects')
    op.drop_table('groups')
    op.drop_table('classes')
    op.drop_table('telegram_autorizations')
    op.drop_table('teacher_keys')
    op.drop_table('schools')
    op.drop_table('keys')
    op.drop_table('admins')
    # ### end Alembic commands ###

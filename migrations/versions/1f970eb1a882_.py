"""empty message

Revision ID: 1f970eb1a882
Revises: f92126c38ede
Create Date: 2021-10-13 09:22:12.539489

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1f970eb1a882'
down_revision = 'f92126c38ede'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('manager',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=15), nullable=False),
    sa.Column('password', sa.String(length=64), nullable=False),
    sa.Column('phone', sa.String(length=11), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notice',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('notice_title', sa.String(length=20), nullable=False),
    sa.Column('notice_content', sa.TEXT(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('students',
    sa.Column('id', sa.String(length=8), nullable=False),
    sa.Column('username', sa.String(length=15), nullable=False),
    sa.Column('password', sa.String(length=64), nullable=False),
    sa.Column('phone', sa.String(length=11), nullable=False),
    sa.Column('dormitory', sa.String(length=8), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('worker',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=15), nullable=False),
    sa.Column('password', sa.String(length=64), nullable=False),
    sa.Column('phone', sa.String(length=11), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_index('id', table_name='miss_person')
    op.drop_table('miss_person')
    op.drop_table('users')
    op.drop_table('news')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('news',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('news_area', mysql.VARCHAR(length=20), nullable=False),
    sa.Column('news_title', mysql.VARCHAR(length=20), nullable=False),
    sa.Column('news_main', mysql.TEXT(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('users',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', mysql.VARCHAR(length=15), nullable=False),
    sa.Column('password', mysql.VARCHAR(length=64), nullable=False),
    sa.Column('phone', mysql.VARCHAR(length=11), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('miss_person',
    sa.Column('id', mysql.VARCHAR(length=18), nullable=False),
    sa.Column('miss_name', mysql.VARCHAR(length=10), nullable=False),
    sa.Column('miss_reason', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('miss_place', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('miss_sex', mysql.VARCHAR(length=1), nullable=False),
    sa.Column('phone', mysql.VARCHAR(length=11), nullable=False),
    sa.Column('other_phone', mysql.VARCHAR(length=11), nullable=True),
    sa.Column('miss_info', mysql.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('id', 'miss_person', ['id'], unique=False)
    op.drop_table('worker')
    op.drop_table('students')
    op.drop_table('notice')
    op.drop_table('manager')
    # ### end Alembic commands ###

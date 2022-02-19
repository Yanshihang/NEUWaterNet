"""empty message

Revision ID: e807ed32cfe8
Revises: 4e795598fe95
Create Date: 2021-10-17 21:11:10.023516

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e807ed32cfe8'
down_revision = '4e795598fe95'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notify',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=20), nullable=False),
    sa.Column('content', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('notice')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notice',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', mysql.VARCHAR(length=20), nullable=False),
    sa.Column('content', mysql.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('notify')
    # ### end Alembic commands ###
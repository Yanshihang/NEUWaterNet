"""empty message

Revision ID: c4cba5d35043
Revises: fd2f8b6c428c
Create Date: 2021-10-17 17:23:20.477592

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4cba5d35043'
down_revision = 'fd2f8b6c428c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('students', sa.Column('order', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('students', 'order')
    # ### end Alembic commands ###

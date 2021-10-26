"""removed column.

Revision ID: 848636aa4b59
Revises: 
Create Date: 2021-10-26 21:33:54.067953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '848636aa4b59'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('plots',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('users_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=45), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sensor_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('sensors_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sensors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sensor_type', sa.Integer(), nullable=True),
    sa.Column('plots_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=45), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=45), nullable=True),
    sa.Column('name', sa.String(length=45), nullable=True),
    sa.Column('password', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('sensors')
    op.drop_table('sensor_data')
    op.drop_table('plots')
    # ### end Alembic commands ###
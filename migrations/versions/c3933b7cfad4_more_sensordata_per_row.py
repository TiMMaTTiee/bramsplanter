"""More sensordata per row

Revision ID: c3933b7cfad4
Revises: 5ca6f7023a79
Create Date: 2021-11-26 20:34:02.486776

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c3933b7cfad4'
down_revision = '5ca6f7023a79'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sensor_data', sa.Column('soil_moist1', sa.Integer(), nullable=True))
    op.add_column('sensor_data', sa.Column('soil_moist2', sa.Integer(), nullable=True))
    op.add_column('sensor_data', sa.Column('soil_temp1', sa.Integer(), nullable=True))
    op.add_column('sensor_data', sa.Column('soil_temp2', sa.Integer(), nullable=True))
    op.add_column('sensor_data', sa.Column('cell1', sa.Integer(), nullable=True))
    op.add_column('sensor_data', sa.Column('cell2', sa.Integer(), nullable=True))
    op.add_column('sensor_data', sa.Column('cell3', sa.Integer(), nullable=True))
    op.add_column('sensor_data', sa.Column('air_moist1', sa.Integer(), nullable=True))
    op.add_column('sensor_data', sa.Column('air_temp1', sa.Integer(), nullable=True))
    op.add_column('sensor_data', sa.Column('solar_bool', sa.Integer(), nullable=True))
    op.add_column('sensor_data', sa.Column('air_moist2', sa.Integer(), nullable=True))
    op.add_column('sensor_data', sa.Column('air_temp2', sa.Integer(), nullable=True))
    op.add_column('sensor_data', sa.Column('lux', sa.Integer(), nullable=True))
    op.add_column('sensor_data', sa.Column('flow_rate', sa.Integer(), nullable=True))
    op.add_column('sensor_data', sa.Column('plots_id', sa.Integer(), nullable=True))
    op.drop_column('sensor_data', 'value')
    op.drop_column('sensor_data', 'sensors_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sensor_data', sa.Column('sensors_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('sensor_data', sa.Column('value', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('sensor_data', 'plots_id')
    op.drop_column('sensor_data', 'flow_rate')
    op.drop_column('sensor_data', 'lux')
    op.drop_column('sensor_data', 'air_temp2')
    op.drop_column('sensor_data', 'air_moist2')
    op.drop_column('sensor_data', 'solar_bool')
    op.drop_column('sensor_data', 'air_temp1')
    op.drop_column('sensor_data', 'air_moist1')
    op.drop_column('sensor_data', 'cell3')
    op.drop_column('sensor_data', 'cell2')
    op.drop_column('sensor_data', 'cell1')
    op.drop_column('sensor_data', 'soil_temp2')
    op.drop_column('sensor_data', 'soil_temp1')
    op.drop_column('sensor_data', 'soil_moist2')
    op.drop_column('sensor_data', 'soil_moist1')
    # ### end Alembic commands ###
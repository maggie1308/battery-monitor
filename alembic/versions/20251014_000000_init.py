from alembic import op
import sqlalchemy as sa

revision = '20251014_000000_init'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'devices',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False, unique=True),
        sa.Column('firmware_version', sa.String(length=50), nullable=False),
        sa.Column('is_on', sa.Boolean(), nullable=False, server_default=sa.false()),
    )

    op.create_table(
        'batteries',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('nominal_voltage', sa.Float(), nullable=False),
        sa.Column('remaining_capacity', sa.Float(), nullable=False),
        sa.Column('service_life_months', sa.Integer(), nullable=False),
    )

    op.create_table(
        'device_battery',
        sa.Column('device_id', sa.Integer(), sa.ForeignKey('devices.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('battery_id', sa.Integer(), sa.ForeignKey('batteries.id', ondelete='CASCADE'), primary_key=True),
    )
    op.create_unique_constraint('uq_device_battery', 'device_battery', ['device_id','battery_id'])

def downgrade() -> None:
    op.drop_constraint('uq_device_battery', 'device_battery', type_='unique')
    op.drop_table('device_battery')
    op.drop_table('batteries')
    op.drop_table('devices')

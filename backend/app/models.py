from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, UniqueConstraint, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

device_battery = Table(
    "device_battery",
    Base.metadata,
    Column("device_id", ForeignKey("devices.id", ondelete="CASCADE"), primary_key=True),
    Column("battery_id", ForeignKey("batteries.id", ondelete="CASCADE"), primary_key=True),
    UniqueConstraint("device_id", "battery_id", name="uq_device_battery")
)

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    firmware_version = Column(String(50), nullable=False)
    is_on = Column(Boolean, nullable=False, default=False)

    batteries = relationship(
        "Battery",
        secondary=device_battery,
        back_populates="devices",
        cascade="all,delete"
    )

class Battery(Base):
    __tablename__ = "batteries"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    nominal_voltage = Column(Float, nullable=False)
    remaining_capacity = Column(Float, nullable=False)
    service_life_months = Column(Integer, nullable=False)

    devices = relationship(
        "Device",
        secondary=device_battery,
        back_populates="batteries",
    )

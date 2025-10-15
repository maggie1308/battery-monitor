from typing import List, Optional
from pydantic import BaseModel, Field, conint

class BatteryBase(BaseModel):
    name: str = Field(..., max_length=100)
    nominal_voltage: float
    remaining_capacity: float
    service_life_months: conint(ge=0)

class BatteryCreate(BatteryBase):
    pass

class BatteryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    nominal_voltage: Optional[float] = None
    remaining_capacity: Optional[float] = None
    service_life_months: Optional[int] = None

class BatteryOut(BatteryBase):
    id: int
    class Config:
        from_attributes = True

class DeviceBase(BaseModel):
    name: str = Field(..., max_length=100)
    firmware_version: str = Field(..., max_length=50)
    is_on: bool = False

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    firmware_version: Optional[str] = Field(None, max_length=50)
    is_on: Optional[bool] = None

class DeviceOut(DeviceBase):
    id: int
    class Config:
        from_attributes = True

class DeviceWithBatteries(DeviceOut):
    batteries: List[BatteryOut] = []

class BatteryWithDevices(BatteryOut):
    devices: List[DeviceOut] = []

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..deps import get_db_sess, http_404

router = APIRouter(prefix="/devices", tags=["links"])

@router.post("/{device_id}/batteries/{battery_id}", status_code=201)
def link_battery(device_id: int, battery_id: int, db: Session = Depends(get_db_sess)):
    device = db.query(models.Device).get(device_id)
    if not device:
        http_404("Device")
    battery = db.query(models.Battery).get(battery_id)
    if not battery:
        http_404("Battery")

    if len(device.batteries) >= 5 and battery not in device.batteries:
        raise HTTPException(status_code=400, detail="device already has 5 batteries")

    if battery in device.batteries:
        return {"message": "already linked"}

    device.batteries.append(battery)
    db.commit()
    return {"message": "linked"}

@router.delete("/{device_id}/batteries/{battery_id}", status_code=204)
def unlink_battery(device_id: int, battery_id: int, db: Session = Depends(get_db_sess)):
    device = db.query(models.Device).get(device_id)
    if not device:
        http_404("Device")
    battery = db.query(models.Battery).get(battery_id)
    if not battery:
        http_404("Battery")

    if battery in device.batteries:
        device.batteries.remove(battery)
        db.commit()
    return None

@router.get("/{device_id}/batteries", response_model=list[schemas.BatteryOut])
def list_device_batteries(device_id: int, db: Session = Depends(get_db_sess)):
    device = db.query(models.Device).get(device_id)
    if not device:
        http_404("Device")
    return device.batteries

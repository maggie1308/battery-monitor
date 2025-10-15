from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..deps import get_db_sess, http_404

router = APIRouter(prefix="/devices", tags=["devices"])

@router.get("", response_model=List[schemas.DeviceOut])
def list_devices(db: Session = Depends(get_db_sess)):
    return db.query(models.Device).order_by(models.Device.id).all()

@router.post("", response_model=schemas.DeviceOut, status_code=201)
def create_device(payload: schemas.DeviceCreate, db: Session = Depends(get_db_sess)):
    if db.query(models.Device).filter_by(name=payload.name).first():
        raise HTTPException(status_code=400, detail="device name must be unique")
    obj = models.Device(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/{device_id}", response_model=schemas.DeviceWithBatteries)
def get_device(device_id: int, db: Session = Depends(get_db_sess)):
    obj = db.query(models.Device).get(device_id)
    if not obj:
        http_404("Device")
    return obj

@router.put("/{device_id}", response_model=schemas.DeviceOut)
@router.patch("/{device_id}", response_model=schemas.DeviceOut)
def update_device(device_id: int, payload: schemas.DeviceUpdate, db: Session = Depends(get_db_sess)):
    obj = db.query(models.Device).get(device_id)
    if not obj:
        http_404("Device")
    data = payload.model_dump(exclude_unset=True)
    if "name" in data:
        exists = db.query(models.Device).filter(models.Device.name==data["name"], models.Device.id!=device_id).first()
        if exists:
            raise HTTPException(status_code=400, detail="device name must be unique")
    for k, v in data.items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{device_id}", status_code=204)
def delete_device(device_id: int, db: Session = Depends(get_db_sess)):
    obj = db.query(models.Device).get(device_id)
    if not obj:
        http_404("Device")
    db.delete(obj)
    db.commit()
    return None

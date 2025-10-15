from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..deps import get_db_sess, http_404

router = APIRouter(prefix="/batteries", tags=["batteries"])

@router.get("", response_model=List[schemas.BatteryOut])
def list_batteries(db: Session = Depends(get_db_sess)):
    return db.query(models.Battery).order_by(models.Battery.id).all()

@router.post("", response_model=schemas.BatteryOut, status_code=201)
def create_battery(payload: schemas.BatteryCreate, db: Session = Depends(get_db_sess)):
    obj = models.Battery(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/{battery_id}", response_model=schemas.BatteryWithDevices)
def get_battery(battery_id: int, db: Session = Depends(get_db_sess)):
    obj = db.query(models.Battery).get(battery_id)
    if not obj:
        http_404("Battery")
    return obj

@router.put("/{battery_id}", response_model=schemas.BatteryOut)
@router.patch("/{battery_id}", response_model=schemas.BatteryOut)
def update_battery(battery_id: int, payload: schemas.BatteryUpdate, db: Session = Depends(get_db_sess)):
    obj = db.query(models.Battery).get(battery_id)
    if not obj:
        http_404("Battery")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{battery_id}", status_code=204)
def delete_battery(battery_id: int, db: Session = Depends(get_db_sess)):
    obj = db.query(models.Battery).get(battery_id)
    if not obj:
        http_404("Battery")
    db.delete(obj)
    db.commit()
    return None

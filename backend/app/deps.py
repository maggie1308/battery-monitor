from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db

def get_db_sess(db: Session = Depends(get_db)) -> Session:
    return db

def http_404(entity: str):
    raise HTTPException(status_code=404, detail=f"{entity} not found")

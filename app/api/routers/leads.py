from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import SessionLocal
from app.db import crud_lead
from app.schemas.lead import LeadCreate, LeadOut

router = APIRouter(prefix="/leads", tags=["leads"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=List[LeadOut])
def list_leads(
    location: Optional[str] = Query(None, description="Ciudad exacta, e.g., Bogota"),
    min: Optional[int] = Query(None, ge=0),
    max: Optional[int] = Query(None, ge=0),
    db: Session = Depends(get_db),
):
    items = crud_lead.list_filtered(db, location, min, max)
    return items

@router.post("", response_model=LeadOut, status_code=201)
def create_lead(payload: LeadCreate, db: Session = Depends(get_db)):
    try:
        obj = crud_lead.create_one(db, payload.model_dump())
        return obj
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

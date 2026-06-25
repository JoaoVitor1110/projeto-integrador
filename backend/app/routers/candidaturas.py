from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models
from app.schemas import CandidaturaCreate, CandidaturaResponse
from datetime import date

router = APIRouter()

@router.post("/", response_model=CandidaturaResponse)
def create_candidatura(candidatura: CandidaturaCreate, db: Session = Depends(get_db)):
    data = candidatura.model_dump()
    if data.get("data_candidatura") is None:
        data["data_candidatura"] = date.today()
    db_candidatura = models.Candidatura(**data)
    db.add(db_candidatura)
    db.commit()
    db.refresh(db_candidatura)
    return db_candidatura

@router.get("/", response_model=List[CandidaturaResponse])
def list_candidaturas(db: Session = Depends(get_db)):
    return db.query(models.Candidatura).all()

@router.get("/{id}", response_model=CandidaturaResponse)
def get_candidatura(id: int, db: Session = Depends(get_db)):
    candidatura = db.query(models.Candidatura).filter(models.Candidatura.id == id).first()
    if not candidatura:
        raise HTTPException(status_code=404, detail="Candidatura não encontrada")
    return candidatura

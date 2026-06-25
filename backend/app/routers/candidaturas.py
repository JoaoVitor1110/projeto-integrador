from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/candidaturas", tags=["candidaturas"])


@router.post("/", response_model=schemas.CandidaturaResponse, status_code=201)
def create_candidatura(candidatura: schemas.CandidaturaCreate, db: Session = Depends(get_db)):
    db_candidatura = models.Candidatura(**candidatura.model_dump())
    db.add(db_candidatura)
    db.commit()
    db.refresh(db_candidatura)
    return db_candidatura


@router.get("/", response_model=List[schemas.CandidaturaResponse])
def list_candidaturas(db: Session = Depends(get_db)):
    return db.query(models.Candidatura).all()


@router.get("/{candidatura_id}", response_model=schemas.CandidaturaResponse)
def get_candidatura(candidatura_id: int, db: Session = Depends(get_db)):
    candidatura = db.query(models.Candidatura).filter(models.Candidatura.id == candidatura_id).first()
    if not candidatura:
        raise HTTPException(status_code=404, detail="Candidatura não encontrada")
    return candidatura

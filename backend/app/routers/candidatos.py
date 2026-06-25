from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/candidatos", tags=["candidatos"])


@router.post("/", response_model=schemas.CandidatoResponse, status_code=201)
def create_candidato(candidato: schemas.CandidatoCreate, db: Session = Depends(get_db)):
    db_candidato = models.Candidato(**candidato.model_dump())
    db.add(db_candidato)
    db.commit()
    db.refresh(db_candidato)
    return db_candidato


@router.get("/", response_model=List[schemas.CandidatoResponse])
def list_candidatos(db: Session = Depends(get_db)):
    return db.query(models.Candidato).all()


@router.get("/{candidato_id}", response_model=schemas.CandidatoResponse)
def get_candidato(candidato_id: int, db: Session = Depends(get_db)):
    candidato = db.query(models.Candidato).filter(models.Candidato.id == candidato_id).first()
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato não encontrado")
    return candidato

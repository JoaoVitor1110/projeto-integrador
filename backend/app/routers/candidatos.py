from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models
from app.schemas import CandidatoCreate, CandidatoResponse

router = APIRouter()

@router.post("/", response_model=CandidatoResponse)
def create_candidato(candidato: CandidatoCreate, db: Session = Depends(get_db)):
    db_candidato = models.Candidato(**candidato.model_dump())
    db.add(db_candidato)
    db.commit()
    db.refresh(db_candidato)
    return db_candidato

@router.get("/", response_model=List[CandidatoResponse])
def list_candidatos(db: Session = Depends(get_db)):
    return db.query(models.Candidato).all()

@router.get("/{id}", response_model=CandidatoResponse)
def get_candidato(id: int, db: Session = Depends(get_db)):
    candidato = db.query(models.Candidato).filter(models.Candidato.id == id).first()
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato não encontrado")
    return candidato

@router.put("/{id}", response_model=CandidatoResponse)
def update_candidato(id: int, dados: CandidatoCreate, db: Session = Depends(get_db)):
    candidato = db.query(models.Candidato).filter(models.Candidato.id == id).first()
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato não encontrado")
    for k, v in dados.model_dump().items():
        setattr(candidato, k, v)
    db.commit()
    db.refresh(candidato)
    return candidato

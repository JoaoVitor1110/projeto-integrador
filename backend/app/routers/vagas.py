from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app import models
from app.schemas import VagaCreate, VagaResponse
from app.models import ModalidadeEnum, TipoContratoEnum, StatusVagaEnum
from datetime import date

router = APIRouter()

@router.post("/", response_model=VagaResponse)
def create_vaga(vaga: VagaCreate, db: Session = Depends(get_db)):
    data = vaga.model_dump()
    if data.get("data_publicacao") is None:
        data["data_publicacao"] = date.today()
    db_vaga = models.Vaga(**data)
    db.add(db_vaga)
    db.commit()
    db.refresh(db_vaga)
    return db_vaga

@router.get("/", response_model=List[VagaResponse])
def list_vagas(
    modalidade: Optional[ModalidadeEnum] = None,
    tipo_contrato: Optional[TipoContratoEnum] = None,
    vaga_pcd: Optional[bool] = None,
    status: Optional[StatusVagaEnum] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Vaga)
    if modalidade:
        query = query.filter(models.Vaga.modalidade == modalidade)
    if tipo_contrato:
        query = query.filter(models.Vaga.tipo_contrato == tipo_contrato)
    if vaga_pcd is not None:
        query = query.filter(models.Vaga.vaga_pcd == vaga_pcd)
    if status:
        query = query.filter(models.Vaga.status == status)
    return query.all()

@router.get("/{id}", response_model=VagaResponse)
def get_vaga(id: int, db: Session = Depends(get_db)):
    vaga = db.query(models.Vaga).filter(models.Vaga.id == id).first()
    if not vaga:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    return vaga

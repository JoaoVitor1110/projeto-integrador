from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.database import get_db
from app import models, auth
from app.schemas import VagaCreate, VagaResponse
from app.models import ModalidadeEnum, TipoContratoEnum, StatusVagaEnum, PerfilEnum

router = APIRouter()

_ESCRITORES = Depends(auth.exigir_perfil(PerfilEnum.admin, PerfilEnum.recrutador))


@router.post("/", response_model=VagaResponse)
def create_vaga(
    vaga: VagaCreate,
    db: Session = Depends(get_db),
    _: models.Usuario = _ESCRITORES,
):
    data = vaga.model_dump()
    if data.get("data_publicacao") is None:
        data["data_publicacao"] = date.today()
    if data.get("data_abertura") is None:
        data["data_abertura"] = date.today()
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


@router.put("/{id}", response_model=VagaResponse)
def update_vaga(
    id: int,
    vaga: VagaCreate,
    db: Session = Depends(get_db),
    _: models.Usuario = _ESCRITORES,
):
    db_vaga = db.query(models.Vaga).filter(models.Vaga.id == id).first()
    if not db_vaga:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    data = vaga.model_dump()
    if data.get("status") == StatusVagaEnum.encerrada and db_vaga.status != StatusVagaEnum.encerrada:
        if not data.get("data_fechamento"):
            data["data_fechamento"] = date.today()
    for k, v in data.items():
        setattr(db_vaga, k, v)
    db.commit()
    db.refresh(db_vaga)
    return db_vaga


@router.delete("/{id}", status_code=204)
def delete_vaga(
    id: int,
    db: Session = Depends(get_db),
    _: models.Usuario = _ESCRITORES,
):
    db_vaga = db.query(models.Vaga).filter(models.Vaga.id == id).first()
    if not db_vaga:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    db.delete(db_vaga)
    db.commit()

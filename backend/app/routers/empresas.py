from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, auth
from app.schemas import EmpresaCreate, EmpresaResponse
from app.models import PerfilEnum

router = APIRouter()

_ESCRITORES = Depends(auth.exigir_perfil(PerfilEnum.admin, PerfilEnum.recrutador))


@router.post("/", response_model=EmpresaResponse)
def create_empresa(
    empresa: EmpresaCreate,
    db: Session = Depends(get_db),
    _: models.Usuario = _ESCRITORES,
):
    db_empresa = models.Empresa(**empresa.model_dump())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa


@router.get("/", response_model=List[EmpresaResponse])
def list_empresas(db: Session = Depends(get_db)):
    return db.query(models.Empresa).all()


@router.get("/{id}", response_model=EmpresaResponse)
def get_empresa(id: int, db: Session = Depends(get_db)):
    empresa = db.query(models.Empresa).filter(models.Empresa.id == id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return empresa


@router.put("/{id}", response_model=EmpresaResponse)
def update_empresa(
    id: int,
    empresa: EmpresaCreate,
    db: Session = Depends(get_db),
    _: models.Usuario = _ESCRITORES,
):
    db_empresa = db.query(models.Empresa).filter(models.Empresa.id == id).first()
    if not db_empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    for k, v in empresa.model_dump().items():
        setattr(db_empresa, k, v)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa


@router.delete("/{id}", status_code=204)
def delete_empresa(
    id: int,
    db: Session = Depends(get_db),
    _: models.Usuario = _ESCRITORES,
):
    empresa = db.query(models.Empresa).filter(models.Empresa.id == id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    db.delete(empresa)
    db.commit()

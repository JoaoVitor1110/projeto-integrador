from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from pydantic import BaseModel

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
    beneficios_nomes = data.pop("beneficios_nomes", [])
    requisitos_lista = data.pop("requisitos_lista", [])
    if data.get("data_publicacao") is None:
        data["data_publicacao"] = date.today()
    if data.get("data_abertura") is None:
        data["data_abertura"] = date.today()
    db_vaga = models.Vaga(**data)
    db.add(db_vaga)
    db.flush()
    for nome in beneficios_nomes:
        nome = nome.strip()
        if not nome:
            continue
        b = db.query(models.Beneficio).filter(models.Beneficio.nome == nome).first()
        if not b:
            b = models.Beneficio(nome=nome)
            db.add(b)
            db.flush()
        db_vaga.beneficios.append(b)
    for r in requisitos_lista:
        desc = r.get("descricao", "").strip()
        nivel = r.get("nivel", "desejavel")
        if not desc:
            continue
        req = models.Requisito(descricao=desc, nivel=nivel)
        db.add(req)
        db.flush()
        db_vaga.requisitos.append(req)
    db.commit()
    db.refresh(db_vaga)
    return db_vaga


@router.get("/", response_model=List[VagaResponse])
def list_vagas(
    modalidade: Optional[ModalidadeEnum] = None,
    tipo_contrato: Optional[TipoContratoEnum] = None,
    vaga_pcd: Optional[bool] = None,
    status: Optional[StatusVagaEnum] = None,
    recrutador_id: Optional[int] = None,
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
    if recrutador_id is not None:
        query = query.filter(models.Vaga.recrutador_id == recrutador_id)
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


class AtribuirRecrutadorBody(BaseModel):
    recrutador_id: Optional[int] = None


@router.patch("/{id}/recrutador", response_model=VagaResponse)
def atribuir_recrutador(
    id: int,
    body: AtribuirRecrutadorBody,
    db: Session = Depends(get_db),
    atual: models.Usuario = _ESCRITORES,
):
    db_vaga = db.query(models.Vaga).filter(models.Vaga.id == id).first()
    if not db_vaga:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    if body.recrutador_id is not None:
        recrutador = db.query(models.Usuario).filter(models.Usuario.id == body.recrutador_id).first()
        if not recrutador:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        if recrutador.perfil not in (PerfilEnum.admin, PerfilEnum.recrutador):
            raise HTTPException(status_code=400, detail="Usuário não tem perfil de recrutador")
    db_vaga.recrutador_id = body.recrutador_id
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

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/vagas", tags=["vagas"])


@router.post("/", response_model=schemas.VagaResponse, status_code=201)
def create_vaga(vaga: schemas.VagaCreate, db: Session = Depends(get_db)):
    data = vaga.model_dump(exclude={"beneficio_ids", "requisito_ids"})
    db_vaga = models.Vaga(**data)
    if vaga.beneficio_ids:
        db_vaga.beneficios = db.query(models.Beneficio).filter(models.Beneficio.id.in_(vaga.beneficio_ids)).all()
    if vaga.requisito_ids:
        db_vaga.requisitos = db.query(models.Requisito).filter(models.Requisito.id.in_(vaga.requisito_ids)).all()
    db.add(db_vaga)
    db.commit()
    db.refresh(db_vaga)
    return db_vaga


@router.get("/", response_model=List[schemas.VagaResponse])
def list_vagas(
    modalidade: Optional[models.ModalidadeEnum] = Query(None),
    tipo_contrato: Optional[models.TipoContratoEnum] = Query(None),
    vaga_pcd: Optional[bool] = Query(None),
    status: Optional[models.StatusVagaEnum] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(models.Vaga)
    if modalidade:
        q = q.filter(models.Vaga.modalidade == modalidade)
    if tipo_contrato:
        q = q.filter(models.Vaga.tipo_contrato == tipo_contrato)
    if vaga_pcd is not None:
        q = q.filter(models.Vaga.vaga_pcd == vaga_pcd)
    if status:
        q = q.filter(models.Vaga.status == status)
    return q.all()


@router.get("/{vaga_id}", response_model=schemas.VagaResponse)
def get_vaga(vaga_id: int, db: Session = Depends(get_db)):
    vaga = db.query(models.Vaga).filter(models.Vaga.id == vaga_id).first()
    if not vaga:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    return vaga

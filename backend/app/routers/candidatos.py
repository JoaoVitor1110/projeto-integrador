import os
import shutil
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, auth
from app.schemas import CandidatoCreate, CandidatoResponse

router = APIRouter()

UPLOAD_DIR = "/app/uploads/curriculos"
ALLOWED_TYPES = {
    "application/pdf": ".pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "application/msword": ".doc",
}


def _ensure_upload_dir():
    os.makedirs(UPLOAD_DIR, exist_ok=True)


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


@router.delete("/{id}", status_code=204)
def delete_candidato(
    id: int,
    db: Session = Depends(get_db),
    _=Depends(auth.exigir_perfil("admin")),
):
    candidato = db.query(models.Candidato).filter(models.Candidato.id == id).first()
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato não encontrado")
    if candidato.curriculo_path and os.path.exists(candidato.curriculo_path):
        os.remove(candidato.curriculo_path)
    db.delete(candidato)
    db.commit()


@router.post("/{id}/curriculo", response_model=CandidatoResponse)
def upload_curriculo(
    id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    atual: models.Usuario = Depends(auth.get_usuario_atual),
):
    candidato = db.query(models.Candidato).filter(models.Candidato.id == id).first()
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato não encontrado")

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Formato inválido. Envie um arquivo PDF ou DOCX.",
        )

    ext = ALLOWED_TYPES[file.content_type]
    _ensure_upload_dir()

    # Remove currículo anterior se existir
    if candidato.curriculo_path and os.path.exists(candidato.curriculo_path):
        os.remove(candidato.curriculo_path)

    filename = f"candidato_{id}_{uuid.uuid4().hex[:8]}{ext}"
    dest = os.path.join(UPLOAD_DIR, filename)
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)

    candidato.curriculo_path = dest
    db.commit()
    db.refresh(candidato)
    return candidato


@router.get("/{id}/curriculo")
def download_curriculo(
    id: int,
    db: Session = Depends(get_db),
    _=Depends(auth.get_usuario_atual),
):
    candidato = db.query(models.Candidato).filter(models.Candidato.id == id).first()
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato não encontrado")
    if not candidato.curriculo_path or not os.path.exists(candidato.curriculo_path):
        raise HTTPException(status_code=404, detail="Currículo não encontrado")

    ext = os.path.splitext(candidato.curriculo_path)[1].lower()
    media_type = (
        "application/pdf" if ext == ".pdf"
        else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    safe_name = f"curriculo_{candidato.nome.replace(' ', '_')}{ext}"
    return FileResponse(candidato.curriculo_path, media_type=media_type, filename=safe_name)

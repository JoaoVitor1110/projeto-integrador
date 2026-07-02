from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict

from app.database import get_db
from app import models, auth

router = APIRouter()


class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str
    perfil: models.PerfilEnum = models.PerfilEnum.visualizador


class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    email: str
    perfil: models.PerfilEnum


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    usuario: UsuarioResponse


@router.post("/login", response_model=TokenResponse)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == form.username).first()
    if not usuario or not auth.verificar_senha(form.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = auth.criar_token(
        {"sub": usuario.email},
        timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": token, "token_type": "bearer", "usuario": usuario}


@router.post("/usuarios", response_model=UsuarioResponse)
def criar_usuario(
    dados: UsuarioCreate,
    db: Session = Depends(get_db),
    _: models.Usuario = Depends(auth.exigir_perfil(models.PerfilEnum.admin)),
):
    if db.query(models.Usuario).filter(models.Usuario.email == dados.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    usuario = models.Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=auth.hash_senha(dados.senha),
        perfil=dados.perfil,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.get("/me", response_model=UsuarioResponse)
def me(usuario: models.Usuario = Depends(auth.get_usuario_atual)):
    return usuario


@router.get("/usuarios", response_model=list[UsuarioResponse])
def listar_usuarios(
    db: Session = Depends(get_db),
    _: models.Usuario = Depends(auth.exigir_perfil(models.PerfilEnum.admin)),
):
    return db.query(models.Usuario).all()


@router.delete("/usuarios/{usuario_id}", status_code=204)
def deletar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    atual: models.Usuario = Depends(auth.exigir_perfil(models.PerfilEnum.admin)),
):
    if atual.id == usuario_id:
        raise HTTPException(status_code=400, detail="Você não pode excluir seu próprio usuário.")
    alvo = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not alvo:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    if alvo.perfil == models.PerfilEnum.admin:
        total_admins = db.query(models.Usuario).filter(
            models.Usuario.perfil == models.PerfilEnum.admin
        ).count()
        if total_admins <= 1:
            raise HTTPException(status_code=400, detail="Não é possível excluir o último admin do sistema.")
    db.delete(alvo)
    db.commit()

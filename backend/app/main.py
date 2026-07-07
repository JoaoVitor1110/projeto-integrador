import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine, SessionLocal
from app import models  # noqa: F401 - registers models
from app.routers import empresas, vagas, candidatos, candidaturas
from app.routers import auth as auth_router
from app.auth import hash_senha

Base.metadata.create_all(bind=engine)

def _seed_admin():
    db = SessionLocal()
    try:
        if db.query(models.Usuario).count() == 0:
            admin_email = os.getenv("ADMIN_EMAIL")
            admin_senha = os.getenv("ADMIN_SENHA")
            admin_nome = os.getenv("ADMIN_NOME", "Admin")
            if not admin_email or not admin_senha:
                return  # skip seed if credentials not configured
            db.add(models.Usuario(
                nome=admin_nome,
                email=admin_email,
                senha_hash=hash_senha(admin_senha),
                perfil=models.PerfilEnum.admin,
            ))
            db.commit()
    finally:
        db.close()

_seed_admin()

app = FastAPI(title="Agência de Empregos API")

_cors_origins_env = os.getenv("CORS_ORIGINS", "")
_allowed_origins = (
    [o.strip() for o in _cors_origins_env.split(",") if o.strip()]
    if _cors_origins_env
    else [
        "https://projeto-integrador-senac.streamlit.app",
        "http://localhost:8501",
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
app.include_router(empresas.router, prefix="/empresas", tags=["Empresas"])
app.include_router(vagas.router, prefix="/vagas", tags=["Vagas"])
app.include_router(candidatos.router, prefix="/candidatos", tags=["Candidatos"])
app.include_router(candidaturas.router, prefix="/candidaturas", tags=["Candidaturas"])


@app.get("/")
def root():
    return {"message": "Agência de Empregos API", "docs": "/docs"}

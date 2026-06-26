from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app import models  # noqa: F401 - registers models
from app.routers import empresas, vagas, candidatos, candidaturas
from app.routers import auth as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Agência de Empregos API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
app.include_router(empresas.router, prefix="/empresas", tags=["Empresas"])
app.include_router(vagas.router, prefix="/vagas", tags=["Vagas"])
app.include_router(candidatos.router, prefix="/candidatos", tags=["Candidatos"])
app.include_router(candidaturas.router, prefix="/candidaturas", tags=["Candidaturas"])


@app.get("/")
def root():
    return {"message": "Agência de Empregos API", "docs": "/docs"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app import models
from app.routers import empresas, vagas, candidatos, candidaturas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Agência de Empregos API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(empresas.router)
app.include_router(vagas.router)
app.include_router(candidatos.router)
app.include_router(candidaturas.router)


@app.get("/")
def root():
    return {"message": "Agência de Empregos API", "docs": "/docs"}

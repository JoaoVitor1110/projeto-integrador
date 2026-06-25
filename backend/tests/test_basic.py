import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

# StaticPool garante que a mesma conexão in-memory é reutilizada em todos os testes
TEST_DATABASE_URL = "sqlite://"
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_root_returns_200():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Agência de Empregos API"


def test_create_empresa():
    response = client.post("/empresas/", json={
        "nome": "Empresa Teste",
        "cnpj": "99.999.999/0001-99",
        "setor": "Tecnologia",
        "descricao": "Empresa de teste",
        "cidade": "São Paulo",
        "estado": "SP"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Empresa Teste"
    assert "id" in data


def test_list_empresas():
    response = client.get("/empresas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_create_vaga():
    emp_response = client.post("/empresas/", json={
        "nome": "Empresa Vaga Teste",
        "cnpj": "88.888.888/0001-88",
        "setor": "Tech",
        "cidade": "Rio de Janeiro",
        "estado": "RJ"
    })
    empresa_id = emp_response.json()["id"]

    response = client.post("/vagas/", json={
        "titulo": "Dev Backend",
        "local": "Rio de Janeiro, RJ",
        "salario": 8000.0,
        "modalidade": "remoto",
        "horario": "Segunda a Sexta",
        "tipo_contrato": "CLT",
        "publico_alvo": "ambos",
        "vaga_pcd": False,
        "status": "aberta",
        "empresa_id": empresa_id
    })
    assert response.status_code == 200
    assert response.json()["titulo"] == "Dev Backend"


def test_list_vagas():
    response = client.get("/vagas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_create_candidato():
    response = client.post("/candidatos/", json={
        "nome": "João Teste",
        "email": "joao.teste@email.com",
        "telefone": "(11) 91234-5678",
        "cidade": "Campinas",
        "estado": "SP"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "João Teste"
    assert "id" in data

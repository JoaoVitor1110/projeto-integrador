import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app import models
from app.auth import hash_senha

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


# ── fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def limpar_bd():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)


def _criar_usuario(perfil: models.PerfilEnum) -> dict:
    email = f"{perfil.value}@teste.com"
    db = TestingSessionLocal()
    try:
        u = models.Usuario(nome=perfil.value, email=email, senha_hash=hash_senha("senha123"), perfil=perfil)
        db.add(u)
        db.commit()
    finally:
        db.close()
    resp = client.post("/auth/login", data={"username": email, "password": "senha123"})
    assert resp.status_code == 200
    return resp.json()["access_token"]


def _headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _criar_empresa(token: str) -> dict:
    r = client.post("/empresas/", json={
        "nome": "Emp Teste", "cnpj": "11.111.111/0001-11",
        "setor": "TI", "cidade": "SP", "estado": "SP",
    }, headers=_headers(token))
    assert r.status_code == 200
    return r.json()


# ── testes gerais ────────────────────────────────────────────────────────────

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["message"] == "Agência de Empregos API"


# ── testes de auth ────────────────────────────────────────────────────────────

def test_login_correto():
    _criar_usuario(models.PerfilEnum.visualizador)
    # login já testado dentro de _criar_usuario, só verificamos /me
    token = _criar_usuario(models.PerfilEnum.admin)
    r = client.get("/auth/me", headers=_headers(token))
    assert r.status_code == 200
    assert r.json()["perfil"] == "admin"


def test_login_senha_errada():
    _criar_usuario(models.PerfilEnum.visualizador)
    r = client.post("/auth/login", data={"username": "visualizador@teste.com", "password": "errada"})
    assert r.status_code == 401


def test_token_invalido_retorna_401():
    r = client.get("/auth/me", headers={"Authorization": "Bearer token-invalido"})
    assert r.status_code == 401


# ── proteção de endpoints ────────────────────────────────────────────────────

def test_criar_empresa_sem_token_retorna_401():
    r = client.post("/empresas/", json={
        "nome": "X", "cnpj": "00.000.000/0001-00", "setor": "X", "cidade": "X", "estado": "SP"
    })
    assert r.status_code == 401


def test_criar_empresa_visualizador_retorna_403():
    token = _criar_usuario(models.PerfilEnum.visualizador)
    r = client.post("/empresas/", json={
        "nome": "X", "cnpj": "00.000.000/0001-00", "setor": "X", "cidade": "X", "estado": "SP"
    }, headers=_headers(token))
    assert r.status_code == 403


def test_criar_empresa_admin_ok():
    token = _criar_usuario(models.PerfilEnum.admin)
    emp = _criar_empresa(token)
    assert emp["nome"] == "Emp Teste"


def test_criar_vaga_recrutador_ok():
    token = _criar_usuario(models.PerfilEnum.recrutador)
    emp = _criar_empresa(_criar_usuario(models.PerfilEnum.admin))
    r = client.post("/vagas/", json={
        "titulo": "Dev", "local": "SP", "salario": 5000,
        "modalidade": "remoto", "tipo_contrato": "CLT",
        "publico_alvo": "ambos", "vaga_pcd": False,
        "status": "aberta", "empresa_id": emp["id"],
    }, headers=_headers(token))
    assert r.status_code == 200
    assert r.json()["titulo"] == "Dev"


def test_criar_vaga_sem_token_retorna_401():
    r = client.post("/vagas/", json={
        "titulo": "Dev", "local": "SP", "salario": 5000,
        "modalidade": "remoto", "tipo_contrato": "CLT",
        "publico_alvo": "ambos", "vaga_pcd": False,
        "status": "aberta", "empresa_id": 1,
    })
    assert r.status_code == 401


def test_listar_vagas_publico():
    r = client.get("/vagas/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_criar_candidato_publico():
    r = client.post("/candidatos/", json={
        "nome": "João", "email": "joao@email.com",
        "cidade": "SP", "estado": "SP",
    })
    assert r.status_code == 200
    assert r.json()["nome"] == "João"


def test_senha_nao_exposta():
    token = _criar_usuario(models.PerfilEnum.admin)
    r = client.get("/auth/me", headers=_headers(token))
    assert "senha" not in r.json()
    assert "senha_hash" not in r.json()

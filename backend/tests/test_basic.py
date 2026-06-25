import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_returns_200():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Agência de Empregos API"

def test_create_empresa():
    response = client.post("/empresas/", json={
        "nome": "Empresa Teste",
        "cnpj": "99.999.999/0001-99",
        "setor": "Tecnologia",
        "descricao": "Empresa de teste",
        "cidade": "São Paulo",
        "estado": "SP"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Empresa Teste"
    assert "id" in data

def test_list_empresas():
    response = client.get("/empresas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_vaga():
    # First create an empresa to reference
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
    assert response.status_code == 201
    data = response.json()
    assert data["titulo"] == "Dev Backend"

def test_list_vagas_after_seed():
    # Seed data inline for test isolation
    from app.database import SessionLocal, engine
    from app.database import Base
    from app import models
    from datetime import date

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(models.Empresa).filter(models.Empresa.cnpj == "11.111.111/0001-11").first() is None:
            emp = models.Empresa(nome="Seed Test Co", cnpj="11.111.111/0001-11", setor="TI", cidade="SP", estado="SP")
            db.add(emp)
            db.commit()
            db.refresh(emp)
            vaga = models.Vaga(titulo="QA Engineer", local="SP", salario=7000.0, modalidade=models.ModalidadeEnum.remoto, tipo_contrato=models.TipoContratoEnum.CLT, empresa_id=emp.id, data_publicacao=date.today())
            db.add(vaga)
            db.commit()
    finally:
        db.close()

    response = client.get("/vagas/")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_create_candidato():
    response = client.post("/candidatos/", json={
        "nome": "João Teste",
        "email": "joao.teste.unique@email.com",
        "telefone": "(11) 91234-5678",
        "cidade": "Campinas",
        "estado": "SP"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "João Teste"
    assert "id" in data

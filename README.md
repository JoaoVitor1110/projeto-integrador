# Projeto Integrador — Agência de Empregos

Sistema de gerenciamento de vagas de emprego desenvolvido com Python e FastAPI.

## Descrição

API RESTful para uma agência de empregos, permitindo o cadastro de empresas, vagas, candidatos e candidaturas. O sistema suporta filtros por modalidade, tipo de contrato, status da vaga e acessibilidade (PcD).

## Tecnologias

- **Python 3.11+**
- **FastAPI** — framework web moderno e de alta performance
- **SQLAlchemy 2.0** — ORM para banco de dados
- **SQLite** — banco de dados relacional leve
- **Pydantic v2** — validação de dados
- **Uvicorn** — servidor ASGI

## Instalação

```bash
pip install -r backend/requirements.txt
```

## Como executar

```bash
cd backend
uvicorn app.main:app --reload
```

## Popular o banco de dados (seed)

```bash
cd backend
python seed.py
```

## Executar os testes

```bash
cd backend
pytest tests/
```

## Documentação interativa

Após iniciar o servidor, acesse: http://localhost:8000/docs

## Inspecionar o banco de dados

O arquivo `agencia_empregos.db` é criado na pasta `backend/` ao iniciar o servidor.
Para inspecioná-lo visualmente, utilize o [DB Browser for SQLite](https://sqlitebrowser.org/).

## Estrutura do projeto

```
backend/
├── app/
│   ├── main.py          # Entrypoint da aplicação FastAPI
│   ├── models.py        # Modelos SQLAlchemy
│   ├── database.py      # Configuração do banco de dados
│   ├── schemas.py       # Schemas Pydantic
│   └── routers/         # Rotas da API
│       ├── empresas.py
│       ├── vagas.py
│       ├── candidatos.py
│       └── candidaturas.py
├── tests/
│   └── test_basic.py    # Testes automatizados
├── seed.py              # Script para popular o banco
└── requirements.txt     # Dependências Python
```

## Endpoints principais

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | / | Status da API |
| POST | /empresas/ | Cadastrar empresa |
| GET | /empresas/ | Listar empresas |
| GET | /empresas/{id} | Buscar empresa |
| POST | /vagas/ | Cadastrar vaga |
| GET | /vagas/ | Listar vagas (com filtros) |
| GET | /vagas/{id} | Buscar vaga |
| POST | /candidatos/ | Cadastrar candidato |
| GET | /candidatos/ | Listar candidatos |
| POST | /candidaturas/ | Registrar candidatura |
| GET | /candidaturas/ | Listar candidaturas |

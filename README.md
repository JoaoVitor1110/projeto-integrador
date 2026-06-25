# Projeto Integrador — Agência de Empregos

Sistema de gerenciamento de vagas de emprego desenvolvido com Python e FastAPI.

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Backend/API | Python 3.11 + FastAPI |
| Banco (Fase 1) | SQLite (arquivo local, zero configuração) |
| Banco (Fase 2+) | PostgreSQL local → AWS RDS |
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic |
| Validação | Pydantic v2 |
| Servidor | Uvicorn |

---

## Fase 1 — SQLite local

### Instalação

```bash
pip install -r backend/requirements.txt
```

### Executar a aplicação

```bash
cd backend
uvicorn app.main:app --reload
```

### Popular o banco (seed)

```bash
cd backend
python seed.py
```

Insere: 5 empresas, 10 vagas, 5 benefícios, 6 requisitos, 3 candidatos, 2 candidaturas.

### Executar os testes

```bash
cd backend
pytest tests/ -v
```

Os testes rodam em banco SQLite in-memory isolado — sem dependência de serviços externos.

### Documentação interativa

Após iniciar o servidor: http://localhost:8000/docs

### Inspecionar o banco

O arquivo `agencia_empregos.db` é criado em `backend/`. Use o [DB Browser for SQLite](https://sqlitebrowser.org/) para inspecioná-lo visualmente.

---

## Fase 2 — PostgreSQL com Docker

### Pré-requisitos

- Docker e Docker Compose instalados

### Configurar variáveis de ambiente

```bash
cp .env.example .env
# Edite .env se necessário (os valores padrão já funcionam com o docker-compose)
```

### Subir o banco PostgreSQL

```bash
docker-compose up -d
```

### Executar as migrations (Alembic)

```bash
cd backend
DATABASE_URL=postgresql://agencia_user:agencia_pass@localhost:5432/agencia_empregos \
  alembic upgrade head
```

### Executar a aplicação com PostgreSQL

```bash
cd backend
DATABASE_URL=postgresql://agencia_user:agencia_pass@localhost:5432/agencia_empregos \
  uvicorn app.main:app --reload
```

### Popular o banco com PostgreSQL

```bash
cd backend
DATABASE_URL=postgresql://agencia_user:agencia_pass@localhost:5432/agencia_empregos \
  python seed.py
```

### Plano de migração para AWS RDS

Quando for migrar para produção, basta:

1. Criar uma instância RDS PostgreSQL na AWS (via console ou Terraform)
2. Configurar o security group para liberar a porta 5432 somente do servidor backend
3. Atualizar a variável `DATABASE_URL` no `.env` de produção:

```
DATABASE_URL=postgresql://usuario:senha@endpoint-do-rds.us-east-1.rds.amazonaws.com:5432/agencia_empregos
```

**Nenhuma linha de código precisa ser alterada** — a troca é só na variável de ambiente.

---

## Estrutura do projeto

```
projeto-integrador/
├── backend/
│   ├── app/
│   │   ├── main.py          # Entrypoint FastAPI
│   │   ├── models.py        # Modelos SQLAlchemy
│   │   ├── database.py      # Conexão via DATABASE_URL
│   │   ├── schemas.py       # Schemas Pydantic v2
│   │   └── routers/         # Endpoints REST
│   ├── alembic/             # Migrations versionadas
│   ├── tests/               # Testes automatizados
│   ├── seed.py              # Dados de exemplo
│   └── requirements.txt
├── docker-compose.yml        # PostgreSQL local
├── .env.example              # Template de variáveis (sem credenciais reais)
└── README.md
```

## Endpoints principais

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | / | Status da API |
| POST | /empresas/ | Cadastrar empresa |
| GET | /empresas/ | Listar empresas |
| GET | /empresas/{id} | Buscar empresa por ID |
| POST | /vagas/ | Cadastrar vaga |
| GET | /vagas/ | Listar vagas (filtros: modalidade, tipo_contrato, vaga_pcd, status) |
| GET | /vagas/{id} | Buscar vaga por ID |
| POST | /candidatos/ | Cadastrar candidato |
| GET | /candidatos/ | Listar candidatos |
| POST | /candidaturas/ | Registrar candidatura |
| GET | /candidaturas/ | Listar candidaturas |

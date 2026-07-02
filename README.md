# 💼 Agência de Empregos

> Sistema web completo para gestão de vagas de emprego — Projeto Integrador UC6 · SENAC Lapa Tito · 2026

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://projeto-integrador-senac.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3.x-003B57?logo=sqlite&logoColor=white)
![AWS EC2](https://img.shields.io/badge/AWS-EC2-FF9900?logo=amazonaws&logoColor=white)

---

## 🌐 Acesso

**[https://projeto-integrador-senac.streamlit.app](https://projeto-integrador-senac.streamlit.app)**

Sem instalação — basta abrir no navegador.

---

## 📋 Sobre o Projeto

A **Agência de Empregos** é uma plataforma web que conecta empresas recrutadoras e candidatos. O sistema permite publicar e gerenciar vagas, receber candidaturas e acompanhar todo o processo seletivo por meio de uma interface simples e intuitiva.

Desenvolvido como **Projeto Integrador da UC6** do Curso Técnico em Inteligência Artificial do SENAC Lapa Tito, integrando backend REST com FastAPI, banco de dados SQLite e interface web com Streamlit — implantado em infraestrutura real na AWS.

---

## ✨ Funcionalidades

| Perfil | Funcionalidades |
|---|---|
| 👑 **Admin** | Gerencia usuários, empresas, candidatos e vagas. Acessa o dashboard. |
| 📋 **Recrutador** | Cadastra e edita vagas, acompanha candidaturas, acessa o dashboard. |
| 🙋 **Candidato** | Visualiza vagas, se candidata e acompanha o status das candidaturas. |

### Destaques
- 🔐 Autenticação com JWT (login seguro por token)
- 📊 Dashboard com KPIs, gráficos por modalidade, contrato, empresa e salário médio
- ⚠️ Alertas de vagas abertas há mais de 30/60/90 dias
- ♿ Filtro de vagas PcD
- 🛡️ Proteções de integridade (admin não pode se excluir; último admin protegido)
- 📝 Auto-cadastro de candidatos com criação automática de perfil

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────┐
│     Usuário (Navegador Web)         │
└──────────────┬──────────────────────┘
               │ HTTPS
┌──────────────▼──────────────────────┐
│       Streamlit Cloud               │
│  projeto-integrador-senac.app       │
│       streamlit_app.py              │
└──────────────┬──────────────────────┘
               │ HTTPS via Cloudflare Tunnel
┌──────────────▼──────────────────────┐
│         AWS EC2 t3.micro            │
│      Amazon Linux 2023              │
│   FastAPI + Uvicorn  :8000          │
│   SQLite → agencia_empregos.db      │
└─────────────────────────────────────┘
```

---

## 🛠️ Tecnologias

| Camada | Tecnologia | Função |
|---|---|---|
| **Backend** | FastAPI + Uvicorn | API REST |
| **Banco de dados** | SQLite + SQLAlchemy | Persistência ORM |
| **Migrações** | Alembic | Versionamento do schema |
| **Autenticação** | JWT (python-jose) + bcrypt | Login seguro |
| **Frontend** | Streamlit | Interface web |
| **Servidor** | AWS EC2 t3.micro | Hospedagem do backend |
| **HTTPS** | Cloudflare Tunnel | Exposição segura da API |
| **Deploy frontend** | Streamlit Cloud | Hospedagem do frontend |
| **Versionamento** | Git + GitHub | Controle de código |

---

## 📁 Estrutura do Projeto

```
projeto-integrador/
├── streamlit_app.py              # Interface web (frontend)
├── requirements.txt              # Dependências do frontend
├── .streamlit/
│   └── secrets.toml              # API_URL (não versionado)
└── backend/
    ├── app/
    │   ├── main.py               # Ponto de entrada da API
    │   ├── database.py           # Configuração do banco
    │   ├── models.py             # Modelos ORM
    │   ├── schemas.py            # Schemas Pydantic
    │   ├── auth.py               # JWT + bcrypt
    │   └── routers/
    │       ├── auth.py           # Login, registro, usuários
    │       ├── vagas.py          # CRUD de vagas
    │       ├── empresas.py       # CRUD de empresas
    │       ├── candidatos.py     # CRUD de candidatos
    │       └── candidaturas.py   # CRUD de candidaturas
    ├── alembic/                  # Migrações do banco
    ├── requirements.txt          # Dependências do backend
    └── agencia_empregos.db       # Banco SQLite
```

---

## 🚀 Como Rodar Localmente

### Pré-requisitos
- Python 3.11+
- Git

### Backend

```bash
# Clone o repositório
git clone https://github.com/joaovitor1110/projeto-integrador.git
cd projeto-integrador/backend

# Crie e ative o ambiente virtual
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Instale as dependências
pip install -r requirements.txt

# Aplique as migrações
alembic upgrade head

# Inicie a API
uvicorn app.main:app --reload --port 8000
```

API disponível em `http://localhost:8000` · Docs: `http://localhost:8000/docs`

### Frontend

```bash
# Na raiz do projeto
pip install -r requirements.txt

# Configure a URL da API
mkdir -p .streamlit
echo 'API_URL = "http://localhost:8000"' > .streamlit/secrets.toml

# Inicie o Streamlit
streamlit run streamlit_app.py
```

---

## 🗄️ Banco de Dados

### Diagrama de relacionamentos

```
USUARIOS          EMPRESAS
                      │ 1:N
                   VAGAS ──── N:N ──── BENEFICIOS
                      │ N:N ─────────── REQUISITOS
                      │ 1:N
CANDIDATOS ──── CANDIDATURAS
```

### Tabelas principais

| Tabela | Descrição |
|---|---|
| `usuarios` | Contas de acesso (admin, recrutador, candidato) |
| `empresas` | Empresas cadastradas no sistema |
| `vagas` | Oportunidades de emprego |
| `candidatos` | Perfis de candidatos |
| `candidaturas` | Inscrições de candidatos em vagas |
| `beneficios` | Benefícios vinculados às vagas |
| `requisitos` | Requisitos obrigatórios e desejáveis |

### Visualizar o banco (DB Browser for SQLite)

```bash
# Copiar o banco do servidor EC2 para local
scp -i sua-chave.pem ec2-user@<IP>:/home/ec2-user/projeto-integrador/backend/agencia_empregos.db .
```

Depois abra o arquivo no [DB Browser for SQLite](https://sqlitebrowser.org/) — gratuito.

---

## 🔑 Credenciais de Teste

| Perfil | E-mail | Senha |
|---|---|---|
| 👑 Admin | joao@jvsatech.com.br | 123456Dd. |
| 🙋 Candidato | ana.lima@email.com | Senha123! |

---

## 🌍 Infraestrutura de Produção

```
GitHub (branch main)
    │
    ├── Streamlit Cloud → redeploy automático do frontend a cada push
    └── EC2 → git pull + restart uvicorn (manual)

Cloudflare Tunnel → expõe http://localhost:8000 como HTTPS público
```

### Comandos úteis no servidor EC2

```bash
# Reiniciar a API
pkill -f uvicorn
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > ~/api.log 2>&1 &

# Ver URL atual do túnel Cloudflare
grep 'trycloudflare.com' ~/tunnel.log | tail -1

# Ver logs em tempo real
tail -f ~/api.log

# Atualizar código
git pull https://joaovitor1110:<TOKEN>@github.com/joaovitor1110/projeto-integrador.git main
```

---

## 📡 Endpoints da API

| Método | Rota | Descrição | Auth |
|---|---|---|---|
| POST | `/auth/registro` | Auto-cadastro de candidato | ❌ |
| POST | `/auth/login` | Login (retorna JWT) | ❌ |
| GET | `/auth/me` | Dados do usuário logado | ✅ |
| GET/POST | `/vagas/` | Listar / criar vagas | ✅ |
| GET/PUT | `/vagas/{id}` | Detalhe / editar vaga | ✅ |
| GET/POST | `/empresas/` | Listar / criar empresas | ✅ |
| GET/PUT | `/empresas/{id}` | Detalhe / editar empresa | ✅ |
| GET/POST | `/candidatos/` | Listar / criar candidatos | ✅ |
| GET/PUT | `/candidatos/{id}` | Detalhe / editar candidato | ✅ |
| GET/POST | `/candidaturas/` | Listar / criar candidaturas | ✅ |

Documentação completa: `http://<servidor>:8000/docs`

---

## 👥 Equipe

| Nome | Instituição |
|---|---|
| João Vitor dos Santos Alves | SENAC Lapa Tito |
| Paulo Henrique Moreira Araujo | SENAC Lapa Tito |
| João Paulo Pereira da Silva | SENAC Lapa Tito |

**Orientador:** Prof. Vitor de Souza Batista

---

## 📄 Licença

Projeto acadêmico desenvolvido para fins educacionais — SENAC Lapa Tito · 2026.

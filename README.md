# 💼 Agência de Empregos

> Sistema web completo para gestão de vagas de emprego — Projeto Integrador UC6 · SENAC Lapa Tito · 2026

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://projeto-integrador-senac.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3.x-003B57?logo=sqlite&logoColor=white)
![EasyPanel](https://img.shields.io/badge/EasyPanel-Hostinger-6C47FF?logo=docker&logoColor=white)

---

## 🌐 Acesso

**[https://projeto-integrador-senac.streamlit.app](https://projeto-integrador-senac.streamlit.app)**

Sem instalação — basta abrir no navegador.

---

## 📋 Sobre o Projeto

A **Agência de Empregos** é uma plataforma web que conecta empresas recrutadoras e candidatos. O sistema permite publicar e gerenciar vagas, receber candidaturas, acompanhar todo o processo seletivo e contar com um **assistente de IA** para insights e perguntas em linguagem natural.

Desenvolvido como **Projeto Integrador da UC6** do Curso Técnico em Inteligência Artificial do SENAC Lapa Tito, integrando backend REST com FastAPI, banco de dados SQLite, interface web com Streamlit e inteligência artificial via Google Gemini — implantado em infraestrutura real na Hostinger via EasyPanel.

---

## ✨ Funcionalidades

| Perfil | Funcionalidades |
|---|---|
| 👑 **Admin** | Gerencia usuários, empresas, candidatos e vagas. Acessa o dashboard e o assistente IA. |
| 📋 **Recrutador** | Cadastra e edita vagas, acompanha candidaturas, vê candidatos inscritos por vaga, acessa o dashboard. |
| 🙋 **Candidato** | Visualiza vagas, se candidata, acompanha status das candidaturas e edita dados de contato. |

### Destaques
- 🔐 Autenticação com JWT (login seguro por token)
- 📊 Dashboard com KPIs, gráficos por modalidade, contrato, empresa e salário médio
- ⚠️ Alertas de vagas abertas há mais de 60 dias
- ♿ Filtro de vagas PcD
- 🤖 Assistente IA integrado (Google Gemini 2.5 Flash) — responde perguntas sobre vagas, candidaturas e carreira
- 👥 Recrutadores visualizam candidatos inscritos por vaga com dados de contato
- 🔄 Atualização de status de candidatura diretamente na tela da vaga
- 📝 Auto-cadastro de candidatos com criação automática de perfil
- 🛡️ Proteções de integridade (admin não pode se excluir; último admin protegido)
- 🔒 Segurança reforçada: credenciais exclusivamente por variáveis de ambiente, CORS restrito, todos os endpoints autenticados

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────┐
│        Usuário (Navegador)          │
└──────────────┬──────────────────────┘
               │ HTTPS
┌──────────────▼──────────────────────┐
│         Streamlit Cloud             │
│  projeto-integrador-senac.app       │
│  streamlit_app.py + Google Gemini   │
└──────────────┬──────────────────────┘
               │ HTTPS (Cloudflare)
┌──────────────▼──────────────────────┐
│    Hostinger VPS · EasyPanel        │
│    Docker container                 │
│    FastAPI + Uvicorn  :8000         │
│    SQLite → /data/agencia.db        │
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
| **IA** | Google Gemini 2.5 Flash | Assistente conversacional |
| **Servidor** | Hostinger VPS + EasyPanel | Hospedagem do backend em Docker |
| **HTTPS** | Cloudflare DNS + Proxy | Exposição segura da API |
| **Deploy frontend** | Streamlit Cloud | Hospedagem do frontend |
| **Versionamento** | Git + GitHub | Controle de código |

---

## 📁 Estrutura do Projeto

```
projeto-integrador/
├── streamlit_app.py              # Interface web (frontend)
├── requirements.txt              # Dependências do frontend
├── .streamlit/
│   └── secrets.toml              # API_URL + GEMINI_API_KEY (não versionado)
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
    │       └── candidaturas.py   # CRUD de candidaturas + status
    ├── alembic/                  # Migrações do banco
    ├── seed_dados.py             # Script de dados de exemplo
    └── requirements.txt          # Dependências do backend
```

---

## 🚀 Como Rodar Localmente

### Pré-requisitos
- Python 3.11+
- Git

### Backend

```bash
git clone https://github.com/joaovitor1110/projeto-integrador.git
cd projeto-integrador/backend

python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt
alembic upgrade head

export SECRET_KEY="gere-uma-chave-segura-aqui"
export ADMIN_EMAIL="admin@exemplo.com"
export ADMIN_SENHA="SuaSenhaForte!"

uvicorn app.main:app --reload --port 8000
```

API disponível em `http://localhost:8000` · Docs: `http://localhost:8000/docs`

### Frontend

```bash
pip install -r requirements.txt

mkdir -p .streamlit
cat > .streamlit/secrets.toml <<EOF
API_URL = "http://localhost:8000"
GEMINI_API_KEY = "sua-chave-aqui"
EOF

streamlit run streamlit_app.py
```

### Popular dados de exemplo

```bash
cd backend
pip install requests

SEED_API_URL=http://localhost:8000 \
SEED_ADMIN_EMAIL=admin@exemplo.com \
SEED_ADMIN_SENHA=SuaSenhaForte! \
python seed_dados.py
```

---

## 🔐 Variáveis de Ambiente

### Backend (EasyPanel / container)

| Variável | Obrigatória | Descrição |
|---|---|---|
| `SECRET_KEY` | ✅ | Chave JWT — string aleatória longa |
| `ADMIN_EMAIL` | ✅ | E-mail do admin criado na primeira inicialização |
| `ADMIN_SENHA` | ✅ | Senha do admin (mín. 8 caracteres) |
| `ADMIN_NOME` | ❌ | Nome do admin (padrão: `Admin`) |
| `CORS_ORIGINS` | ❌ | Lista separada por vírgula de origens permitidas |

### Frontend (Streamlit Cloud secrets)

| Variável | Descrição |
|---|---|
| `API_URL` | URL base do backend (ex: `https://api.alvesmotionlab.com.br`) |
| `GEMINI_API_KEY` | Chave da API do Google AI Studio |

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

### Visualizar o banco

```bash
# No terminal do EasyPanel — ver dados via SQL
sqlite3 /data/agencia_empregos.db ".tables"
sqlite3 /data/agencia_empregos.db "SELECT COUNT(*) FROM vagas;"

# Ou copie o arquivo e abra no DB Browser for SQLite (sqlitebrowser.org)
cp /data/agencia_empregos.db /app/agencia_empregos.db
```

---

## 🌍 Infraestrutura de Produção

```
GitHub (branch main)
    │
    ├── Streamlit Cloud → redeploy automático do frontend a cada push
    └── EasyPanel (Hostinger VPS) → Docker container com FastAPI
                                    volume /data para o SQLite
```

**Domínio da API:** `https://api.alvesmotionlab.com.br`

### Comandos úteis no EasyPanel (terminal do container)

```bash
# Aplicar migrações
/opt/venv/bin/alembic upgrade head

# Popular banco com dados de exemplo (requer pip install requests)
SEED_API_URL=https://api.alvesmotionlab.com.br \
SEED_ADMIN_EMAIL=seu@email.com \
SEED_ADMIN_SENHA=SuaSenha \
/opt/venv/bin/python /app/seed_dados.py

# Sincronizar versão do alembic (se necessário)
/opt/venv/bin/alembic stamp head
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
| PUT | `/candidaturas/{id}/status` | Atualizar status (admin/recrutador) | ✅ |

Documentação completa: `https://api.alvesmotionlab.com.br/docs`

---

## 🤖 Assistente IA

O assistente usa o **Google Gemini 2.5 Flash** (gratuito) e tem acesso em tempo real aos dados do sistema:

- Responde perguntas sobre vagas abertas, salários, modalidades e empresas
- Informa estatísticas de candidaturas por status
- Responde perguntas gerais sobre carreira, currículo e mercado de trabalho

**Configuração:** adicione `GEMINI_API_KEY` nos secrets do Streamlit Cloud.

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

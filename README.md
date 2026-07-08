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

A **Agência de Empregos** é uma plataforma web que conecta empresas recrutadoras e candidatos. O sistema permite publicar e gerenciar vagas com benefícios e requisitos, atribuir vagas a recrutadoras, acompanhar candidaturas com atualização de status, fazer upload de currículos e contar com um **assistente de IA** para insights em linguagem natural.

Desenvolvido como **Projeto Integrador da UC6** do Curso Técnico em Inteligência Artificial do SENAC Lapa Tito, integrando backend REST com FastAPI, banco de dados SQLite, interface web com Streamlit e inteligência artificial via Google Gemini — implantado em infraestrutura real na Hostinger via EasyPanel.

---

## ✨ Funcionalidades

| Perfil | Funcionalidades |
|---|---|
| 👑 **Admin** | Gerencia usuários, empresas, candidatos e vagas. Atribui e reatribui vagas a recrutadoras. Acessa dashboard completo com filtros e assistente IA. Baixa currículos de candidatos. |
| 📋 **Recrutador** | Cadastra e edita vagas (com benefícios e requisitos), acompanha candidaturas, vê candidatos inscritos por vaga, baixa currículos, acessa dashboard com visão das suas vagas. |
| 🙋 **Candidato** | Visualiza vagas com filtros, se candidata, acompanha status das candidaturas, edita dados de contato e envia currículo (PDF ou DOCX). |

### Destaques

- 🔐 Autenticação com JWT (login seguro por token)
- 👤 **Recrutadora responsável por vaga** — atribuição e reatribuição via botão no detalhe da vaga
- 🎁 **Benefícios e requisitos por vaga** — cadastro inline no formulário (obrigatórios e desejáveis)
- 📎 **Upload de currículo** (PDF ou DOCX) por candidato — download disponível para recrutadoras e admins
- 📊 **Dashboard completo** com filtros (recrutador, status, modalidade, empresa), KPIs de vagas e candidaturas, barras por modalidade/contrato/empresa/setor, métricas de clientes e tabela de vagas em atraso
- ⚠️ Tabela de vagas abertas há mais tempo com destaque visual para +30 dias
- 🏭 **Tela de Empresas** com métricas de clientes: ativos, empresa com mais vagas, clientes sem recrutador, tabela de gestão
- ♿ Filtro de vagas PcD
- 🤖 **Assistente IA** (Google Gemini 2.5 Flash) com contexto completo de vagas, benefícios, requisitos e candidaturas
- 👥 Recrutadoras visualizam candidatos inscritos com dados de contato e atualizam status de candidatura
- 🔄 **Auto-seed completo** na inicialização: 9 recrutadoras, 43 empresas reais, 112 vagas do backlog, 12 benefícios, requisitos por cargo e 20 candidatos fictícios com candidaturas
- 🔑 **Usuários fixos garantidos** a cada redeploy (seed de usuários por email, idempotente)
- 📝 Auto-cadastro de candidatos com criação automática de perfil ao registrar
- 🛡️ Proteções de integridade (admin não pode se excluir; último admin protegido)
- 🔒 Credenciais exclusivamente por variáveis de ambiente, CORS restrito, endpoints autenticados
- 🗄️ Migrações automáticas de schema na inicialização (sem perda de dados)

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
│    SQLite → /app/agencia_empregos.db│
│    Currículos → /app/uploads/       │
└─────────────────────────────────────┘
```

---

## 🛠️ Tecnologias

| Camada | Tecnologia | Função |
|---|---|---|
| **Backend** | FastAPI + Uvicorn | API REST |
| **Banco de dados** | SQLite + SQLAlchemy | Persistência ORM |
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
├── docs/
│   ├── api.md                    # Documentação completa dos endpoints
│   └── arquitetura.md            # Arquitetura, modelos e fluxos
└── backend/
    ├── app/
    │   ├── main.py               # Ponto de entrada; seed e migrações na inicialização
    │   ├── database.py           # Configuração do banco SQLite + SQLAlchemy
    │   ├── models.py             # Modelos ORM (Vaga, Empresa, Candidato, ...)
    │   ├── schemas.py            # Schemas Pydantic (request/response)
    │   ├── auth.py               # JWT + bcrypt + dependências de perfil
    │   └── routers/
    │       ├── auth.py           # Login, registro, usuários, recrutadores
    │       ├── vagas.py          # CRUD vagas + atribuição de recrutador
    │       ├── empresas.py       # CRUD de empresas
    │       ├── candidatos.py     # CRUD de candidatos + upload/download de currículo
    │       └── candidaturas.py   # CRUD de candidaturas + atualização de status
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

export SECRET_KEY="gere-uma-chave-segura-aqui"
export ADMIN_EMAIL="admin@exemplo.com"
export ADMIN_SENHA="SuaSenhaForte!"

uvicorn app.main:app --reload --port 8000
```

Na primeira execução o banco é criado e populado automaticamente com dados do backlog real.

API disponível em `http://localhost:8000` · Docs: `http://localhost:8000/docs`

### Frontend

```bash
cd projeto-integrador
pip install -r requirements.txt

mkdir -p .streamlit
cat > .streamlit/secrets.toml <<EOF
API_URL = "http://localhost:8000"
GEMINI_API_KEY = "sua-chave-aqui"
EOF

streamlit run streamlit_app.py
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
| `CORS_ORIGINS` | ❌ | Origens permitidas separadas por vírgula |

### Frontend (Streamlit Cloud secrets)

| Variável | Descrição |
|---|---|
| `API_URL` | URL base do backend (ex: `https://api.alvesmotionlab.com.br`) |
| `GEMINI_API_KEY` | Chave da API do Google AI Studio |

---

## 🗄️ Banco de Dados

### Diagrama de relacionamentos

```
USUARIOS ◄──── recrutador_id ────┐
                                  │
EMPRESAS ──── 1:N ───► VAGAS ────┘
                         │ N:N ──► BENEFICIOS
                         │ N:N ──► REQUISITOS
                         │ 1:N
CANDIDATOS ──── CANDIDATURAS
(curriculo_path)
```

### Tabelas principais

| Tabela | Descrição |
|---|---|
| `usuarios` | Contas de acesso (admin, recrutador, visualizador) |
| `empresas` | Empresas cadastradas no sistema |
| `vagas` | Oportunidades de emprego (inclui `recrutador_id` FK) |
| `candidatos` | Perfis de candidatos (inclui `curriculo_path`) |
| `candidaturas` | Inscrições de candidatos em vagas |
| `beneficios` | Benefícios vinculados às vagas (N:N via `vaga_beneficio`) |
| `requisitos` | Requisitos obrigatórios e desejáveis (N:N via `vaga_requisito`) |

### Auto-seed e migrações

Na inicialização o backend executa em ordem:

1. `_migrate()` — aplica colunas novas em tabelas existentes (idempotente via try/except)
2. `_seed_admin()` — cria o admin via variáveis de ambiente (apenas se `usuarios` vazio)
3. `_seed_usuarios_fixos()` — garante usuários fixos por email (idempotente a cada redeploy)
4. `_seed_dados()` — popula dados reais se `empresas` estiver vazio:
   - 9 recrutadoras (perfil recrutador, senha `Senha@123`)
   - 43 empresas reais do backlog
   - 12 benefícios (pool reutilizável por tipo de cargo)
   - 112 vagas com benefícios e requisitos gerados automaticamente
   - 20 candidatos fictícios com candidaturas aleatórias

---

## 📡 Endpoints da API

| Método | Rota | Descrição | Auth |
|---|---|---|---|
| POST | `/auth/registro` | Auto-cadastro (cria conta + perfil candidato) | ❌ |
| POST | `/auth/login` | Login (retorna JWT) | ❌ |
| GET | `/auth/me` | Dados do usuário logado | ✅ |
| GET/POST | `/auth/usuarios` | Listar / criar usuários | 👑 Admin |
| DELETE | `/auth/usuarios/{id}` | Excluir usuário | 👑 Admin |
| GET | `/auth/recrutadores` | Listar admins e recrutadores | ✅ |
| GET/POST | `/vagas/` | Listar (com filtros) / criar vagas | ✅ |
| GET/PUT/DELETE | `/vagas/{id}` | Detalhe / editar / excluir vaga | ✅ |
| PATCH | `/vagas/{id}/recrutador` | Atribuir / reatribuir recrutador | 📋 Recrutador+ |
| GET/POST | `/empresas/` | Listar / criar empresas | ✅ |
| GET/PUT/DELETE | `/empresas/{id}` | Detalhe / editar / excluir empresa | ✅ |
| GET/POST | `/candidatos/` | Listar / criar candidatos | ✅ |
| GET/PUT/DELETE | `/candidatos/{id}` | Detalhe / editar / excluir candidato | ✅ |
| POST | `/candidatos/{id}/curriculo` | Upload de currículo (PDF/DOCX) | ✅ |
| GET | `/candidatos/{id}/curriculo` | Download do currículo | ✅ |
| GET/POST | `/candidaturas/` | Listar (com filtros) / criar candidaturas | ✅ |
| PUT | `/candidaturas/{id}/status` | Atualizar status | 📋 Recrutador+ |

**Filtros disponíveis em `GET /vagas/`:** `modalidade`, `tipo_contrato`, `vaga_pcd`, `status`, `recrutador_id`

Documentação interativa: `https://api.alvesmotionlab.com.br/docs`

---

## 🤖 Assistente IA

O assistente usa o **Google Gemini 2.5 Flash** e recebe contexto em tempo real dos dados do sistema:

- Vagas abertas com salário, modalidade, benefícios e requisitos
- Vagas encerradas
- Lista de empresas cadastradas
- Resumo de candidaturas por status (pendente, em análise, aprovado, reprovado)

Exemplos de perguntas:
> "Quais vagas remotas estão abertas?"
> "Qual empresa tem mais vagas?"
> "Quantas candidaturas estão pendentes?"
> "Como formatar um currículo para vaga de produção?"

**Configuração:** adicione `GEMINI_API_KEY` nos secrets do Streamlit Cloud (Google AI Studio → gratuito).

---

## 🌍 Infraestrutura de Produção

```
GitHub (branch main)
    │
    ├── Streamlit Cloud → redeploy automático do frontend a cada push
    └── EasyPanel (Hostinger VPS) → Docker container com FastAPI
                                    SQLite em /app/agencia_empregos.db
                                    Currículos em /app/uploads/curriculos/
```

**Domínio da API:** `https://api.alvesmotionlab.com.br`

### Comandos úteis no EasyPanel (terminal do container)

```bash
# Ver tabelas e contagens
/opt/venv/bin/python3 -c "
import sqlite3; conn = sqlite3.connect('/app/agencia_empregos.db')
for t in ['usuarios','empresas','vagas','candidatos','candidaturas','beneficios','requisitos']:
    print(t, conn.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0])
"

# Resetar banco (força novo seed no próximo start)
rm /app/agencia_empregos.db
# → reinicie o container no EasyPanel
```

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

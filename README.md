# Agência de Empregos

> Sistema web completo para gestão de vagas de emprego

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://projeto-integrador-senac.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3.x-003B57?logo=sqlite&logoColor=white)
![EasyPanel](https://img.shields.io/badge/EasyPanel-Hostinger-6C47FF?logo=docker&logoColor=white)

---

## Acesso

**[https://projeto-integrador-senac.streamlit.app](https://projeto-integrador-senac.streamlit.app)**

Sem instalação, basta abrir no navegador.

**API (docs interativos):** [https://api.alvesmotionlab.com.br/docs](https://api.alvesmotionlab.com.br/docs)

---

## Sobre o Projeto

A **Agência de Empregos** é uma plataforma web que conecta empresas recrutadoras e candidatos. O sistema permite publicar e gerenciar vagas com benefícios e requisitos, atribuir vagas a recrutadoras, acompanhar candidaturas com atualização de status, fazer upload de currículos e contar com um **assistente por palavras-chave** para consultas em linguagem natural.

Desenvolvido como **Projeto Integrador da UC6** do Curso Técnico em Inteligência Artificial do SENAC Lapa Tito, integrando backend REST com FastAPI, banco de dados SQLite, interface web com Streamlit e implantado em infraestrutura real na Hostinger via EasyPanel.

---

## Funcionalidades

| Perfil | Funcionalidades |
|---|---|
| **Admin** | Gerencia usuários, empresas, candidatos e vagas. Atribui e reatribui vagas a recrutadoras. Acessa dashboard completo com filtros e assistente. Baixa currículos de candidatos. |
| **Recrutador** | Cadastra e edita vagas (com benefícios e requisitos), acompanha candidaturas, vê candidatos inscritos por vaga, baixa currículos, acessa dashboard com visão das suas vagas. |
| **Candidato** | Visualiza vagas com filtros, se candidata, acompanha status das candidaturas, edita dados de contato e envia currículo (PDF ou DOCX). |

### Destaques

- Autenticação com JWT (login seguro por token)
- **Recrutadora responsável por vaga** — atribuição e reatribuição via botão no detalhe da vaga
- **Benefícios e requisitos por vaga** — cadastro inline no formulário (obrigatórios e desejáveis)
- **Upload de currículo** (PDF ou DOCX) por candidato — download disponível para recrutadoras e admins
- **Dashboard completo** com filtros (recrutador, status, modalidade, empresa), KPIs de vagas e candidaturas, barras por modalidade/contrato/empresa/setor, métricas de clientes e tabela de vagas em atraso
- Tabela de vagas abertas há mais tempo com destaque visual para +30 dias
- **Tela de Empresas** com métricas de clientes: ativos, empresa com mais vagas, clientes sem recrutador, tabela de gestão
- Filtro de vagas PcD
- **Assistente por palavras-chave** com 9 botões de atalho rápido e cards clicáveis de vagas
- Recrutadoras visualizam candidatos inscritos com dados de contato e atualizam status de candidatura
- **Auto-seed completo** na inicialização: 9 recrutadoras, 15 empresas, 15 vagas, 12 benefícios, 20 candidatos fictícios com candidaturas
- **Usuários fixos garantidos** a cada redeploy (seed idempotente por email)
- Auto-cadastro de candidatos com criação automática de perfil ao registrar
- Proteções de integridade (admin não pode se excluir; último admin protegido)
- **Exclusão em cascata de empresas** — remove vagas, candidaturas e relacionamentos automaticamente
- Credenciais exclusivamente por variáveis de ambiente, CORS restrito, endpoints autenticados
- Migrações automáticas de schema na inicialização (sem perda de dados)

---

## Arquitetura

```
┌─────────────────────────────────────┐
│        Usuário (Navegador)          │
└──────────────┬──────────────────────┘
               │ HTTPS
┌──────────────▼──────────────────────┐
│         Streamlit Cloud             │
│  projeto-integrador-senac.app       │
│  streamlit_app.py                   │
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

## Tecnologias

| Camada | Tecnologia | Função |
|---|---|---|
| **Backend** | FastAPI + Uvicorn | API REST |
| **Banco de dados** | SQLite + SQLAlchemy | Persistência ORM |
| **Autenticação** | JWT (python-jose) + bcrypt | Login seguro |
| **Frontend** | Streamlit | Interface web |
| **Assistente** | Lógica Python (palavras-chave) | Consultas em linguagem natural sem IA externa |
| **Servidor** | Hostinger VPS + EasyPanel | Hospedagem do backend em Docker |
| **HTTPS** | Cloudflare DNS + Proxy | Exposição segura da API |
| **Deploy frontend** | Streamlit Cloud | Hospedagem do frontend |
| **Versionamento** | Git + GitHub | Controle de código |

---

## Estrutura do Projeto

```
projeto-integrador/
├── streamlit_app.py              # Interface web (frontend)
├── requirements.txt              # Dependências do frontend
├── DOCUMENTACAO.md               # Documentação completa do projeto
├── .streamlit/
│   └── secrets.toml              # API_URL (não versionado)
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
    │       ├── empresas.py       # CRUD empresas (com cascade delete)
    │       ├── candidatos.py     # CRUD candidatos + upload/download de currículo
    │       └── candidaturas.py   # CRUD candidaturas + atualização de status
    ├── Dockerfile
    └── requirements.txt          # Dependências do backend
```

---

## Como Rodar Localmente

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

Na primeira execução o banco é criado e populado automaticamente.

API disponível em `http://localhost:8000` · Docs: `http://localhost:8000/docs`

### Frontend

```bash
cd projeto-integrador
pip install -r requirements.txt

mkdir -p .streamlit
cat > .streamlit/secrets.toml <<EOF
API_URL = "http://localhost:8000"
EOF

streamlit run streamlit_app.py
```

---

## Variáveis de Ambiente

### Backend (EasyPanel / container)

| Variável | Obrigatória | Descrição |
|---|---|---|
| `SECRET_KEY` | Sim | Chave JWT — string aleatória longa |
| `ADMIN_EMAIL` | Sim | E-mail do admin criado na primeira inicialização |
| `ADMIN_SENHA` | Sim | Senha do admin (mín. 8 caracteres) |
| `ADMIN_NOME` | Não | Nome do admin (padrão: `Admin`) |
| `EXTRA_ADMIN_EMAIL` | Não | E-mail de um admin extra criado a cada boot (idempotente) |
| `EXTRA_ADMIN_SENHA` | Não | Senha do admin extra |
| `EXTRA_ADMIN_NOME` | Não | Nome do admin extra (padrão: `Admin Extra`) |
| `CORS_ORIGINS` | Não | Origens permitidas separadas por vírgula |

> **Contas de demonstração (recrutadoras):** na primeira inicialização, 9 contas de recrutadora são criadas com senhas geradas aleatoriamente e impressas **uma única vez** no log do container. Para consultá-las: `docker logs <container> | grep "@agencia.com"`. Essas contas são apenas para demonstração — troque as senhas em produção real.

### Frontend (Streamlit Cloud secrets)

| Variável | Descrição |
|---|---|
| `API_URL` | URL base do backend (ex: `https://api.alvesmotionlab.com.br`) |

---

## Banco de Dados

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
4. `_seed_dados()` — popula dados iniciais se `empresas` estiver vazio

---

## Endpoints da API

| Método | Rota | Descrição | Auth |
|---|---|---|---|
| POST | `/auth/registro` | Auto-cadastro (cria conta + perfil candidato) | Não |
| POST | `/auth/login` | Login — retorna JWT (form: `username` + `password`) | Não |
| GET | `/auth/me` | Dados do usuário logado | Sim |
| GET/POST | `/auth/usuarios` | Listar / criar usuários | Admin |
| DELETE | `/auth/usuarios/{id}` | Excluir usuário | Admin |
| GET | `/auth/recrutadores` | Listar admins e recrutadores | Sim |
| GET/POST | `/vagas/` | Listar (com filtros) / criar vagas | Sim |
| GET/PUT/DELETE | `/vagas/{id}` | Detalhe / editar / excluir vaga | Sim |
| PATCH | `/vagas/{id}/recrutador` | Atribuir / reatribuir recrutador | Recrutador+ |
| GET/POST | `/empresas/` | Listar / criar empresas | Sim |
| GET/PUT/DELETE | `/empresas/{id}` | Detalhe / editar / excluir empresa (cascade) | Sim |
| GET/POST | `/candidatos/` | Listar / criar candidatos | Sim |
| GET/PUT/DELETE | `/candidatos/{id}` | Detalhe / editar / excluir candidato | Sim |
| POST | `/candidatos/{id}/curriculo` | Upload de currículo (PDF/DOCX) | Sim |
| GET | `/candidatos/{id}/curriculo` | Download do currículo | Sim |
| GET/POST | `/candidaturas/` | Listar (com filtros) / criar candidaturas | Sim |
| PUT | `/candidaturas/{id}/status` | Atualizar status | Recrutador+ |

**Filtros disponíveis em `GET /vagas/`:** `modalidade`, `tipo_contrato`, `vaga_pcd`, `status`, `recrutador_id`

---

## Assistente por Palavras-Chave

O assistente integrado ao chat responde perguntas em linguagem natural sem depender de IA externa. Ele identifica a intenção pelo texto digitado e consulta a API em tempo real.

### Botões de atalho

| Botão | O que faz |
|---|---|
| Vagas abertas | Lista todas as vagas com status aberta |
| Vagas remotas | Filtra vagas com modalidade remoto |
| Vagas híbridas | Filtra vagas com modalidade híbrido |
| Vagas PcD | Filtra vagas inclusivas para pessoas com deficiência |
| Vagas CLT | Filtra vagas com contrato CLT |
| Vagas de estágio | Filtra vagas de estágio |
| Candidaturas | Mostra resumo das candidaturas por status |
| Empresas | Lista as empresas cadastradas |
| Resumo geral | Exibe estatísticas completas do sistema |

### Palavras-chave reconhecidas (exemplos)

| Intenção | Exemplos de frase |
|---|---|
| Vagas abertas | "tem vaga", "ver vagas", "oportunidades" |
| Remoto | "home office", "trabalhar de casa", "a distância" |
| PcD | "deficiência", "inclusão", "portador" |
| Candidaturas aprovadas | "aprovei", "fui aprovado", "quais aprovadas" |
| Empresas | "quais empresas", "lista de clientes" |

Os resultados de vagas aparecem como **cards clicáveis** com botão "Ver vaga" que abre o detalhe direto na tela de vagas.

---

## Infraestrutura de Produção

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
# Ver contagens de cada tabela
/opt/venv/bin/python3 -c "
import sqlite3; conn = sqlite3.connect('/app/agencia_empregos.db')
for t in ['usuarios','empresas','vagas','candidatos','candidaturas','beneficios','requisitos']:
    print(t, conn.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0])
"

# Resetar banco (força novo seed no próximo start)
rm /app/agencia_empregos.db
# reinicie o container no EasyPanel
```

---

## Equipe

| João Vitor dos Santos Alves | Paulo Henrique Moreira Araujo | João Paulo Pereira da Silva |
|:---:|:---:|:---:|
| [![LinkedIn](https://img.shields.io/badge/LinkedIn-000000?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyByb2xlPSJpbWciIHZpZXdCb3g9IjAgMCAyNCAyNCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTIwLjQ0NyAyMC40NTJoLTMuNTU0di01LjU2OWMwLTEuMzI4LS4wMjctMy4wMzctMS44NTItMy4wMzctMS44NTMgMC0yLjEzNiAxLjQ0NS0yLjEzNiAyLjkzOXY1LjY2N0g5LjM1MVY5aDMuNDE0djEuNTYxaC4wNDZjLjQ3Ny0uOSAxLjYzNy0xLjg1IDMuMzctMS44NSAzLjYwMSAwIDQuMjY3IDIuMzcgNC4yNjcgNS40NTV2Ni4yODZ6TTUuMzM3IDcuNDMzYTIuMDYyIDIuMDYyIDAgMCAxLTIuMDYzLTIuMDY1IDIuMDY0IDIuMDY0IDAgMSAxIDIuMDYzIDIuMDY1em0xLjc4MiAxMy4wMTlIMy41NTVWOWgzLjU2NHYxMS40NTJ6TTIyLjIyNSAwSDEuNzcxQy43OTIgMCAwIC43NzQgMCAxLjcyOXYyMC41NDJDMCAyMy4yMjcuNzkyIDI0IDEuNzcxIDI0aDIwLjQ1MUMyMy4yIDI0IDI0IDIzLjIyNyAyNCAyMi4yNzFWMS43MjlDMjQgLjc3NCAyMy4yIDAgMjIuMjIyIDBoLjAwM3oiLz48L3N2Zz4=)](https://linkedin.com/in/jvs-alves) [![GitHub](https://img.shields.io/badge/Github-000000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/JoaoVitor1110) | [![LinkedIn](https://img.shields.io/badge/LinkedIn-000000?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyByb2xlPSJpbWciIHZpZXdCb3g9IjAgMCAyNCAyNCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTIwLjQ0NyAyMC40NTJoLTMuNTU0di01LjU2OWMwLTEuMzI4LS4wMjctMy4wMzctMS44NTItMy4wMzctMS44NTMgMC0yLjEzNiAxLjQ0NS0yLjEzNiAyLjkzOXY1LjY2N0g5LjM1MVY5aDMuNDE0djEuNTYxaC4wNDZjLjQ3Ny0uOSAxLjYzNy0xLjg1IDMuMzctMS44NSAzLjYwMSAwIDQuMjY3IDIuMzcgNC4yNjcgNS40NTV2Ni4yODZ6TTUuMzM3IDcuNDMzYTIuMDYyIDIuMDYyIDAgMCAxLTIuMDYzLTIuMDY1IDIuMDY0IDIuMDY0IDAgMSAxIDIuMDYzIDIuMDY1em0xLjc4MiAxMy4wMTlIMy41NTVWOWgzLjU2NHYxMS40NTJ6TTIyLjIyNSAwSDEuNzcxQy43OTIgMCAwIC43NzQgMCAxLjcyOXYyMC41NDJDMCAyMy4yMjcuNzkyIDI0IDEuNzcxIDI0aDIwLjQ1MUMyMy4yIDI0IDI0IDIzLjIyNyAyNCAyMi4yNzFWMS43MjlDMjQgLjc3NCAyMy4yIDAgMjIuMjIyIDBoLjAwM3oiLz48L3N2Zz4=)](https://linkedin.com/in/devoluap) [![GitHub](https://img.shields.io/badge/Github-000000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/devoluap) | [![LinkedIn](https://img.shields.io/badge/LinkedIn-000000?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyByb2xlPSJpbWciIHZpZXdCb3g9IjAgMCAyNCAyNCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTIwLjQ0NyAyMC40NTJoLTMuNTU0di01LjU2OWMwLTEuMzI4LS4wMjctMy4wMzctMS44NTItMy4wMzctMS44NTMgMC0yLjEzNiAxLjQ0NS0yLjEzNiAyLjkzOXY1LjY2N0g5LjM1MVY5aDMuNDE0djEuNTYxaC4wNDZjLjQ3Ny0uOSAxLjYzNy0xLjg1IDMuMzctMS44NSAzLjYwMSAwIDQuMjY3IDIuMzcgNC4yNjcgNS40NTV2Ni4yODZ6TTUuMzM3IDcuNDMzYTIuMDYyIDIuMDYyIDAgMCAxLTIuMDYzLTIuMDY1IDIuMDY0IDIuMDY0IDAgMSAxIDIuMDYzIDIuMDY1em0xLjc4MiAxMy4wMTlIMy41NTVWOWgzLjU2NHYxMS40NTJ6TTIyLjIyNSAwSDEuNzcxQy43OTIgMCAwIC43NzQgMCAxLjcyOXYyMC41NDJDMCAyMy4yMjcuNzkyIDI0IDEuNzcxIDI0aDIwLjQ1MUMyMy4yIDI0IDI0IDIzLjIyNyAyNCAyMi4yNzFWMS43MjlDMjQgLjc3NCAyMy4yIDAgMjIuMjIyIDBoLjAwM3oiLz48L3N2Zz4=)](https://linkedin.com/in/joao-paulo-pereira-silva-03bb53100) |

**Orientador:** Prof. Vitor de Souza Batista

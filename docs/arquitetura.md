# 🏗️ Arquitetura do Sistema

## Visão Geral

```
Navegador
    │
    ▼ HTTPS
Streamlit Cloud  ──────────────►  Google Gemini API
(streamlit_app.py)                (IA conversacional)
    │
    ▼ HTTPS (Cloudflare)
Hostinger VPS / EasyPanel
    └── Docker container
            ├── FastAPI + Uvicorn (:8000)
            ├── SQLite (/app/agencia_empregos.db)
            └── Currículos (/app/uploads/curriculos/)
```

---

## Backend (FastAPI)

### Ponto de entrada — `main.py`

Executa na ordem ao iniciar o container:

1. `Base.metadata.create_all()` — cria tabelas ainda não existentes
2. `_migrate()` — aplica colunas novas em tabelas existentes (idempotente via try/except no SQLite)
3. `_seed_admin()` — cria o admin via variáveis de ambiente se `usuarios` estiver vazio
4. `_seed_usuarios_fixos()` — garante usuários fixos por email a cada redeploy (idempotente)
5. `_seed_dados()` — popula dados reais se `empresas` estiver vazio
6. Registra middlewares (CORS com métodos GET/POST/PUT/PATCH/DELETE/OPTIONS)
7. Inclui os routers

### Routers

| Arquivo | Prefixo | Responsabilidade |
|---|---|---|
| `routers/auth.py` | `/auth` | Login, registro, CRUD de usuários, listagem de recrutadores |
| `routers/vagas.py` | `/vagas` | CRUD de vagas, atribuição de recrutador, filtros |
| `routers/empresas.py` | `/empresas` | CRUD de empresas |
| `routers/candidatos.py` | `/candidatos` | CRUD de candidatos, upload/download de currículo |
| `routers/candidaturas.py` | `/candidaturas` | CRUD de candidaturas, atualização de status |

### Autenticação e autorização

- `auth.py` implementa JWT com `python-jose` e hash bcrypt com `passlib`
- `get_usuario_atual` — extrai o usuário do token, injetado via `Depends`
- `exigir_perfil(*perfis)` — dependência de autorização por perfil; retorna 403 se o perfil não for permitido
- `_ESCRITORES` em `vagas.py` — shorthand para exigir `admin` ou `recrutador`

### Modelos ORM — `models.py`

```
Usuario
  ├── id, nome, email, senha_hash, perfil

Empresa
  ├── id, nome, cnpj (opcional), setor, descricao, cidade, estado
  └── vagas (1:N)

Vaga
  ├── id, titulo, local, descricao, salario
  ├── modalidade, horario, tipo_contrato, publico_alvo
  ├── vaga_pcd, status, data_publicacao, data_abertura, data_fechamento
  ├── quantidade_vagas
  ├── empresa_id (FK → Empresa)
  ├── recrutador_id (FK → Usuario, nullable)
  ├── beneficios (N:N via vaga_beneficio)
  ├── requisitos (N:N via vaga_requisito)
  └── candidaturas (1:N)

Beneficio
  ├── id, nome, descricao
  └── vagas (N:N)

Requisito
  ├── id, descricao, nivel (obrigatorio | desejavel)
  └── vagas (N:N)

Candidato
  ├── id, nome, email, telefone, cidade, estado, data_nascimento
  ├── curriculo_path (caminho do arquivo no container, nullable)
  └── candidaturas (1:N)

Candidatura
  ├── id, candidato_id, vaga_id, data_candidatura
  └── status (pendente | em_analise | aprovado | reprovado)
```

### Upload de currículos

- Arquivos salvos em `/app/uploads/curriculos/` no container
- Nome do arquivo: `candidato_{id}_{uuid8}{ext}`
- Tipos aceitos: `application/pdf`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document`, `application/msword`
- Upload substitui o arquivo anterior automaticamente
- Download autenticado via `GET /candidatos/{id}/curriculo`

---

## Frontend (Streamlit)

### Estrutura de telas

```
streamlit_app.py
├── tela_login()              — login e cadastro
├── _navbar()                 — barra de navegação superior
│
├── tela_painel()             — listagem de vagas com filtros e cards
│   └── _form_nova_vaga()     — formulário de criação de vaga (com seleção de recrutador)
│
├── tela_detalhe(id)          — detalhe da vaga
│   ├── candidaturas inscritas com botão de currículo (para recrutador/admin)
│   ├── atribuição de recrutador responsável
│   └── candidatura própria (para visualizador)
│
├── tela_dashboard()          — KPIs (vagas + candidaturas), filtros, gráficos,
│                               métricas de clientes, tabela de vagas em atraso
│
├── tela_empresas()           — métricas de clientes (KPIs + tabela de gestão) + CRUD
├── tela_candidatos()         — listagem de candidatos com botão de download de currículo
├── tela_usuarios()           — CRUD de usuários (admin)
├── tela_candidaturas()       — perfil do candidato, upload de currículo e candidaturas
└── tela_assistente()         — chat com IA Gemini
```

### Fluxo de estado de sessão

```python
st.session_state.token         # JWT retornado pelo login
st.session_state.usuario       # dict com id, nome, email, perfil
st.session_state.pagina        # tela ativa (vagas, dashboard, empresas, ...)
st.session_state.vaga_aberta   # ID da vaga em detalhe
st.session_state.vaga_editar   # ID da vaga sendo editada
```

### Helpers de API

| Função | Método HTTP |
|---|---|
| `api_get(path, params)` | GET |
| `api_post(path, json, form)` | POST |
| `api_put(path, json)` | PUT |
| `api_patch(path, json)` | PATCH |
| `api_delete(path)` | DELETE |
| `api_upload(path, file_bytes, filename, content_type)` | POST multipart/form-data |
| `api_download_bytes(path)` | GET → (bytes, content_type, filename) |

Todas injetam `Authorization: Bearer <token>` automaticamente. Erros 401 fazem logout automático.

---

## Banco de Dados

### Arquivo

Em produção: `/app/agencia_empregos.db` (SQLite).  
Em desenvolvimento local: criado na raiz do `backend/` ao iniciar.

### Auto-seed (`_seed_dados()`)

Executa apenas quando `empresas` está vazia. Insere:

- **9 recrutadoras** (perfil `recrutador`, senha `Senha@123`): Juliana, Manu, Mel, Sara, Silvia, Thais, Ully, Yasmin, Yumi
- **43 empresas** reais do backlog (ACRIMET, ALFA ALIMENTOS, AUTOMETAL, GRUPO LUKSCOLOR, INYLBRA, PLASFIL, RASSINI, SPRAYING, ZEPPINI, etc.)
- **12 benefícios** (pool reutilizável): Vale Refeição, Vale Transporte, Plano de Saúde, Plano Odontológico, EPI Completo, Seguro de Vida, Vale Alimentação, Cesta Básica, Adiantamento Salarial, PPR/PLR, Convênio Farmácia, Uniforme
- **112 vagas** do backlog real, com benefícios e requisitos gerados por palavras-chave no título do cargo
- **20 candidatos** fictícios com dados completos
- **Candidaturas** aleatórias (3–6 por candidato, nas primeiras 40 vagas)

### Usuários fixos (`_seed_usuarios_fixos()`)

Roda a cada inicialização. Cria usuários por email se não existirem. Útil para garantir contas de desenvolvimento ou administradores conhecidos mesmo após redeploy.

### Migrações (`_migrate()`)

Executa DDL via `ALTER TABLE ... ADD COLUMN` envolto em try/except. SQLite ignora o erro se a coluna já existir, tornando a operação idempotente.

---

## Segurança

| Aspecto | Implementação |
|---|---|
| Senhas | bcrypt (passlib) — nunca armazenadas em texto plano |
| Tokens | JWT HS256 com expiração configurável |
| CORS | Lista de origens explícita via `CORS_ORIGINS` ou padrão restrito |
| Credenciais | Exclusivamente via variáveis de ambiente |
| Autorização | Verificação de perfil em cada endpoint sensível |
| Admin único | Proteção contra exclusão do último admin |
| Auto-exclusão | Admin não pode excluir o próprio usuário |
| Currículos | Acesso autenticado; UUID no nome do arquivo evita colisões |

---

## Deploy

### Backend — EasyPanel (Hostinger VPS)

1. Cada push na branch `main` pode acionar redeploy automático via webhook do EasyPanel
2. O container executa `uvicorn app.main:app --host 0.0.0.0 --port 8000`
3. O SQLite persiste em `/app/agencia_empregos.db` dentro do container
4. Currículos persistem em `/app/uploads/curriculos/`
5. Variáveis de ambiente configuradas na interface do EasyPanel

### Frontend — Streamlit Cloud

1. Redeploy automático a cada push na branch `main`
2. Secrets configurados em `share.streamlit.io` → Settings → Secrets
3. Não requer build — Streamlit instala `requirements.txt` automaticamente

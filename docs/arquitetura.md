# 🏗️ Arquitetura do Sistema

## Visão Geral

O sistema é dividido em dois serviços independentes que se comunicam via HTTP:

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
            └── SQLite (/app/agencia_empregos.db)
```

---

## Backend (FastAPI)

### Ponto de entrada — `main.py`

1. Cria tabelas via `Base.metadata.create_all()`
2. Executa `_seed_admin()` — cria o admin inicial se `usuarios` estiver vazio
3. Executa `_seed_dados()` — popula dados de exemplo se `empresas` estiver vazio
4. Registra middlewares (CORS)
5. Inclui os routers

### Routers

| Arquivo | Prefixo | Responsabilidade |
|---|---|---|
| `routers/auth.py` | `/auth` | Login, registro, CRUD de usuários, listagem de recrutadores |
| `routers/vagas.py` | `/vagas` | CRUD de vagas, atribuição de recrutador, filtros |
| `routers/empresas.py` | `/empresas` | CRUD de empresas |
| `routers/candidatos.py` | `/candidatos` | CRUD de candidatos |
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
  ├── id, nome, cnpj, setor, descricao, cidade, estado
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
  └── candidaturas (1:N)

Candidatura
  ├── id, candidato_id, vaga_id, data_candidatura
  └── status (pendente | em_analise | aprovado | reprovado)
```

---

## Frontend (Streamlit)

### Estrutura de telas

```
streamlit_app.py
├── tela_login()           — login e cadastro
├── _navbar()              — barra de navegação superior
│
├── tela_painel()          — listagem de vagas com filtros e cards
│   └── _form_nova_vaga()  — formulário de criação de vaga
│
├── tela_detalhe(id)       — detalhe da vaga
│   ├── candidaturas inscritas (para recrutador/admin)
│   ├── atribuição de recrutador
│   └── candidatura própria (para visualizador)
│
├── tela_dashboard()       — KPIs, filtros, gráficos de barras, tabela
│
├── tela_empresas()        — CRUD de empresas (admin)
├── tela_candidatos()      — listagem de candidatos (admin)
├── tela_usuarios()        — CRUD de usuários (admin)
├── tela_candidaturas()    — perfil e candidaturas do candidato
└── tela_assistente()      — chat com IA Gemini
```

### Fluxo de estado de sessão

```python
st.session_state.token    # JWT retornado pelo login
st.session_state.usuario  # dict com id, nome, email, perfil
st.session_state.pagina   # tela ativa (vagas, dashboard, empresas, ...)
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

Todas injetam o header `Authorization: Bearer <token>` automaticamente. Erros 401 fazem logout automático.

---

## Banco de Dados

### Arquivo

Em produção: `/app/agencia_empregos.db` (SQLite).  
Em desenvolvimento local: criado na raiz do `backend/` ao iniciar.

### Auto-seed

A função `_seed_dados()` em `main.py` roda na inicialização e verifica se `empresas` está vazia. Se sim, insere:

- 10 empresas (Google, Nubank, Magazine Luiza, Ambev, Hospital Albert Einstein, Itaú, iFood, Embraer, Natura, XP Inc.)
- 23 vagas com benefícios e requisitos via `vaga_beneficio` e `vaga_requisito`
- 20 candidatos fictícios
- Candidaturas aleatórias para as primeiras 15 vagas

Idempotente — redeployes não reexecutam o seed.

---

## Segurança

| Aspecto | Implementação |
|---|---|
| Senhas | bcrypt (passlib) — nunca armazenadas em texto plano |
| Tokens | JWT HS256 com expiração configurável |
| CORS | Lista de origens explícita via `CORS_ORIGINS` ou padrão restrito |
| Credenciais | Exclusivamente via variáveis de ambiente (nunca no código) |
| Autorização | Verificação de perfil em cada endpoint sensível |
| Admin único | Proteção contra exclusão do último admin |
| Auto-exclusão | Admin não pode excluir o próprio usuário |

---

## Deploy

### Backend — EasyPanel (Hostinger VPS)

1. Cada push na branch `main` pode ser configurado para redeploy automático via webhook do EasyPanel
2. O container executa `uvicorn app.main:app --host 0.0.0.0 --port 8000`
3. O SQLite persiste em `/app/agencia_empregos.db` dentro do container
4. Variáveis de ambiente configuradas na interface do EasyPanel

### Frontend — Streamlit Cloud

1. Redeploy automático a cada push na branch `main`
2. Secrets configurados em `share.streamlit.io` → Settings → Secrets
3. Não requer build — Streamlit instala `requirements.txt` automaticamente

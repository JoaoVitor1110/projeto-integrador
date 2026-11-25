# Design — Agência de Empregos v2: migração para Azure + frontend novo

**Data:** 2026-11-25
**Escopo deste documento:** Fase 1 (fundação na Azure + frontend React novo com todas as funções atuais).
Chatbot com LLM/RAG/LangChain e dashboard diretoria × operacional terão designs próprios depois.

---

## 1. Intenção e porquê

- Projeto Integrador (UC6, Técnico em IA — SENAC Lapa Tito). Entrega final em **janeiro/2027**.
- A Azure é a nuvem que o SENAC disponibiliza (assinatura de estudante). O sistema atual roda em
  Hostinger/EasyPanel (backend + SQLite) e Streamlit Cloud (frontend).
- **"Funcionar de verdade":** qualquer pessoa abre um link e usa; dados persistem num banco real;
  nada simulado.
- **Objetivo de aprendizado do dono do projeto:** aprender a **criar e conectar os serviços da Azure**.
  Depois de conectados ao GitHub, o fluxo é só atualizar o código (push → deploy automático).
- **Marco intermediário:** até **2026-12-02** (semana que vem) — frontend novo + funções funcionando,
  já na Azure (opção B escolhida pelo dono).

## 2. Objetivos, não-objetivos, anti-objetivos

**Objetivos (Fase 1)**
1. Banco **PostgreSQL** na Azure substituindo o SQLite (com extensão `pgvector` habilitada, para a fase do chatbot).
2. Backend **FastAPI** na Azure, deploy automático a partir do GitHub.
3. Frontend **React + Vite** novo, com **paridade de funções** com o Streamlit atual, animações e transições no estilo **Cult UI**.
4. Currículos guardados no **Azure Blob Storage** (não mais no disco do container).
5. Assistente por palavras-chave atual **movido do Streamlit para o backend** (`POST /chat`), para que a tela de chat
   não mude quando o motor virar LangChain.
6. **Passo a passo para leigo** de cada serviço da Azure, dentro da documentação existente.
7. Documentação existente **continuada e atualizada** (não recriada).

**Não-objetivos (Fase 1)**
- Chatbot com LLM, RAG, embeddings, LangChain → Fase 3 (design próprio).
- Dashboard novo diretoria × operacional → Fase 4 (design próprio). Na Fase 1 o dashboard atual é **portado como está** (mesmos KPIs/filtros).
- Migrar os dados do SQLite de produção. O banco novo começa vazio e é populado pelo seed existente.
- Ollama em VM na nuvem (fica para a apresentação, se desejado).

**Anti-objetivos (seria fracasso mesmo funcionando)**
- Estourar os US$ 100 de crédito antes de janeiro (serviços param).
- A LLM (em fases futuras) decidir autenticação/autorização. Autorização é sempre código.
- Documentação antiga apagada ou substituída por uma nova desconectada.
- Frontend novo perder alguma função que o Streamlit tem hoje.

## 3. Restrições

- **Assinatura Azure for Students** (a confirmar pelo dono): US$ 100/ano, sem cartão; **apenas 5 regiões permitidas**
  (ver em Policy → Assignments → "Allowed resource deployment regions"). Todos os recursos devem ficar na **mesma região
  permitida**, de preferência a mais próxima do Brasil entre as liberadas.
- Azure OpenAI praticamente indisponível nessa assinatura (quota de 1K TPM) — relevante só para a Fase 3.
- Prazo: 7 dias para o marco intermediário.
- O dono é iniciante em Azure; o passo a passo deve ser via **Portal da Azure** (cliques), não CLI/Terraform.
- **Quem faz o quê:** o dono cria e conecta os recursos no Portal seguindo `docs/azure-passo-a-passo.md` (é o aprendizado
  que ele quer). O Claude não tem acesso à Azure: escreve o código, o guia e os workflows, e diagnostica a partir das URLs,
  mensagens de erro e do **Log stream** do App Service que o dono enviar. Por isso o plano escreve o guia **antes** de cada
  etapa de infraestrutura e prevê pontos de espera pelo dono. *(decisão do Claude)*
- Se o GitHub não puder ser conectado pelo Deployment Center (restrição de tenant institucional), o fallback é deploy por
  **publish profile** / token de deploy salvo como segredo no GitHub. *(decisão do Claude)*

## 4. Abordagens consideradas

| | Abordagem | Trade-off | Decisão |
|---|---|---|---|
| A | Tudo local na semana 1, Azure na semana 2 | Zero risco de prazo, mas sem link na semana que vem | Descartada |
| **B** | **Tudo na Azure já na semana 1** (front, back, Postgres) | Arquitetura final logo; mais coisas novas ao mesmo tempo | **Escolhida pelo dono** — o objetivo dele é justamente aprender a ligar e conectar os serviços |
| C | Front na Azure apontando para o backend atual; backend/DB depois | Menor risco, mas adia o aprendizado principal | Descartada |

**Frontend:** React + Vite (decisão do Claude, delegada pelo dono). Cult UI só existe para React (shadcn/ui + Tailwind + Motion).
Vue descartado (perde Cult UI). Next.js descartado (exige servidor Node; React+Vite gera arquivos estáticos hospedáveis de graça).
O protótipo em `frontend/` (React 19 + Vite + Tailwind) é reaproveitado como ponto de partida.

## 5. Arquitetura

```
                    GitHub (repositório)
           push ──────────┬───────────────────────┐
                          │ GitHub Actions        │ GitHub Actions
                          ▼                       ▼
  Navegador ──HTTPS──► Azure Static Web Apps   Azure App Service (Linux, Python 3.11)
                       (React + Vite, grátis)   FastAPI + Uvicorn/Gunicorn
                              │                       │
                              └──── chamadas REST ───►│
                                    (JWT no header)   ├──► Azure Database for PostgreSQL
                                                      │    Flexible Server (Burstable B1ms)
                                                      │    + extensão pgvector (habilitada, uso na Fase 3)
                                                      │
                                                      └──► Azure Blob Storage
                                                           container "curriculos" (privado)
```

### 5.1 Serviços Azure (todos num único Resource Group, ex.: `rg-agencia-empregos`)

| Serviço | Plano | Custo aprox./mês* | Por quê |
|---|---|---|---|
| Static Web Apps | Free | US$ 0 | Hospeda o React; conecta ao GitHub num assistente |
| App Service (Linux) | B1 | ~US$ 13 | Roda o FastAPI; deploy pelo "Deployment Center" ligado ao GitHub. F1 (grátis) é fallback se o crédito apertar, com limite de 60 min de CPU/dia |
| PostgreSQL Flexible Server | Burstable B1ms, 32 GB | ~US$ 13–17 (pode estar coberto pelos serviços gratuitos da assinatura — conferir) | Banco relacional + pgvector num só lugar |
| Storage Account (Blob) | Standard LRS | < US$ 1 | Currículos (PDF/DOCX) |

\* Valores aproximados; conferir na calculadora de preços para a região permitida. Total estimado ~US$ 30/mês →
o crédito cobre dez/2026–jan/2027 com folga. **Orçamento com alerta** em US$ 50 e US$ 80 (Cost Management → Budgets).
O Postgres pode ser **parado** quando não estiver em uso (até 7 dias seguidos).

### 5.2 Configuração / segredos

Variáveis de ambiente no App Service (Configuration → Application settings), nunca no código:
`DATABASE_URL`, `SECRET_KEY`, `CORS_ORIGINS` (URL do Static Web Apps), `ADMIN_EMAIL`, `ADMIN_SENHA`, `ADMIN_NOME`,
`AZURE_STORAGE_CONNECTION_STRING`, `AZURE_STORAGE_CONTAINER=curriculos`.
No Static Web Apps: `VITE_API_URL` (URL do App Service) definida no workflow do GitHub Actions.
Key Vault fica fora (complexidade extra sem ganho para a entrega).

## 6. Backend — o que muda

**Manter:** FastAPI, SQLAlchemy, modelos, schemas, JWT + perfis (`exigir_perfil`), routers e endpoints atuais
(contratos da API preservados — mesma documentação em `docs/api.md`).

**Reformular:**
1. **Banco:** `DATABASE_URL` aponta para o Postgres (`postgresql+psycopg2://...?sslmode=require`). SQLite continua
   funcionando para testes e desenvolvimento local.
2. **Migrações:** remover o `_migrate()` com `ALTER TABLE` em try/except do `main.py`; usar **Alembic** de verdade
   (`alembic upgrade head` no startup do App Service). Nova migração habilita `CREATE EXTENSION IF NOT EXISTS vector`
   apenas quando o banco for Postgres.
3. **Camada de serviços:** extrair a lógica de negócio dos routers para `app/services/` (ex.: `vagas_service.listar(usuario, filtros)`),
   **recebendo o usuário atual e aplicando as regras de perfil ali**. Routers ficam finos. Motivo: na Fase 3 as
   ferramentas do LangChain chamarão essas mesmas funções, herdando as regras de permissão.
4. **Currículos → Blob Storage:** `app/storage.py` com interface `salvar / baixar / remover`; implementação Blob em produção
   e disco local em dev/teste (escolhida por `AZURE_STORAGE_CONNECTION_STRING` presente ou não). `curriculo_path` passa a guardar o nome do blob.
   Download continua via endpoint autenticado do backend (o blob é privado).
5. **Chat:** novo router `POST /chat` (`{"mensagem": str}` → `{"resposta": str, "vagas": [...]}`), com a lógica de
   palavras-chave hoje em `streamlit_app.py::_responder_chatbot` portada para `app/services/chat_service.py`,
   usando os serviços (não chamadas HTTP a si mesmo).
6. **Dashboard:** novo `GET /dashboard/resumo` com os agregados que hoje o Streamlit calcula no cliente (KPIs, contagens
   por modalidade/contrato/empresa/setor, vagas em atraso), respeitando o filtro de recrutador por perfil.
7. **Seeds:** `_seed_admin`, `_seed_usuarios_fixos`, `_seed_dados` mantidos (idempotentes), rodando no startup.
8. **Produção:** comando de inicialização do App Service com Gunicorn + workers Uvicorn.

## 7. Frontend — React novo

**Stack:** React 19 + Vite + **Tailwind CSS v4** + **shadcn/ui** + **Cult UI** + **Motion** (animações),
**React Router** (rotas), **TanStack Query** (chamadas à API e cache), **Recharts** (gráficos do dashboard),
**lucide-react** (ícones), **sonner** (toasts).

**Paridade com o Streamlit (telas e quem vê):**

| Rota | Tela | Perfis |
|---|---|---|
| `/login` | Login e criar conta (abas) | público |
| `/vagas` | Painel de vagas: cards, filtros (modalidade, contrato, status, PcD) | todos |
| `/vagas/nova`, `/vagas/:id/editar` | Formulário de vaga com benefícios e requisitos inline e seleção de recrutador | admin, recrutador |
| `/vagas/:id` | Detalhe: candidaturas inscritas + download de currículo + atualizar status; atribuir recrutador; candidatar-se | todos (ações por perfil) |
| `/dashboard` | Dashboard atual portado (KPIs, filtros, barras, métricas de clientes, vagas em atraso) | admin, recrutador |
| `/empresas`, `/empresas/:id/editar` | Métricas de clientes + CRUD | admin |
| `/candidatos`, `/candidatos/:id/editar` | Lista + download de currículo + editar | admin |
| `/usuarios` | CRUD de usuários | admin |
| `/minhas-candidaturas` | Perfil do candidato, upload de currículo, minhas candidaturas | visualizador (candidato) |
| `/assistente` | Chat com botões de atalho e cards de vaga clicáveis, consumindo `POST /chat` | todos |

**Comportamentos:** token JWT em `localStorage`; 401 → logout e volta ao login (igual ao Streamlit);
rotas protegidas por perfil no cliente (a proteção real continua no backend).
**Animações (estilo Cult UI):** transição entre páginas, entrada em cascata dos cards, hover/expand nos cards,
modais e drawers animados, números dos KPIs contando, skeletons de carregamento, tema claro/escuro.
**Visual:** mockups das telas principais (login, painel de vagas, detalhe, dashboard, assistente) desenhados como
artefato visual para aprovação do dono **no dia 1**. A aprovação **não bloqueia**: enquanto isso, o builder faz camada de API,
rotas, autenticação e componentes base; o visual aprovado é aplicado por cima. *(decisão do Claude)*

## 8. Branches e versão antiga

- `main` permanece com o sistema atual (Streamlit + Hostinger), que segue no ar até a v2 estar pronta.
- Tag `v1-legado` no commit atual do `main` (criada com autorização do dono).
- Trabalho da v2 na branch `claude/epic-archimedes-v8dpej`, com PR em rascunho para o `main`.
- **Static Web Apps e App Service fazem deploy a partir da branch da v2**, não do `main` — assim os workflows que a Azure
  commita não tocam o `main` nem o deploy da Hostinger. Quando a v2 for para o `main`, o deploy passa para o `main`. *(decisão do Claude)*
- `streamlit_app.py` fica no repositório até o fim da Fase 1 (referência de paridade) e depois vai para `legado/`.

## 9. Documentação (continuar a existente)

- **`DOCUMENTACAO.md`** (ABNT): atualizar Resumo, 5.1 Arquitetura, 5.2 Tecnologias, estrutura de diretórios, 5.6 Funcionalidades
  (telas React), 5.7 Assistente (agora via backend), 6. Guia de acesso (novos links). Manter histórico citando a v1.
- **`README.md`:** badges, links, stack, instalação local (backend + frontend), variáveis de ambiente.
- **`docs/arquitetura.md`:** novo diagrama Azure, camada de serviços, storage, CI/CD.
- **`docs/api.md`:** adicionar `POST /chat` e `GET /dashboard/resumo`.
- **Novo `docs/azure-passo-a-passo.md`:** guia para leigo, em ordem: criar conta/conferir assinatura e regiões →
  Resource Group → orçamento com alertas → PostgreSQL (firewall, extensão `VECTOR` permitida) → Storage Account + container →
  App Service + Deployment Center (GitHub) + variáveis → Static Web Apps (GitHub) + `VITE_API_URL` → CORS → testar →
  como parar/religar o Postgres para economizar. Cada passo com "o que é", "por que", "onde clicar" e "como saber que deu certo".
- O `.docx` ABNT é atualizado pelo dono a partir do `DOCUMENTACAO.md` (fora do escopo do código).

## 10. Testes e critério de pronto (marco de 2026-12-02)

- Testes do backend (`backend/tests/`) passam com SQLite; novos testes para `services/`, `/chat`, `/dashboard/resumo` e storage local.
- Build do frontend sem erros; lint passa.
- **Pronto quando:** link do Static Web Apps abre, login funciona com o admin do seed, e cada linha da tabela de paridade
  (seção 7) funciona contra o backend no App Service com Postgres, incluindo upload/download de currículo via Blob.

## 11. Decisões deixadas ao builder

- Organização interna de pastas do frontend e dos componentes Cult UI escolhidos.
- Nomes exatos dos recursos Azure (sugestão: prefixo `agencia-`).
- Detalhes do workflow do GitHub Actions (os gerados pela Azure são aceitáveis).
- Paleta e tipografia, dentro do que for aprovado nos mockups.

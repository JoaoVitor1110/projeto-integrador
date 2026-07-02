# SERVIÇO NACIONAL DE APRENDIZAGEM COMERCIAL
# SENAC LAPA TITO
# CURSO TÉCNICO EM INTELIGÊNCIA ARTIFICIAL

---

&nbsp;

&nbsp;

&nbsp;

# AGÊNCIA DE EMPREGOS

## Sistema Web de Gestão de Vagas de Emprego

### *Projeto Integrador — UC6*

&nbsp;

&nbsp;

&nbsp;

**João Vitor dos Santos Alves**

**Paulo Henrique Moreira Araujo**

**João Paulo Pereira da Silva**

&nbsp;

&nbsp;

Orientador: Prof. Vitor de Souza Batista

&nbsp;

São Paulo – SP

2026

---

&nbsp;

&nbsp;

## RESUMO

O presente trabalho descreve o desenvolvimento de um sistema web completo para gestão de vagas de emprego, denominado **Agência de Empregos**, elaborado como Projeto Integrador da Unidade Curricular 6 (UC6) do Curso Técnico em Inteligência Artificial do SENAC Lapa Tito. A solução integra um backend construído com o framework FastAPI em linguagem Python, banco de dados relacional SQLite gerenciado via SQLAlchemy e interface web interativa desenvolvida com Streamlit. O sistema permite o cadastro e gerenciamento de empresas, vagas de emprego com descrição detalhada, candidatos e candidaturas, com controle de acesso baseado em perfis de usuário (Administrador, Recrutador e Candidato). O backend é conteinerizado com Docker e hospedado em VPS (Hostinger) gerenciada pelo EasyPanel, com domínio próprio `api.alvesmotionlab.com.br` e certificado HTTPS via Cloudflare. O frontend é publicado no Streamlit Cloud com deploy automático a partir do repositório GitHub. O sistema encontra-se em pleno funcionamento no endereço **https://projeto-integrador-senac.streamlit.app**.

**Palavras-chave:** sistema web; gestão de vagas; FastAPI; Streamlit; Docker; EasyPanel; Python.

---

## SUMÁRIO

1. IDENTIFICAÇÃO DO PROJETO
2. TEMA DO PROJETO
3. OBJETIVO
   - 3.1 Objetivo Geral
   - 3.2 Objetivos Específicos
4. JUSTIFICATIVA
5. EXPLICAÇÃO DA SOLUÇÃO
   - 5.1 Visão Geral da Arquitetura
   - 5.2 Tecnologias Utilizadas
   - 5.3 Modelagem do Banco de Dados
   - 5.4 Diagrama Entidade-Relacionamento
   - 5.5 Controle de Acesso e Perfis de Usuário
   - 5.6 Funcionalidades do Sistema
   - 5.7 Endpoints da API REST
6. GUIA DE ACESSO E UTILIZAÇÃO
   - 6.1 Acesso ao Sistema
   - 6.2 Como Criar um Usuário
   - 6.3 Perfis e Permissões
   - 6.4 Como Cadastrar uma Vaga
   - 6.5 Como se Candidatar a uma Vaga
   - 6.6 Como Gerenciar Candidaturas (Recrutador/Admin)
   - 6.7 Como Acessar o Banco de Dados
   - 6.8 Como Acessar o Servidor (EasyPanel)
7. INFRAESTRUTURA E IMPLANTAÇÃO
   - 7.1 Servidor Backend (EasyPanel + Docker)
   - 7.2 Frontend (Streamlit Cloud)
   - 7.3 DNS e HTTPS (Cloudflare)
   - 7.4 Versionamento (GitHub)
8. CRONOGRAMA
9. CONSIDERAÇÕES FINAIS
10. REFERÊNCIAS

---

## 1. IDENTIFICAÇÃO DO PROJETO

| Campo | Informação |
|---|---|
| **Título do projeto** | Agência de Empregos — Sistema Web de Gestão de Vagas de Emprego |
| **Instituição** | SENAC Lapa Tito |
| **Curso** | Técnico em Inteligência Artificial |
| **Unidade curricular** | UC6 — Projeto Integrador |
| **Orientador** | Prof. Vitor de Souza Batista |
| **Integrantes** | João Vitor dos Santos Alves · Paulo Henrique Moreira Araujo · João Paulo Pereira da Silva |
| **Cidade / UF** | São Paulo – SP |
| **Período** | 1.º Semestre de 2026 |
| **URL do sistema** | https://projeto-integrador-senac.streamlit.app |
| **URL da API** | https://api.alvesmotionlab.com.br |
| **Repositório** | https://github.com/joaovitor1110/projeto-integrador |

---

## 2. TEMA DO PROJETO

O presente projeto aborda o desenvolvimento de uma plataforma web completa para gestão de vagas de emprego, destinada a conectar empresas recrutadoras e candidatos a oportunidades de trabalho. O sistema, denominado **Agência de Empregos**, simula o funcionamento de uma agência digital de recrutamento, oferecendo ferramentas para publicação, gerenciamento e candidatura a vagas.

O mercado de trabalho brasileiro enfrenta um desafio crescente de intermediação eficiente entre oferta e demanda de empregos. Plataformas digitais de recrutamento tornaram-se indispensáveis tanto para empresas que buscam talentos quanto para candidatos que buscam oportunidades. Diante desse contexto, o projeto propõe a implementação de um sistema web funcional e completo, capaz de organizar todo o ciclo de uma vaga: desde o cadastro pela empresa até a candidatura, acompanhamento e decisão final pelo recrutador.

O sistema contempla as seguintes áreas:

- cadastro e gerenciamento de empresas;
- publicação e gestão de vagas com descrição detalhada, benefícios e requisitos;
- cadastro e acompanhamento de candidatos;
- registro e acompanhamento de candidaturas com atualização de status;
- visão do recrutador sobre candidatos inscritos por vaga;
- dashboard analítico com indicadores de vagas;
- controle de acesso com três perfis distintos de usuário.

---

## 3. OBJETIVO

### 3.1 Objetivo Geral

Desenvolver um sistema web completo e funcional para gestão de vagas de emprego, integrando um backend RESTful construído com FastAPI em Python, banco de dados relacional SQLite, e interface web interativa com Streamlit, implantado em infraestrutura de nuvem com domínio próprio e acesso público seguro via HTTPS.

### 3.2 Objetivos Específicos

- Modelar e implementar um banco de dados relacional com entidades, atributos e relacionamentos coerentes com o contexto de uma agência de empregos;
- Desenvolver uma API REST completa com FastAPI, incluindo autenticação JWT, controle de perfis e operações CRUD para todas as entidades do sistema;
- Implementar controle de acesso baseado em perfis (Admin, Recrutador e Candidato), com restrições de permissão por funcionalidade;
- Construir uma interface web responsiva com navbar horizontal, fonte Poppins e cards informativos, utilizando Streamlit;
- Conteinerizar o backend com Docker e implantá-lo em VPS (Hostinger) gerenciada pelo EasyPanel com domínio `api.alvesmotionlab.com.br`;
- Configurar DNS e HTTPS via Cloudflare para o domínio da API;
- Hospedar o frontend no Streamlit Cloud com deploy automático a partir do GitHub;
- Permitir que recrutadores visualizem os candidatos inscritos em cada vaga com dados de contato e atualizem o status de cada candidatura;
- Versionar o código-fonte no GitHub com histórico de commits documentado;
- Elaborar documentação técnica completa em conformidade com as normas da ABNT.

---

## 4. JUSTIFICATIVA

A digitalização dos processos seletivos é uma realidade consolidada no mercado de trabalho contemporâneo. Empresas de todos os portes utilizam plataformas digitais para publicar vagas, receber candidaturas e gerenciar processos seletivos. A construção de um sistema com essa finalidade permite ao estudante de tecnologia vivenciar, na prática, o desenvolvimento completo de uma aplicação real — desde a modelagem do banco de dados até a implantação em produção.

Do ponto de vista acadêmico, o projeto justifica-se por integrar, de forma coesa e aplicada, as principais tecnologias estudadas ao longo do Curso Técnico em Inteligência Artificial: desenvolvimento de APIs REST com Python, modelagem e persistência de dados relacionais, autenticação e segurança, conteinerização com Docker, desenvolvimento de interfaces web e implantação em infraestrutura de nuvem.

A escolha do FastAPI como framework principal agrega relevância técnica ao trabalho, por se tratar de um dos frameworks Python mais modernos e de alta performance do mercado, amplamente utilizado na indústria para construção de APIs REST. O uso do Streamlit como camada de interface permite desenvolver aplicações web interativas com Python puro, sem a necessidade de conhecimento em JavaScript ou frameworks de frontend tradicionais.

A implantação em infraestrutura real de nuvem com domínio próprio (EasyPanel + Hostinger VPS + Cloudflare) e a exposição pública do sistema via Streamlit Cloud distinguem este projeto de soluções que funcionam apenas em ambiente local, demonstrando domínio sobre o ciclo completo de desenvolvimento de software: concepção, implementação, conteinerização e implantação em produção com disponibilidade contínua (24/7).

---

## 5. EXPLICAÇÃO DA SOLUÇÃO

### 5.1 Visão Geral da Arquitetura

A solução é composta por três camadas principais integradas entre si:

```
┌──────────────────────────────────────────────────────────────┐
│                    USUÁRIO (Navegador)                        │
└──────────────────────────────┬───────────────────────────────┘
                               │ HTTPS
┌──────────────────────────────▼───────────────────────────────┐
│              STREAMLIT CLOUD (Frontend)                       │
│          projeto-integrador-senac.streamlit.app              │
│          streamlit_app.py  (Python + Streamlit)              │
│          Deploy automático via GitHub (branch main)          │
└──────────────────────────────┬───────────────────────────────┘
                               │ HTTPS
                    api.alvesmotionlab.com.br
                    (DNS Cloudflare → IP da VPS)
┌──────────────────────────────▼───────────────────────────────┐
│           HOSTINGER VPS — EasyPanel (Backend)                │
│           IP: 72.60.51.179                                   │
│   ┌──────────────────────────────────────────────────────┐   │
│   │  Docker Container                                    │   │
│   │  FastAPI + Uvicorn  →  porta 8000                   │   │
│   │  Alembic (migrações automáticas no startup)         │   │
│   └──────────────────────────┬───────────────────────────┘   │
│                              │ Volume persistente            │
│   ┌──────────────────────────▼───────────────────────────┐   │
│   │  /data/agencia_empregos.db  (SQLite)                │   │
│   └──────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

- **Camada de apresentação:** interface web construída com Streamlit, hospedada no Streamlit Cloud. Navbar horizontal azul com navegação por perfil, cards de vagas, dashboard analítico, painel de candidato e área administrativa;
- **Camada de aplicação:** API REST construída com FastAPI, conteinerizada com Docker e executada via servidor Uvicorn em VPS Hostinger gerenciada pelo EasyPanel. Responsável pela lógica de negócio, autenticação JWT e persistência;
- **Camada de dados:** banco de dados relacional SQLite, gerenciado pelo ORM SQLAlchemy com migrações controladas pelo Alembic. O arquivo do banco persiste em volume Docker (`/data`) independente do ciclo de vida do container.

---

### 5.2 Tecnologias Utilizadas

| Tecnologia | Versão | Função |
|---|---|---|
| **Python** | 3.11 | Linguagem principal do backend e frontend |
| **FastAPI** | ≥ 0.115 | Framework para construção da API REST |
| **Uvicorn** | 0.30 | Servidor ASGI para execução do FastAPI |
| **SQLAlchemy** | 2.0 | ORM para mapeamento objeto-relacional |
| **SQLite** | 3.x | Banco de dados relacional embutido |
| **Alembic** | 1.13 | Controle de migrações do banco de dados |
| **Pydantic** | 2.9 | Validação de dados e schemas da API |
| **python-jose** | 3.3 | Geração e validação de tokens JWT |
| **passlib[bcrypt]** | 1.7.4 | Hash seguro de senhas |
| **bcrypt** | 3.2.2 | Algoritmo de hash (versão compatível com passlib 1.7.4) |
| **Docker** | — | Conteinerização do backend |
| **EasyPanel** | — | Painel de gerenciamento de containers na VPS |
| **Hostinger VPS** | — | Servidor virtual com IP fixo (72.60.51.179) |
| **Cloudflare** | — | DNS e HTTPS para o domínio da API |
| **Streamlit** | ≥ 1.35 | Framework para interface web interativa |
| **Requests** | 2.31 | Cliente HTTP para consumo da API no frontend |
| **Google Fonts** | — | Tipografia Poppins na interface |
| **GitHub** | — | Versionamento e repositório do código-fonte |
| **Streamlit Cloud** | — | Hospedagem do frontend com deploy automático |

#### Estrutura de Diretórios do Projeto

```
projeto-integrador/
├── streamlit_app.py              # Interface web (frontend)
├── requirements.txt              # Dependências do frontend
├── .streamlit/
│   └── secrets.toml              # Configurações (API_URL)
├── DOCUMENTACAO.md               # Documentação técnica (este arquivo)
└── backend/
    ├── Dockerfile                # Imagem Docker do backend
    ├── requirements.txt          # Dependências do backend
    ├── seed_dados.py             # Script de carga de dados de teste
    ├── app/
    │   ├── main.py               # Ponto de entrada da API + seed automático
    │   ├── database.py           # Configuração do banco de dados
    │   ├── models.py             # Modelos ORM (entidades)
    │   ├── schemas.py            # Schemas Pydantic (validação)
    │   ├── auth.py               # Autenticação JWT e bcrypt
    │   └── routers/
    │       ├── auth.py           # Rotas de autenticação e usuários
    │       ├── vagas.py          # Rotas de vagas
    │       ├── empresas.py       # Rotas de empresas
    │       ├── candidatos.py     # Rotas de candidatos
    │       └── candidaturas.py   # Rotas de candidaturas
    └── alembic/
        ├── env.py                # Configuração do Alembic
        ├── alembic.ini           # Configuração principal
        └── versions/             # Arquivos de migração
            ├── 5f222dc0b381_initial_schema.py
            ├── 063891927353_add_usuarios_table.py
            ├── a1b2c3d4e5f6_add_vaga_fields.py
            └── b2c3d4e5f6a7_add_descricao_to_vaga.py
```

---

### 5.3 Modelagem do Banco de Dados

O banco de dados relacional é composto pelas seguintes entidades:

| Entidade | Principais atributos |
|---|---|
| **usuarios** | id, nome, email, senha_hash, perfil (admin/recrutador/visualizador) |
| **empresas** | id, nome, cnpj, setor, descricao, cidade, estado |
| **vagas** | id, titulo, local, descricao, salario, modalidade, horario, tipo_contrato, publico_alvo, vaga_pcd, status, data_publicacao, data_abertura, data_fechamento, quantidade_vagas, empresa_id |
| **candidatos** | id, nome, email, telefone, cidade, estado, data_nascimento |
| **candidaturas** | id, candidato_id, vaga_id, data_candidatura, status |
| **beneficios** | id, nome, descricao |
| **requisitos** | id, descricao, nivel (obrigatorio/desejavel) |
| **vaga_beneficio** | vaga_id, beneficio_id *(tabela associativa N:N)* |
| **vaga_requisito** | vaga_id, requisito_id *(tabela associativa N:N)* |

#### Enumerações (ENUMs)

| Enum | Valores |
|---|---|
| **PerfilEnum** | admin, recrutador, visualizador |
| **ModalidadeEnum** | presencial, remoto, hibrido |
| **TipoContratoEnum** | CLT, PJ, temporario, estagio |
| **PublicoAlvoEnum** | masculino, feminino, ambos |
| **StatusVagaEnum** | aberta, encerrada |
| **NivelRequisitoEnum** | obrigatorio, desejavel |
| **StatusCandidaturaEnum** | pendente, em_analise, aprovado, reprovado |

---

### 5.4 Diagrama Entidade-Relacionamento

```
USUARIOS
├── id (PK)
├── nome
├── email (UNIQUE)
├── senha_hash
└── perfil [admin | recrutador | visualizador]

EMPRESAS                          VAGAS
├── id (PK)                       ├── id (PK)
├── nome                          ├── titulo
├── cnpj (UNIQUE)                 ├── local
├── setor                         ├── descricao
├── descricao                     ├── salario
├── cidade                        ├── modalidade
└── estado                        ├── horario
         │                        ├── tipo_contrato
         │  1:N                   ├── publico_alvo
         └──────────────────────► ├── vaga_pcd
                                  ├── status
                                  ├── data_publicacao
                                  ├── data_abertura
                                  ├── data_fechamento
                                  ├── quantidade_vagas
                                  └── empresa_id (FK → EMPRESAS)
                                           │
                          ┌────────────────┼────────────────┐
                          │ N:N            │ N:N            │ 1:N
                          ▼                ▼                ▼
                     BENEFICIOS       REQUISITOS       CANDIDATURAS
                     ├── id (PK)      ├── id (PK)      ├── id (PK)
                     ├── nome         ├── descricao     ├── candidato_id (FK)
                     └── descricao    └── nivel         ├── vaga_id (FK)
                                                        ├── data_candidatura
                                                        └── status

                                                   CANDIDATOS
                                                   ├── id (PK)
                                                   ├── nome
                                                   ├── email (UNIQUE)
                                                   ├── telefone
                                                   ├── cidade
                                                   ├── estado
                                                   └── data_nascimento
```

**Relacionamentos:**

- `EMPRESAS` → `VAGAS`: uma empresa possui muitas vagas (1:N)
- `VAGAS` ↔ `BENEFICIOS`: N:N via tabela `vaga_beneficio`
- `VAGAS` ↔ `REQUISITOS`: N:N via tabela `vaga_requisito`
- `CANDIDATOS` → `CANDIDATURAS`: um candidato faz muitas candidaturas (1:N)
- `VAGAS` → `CANDIDATURAS`: uma vaga recebe muitas candidaturas (1:N)

---

### 5.5 Controle de Acesso e Perfis de Usuário

O sistema implementa autenticação via **JSON Web Token (JWT)**. Ao realizar login, o usuário recebe um token de acesso. Todas as rotas protegidas exigem o envio desse token no cabeçalho HTTP (`Authorization: Bearer <token>`).

Existem três perfis de usuário com permissões distintas:

| Funcionalidade | Admin | Recrutador | Candidato |
|---|:---:|:---:|:---:|
| Visualizar vagas | ✅ | ✅ | ✅ |
| Cadastrar/editar vagas (com descrição) | ✅ | ✅ | ❌ |
| Encerrar/reabrir vagas | ✅ | ✅ | ❌ |
| Dashboard analítico | ✅ | ✅ | ❌ |
| Ver candidatos inscritos por vaga | ✅ | ✅ | ❌ |
| Atualizar status de candidatura | ✅ | ✅ | ❌ |
| Candidatar-se a vagas | ❌ | ❌ | ✅ |
| Ver minhas candidaturas | ❌ | ❌ | ✅ |
| Editar dados de contato do perfil | ❌ | ❌ | ✅ |
| Gerenciar empresas | ✅ | ❌ | ❌ |
| Gerenciar candidatos | ✅ | ❌ | ❌ |
| Gerenciar usuários | ✅ | ❌ | ❌ |
| Criar usuários com qualquer perfil | ✅ | ❌ | ❌ |
| Excluir usuários* | ✅ | ❌ | ❌ |

> \* O administrador não pode excluir a si próprio.

---

### 5.6 Funcionalidades do Sistema

#### Navbar Horizontal
Barra de navegação azul no topo da página, exibida após login. Apresenta o logotipo, botões de navegação conforme o perfil do usuário, e o nome/badge do usuário logado. O botão da página ativa é destacado visualmente.

#### Painel de Vagas
Exibe todas as vagas cadastradas em formato de cards (3 colunas) com: título, status, empresa, localidade, modalidade, tipo de contrato, indicador PcD e salário. Possui filtros por modalidade, tipo de contrato, status e vagas PcD, exibidos em um expander "🔍 Filtros".

#### Detalhe da Vaga
Apresenta todas as informações de uma vaga:
- Métricas: salário, modalidade, tipo de contrato, PcD, quantidade de vagas;
- Descrição da vaga (sobre o que a pessoa vai fazer);
- Benefícios e requisitos (obrigatórios e desejáveis);
- Dias em aberto desde a data de abertura.

Para **recrutadores e admins**: seção "👥 Candidatos Inscritos" com nome, e-mail, telefone, cidade e data de candidatura de cada inscrito, além de seletor para atualizar o status individualmente (Pendente → Em análise → Aprovado → Reprovado).

Para **candidatos**: botão de candidatura (ou mensagem de "já inscrito" caso o candidato já tenha se candidatado).

#### Dashboard Analítico (Admin/Recrutador)
Exibe indicadores visuais com:
- KPIs: total de vagas, vagas abertas, vagas encerradas, posições disponíveis e vagas PcD;
- Gráficos de barras horizontais: vagas por modalidade, por tipo de contrato, por empresa e salário médio por setor;
- Percentuais de status das vagas (abertas vs. encerradas vs. PcD);
- Alerta de vagas abertas há mais de 60 dias (até 10 itens, com escala de cores: amarelo ≥60d, laranja ≥90d, vermelho ≥120d).

#### Cadastrar / Editar Vaga (Admin/Recrutador)
Formulário com campos: título, local, descrição (texto livre sobre a vaga), salário, quantidade de vagas, empresa, modalidade, tipo de contrato, público-alvo, horário e indicador PcD.

#### Gerenciamento de Empresas (Admin)
CRUD completo de empresas: nome, CNPJ, setor, cidade, estado e descrição.

#### Gerenciamento de Candidatos (Admin)
Listagem e edição dos perfis de candidatos cadastrados: nome, e-mail, telefone, cidade, estado e data de nascimento.

#### Gerenciamento de Usuários (Admin)
Criação de usuários com qualquer perfil (Admin, Recrutador, Candidato) e exclusão com proteção contra auto-exclusão.

#### Perfil do Candidato / Minhas Candidaturas (Candidato)
Painel com dados de contato do candidato (editáveis via expander), histórico de candidaturas com status colorido (Pendente, Em análise, Aprovado, Reprovado) e informações da vaga e empresa de cada candidatura.

---

### 5.7 Endpoints da API REST

A documentação interativa completa (Swagger UI) está disponível em:

**https://api.alvesmotionlab.com.br/docs**

| Método | Endpoint | Descrição | Autenticação |
|---|---|---|---|
| POST | /auth/registro | Cadastro de novo usuário | Pública |
| POST | /auth/login | Login (retorna token JWT) | Pública |
| GET | /auth/usuarios | Lista todos os usuários | Admin |
| POST | /auth/usuarios | Cria usuário (qualquer perfil) | Admin |
| DELETE | /auth/usuarios/{id} | Exclui usuário | Admin |
| GET | /vagas/ | Lista vagas (com filtros opcionais) | Autenticado |
| POST | /vagas/ | Cria nova vaga | Admin/Recrutador |
| GET | /vagas/{id} | Detalhe de uma vaga | Autenticado |
| PUT | /vagas/{id} | Atualiza vaga | Admin/Recrutador |
| DELETE | /vagas/{id} | Exclui vaga | Admin/Recrutador |
| GET | /empresas/ | Lista empresas | Autenticado |
| POST | /empresas/ | Cria empresa | Admin |
| GET | /empresas/{id} | Detalhe de empresa | Autenticado |
| PUT | /empresas/{id} | Atualiza empresa | Admin |
| DELETE | /empresas/{id} | Exclui empresa | Admin |
| GET | /candidatos/ | Lista candidatos | Autenticado |
| POST | /candidatos/ | Cria perfil de candidato | Autenticado |
| GET | /candidatos/{id} | Detalhe de candidato | Autenticado |
| PUT | /candidatos/{id} | Atualiza candidato | Autenticado |
| GET | /candidaturas/ | Lista candidaturas (filtro: ?vaga_id=) | Autenticado |
| POST | /candidaturas/ | Registra candidatura | Autenticado |
| GET | /candidaturas/{id} | Detalhe de candidatura | Autenticado |
| PUT | /candidaturas/{id}/status | Atualiza status da candidatura | Admin/Recrutador |

---

## 6. GUIA DE ACESSO E UTILIZAÇÃO

### 6.1 Acesso ao Sistema

O sistema está disponível publicamente na internet pelo endereço:

**https://projeto-integrador-senac.streamlit.app**

Não é necessária nenhuma instalação no computador do usuário. Basta um navegador web atualizado (Chrome, Firefox, Edge ou Safari).

> **Dica para celular:** ao digitar e-mail e senha, desative o autocomplete/autocorrect do teclado para evitar que letras maiúsculas sejam inseridas automaticamente.

---

### 6.2 Como Criar um Usuário

#### Opção A — Auto-cadastro (Candidatos)

1. Acesse **https://projeto-integrador-senac.streamlit.app**
2. Na tela inicial, clique na aba **"📝 Criar conta"**
3. Preencha: nome completo, e-mail, senha (mínimo 6 caracteres) e confirmação de senha
4. Clique em **"Criar conta"**
5. O sistema criará automaticamente um perfil de **Candidato**

#### Opção B — Criação pelo Administrador

1. Faça login com uma conta de **Administrador**
2. Na navbar, clique em **"👥 Usuários"**
3. Clique em **"➕ Criar novo usuário"**
4. Preencha nome, e-mail, senha e selecione o perfil desejado (Candidato, Recrutador ou Admin)
5. Clique em **"Criar usuário"**

> Somente o Administrador pode criar usuários com perfil de **Recrutador** ou **Administrador**.

#### Credenciais do Administrador Padrão

| Campo | Valor |
|---|---|
| E-mail | joao@jvsatech.com.br |
| Senha | 123456Dd. |

---

### 6.3 Perfis e Permissões

| Perfil | Descrição | Como é criado |
|---|---|---|
| **Admin** | Acesso total ao sistema | Criado por outro Admin |
| **Recrutador** | Gerencia vagas, vê dashboard e candidatos inscritos | Criado por Admin |
| **Candidato** | Visualiza vagas, se candidata e acompanha candidaturas | Auto-cadastro ou criado por Admin |

---

### 6.4 Como Cadastrar uma Vaga

1. Faça login com conta de **Admin** ou **Recrutador**
2. Na navbar, clique em **"💼 Vagas"**
3. Clique em **"➕ Cadastrar nova vaga"**
4. Preencha os campos:
   - **Título** — nome do cargo
   - **Local** — cidade/estado
   - **Salário** — valor em R$ (deixe 0 para "A combinar")
   - **Quantidade de vagas** — número de posições abertas
   - **Empresa** — selecione da lista de empresas cadastradas
   - **Modalidade** — Presencial, Remoto ou Híbrido
   - **Tipo de contrato** — CLT, PJ, Temporário ou Estágio
   - **Público-alvo** — Ambos, Masculino ou Feminino
   - **Horário** — ex.: "Segunda a Sexta, 9h–18h"
   - **Descrição da vaga** — texto livre sobre responsabilidades e o que a pessoa vai fazer
   - **Vaga PcD** — marcar se a vaga é destinada a Pessoa com Deficiência
5. Clique em **"Salvar vaga"**

---

### 6.5 Como se Candidatar a uma Vaga

1. Faça login com conta de **Candidato**
2. No painel de vagas, clique em **"Ver detalhes"** na vaga desejada
3. Role a página até a seção **"🚀 Candidatar-se"**
4. Clique em **"✅ Candidatar-se a esta vaga"**

> Caso o candidato ainda não tenha completado o perfil com dados de contato, o sistema solicitará o preenchimento antes de permitir a candidatura. Após inscrito, a mensagem muda para "✅ Você já está inscrito nessa vaga!".

Para acompanhar candidaturas:
1. Na navbar, clique em **"📋 Candidaturas"**
2. Visualize o histórico com status de cada candidatura

Para editar dados de contato:
1. Na tela de Candidaturas, clique em **"✏️ Editar dados de contato"**
2. Atualize telefone, cidade, estado ou data de nascimento

---

### 6.6 Como Gerenciar Candidaturas (Recrutador/Admin)

1. Faça login com conta de **Admin** ou **Recrutador**
2. Acesse qualquer vaga e clique em **"Ver detalhes"**
3. Role até a seção **"👥 Candidatos Inscritos"**
4. Para cada candidato inscrito são exibidos:
   - Nome completo, e-mail, telefone e cidade
   - Data de candidatura e status atual
5. Para atualizar o status de um candidato:
   - Selecione o novo status no dropdown (Pendente / Em análise / Aprovado / Reprovado)
   - Clique em **"Salvar"**
6. O candidato verá o status atualizado em **"Minhas Candidaturas"**

---

### 6.7 Como Acessar o Banco de Dados

#### Opção A — Via Swagger UI (Recomendado)

A API FastAPI fornece documentação interativa automática:

**https://api.alvesmotionlab.com.br/docs**

Nessa interface é possível executar consultas, criar registros e testar todos os endpoints diretamente pelo navegador após autenticação.

#### Opção B — Via Terminal no EasyPanel

1. Acesse **painel.alvesmotionlab.com.br** e faça login
2. Navegue até o serviço da API
3. Clique em **"Terminal"**
4. Execute:

```bash
# Acessar o SQLite interativo
sqlite3 /data/agencia_empregos.db

# Exemplos de consultas
SELECT v.titulo, e.nome, v.status FROM vagas v JOIN empresas e ON v.empresa_id = e.id;
SELECT status, COUNT(*) FROM candidaturas GROUP BY status;
SELECT v.titulo, COUNT(c.id) AS inscritos FROM vagas v LEFT JOIN candidaturas c ON c.vaga_id = v.id GROUP BY v.id ORDER BY inscritos DESC;
.quit
```

#### Principais Consultas SQL de Exemplo

```sql
-- Listar todas as vagas abertas
SELECT v.titulo, e.nome AS empresa, v.local, v.salario
FROM vagas v
JOIN empresas e ON v.empresa_id = e.id
WHERE v.status = 'aberta';

-- Contar candidaturas por status
SELECT status, COUNT(*) as total
FROM candidaturas
GROUP BY status;

-- Vagas com mais candidaturas
SELECT v.titulo, COUNT(c.id) as total_candidaturas
FROM vagas v
LEFT JOIN candidaturas c ON c.vaga_id = v.id
GROUP BY v.id
ORDER BY total_candidaturas DESC;

-- Candidatos de uma vaga específica com contato
SELECT ca.nome, ca.email, ca.telefone, cu.status, cu.data_candidatura
FROM candidaturas cu
JOIN candidatos ca ON ca.id = cu.candidato_id
WHERE cu.vaga_id = 1;

-- Listar usuários e seus perfis
SELECT nome, email, perfil FROM usuarios ORDER BY perfil;
```

---

### 6.8 Como Acessar o Servidor (EasyPanel)

O backend está hospedado em **VPS Hostinger** gerenciada pelo **EasyPanel**.

#### Acesso ao Painel

1. Acesse **painel.alvesmotionlab.com.br**
2. Faça login com as credenciais do EasyPanel
3. Navegue até o serviço da API

#### Ações disponíveis no EasyPanel

| Ação | Como fazer |
|---|---|
| Ver logs da API | Aba "Logs" no serviço |
| Acessar terminal do container | Aba "Terminal" no serviço |
| Aplicar migration manual | Terminal → `cd /app && alembic upgrade head` |
| Reiniciar o container | Botão "Restart" no serviço |
| Ver/editar variáveis de ambiente | Aba "Environment" |
| Forçar novo deploy | Botão "Deploy" (após `git push`) |

#### Variáveis de Ambiente do Backend

| Variável | Valor | Descrição |
|---|---|---|
| `DATABASE_URL` | sqlite:////data/agencia_empregos.db | Caminho do banco no volume persistente |
| `ADMIN_EMAIL` | joao@jvsatech.com.br | E-mail do admin criado automaticamente |
| `ADMIN_SENHA` | 123456Dd. | Senha do admin criado automaticamente |
| `ADMIN_NOME` | João Vitor | Nome do admin criado automaticamente |

---

## 7. INFRAESTRUTURA E IMPLANTAÇÃO

### 7.1 Servidor Backend (EasyPanel + Docker)

| Configuração | Valor |
|---|---|
| **Provedor** | Hostinger VPS |
| **IP público** | 72.60.51.179 |
| **Painel de gerenciamento** | EasyPanel (painel.alvesmotionlab.com.br) |
| **Conteinerização** | Docker (Dockerfile no diretório `/backend`) |
| **Servidor ASGI** | Uvicorn (porta 8000 interna) |
| **Banco de dados** | SQLite em volume persistente `/data` |
| **DNS** | Cloudflare (domínio alvesmotionlab.com.br) |
| **URL pública** | https://api.alvesmotionlab.com.br |

O backend é conteinerizado via **Dockerfile**. O EasyPanel monitora o repositório GitHub e realiza o build e deploy automático a cada novo commit. As migrações do Alembic são executadas automaticamente no startup do container (`alembic upgrade head`). Caso o banco esteja vazio, o sistema cria automaticamente o usuário administrador padrão (`_seed_admin()`).

**Dockerfile do backend:**

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /data
ENV DATABASE_URL=sqlite:////data/agencia_empregos.db
RUN alembic upgrade head || true
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

O volume `/data` é configurado no EasyPanel como **Storage persistente**, garantindo que o banco de dados SQLite não seja perdido em redeploys.

### 7.2 Frontend (Streamlit Cloud)

O frontend está hospedado na plataforma **Streamlit Cloud**, que monitora o repositório GitHub e realiza o deploy automático a cada novo commit na branch `main`.

**https://projeto-integrador-senac.streamlit.app**

A URL da API é configurada via **Secrets** do Streamlit Cloud:

```toml
API_URL = "https://api.alvesmotionlab.com.br"
```

### 7.3 DNS e HTTPS (Cloudflare)

O domínio `alvesmotionlab.com.br` utiliza os **nameservers do Cloudflare**, que gerencia o DNS e fornece HTTPS automático para o subdomínio `api.alvesmotionlab.com.br`.

| Configuração | Valor |
|---|---|
| **Registro DNS** | A — `api` → `72.60.51.179` |
| **Proxy Cloudflare** | Ativo (modo Proxied — ícone laranja) |
| **HTTPS** | Automático via Cloudflare SSL |
| **Porta exposta pelo EasyPanel** | 443 (HTTPS) → 8000 (container) |

Esta arquitetura elimina a necessidade de certificado SSL próprio no servidor e garante que o Streamlit Cloud (que exige HTTPS em todas as requisições externas) consiga se comunicar com a API.

### 7.4 Versionamento (GitHub)

O código-fonte é versionado no repositório público:

**https://github.com/joaovitor1110/projeto-integrador**

O fluxo de atualização:

1. Alterações são desenvolvidas no ambiente Claude Code (remoto) ou localmente
2. `git add` + `git commit` + `git push origin main` envia para o GitHub
3. O **Streamlit Cloud** detecta o novo commit e realiza o redeploy automático do frontend (em ~1–2 minutos)
4. O **EasyPanel** detecta o novo commit e realiza o rebuild do container Docker do backend

---

## 8. CRONOGRAMA

| Semana | Período | Atividades realizadas |
|---|---|---|
| **1** | Semana 1 | Definição do escopo; modelagem do banco de dados (Diagrama ER); implementação dos modelos SQLAlchemy; configuração do ambiente FastAPI e Uvicorn; implementação da autenticação JWT. |
| **2** | Semana 2 | Desenvolvimento dos routers da API (vagas, empresas, candidatos, candidaturas); implementação dos schemas Pydantic; configuração do Alembic para migrações; testes dos endpoints via Swagger UI. |
| **3** | Semana 3 | Desenvolvimento da interface Streamlit (painel de vagas, detalhe, formulários); implantação inicial na AWS EC2 com Cloudflare Tunnel; publicação no Streamlit Cloud; integração e testes end-to-end. |
| **4** | Semana 4 | Implementação do dashboard analítico; tela de candidaturas para candidatos; gerenciamento de usuários com proteções de segurança; migração do backend para EasyPanel/VPS Hostinger com Docker e domínio próprio; carga de dados de teste (10 empresas, 20 candidatos, 25 vagas, 109 candidaturas). |
| **5** | Semana 5 | Substituição da sidebar por navbar horizontal; aplicação de fonte Poppins; adição de campo descrição nas vagas; implementação da visão de candidatos inscritos por vaga para recrutadores; endpoint de atualização de status de candidatura; correções de compatibilidade com tema dark; ajustes de UX mobile; elaboração da documentação ABNT; apresentação final. |

---

## 9. CONSIDERAÇÕES FINAIS

O projeto **Agência de Empregos** atingiu e superou os objetivos propostos, entregando um sistema web completo, funcional e acessível publicamente com domínio próprio e disponibilidade contínua 24/7.

Entre os principais aprendizados técnicos obtidos durante o desenvolvimento, destacam-se:

- Construção de APIs REST com autenticação JWT e controle de acesso por perfis;
- Gerenciamento de banco de dados relacional com ORM e migrações controladas (Alembic);
- Conteinerização de aplicações Python com Docker e gerenciamento via EasyPanel;
- Configuração de DNS, certificado SSL e proxy reverso via Cloudflare;
- Resolução de desafios de infraestrutura (compatibilidade passlib/bcrypt, volumes persistentes Docker, variáveis de ambiente por perfil);
- Desenvolvimento de interfaces web interativas e responsivas com Streamlit (navbar, cards, filtros, dashboard);
- Gerenciamento de fluxo completo de recrutamento: publicação de vaga → candidatura → análise → decisão;
- Versionamento colaborativo com Git e GitHub com deploy automático.

O sistema encontra-se em plena operação com dados reais de teste, incluindo 10 empresas de renome (Google Brasil, Nubank, Magazine Luiza, Ambev, Hospital Albert Einstein, Itaú Unibanco, iFood, Embraer, Natura &Co, XP Inc.), 25 vagas em diversas modalidades e contratos, 20 candidatos e mais de 109 candidaturas distribuídas estrategicamente para demonstração das métricas do dashboard.

O sistema pode ser demonstrado ao vivo durante a apresentação em:

**https://projeto-integrador-senac.streamlit.app**

---

## 10. REFERÊNCIAS

ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. **NBR 6023**: Informação e documentação — Referências — Elaboração. Rio de Janeiro: ABNT, 2018.

ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. **NBR 14724**: Informação e documentação — Trabalhos acadêmicos — Apresentação. Rio de Janeiro: ABNT, 2011.

CLOUDFLARE. **Cloudflare DNS Documentation**. Disponível em: https://developers.cloudflare.com/dns/. Acesso em: jul. 2026.

CORONEL, C.; MORRIS, S.; ROB, P. **Sistemas de banco de dados**. São Paulo: Cengage Learning, 2011.

DATE, C. J. **Introdução a sistemas de bancos de dados**. 8. ed. Rio de Janeiro: Elsevier, 2004.

DOCKER. **Docker Documentation**. Disponível em: https://docs.docker.com/. Acesso em: jul. 2026.

EASYPANEL. **EasyPanel Documentation**. Disponível em: https://easypanel.io/docs. Acesso em: jul. 2026.

FASTAPI. **FastAPI Documentation**. Disponível em: https://fastapi.tiangolo.com/. Acesso em: jul. 2026.

HOSTINGER. **VPS Hosting Documentation**. Disponível em: https://support.hostinger.com/en/. Acesso em: jul. 2026.

McKINNEY, W. **Python para análise de dados**. São Paulo: Novatec, 2019.

PYTHON SOFTWARE FOUNDATION. **Python 3 Documentation**. Disponível em: https://docs.python.org/3/. Acesso em: jul. 2026.

RAMAKRISHNAN, R.; GEHRKE, J. **Sistemas de gerenciamento de banco de dados**. 3. ed. Porto Alegre: McGraw-Hill, 2008.

SQLALCHEMY. **SQLAlchemy Documentation**. Disponível em: https://docs.sqlalchemy.org/. Acesso em: jul. 2026.

STREAMLIT. **Streamlit Documentation**. Disponível em: https://docs.streamlit.io/. Acesso em: jul. 2026.

---

*Documento elaborado em conformidade com as normas ABNT NBR 14724:2011 e NBR 6023:2018.*

*São Paulo, julho de 2026.*

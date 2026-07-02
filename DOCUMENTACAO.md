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

O presente trabalho descreve o desenvolvimento de um sistema web completo para gestão de vagas de emprego, denominado **Agência de Empregos**, elaborado como Projeto Integrador da Unidade Curricular 6 (UC6) do Curso Técnico em Inteligência Artificial do SENAC Lapa Tito. A solução integra um backend construído com o framework FastAPI em linguagem Python, banco de dados relacional SQLite gerenciado via SQLAlchemy e interface web interativa desenvolvida com Streamlit. O sistema permite o cadastro e gerenciamento de empresas, vagas de emprego, candidatos e candidaturas, com controle de acesso baseado em perfis de usuário (Administrador, Recrutador e Candidato). A aplicação é hospedada em infraestrutura de nuvem utilizando instância AWS EC2 para o backend e Streamlit Cloud para o frontend, com comunicação segura provida por túnel Cloudflare. O código-fonte é versionado no GitHub e o sistema encontra-se em pleno funcionamento no endereço **projeto-integrador-senac.streamlit.app**.

**Palavras-chave:** sistema web; gestão de vagas; FastAPI; Streamlit; banco de dados; AWS; Python.

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
6. GUIA DE ACESSO E UTILIZAÇÃO
   - 6.1 Acesso ao Sistema
   - 6.2 Como Criar um Usuário
   - 6.3 Perfis e Permissões
   - 6.4 Como Cadastrar uma Vaga
   - 6.5 Como se Candidatar a uma Vaga
   - 6.6 Como Acessar o Banco de Dados
   - 6.7 Como Acessar o Servidor (EC2)
7. INFRAESTRUTURA E IMPLANTAÇÃO
   - 7.1 Servidor Backend (AWS EC2)
   - 7.2 Frontend (Streamlit Cloud)
   - 7.3 Exposição HTTPS (Cloudflare Tunnel)
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
| **Repositório** | https://github.com/joaovitor1110/projeto-integrador |

---

## 2. TEMA DO PROJETO

O presente projeto aborda o desenvolvimento de uma plataforma web completa para gestão de vagas de emprego, destinada a conectar empresas recrutadoras e candidatos a oportunidades de trabalho. O sistema, denominado **Agência de Empregos**, simula o funcionamento de uma agência digital de recrutamento, oferecendo ferramentas para publicação, gerenciamento e candidatura a vagas.

O mercado de trabalho brasileiro enfrenta um desafio crescente de intermediação eficiente entre oferta e demanda de empregos. Plataformas digitais de recrutamento tornaram-se indispensáveis tanto para empresas que buscam talentos quanto para candidatos que buscam oportunidades. Diante desse contexto, o projeto propõe a implementação de um sistema web funcional e completo, capaz de organizar todo o ciclo de uma vaga: desde o cadastro pela empresa até a candidatura e acompanhamento pelo candidato.

O sistema contempla as seguintes áreas:

- cadastro e gerenciamento de empresas;
- publicação e gestão de vagas de emprego com atributos detalhados;
- cadastro e acompanhamento de candidatos;
- registro e acompanhamento de candidaturas;
- dashboard analítico com indicadores de vagas;
- controle de acesso com três perfis distintos de usuário.

---

## 3. OBJETIVO

### 3.1 Objetivo Geral

Desenvolver um sistema web completo e funcional para gestão de vagas de emprego, integrando um backend RESTful construído com FastAPI em Python, banco de dados relacional SQLite, e interface web interativa com Streamlit, implantado em infraestrutura de nuvem (AWS EC2 + Streamlit Cloud) com acesso público.

### 3.2 Objetivos Específicos

- Modelar e implementar um banco de dados relacional com entidades, atributos e relacionamentos coerentes com o contexto de uma agência de empregos;
- Desenvolver uma API REST completa com FastAPI, incluindo autenticação JWT, controle de perfis e operações CRUD para todas as entidades do sistema;
- Implementar controle de acesso baseado em perfis (Admin, Recrutador e Candidato), com restrições de permissão por funcionalidade;
- Construir uma interface web responsiva e interativa com Streamlit, contendo painel de vagas, dashboard analítico, gerenciamento de candidaturas e área administrativa;
- Hospedar o backend em instância AWS EC2 com Amazon Linux 2023 e o frontend no Streamlit Cloud, garantindo acesso público e contínuo;
- Implementar túnel HTTPS seguro via Cloudflare para permitir a comunicação entre o frontend (HTTPS) e o backend (HTTP) em ambiente de nuvem;
- Versionar o código-fonte no GitHub com histórico de commits documentado;
- Elaborar documentação técnica completa em conformidade com as normas da ABNT.

---

## 4. JUSTIFICATIVA

A digitalização dos processos seletivos é uma realidade consolidada no mercado de trabalho contemporâneo. Empresas de todos os portes utilizam plataformas digitais para publicar vagas, receber candidaturas e gerenciar processos seletivos. A construção de um sistema com essa finalidade permite ao estudante de tecnologia vivenciar, na prática, o desenvolvimento completo de uma aplicação real — desde a modelagem do banco de dados até a implantação em produção.

Do ponto de vista acadêmico, o projeto justifica-se por integrar, de forma coesa e aplicada, as principais tecnologias estudadas ao longo do Curso Técnico em Inteligência Artificial: desenvolvimento de APIs REST com Python, modelagem e persistência de dados relacionais, autenticação e segurança, desenvolvimento de interfaces web e implantação em infraestrutura de nuvem.

A escolha do FastAPI como framework principal agrega relevância técnica ao trabalho, por se tratar de um dos frameworks Python mais modernos e de alta performance do mercado, amplamente utilizado na indústria para construção de APIs REST. O uso do Streamlit como camada de interface permite desenvolver aplicações web interativas com Python puro, sem a necessidade de conhecimento em JavaScript ou frameworks de frontend tradicionais.

A implantação em infraestrutura real de nuvem (AWS EC2) e a exposição pública do sistema via Streamlit Cloud distinguem este projeto de soluções que funcionam apenas em ambiente local, demonstrando domínio sobre o ciclo completo de desenvolvimento de software: concepção, implementação, testes e implantação em produção.

---

## 5. EXPLICAÇÃO DA SOLUÇÃO

### 5.1 Visão Geral da Arquitetura

A solução é composta por três camadas principais, integradas entre si:

```
┌─────────────────────────────────────────────────────────┐
│                    USUÁRIO (Navegador)                   │
└─────────────────────────────┬───────────────────────────┘
                              │ HTTPS
┌─────────────────────────────▼───────────────────────────┐
│              STREAMLIT CLOUD (Frontend)                  │
│          projeto-integrador-senac.streamlit.app          │
│              streamlit_app.py  (Python)                  │
└─────────────────────────────┬───────────────────────────┘
                              │ HTTPS (Cloudflare Tunnel)
┌─────────────────────────────▼───────────────────────────┐
│              AWS EC2 — t3.micro (Backend)                │
│           Amazon Linux 2023 | IP: 172.31.7.192           │
│    FastAPI + Uvicorn  →  porta 8000                      │
│    SQLite  →  agencia_empregos.db                        │
└─────────────────────────────────────────────────────────┘
```

- **Camada de apresentação:** interface web construída com Streamlit, hospedada no Streamlit Cloud. Acesso público via HTTPS sem necessidade de configuração local;
- **Camada de aplicação:** API REST construída com FastAPI, executada via servidor Uvicorn em instância AWS EC2. Responsável pela lógica de negócio, autenticação e persistência;
- **Camada de dados:** banco de dados relacional SQLite, gerenciado pelo ORM SQLAlchemy com migrações controladas pelo Alembic.

A comunicação entre o Streamlit Cloud (HTTPS obrigatório) e o backend EC2 (HTTP) é viabilizada pelo **Cloudflare Tunnel**, que fornece um endpoint HTTPS público sem necessidade de certificado SSL próprio ou IP fixo.

---

### 5.2 Tecnologias Utilizadas

| Tecnologia | Versão | Função |
|---|---|---|
| **Python** | 3.11+ | Linguagem principal do backend e frontend |
| **FastAPI** | 0.110+ | Framework para construção da API REST |
| **Uvicorn** | 0.29+ | Servidor ASGI para execução do FastAPI |
| **SQLAlchemy** | 2.0+ | ORM para mapeamento objeto-relacional |
| **SQLite** | 3.x | Banco de dados relacional embutido |
| **Alembic** | 1.13+ | Controle de migrações do banco de dados |
| **Pydantic** | 2.x | Validação de dados e schemas da API |
| **python-jose** | 3.3+ | Geração e validação de tokens JWT |
| **passlib[bcrypt]** | 1.7.4 | Hash seguro de senhas com bcrypt |
| **bcrypt** | 4.0.1 | Algoritmo de hash para senhas |
| **Streamlit** | 1.35+ | Framework para interface web interativa |
| **Requests** | 2.31+ | Cliente HTTP para consumo da API no frontend |
| **AWS EC2** | t3.micro | Servidor virtual para hospedagem do backend |
| **Amazon Linux** | 2023 | Sistema operacional do servidor |
| **Cloudflare Tunnel** | — | Túnel HTTPS para exposição segura da API |
| **Streamlit Cloud** | — | Plataforma de hospedagem do frontend |
| **GitHub** | — | Versionamento e repositório do código-fonte |
| **Git** | 2.x | Controle de versão local |

#### Estrutura de Diretórios do Projeto

```
projeto-integrador/
├── streamlit_app.py              # Interface web (frontend)
├── requirements.txt              # Dependências do frontend
├── .streamlit/
│   └── secrets.toml              # Configurações sensíveis (API_URL)
└── backend/
    ├── app/
    │   ├── main.py               # Ponto de entrada da API
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
    ├── alembic/
    │   ├── env.py                # Configuração do Alembic
    │   └── versions/             # Arquivos de migração
    ├── alembic.ini               # Configuração principal do Alembic
    ├── requirements.txt          # Dependências do backend
    └── agencia_empregos.db       # Arquivo do banco de dados SQLite
```

---

### 5.3 Modelagem do Banco de Dados

O banco de dados relacional é composto pelas seguintes entidades:

| Entidade | Principais atributos |
|---|---|
| **usuarios** | id, nome, email, senha_hash, perfil (admin/recrutador/visualizador) |
| **empresas** | id, nome, cnpj, setor, descricao, cidade, estado |
| **vagas** | id, titulo, local, salario, modalidade, horario, tipo_contrato, publico_alvo, vaga_pcd, status, data_publicacao, data_abertura, data_fechamento, quantidade_vagas, empresa_id |
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
├── setor                         ├── salario
├── descricao                     ├── modalidade
├── cidade                        ├── horario
└── estado                        ├── tipo_contrato
         │                        ├── publico_alvo
         │  1:N                   ├── vaga_pcd
         └──────────────────────► ├── status
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
- `VAGAS` ↔ `BENEFICIOS`: uma vaga possui muitos benefícios e um benefício pertence a muitas vagas (N:N via `vaga_beneficio`)
- `VAGAS` ↔ `REQUISITOS`: uma vaga possui muitos requisitos e um requisito pertence a muitas vagas (N:N via `vaga_requisito`)
- `CANDIDATOS` → `CANDIDATURAS`: um candidato faz muitas candidaturas (1:N)
- `VAGAS` → `CANDIDATURAS`: uma vaga recebe muitas candidaturas (1:N)

---

### 5.5 Controle de Acesso e Perfis de Usuário

O sistema implementa autenticação via **JSON Web Token (JWT)**. Ao realizar login, o usuário recebe um token de acesso com validade configurável (padrão: 60 minutos). Todas as rotas protegidas exigem o envio desse token no cabeçalho HTTP (`Authorization: Bearer <token>`).

Existem três perfis de usuário com permissões distintas:

| Funcionalidade | Admin | Recrutador | Candidato |
|---|:---:|:---:|:---:|
| Visualizar vagas | ✅ | ✅ | ✅ |
| Cadastrar/editar vagas | ✅ | ✅ | ❌ |
| Encerrar/reabrir vagas | ✅ | ✅ | ❌ |
| Dashboard analítico | ✅ | ✅ | ❌ |
| Candidatar-se a vagas | ❌ | ❌ | ✅ |
| Ver minhas candidaturas | ❌ | ❌ | ✅ |
| Gerenciar empresas | ✅ | ❌ | ❌ |
| Gerenciar candidatos | ✅ | ❌ | ❌ |
| Gerenciar usuários | ✅ | ❌ | ❌ |
| Criar usuários com qualquer perfil | ✅ | ❌ | ❌ |
| Excluir usuários | ✅* | ❌ | ❌ |

> \* O administrador não pode excluir a si próprio, nem excluir o último administrador do sistema.

---

### 5.6 Funcionalidades do Sistema

#### Painel de Vagas
Exibe todas as vagas cadastradas em formato de cards com informações resumidas: título, empresa, localidade, modalidade, tipo de contrato e salário. Possui filtros por modalidade, tipo de contrato, status e vagas PcD.

#### Detalhe da Vaga
Apresenta todas as informações de uma vaga: benefícios, requisitos (obrigatórios e desejáveis), horário, quantidade de vagas disponíveis, dias em aberto e ações disponíveis conforme perfil do usuário.

#### Dashboard Analítico (Admin/Recrutador)
Exibe indicadores visuais com:
- KPIs: total de vagas, vagas abertas, vagas encerradas, posições disponíveis e vagas PcD;
- Gráficos de barras horizontais: vagas por modalidade, vagas por tipo de contrato, vagas por empresa e salário médio por setor;
- Percentuais de status das vagas;
- Alerta de vagas abertas há muito tempo (30, 60 e 90+ dias).

#### Gerenciamento de Empresas (Admin)
CRUD completo de empresas: nome, CNPJ, setor, cidade, estado e descrição.

#### Gerenciamento de Candidatos (Admin)
Listagem e edição dos perfis de candidatos cadastrados.

#### Gerenciamento de Usuários (Admin)
Criação de usuários com qualquer perfil (Admin, Recrutador, Candidato) e exclusão com proteções de segurança.

#### Minhas Candidaturas (Candidato)
Painel do candidato com seu perfil pessoal e histórico de candidaturas com status colorido: Pendente, Em análise, Aprovado e Reprovado.

---

## 6. GUIA DE ACESSO E UTILIZAÇÃO

### 6.1 Acesso ao Sistema

O sistema está disponível publicamente na internet pelo endereço:

**https://projeto-integrador-senac.streamlit.app**

Não é necessária nenhuma instalação no computador do usuário. Basta um navegador web atualizado (Chrome, Firefox, Edge ou Safari).

---

### 6.2 Como Criar um Usuário

#### Opção A — Auto-cadastro (Candidatos)

1. Acesse **https://projeto-integrador-senac.streamlit.app**
2. Na tela inicial, clique na aba **"📝 Criar conta"**
3. Preencha:
   - Nome completo
   - E-mail
   - Senha (mínimo 6 caracteres)
   - Confirmação de senha
4. Clique em **"Criar conta"**
5. O sistema criará automaticamente um perfil de **Candidato**

> O auto-cadastro cria automaticamente o perfil de usuário e o registro de candidato vinculado. O candidato já pode visualizar vagas e se candidatar imediatamente.

#### Opção B — Criação pelo Administrador

1. Faça login com uma conta de **Administrador**
2. No menu lateral, clique em **"👥 Usuários"**
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
| **Recrutador** | Gerencia vagas e vê dashboard | Criado por Admin |
| **Candidato** | Visualiza vagas e se candidata | Auto-cadastro ou criado por Admin |

---

### 6.4 Como Cadastrar uma Vaga

1. Faça login com conta de **Admin** ou **Recrutador**
2. No menu, clique em **"💼 Vagas"**
3. Clique em **"➕ Cadastrar nova vaga"** (expander no topo da página)
4. Preencha os campos:
   - **Título** — nome do cargo
   - **Local** — cidade/estado
   - **Salário** — valor em R$ (ou deixe 0 para "A combinar")
   - **Quantidade de vagas** — número de posições
   - **Empresa** — selecione da lista de empresas cadastradas
   - **Modalidade** — Presencial, Remoto ou Híbrido
   - **Tipo de contrato** — CLT, PJ, Temporário ou Estágio
   - **Público-alvo** — Ambos, Masculino ou Feminino
   - **Horário** — ex.: "Segunda a Sexta, 9h–18h"
   - **Vaga PcD** — marcar se a vaga é para Pessoa com Deficiência
5. Clique em **"Salvar vaga"**

---

### 6.5 Como se Candidatar a uma Vaga

1. Faça login com conta de **Candidato**
2. No painel de vagas, clique em **"Ver detalhes"** na vaga desejada
3. Role a página até a seção **"🚀 Candidatar-se"**
4. Clique em **"✅ Candidatar-se a esta vaga"**

> Caso o candidato ainda não tenha completado o perfil com dados de contato (telefone, cidade, estado), o sistema solicitará o preenchimento antes de permitir a candidatura.

Para acompanhar candidaturas:
1. No menu lateral, clique em **"📋 Minhas Candidaturas"**
2. Visualize o histórico com status de cada candidatura

---

### 6.6 Como Acessar o Banco de Dados

#### Opção A — Via Navegador (API — Recomendado para consultas rápidas)

A API FastAPI fornece documentação interativa automática (Swagger UI):

```
http://<IP_DO_SERVIDOR>:8000/docs
```

Nessa interface é possível executar consultas, criar registros e testar todos os endpoints diretamente pelo navegador.

#### Opção B — Via DB Browser for SQLite (Interface Gráfica)

1. Baixe e instale o **DB Browser for SQLite** gratuitamente em: https://sqlitebrowser.org
2. No servidor EC2, copie o arquivo do banco para o computador local usando SCP:

```bash
scp -i sua-chave.pem ec2-user@<IP_DO_SERVIDOR>:/home/ec2-user/projeto-integrador/backend/agencia_empregos.db .
```

3. Abra o arquivo `agencia_empregos.db` no DB Browser for SQLite
4. Navegue pelas tabelas na aba **"Browse Data"** ou execute consultas SQL na aba **"Execute SQL"**

#### Opção C — Via Terminal SSH (Linha de Comando)

1. Conecte-se ao servidor EC2 (ver seção 6.7)
2. Execute os comandos:

```bash
cd ~/projeto-integrador/backend
python3 -c "
import sqlite3
conn = sqlite3.connect('agencia_empregos.db')
cursor = conn.cursor()
# Exemplo: listar todas as vagas
cursor.execute('SELECT id, titulo, status FROM vagas')
for row in cursor.fetchall():
    print(row)
conn.close()
"
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

-- Listar usuários e seus perfis
SELECT nome, email, perfil FROM usuarios ORDER BY perfil;
```

---

### 6.7 Como Acessar o Servidor (EC2)

O backend está hospedado em uma instância **AWS EC2 t3.micro** com Amazon Linux 2023.

#### Acesso via AWS Console (Navegador — sem necessidade de chave SSH)

1. Acesse https://aws.amazon.com e faça login
2. Navegue até **EC2 → Instâncias**
3. Selecione a instância do projeto
4. Clique em **"Conectar"** → **"EC2 Instance Connect"**
5. Clique em **"Conectar"** — um terminal abrirá no navegador

#### Comandos Úteis no Servidor

```bash
# Verificar se a API está rodando
ps aux | grep uvicorn

# Ver logs da API em tempo real
tail -f ~/api.log

# Reiniciar a API
pkill -f uvicorn
cd ~/projeto-integrador/backend
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > ~/api.log 2>&1 &

# Verificar URL do túnel Cloudflare
grep 'trycloudflare.com' ~/tunnel.log | tail -1

# Reiniciar o túnel Cloudflare
pkill cloudflared
nohup cloudflared tunnel --url http://localhost:8000 > ~/tunnel.log 2>&1 &

# Atualizar o código do GitHub
cd ~/projeto-integrador
git pull https://joaovitor1110:<TOKEN>@github.com/joaovitor1110/projeto-integrador.git main

# Aplicar migrações do banco de dados
cd ~/projeto-integrador/backend
alembic upgrade head
```

---

## 7. INFRAESTRUTURA E IMPLANTAÇÃO

### 7.1 Servidor Backend (AWS EC2)

| Configuração | Valor |
|---|---|
| **Tipo de instância** | t3.micro |
| **Sistema operacional** | Amazon Linux 2023 |
| **Região AWS** | us-east-1 (Norte da Virgínia) |
| **Porta da API** | 8000 (HTTP) |
| **Servidor ASGI** | Uvicorn (modo background com nohup) |
| **Banco de dados** | SQLite — arquivo `agencia_empregos.db` |
| **Gerenciador de ambiente** | Python venv (`~/projeto-integrador/backend/venv`) |

O processo Uvicorn é iniciado em background com `nohup`, garantindo que continue executando mesmo após o encerramento da sessão SSH:

```bash
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > ~/api.log 2>&1 &
```

### 7.2 Frontend (Streamlit Cloud)

O frontend está hospedado na plataforma **Streamlit Cloud**, que monitora o repositório GitHub e realiza o deploy automático a cada novo commit na branch `main`. O endereço público é:

**https://projeto-integrador-senac.streamlit.app**

A URL da API é configurada via **Secrets** do Streamlit Cloud (`.streamlit/secrets.toml`):

```toml
API_URL = "https://<url-do-tunel>.trycloudflare.com"
```

### 7.3 Exposição HTTPS (Cloudflare Tunnel)

O Streamlit Cloud exige que todas as requisições externas utilizem HTTPS. Como o backend EC2 serve HTTP na porta 8000, utiliza-se o **Cloudflare Tunnel** para criar um endpoint HTTPS público que redireciona para o servidor local:

```bash
nohup cloudflared tunnel --url http://localhost:8000 > ~/tunnel.log 2>&1 &
```

O cloudflared gera automaticamente uma URL no formato:
```
https://<nome-aleatorio>.trycloudflare.com
```

Essa URL deve ser atualizada nos Secrets do Streamlit Cloud sempre que o túnel for reiniciado.

### 7.4 Versionamento (GitHub)

O código-fonte é versionado no repositório público:

**https://github.com/joaovitor1110/projeto-integrador**

O fluxo de atualização segue o padrão:

1. Alterações são feitas localmente (ou no ambiente de desenvolvimento)
2. `git add` + `git commit` + `git push` envia para o GitHub
3. O Streamlit Cloud detecta o novo commit e realiza o redeploy automático do frontend
4. No EC2, executa-se `git pull` e reinicia-se o Uvicorn para aplicar as alterações no backend

---

## 8. CRONOGRAMA

| Semana | Período | Atividades realizadas |
|---|---|---|
| **1** | Semana 1 | Definição do escopo; modelagem do banco de dados (Diagrama ER); implementação dos modelos SQLAlchemy; configuração do ambiente FastAPI e Uvicorn; implementação da autenticação JWT. |
| **2** | Semana 2 | Desenvolvimento dos routers da API (vagas, empresas, candidatos, candidaturas); implementação dos schemas Pydantic; configuração do Alembic para migrações; testes dos endpoints via Swagger UI. |
| **3** | Semana 3 | Desenvolvimento da interface Streamlit (painel de vagas, detalhe, formulários); implantação do backend na AWS EC2; configuração do Cloudflare Tunnel; publicação no Streamlit Cloud; integração e testes end-to-end. |
| **4** | Semana 4 | Implementação do dashboard analítico; tela de candidaturas para candidatos; gerenciamento de usuários com proteções de segurança; cadastro automático de candidato no registro; criação de usuários de teste; elaboração da documentação ABNT; ajustes finais e apresentação. |

---

## 9. CONSIDERAÇÕES FINAIS

O projeto **Agência de Empregos** atingiu todos os objetivos propostos, entregando um sistema web completo, funcional e acessível publicamente. A solução demonstra domínio sobre o ciclo completo de desenvolvimento de software: da modelagem do banco de dados à implantação em infraestrutura de nuvem.

Entre os principais aprendizados técnicos obtidos durante o desenvolvimento, destacam-se:

- Construção de APIs REST com autenticação JWT e controle de acesso por perfis;
- Gerenciamento de banco de dados relacional com ORM e migrações controladas;
- Resolução de desafios de infraestrutura (comunicação HTTPS/HTTP entre Streamlit Cloud e EC2 via Cloudflare Tunnel);
- Gerenciamento de processos em servidor Linux (nohup, background processes);
- Versionamento colaborativo com Git e GitHub;
- Desenvolvimento de interfaces web interativas com Streamlit.

O sistema encontra-se em plena operação com dados reais de teste, incluindo empresas, vagas com benefícios e requisitos, candidatos e candidaturas, podendo ser demonstrado ao vivo durante a apresentação no endereço **https://projeto-integrador-senac.streamlit.app**.

---

## 10. REFERÊNCIAS

ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. **NBR 6023**: Informação e documentação — Referências — Elaboração. Rio de Janeiro: ABNT, 2018.

ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. **NBR 14724**: Informação e documentação — Trabalhos acadêmicos — Apresentação. Rio de Janeiro: ABNT, 2011.

AWS. **Amazon EC2 Documentation**. Disponível em: https://docs.aws.amazon.com/ec2/. Acesso em: jul. 2026.

CLOUDFLARE. **Cloudflare Tunnel Documentation**. Disponível em: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/. Acesso em: jul. 2026.

CORONEL, C.; MORRIS, S.; ROB, P. **Sistemas de banco de dados**. São Paulo: Cengage Learning, 2011.

DATE, C. J. **Introdução a sistemas de bancos de dados**. 8. ed. Rio de Janeiro: Elsevier, 2004.

FASTAPI. **FastAPI Documentation**. Disponível em: https://fastapi.tiangolo.com/. Acesso em: jul. 2026.

GRINBERG, M. **Flask Web Development**: developing web applications with Python. 2. ed. Sebastopol: O'Reilly Media, 2018.

McKINNEY, W. **Python para análise de dados**. São Paulo: Novatec, 2019.

PYTHON SOFTWARE FOUNDATION. **Python 3 Documentation**. Disponível em: https://docs.python.org/3/. Acesso em: jul. 2026.

RAMAKRISHNAN, R.; GEHRKE, J. **Sistemas de gerenciamento de banco de dados**. 3. ed. Porto Alegre: McGraw-Hill, 2008.

SQLALCHEMY. **SQLAlchemy Documentation**. Disponível em: https://docs.sqlalchemy.org/. Acesso em: jul. 2026.

STREAMLIT. **Streamlit Documentation**. Disponível em: https://docs.streamlit.io/. Acesso em: jul. 2026.

---

*Documento elaborado em conformidade com as normas ABNT NBR 14724:2011 e NBR 6023:2018.*

*São Paulo, julho de 2026.*

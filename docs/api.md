# 📡 Documentação da API

Base URL de produção: `https://api.alvesmotionlab.com.br`  
Documentação interativa (Swagger): `https://api.alvesmotionlab.com.br/docs`

---

## Autenticação

Todos os endpoints marcados com 🔒 exigem o header:

```
Authorization: Bearer <token>
```

O token é obtido no endpoint `POST /auth/login`.

### Perfis de acesso

| Perfil | Permissões |
|---|---|
| `admin` | Acesso total — gerencia usuários, empresas, vagas, candidatos |
| `recrutador` | Cria e edita vagas, atribui recrutadores, atualiza status de candidaturas |
| `visualizador` | Lê vagas, cria candidaturas próprias, edita perfil de candidato |

---

## Auth

### `POST /auth/registro`
Cria uma conta de candidato (perfil `visualizador`) e retorna o token JWT.

**Body:**
```json
{
  "nome": "João Silva",
  "email": "joao@email.com",
  "senha": "minimo6chars"
}
```

**Resposta 200:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "usuario": { "id": 1, "nome": "João Silva", "email": "joao@email.com", "perfil": "visualizador" }
}
```

---

### `POST /auth/login`
Login com email e senha (form-urlencoded).

**Body (form):** `username=joao@email.com&password=senha`

**Resposta 200:** igual ao registro.

---

### `GET /auth/me` 🔒
Retorna os dados do usuário autenticado.

---

### `GET /auth/usuarios` 🔒 (admin)
Lista todos os usuários do sistema.

---

### `POST /auth/usuarios` 🔒 (admin)
Cria um usuário com qualquer perfil.

**Body:**
```json
{
  "nome": "Maria Recrutadora",
  "email": "maria@empresa.com",
  "senha": "senha123",
  "perfil": "recrutador"
}
```

---

### `DELETE /auth/usuarios/{id}` 🔒 (admin)
Exclui um usuário. Não é possível excluir a si mesmo nem o último admin.

---

### `GET /auth/recrutadores` 🔒
Lista usuários com perfil `admin` ou `recrutador`. Acessível a qualquer usuário autenticado — usado nos formulários de seleção de responsável.

---

## Vagas

### `GET /vagas/` 🔒
Lista vagas com filtros opcionais via query params.

| Parâmetro | Tipo | Valores |
|---|---|---|
| `modalidade` | string | `presencial`, `remoto`, `hibrido` |
| `tipo_contrato` | string | `CLT`, `PJ`, `temporario`, `estagio` |
| `vaga_pcd` | bool | `true`, `false` |
| `status` | string | `aberta`, `encerrada` |
| `recrutador_id` | int | ID do usuário recrutador |

**Resposta:** array de `VagaResponse`.

---

### `POST /vagas/` 🔒 (recrutador+)
Cria uma nova vaga com benefícios e requisitos.

**Body:**
```json
{
  "titulo": "Desenvolvedor Backend",
  "local": "São Paulo, SP",
  "descricao": "Responsável pelo desenvolvimento da API...",
  "salario": 12000.00,
  "modalidade": "remoto",
  "tipo_contrato": "CLT",
  "publico_alvo": "ambos",
  "vaga_pcd": false,
  "status": "aberta",
  "quantidade_vagas": 2,
  "empresa_id": 1,
  "recrutador_id": 3,
  "beneficios_nomes": ["Vale Refeição", "Plano de Saúde", "Home Office"],
  "requisitos_lista": [
    { "descricao": "Python", "nivel": "obrigatorio" },
    { "descricao": "Docker", "nivel": "desejavel" }
  ]
}
```

---

### `GET /vagas/{id}` 🔒
Retorna detalhes completos de uma vaga, incluindo empresa, recrutador, benefícios e requisitos.

**Resposta `VagaResponse`:**
```json
{
  "id": 1,
  "titulo": "Desenvolvedor Backend",
  "empresa": { "id": 1, "nome": "Nubank", ... },
  "recrutador": { "id": 3, "nome": "Maria", "email": "maria@nubank.com" },
  "beneficios": [{ "id": 1, "nome": "Vale Refeição" }],
  "requisitos": [{ "id": 1, "descricao": "Python", "nivel": "obrigatorio" }],
  ...
}
```

---

### `PUT /vagas/{id}` 🔒 (recrutador+)
Atualiza todos os campos da vaga. Ao mudar o status para `encerrada`, `data_fechamento` é preenchido automaticamente se não fornecido.

---

### `PATCH /vagas/{id}/recrutador` 🔒 (recrutador+)
Atribui ou reatribui o recrutador responsável pela vaga.

**Body:**
```json
{ "recrutador_id": 3 }
```

Para remover o responsável: `{ "recrutador_id": null }`

Retorna erro 400 se o usuário não tiver perfil `admin` ou `recrutador`.

---

### `DELETE /vagas/{id}` 🔒 (recrutador+)
Exclui uma vaga. Retorna 204 sem corpo.

---

## Empresas

### `GET /empresas/` 🔒
Lista todas as empresas.

### `POST /empresas/` 🔒 (admin)
Cria uma empresa.

**Body:**
```json
{
  "nome": "Google Brasil",
  "cnpj": "06.990.590/0001-23",
  "setor": "Tecnologia",
  "cidade": "São Paulo",
  "estado": "SP",
  "descricao": "Subsidiária brasileira do Google."
}
```

### `GET /empresas/{id}` 🔒
### `PUT /empresas/{id}` 🔒 (admin)
### `DELETE /empresas/{id}` 🔒 (admin)

---

## Candidatos

### `GET /candidatos/` 🔒
Lista candidatos. Recrutadores e admins têm acesso completo.

### `POST /candidatos/` 🔒
Cria perfil de candidato vinculado ao usuário logado.

**Body:**
```json
{
  "nome": "Ana Lima",
  "email": "ana@email.com",
  "telefone": "11912340001",
  "cidade": "São Paulo",
  "estado": "SP",
  "data_nascimento": "1995-03-15"
}
```

### `GET /candidatos/{id}` 🔒
### `PUT /candidatos/{id}` 🔒
### `DELETE /candidatos/{id}` 🔒 (admin)

---

## Candidaturas

### `GET /candidaturas/` 🔒
Lista candidaturas com filtros opcionais.

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `vaga_id` | int | Filtra por vaga |
| `candidato_id` | int | Filtra por candidato |

### `POST /candidaturas/` 🔒
Inscreve um candidato em uma vaga.

**Body:**
```json
{
  "candidato_id": 5,
  "vaga_id": 2
}
```

Status inicial: `pendente`.

### `PUT /candidaturas/{id}/status` 🔒 (recrutador+)
Atualiza o status de uma candidatura.

**Body:**
```json
{ "status": "em_analise" }
```

**Valores válidos:** `pendente`, `em_analise`, `aprovado`, `reprovado`

---

## Enums

### Modalidade (`modalidade`)
`presencial` · `remoto` · `hibrido`

### Tipo de contrato (`tipo_contrato`)
`CLT` · `PJ` · `temporario` · `estagio`

### Público-alvo (`publico_alvo`)
`ambos` · `masculino` · `feminino`

### Status da vaga (`status`)
`aberta` · `encerrada`

### Nível do requisito (`nivel`)
`obrigatorio` · `desejavel`

### Status da candidatura
`pendente` · `em_analise` · `aprovado` · `reprovado`

### Perfil do usuário (`perfil`)
`admin` · `recrutador` · `visualizador`

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
| `recrutador` | Cria e edita vagas, atribui recrutadores, atualiza status de candidaturas, baixa currículos |
| `visualizador` | Lê vagas, cria candidaturas próprias, edita perfil e envia currículo |

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
  "beneficios_nomes": ["Vale Refeição", "Plano de Saúde"],
  "requisitos_lista": [
    { "descricao": "Python", "nivel": "obrigatorio" },
    { "descricao": "Docker", "nivel": "desejavel" }
  ]
}
```

---

### `GET /vagas/{id}` 🔒
Retorna detalhes completos de uma vaga, incluindo empresa, recrutador, benefícios e requisitos.

---

### `PUT /vagas/{id}` 🔒 (recrutador+)
Atualiza todos os campos da vaga. Ao mudar o status para `encerrada`, `data_fechamento` é preenchido automaticamente se não fornecido.

---

### `PATCH /vagas/{id}/recrutador` 🔒 (recrutador+)
Atribui ou reatribui o recrutador responsável pela vaga.

**Body:** `{ "recrutador_id": 3 }` — use `null` para remover o responsável.

Retorna erro 400 se o usuário indicado não tiver perfil `admin` ou `recrutador`.

---

### `DELETE /vagas/{id}` 🔒 (recrutador+)
Exclui uma vaga. Retorna 204 sem corpo.

---

## Empresas

### `GET /empresas/` 🔒
Lista todas as empresas.

### `POST /empresas/` 🔒 (admin)
Cria uma empresa. O campo `cnpj` é opcional.

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
Lista candidatos.

### `POST /candidatos/` 🔒
Cria perfil de candidato.

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

### `POST /candidatos/{id}/curriculo` 🔒
Upload do currículo do candidato. Substitui o arquivo anterior automaticamente.

**Content-Type:** `multipart/form-data` — campo `file` (PDF, DOCX ou DOC).

**Resposta 200:** `CandidatoResponse` com `curriculo_path` preenchido.

---

### `GET /candidatos/{id}/curriculo` 🔒
Download do currículo do candidato.

**Resposta:** arquivo binário com `Content-Disposition: attachment`.

---

## Candidaturas

### `GET /candidaturas/` 🔒
Lista candidaturas. Filtros: `vaga_id`, `candidato_id`.

### `POST /candidaturas/` 🔒
Inscreve um candidato em uma vaga. Status inicial: `pendente`.

**Body:** `{ "candidato_id": 5, "vaga_id": 2 }`

### `PUT /candidaturas/{id}/status` 🔒 (recrutador+)
Atualiza o status. **Valores:** `pendente` · `em_analise` · `aprovado` · `reprovado`

**Body:** `{ "status": "em_analise" }`

---

## Enums

| Enum | Valores |
|---|---|
| `modalidade` | `presencial` · `remoto` · `hibrido` |
| `tipo_contrato` | `CLT` · `PJ` · `temporario` · `estagio` |
| `publico_alvo` | `ambos` · `masculino` · `feminino` |
| `status` (vaga) | `aberta` · `encerrada` |
| `nivel` (requisito) | `obrigatorio` · `desejavel` |
| `status` (candidatura) | `pendente` · `em_analise` · `aprovado` · `reprovado` |
| `perfil` | `admin` · `recrutador` · `visualizador` |

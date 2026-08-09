"""
Cria usuários candidatos de teste via API.
Execute: python seed_candidatos.py
"""
import requests

API = "http://localhost:8000"

candidatos = [
    {"nome": "Ana Lima",        "email": "ana.lima@email.com",        "telefone": "(81) 99999-1111", "cidade": "Recife",          "estado": "PE"},
    {"nome": "Carlos Souza",    "email": "carlos.souza@email.com",    "telefone": "(11) 99999-2222", "cidade": "São Paulo",        "estado": "SP"},
    {"nome": "Beatriz Santos",  "email": "beatriz.santos@email.com",  "telefone": "(31) 99999-3333", "cidade": "Belo Horizonte",   "estado": "MG"},
    {"nome": "Lucas Ferreira",  "email": "lucas.ferreira@email.com",  "telefone": "(21) 98888-4444", "cidade": "Rio de Janeiro",   "estado": "RJ"},
    {"nome": "Mariana Costa",   "email": "mariana.costa@email.com",   "telefone": "(41) 97777-5555", "cidade": "Curitiba",         "estado": "PR"},
    {"nome": "Rafael Oliveira", "email": "rafael.oliveira@email.com", "telefone": "(71) 96666-6666", "cidade": "Salvador",         "estado": "BA"},
    {"nome": "Juliana Pereira", "email": "juliana.pereira@email.com", "telefone": "(51) 95555-7777", "cidade": "Porto Alegre",     "estado": "RS"},
    {"nome": "Diego Almeida",   "email": "diego.almeida@email.com",   "telefone": "(62) 94444-8888", "cidade": "Goiânia",          "estado": "GO"},
]

import os, secrets
SENHA_PADRAO = os.getenv("SEED_SENHA_PADRAO") or secrets.token_urlsafe(12)

for c in candidatos:
    # Registra via /auth/registro (já cria usuario + candidato automaticamente)
    r = requests.post(f"{API}/auth/registro", json={
        "nome": c["nome"],
        "email": c["email"],
        "senha": SENHA_PADRAO,
    })
    if r.status_code == 200:
        token = r.json()["access_token"]
        # Busca o candidato recém-criado para atualizar telefone/cidade/estado
        candidatos_list = requests.get(f"{API}/candidatos/", headers={"Authorization": f"Bearer {token}"}).json()
        cand_id = next((x["id"] for x in candidatos_list if x["email"] == c["email"]), None)
        if cand_id:
            requests.put(f"{API}/candidatos/{cand_id}", json={
                "nome": c["nome"],
                "email": c["email"],
                "telefone": c["telefone"],
                "cidade": c["cidade"],
                "estado": c["estado"],
                "data_nascimento": None,
            }, headers={"Authorization": f"Bearer {token}"})
        print(f"✅ {c['nome']} ({c['email']})")
    elif r.status_code == 400 and "já cadastrado" in r.text:
        print(f"⏭  {c['nome']} já existe, pulando")
    else:
        print(f"❌ {c['nome']}: {r.status_code} {r.text}")

print(f"\nSenha usada neste seed: {SENHA_PADRAO}")

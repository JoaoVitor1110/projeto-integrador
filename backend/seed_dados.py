"""
Seed de dados fictícios para o dashboard da Agência de Empregos.
Popula: empresas, usuários/candidatos, vagas, candidaturas.
"""
import requests
import os
import sys
import json
import random

API = os.getenv("SEED_API_URL", "http://localhost:8000")
ADMIN_EMAIL = os.getenv("SEED_ADMIN_EMAIL")
ADMIN_SENHA = os.getenv("SEED_ADMIN_SENHA")

if not ADMIN_EMAIL or not ADMIN_SENHA:
    print("Erro: defina SEED_ADMIN_EMAIL e SEED_ADMIN_SENHA antes de rodar o seed.")
    sys.exit(1)

def login_admin():
    r = requests.post(f"{API}/auth/login", data={"username": ADMIN_EMAIL, "password": ADMIN_SENHA})
    r.raise_for_status()
    return r.json()["access_token"]

def h(token):
    return {"Authorization": f"Bearer {token}"}

# ─── EMPRESAS ───────────────────────────────────────────────────────────────
EMPRESAS = [
    {"nome": "Google Brasil", "cnpj": "06.990.590/0001-23", "setor": "Tecnologia", "cidade": "São Paulo", "estado": "SP"},
    {"nome": "Nubank", "cnpj": "18.236.120/0001-58", "setor": "Fintech", "cidade": "São Paulo", "estado": "SP"},
    {"nome": "Magazine Luiza", "cnpj": "47.960.950/0001-21", "setor": "Varejo", "cidade": "Franca", "estado": "SP"},
    {"nome": "Ambev", "cnpj": "07.526.557/0001-00", "setor": "Bebidas / FMCG", "cidade": "São Paulo", "estado": "SP"},
    {"nome": "Hospital Albert Einstein", "cnpj": "60.765.823/0001-30", "setor": "Saúde", "cidade": "São Paulo", "estado": "SP"},
    {"nome": "Itaú Unibanco", "cnpj": "60.872.504/0001-23", "setor": "Financeiro", "cidade": "São Paulo", "estado": "SP"},
    {"nome": "iFood", "cnpj": "14.380.200/0001-21", "setor": "Tecnologia / Delivery", "cidade": "Osasco", "estado": "SP"},
    {"nome": "Embraer", "cnpj": "07.689.002/0001-89", "setor": "Aeronáutica", "cidade": "São José dos Campos", "estado": "SP"},
    {"nome": "Natura &Co", "cnpj": "71.673.990/0001-77", "setor": "Cosméticos", "cidade": "São Paulo", "estado": "SP"},
    {"nome": "XP Inc.", "cnpj": "02.332.886/0001-04", "setor": "Financeiro / Investimentos", "cidade": "São Paulo", "estado": "SP"},
]

# ─── CANDIDATOS ─────────────────────────────────────────────────────────────
CANDIDATOS = [
    ("Ana Lima", "ana.lima@email.com", "11912340001", "São Paulo", "SP"),
    ("Carlos Souza", "carlos.souza@email.com", "11912340002", "Campinas", "SP"),
    ("Beatriz Santos", "beatriz.santos@email.com", "11912340003", "Rio de Janeiro", "RJ"),
    ("Lucas Ferreira", "lucas.ferreira@email.com", "11912340004", "Belo Horizonte", "MG"),
    ("Mariana Costa", "mariana.costa@email.com", "11912340005", "São Paulo", "SP"),
    ("Rafael Oliveira", "rafael.oliveira@email.com", "11912340006", "Curitiba", "PR"),
    ("Juliana Pereira", "juliana.pereira@email.com", "11912340007", "São Paulo", "SP"),
    ("Diego Almeida", "diego.almeida@email.com", "11912340008", "Porto Alegre", "RS"),
    ("Fernanda Rocha", "fernanda.rocha@email.com", "11912340009", "São Paulo", "SP"),
    ("Pedro Martins", "pedro.martins@email.com", "11912340010", "Fortaleza", "CE"),
    ("Isabela Nunes", "isabela.nunes@email.com", "11912340011", "Recife", "PE"),
    ("Thiago Barbosa", "thiago.barbosa@email.com", "11912340012", "São Paulo", "SP"),
    ("Camila Dias", "camila.dias@email.com", "11912340013", "São Paulo", "SP"),
    ("Bruno Carvalho", "bruno.carvalho@email.com", "11912340014", "Salvador", "BA"),
    ("Leticia Moura", "leticia.moura@email.com", "11912340015", "Manaus", "AM"),
    ("Rodrigo Teixeira", "rodrigo.teixeira@email.com", "11912340016", "São Paulo", "SP"),
    ("Amanda Lopes", "amanda.lopes@email.com", "11912340017", "São Paulo", "SP"),
    ("Felipe Nascimento", "felipe.nascimento@email.com", "11912340018", "Brasília", "DF"),
    ("Vanessa Ribeiro", "vanessa.ribeiro@email.com", "11912340019", "São Paulo", "SP"),
    ("Gabriel Silva", "gabriel.silva@email.com", "11912340020", "Campinas", "SP"),
]

# ─── VAGAS ──────────────────────────────────────────────────────────────────
# (titulo, empresa_idx, modalidade, contrato, salario, pcd, status, data_abertura, beneficios, requisitos)
VAGAS = [
    # TECH - Google
    ("Engenheiro de Software Sênior", 0, "remoto", "PJ", 22000, False, "aberta", "2026-01-10",
     ["Vale Refeição", "Plano de Saúde", "Stock Options", "Home Office"],
     [("Python", "obrigatorio"), ("Cloud GCP", "obrigatorio"), ("Kubernetes", "desejavel")]),

    ("Data Scientist", 0, "hibrido", "CLT", 18000, False, "aberta", "2026-02-05",
     ["Vale Refeição", "Plano de Saúde", "Gympass"],
     [("Machine Learning", "obrigatorio"), ("Python", "obrigatorio"), ("BigQuery", "desejavel")]),

    ("UX Designer", 0, "remoto", "CLT", 12000, False, "aberta", "2026-03-01",
     ["Vale Refeição", "Plano de Saúde"],
     [("Figma", "obrigatorio"), ("Pesquisa de Usuário", "obrigatorio")]),

    # FINTECH - Nubank
    ("Engenheiro de Backend", 1, "remoto", "CLT", 20000, False, "aberta", "2025-11-15",
     ["Vale Refeição", "Plano de Saúde", "Stock Options"],
     [("Clojure", "obrigatorio"), ("Kafka", "desejavel"), ("PostgreSQL", "obrigatorio")]),

    ("Analista de Risco de Crédito", 1, "hibrido", "CLT", 9000, False, "aberta", "2026-01-20",
     ["Vale Refeição", "Plano de Saúde", "PLR"],
     [("SQL", "obrigatorio"), ("Estatística", "obrigatorio"), ("Python", "desejavel")]),

    ("Product Manager", 1, "remoto", "CLT", 25000, False, "encerrada", "2025-10-01",
     ["Vale Refeição", "Plano de Saúde", "Stock Options"],
     [("Gestão de Produto", "obrigatorio"), ("Inglês Fluente", "obrigatorio")]),

    # VAREJO - Magalu
    ("Desenvolvedor Full Stack", 2, "presencial", "CLT", 11000, False, "aberta", "2026-02-15",
     ["Vale Refeição", "Vale Transporte", "Plano de Saúde"],
     [("React", "obrigatorio"), ("Node.js", "obrigatorio"), ("MySQL", "desejavel")]),

    ("Analista de E-commerce", 2, "presencial", "CLT", 6500, False, "aberta", "2026-03-10",
     ["Vale Refeição", "Vale Transporte"],
     [("Google Analytics", "obrigatorio"), ("SEO", "obrigatorio"), ("Excel Avançado", "desejavel")]),

    ("Assistente Logístico PcD", 2, "presencial", "CLT", 2800, True, "aberta", "2026-03-20",
     ["Vale Refeição", "Vale Transporte", "Plano de Saúde"],
     [("Ensino Médio Completo", "obrigatorio")]),

    # FMCG - Ambev
    ("Analista de Marketing Digital", 3, "hibrido", "CLT", 8000, False, "aberta", "2026-01-05",
     ["Vale Refeição", "PLR", "Plano de Saúde", "Gympass"],
     [("Google Ads", "obrigatorio"), ("Meta Ads", "obrigatorio"), ("Inglês Intermediário", "desejavel")]),

    ("Gerente de Trade Marketing", 3, "presencial", "CLT", 15000, False, "aberta", "2025-12-01",
     ["Carro Empresa", "Plano de Saúde", "PLR"],
     [("Gestão de Equipes", "obrigatorio"), ("Excel Avançado", "obrigatorio"), ("MBA", "desejavel")]),

    # SAÚDE - Einstein
    ("Enfermeiro(a) UTI", 4, "presencial", "CLT", 7500, False, "aberta", "2026-02-01",
     ["Plano de Saúde", "Vale Refeição", "Plantão Noturno Premium"],
     [("COREN Ativo", "obrigatorio"), ("Experiência em UTI", "obrigatorio")]),

    ("Analista de TI Hospitalar", 4, "presencial", "CLT", 9000, False, "aberta", "2026-03-05",
     ["Plano de Saúde", "Vale Refeição", "Vale Transporte"],
     [("Suporte a Sistemas Hospitalares", "obrigatorio"), ("ITIL", "desejavel")]),

    ("Auxiliar Administrativo PcD", 4, "presencial", "CLT", 2500, True, "aberta", "2026-03-15",
     ["Plano de Saúde", "Vale Refeição", "Vale Transporte"],
     [("Ensino Médio Completo", "obrigatorio"), ("Pacote Office", "obrigatorio")]),

    # FINANCEIRO - Itaú
    ("Analista de Dados Financeiros", 5, "hibrido", "CLT", 13000, False, "aberta", "2026-01-15",
     ["Vale Refeição", "Plano de Saúde", "PLR", "Previdência Privada"],
     [("SQL", "obrigatorio"), ("Power BI", "obrigatorio"), ("Python", "desejavel")]),

    ("Especialista em Cybersegurança", 5, "hibrido", "CLT", 19000, False, "aberta", "2026-02-20",
     ["Vale Refeição", "Plano de Saúde", "PLR"],
     [("CISSP", "desejavel"), ("Segurança de Redes", "obrigatorio"), ("Inglês Avançado", "obrigatorio")]),

    ("Gerente de Relacionamento PJ", 5, "presencial", "CLT", 11000, False, "encerrada", "2025-09-01",
     ["Vale Refeição", "Plano de Saúde", "PLR", "Carro Empresa"],
     [("Experiência Bancária", "obrigatorio"), ("CPA-10", "obrigatorio")]),

    # TECH/DELIVERY - iFood
    ("Engenheiro de Machine Learning", 6, "remoto", "CLT", 21000, False, "aberta", "2026-02-10",
     ["Vale Refeição", "Plano de Saúde", "Stock Options", "Home Office"],
     [("Python", "obrigatorio"), ("MLOps", "obrigatorio"), ("TensorFlow", "desejavel")]),

    ("Analista de Growth", 6, "hibrido", "CLT", 9500, False, "aberta", "2026-03-01",
     ["Vale Refeição", "Plano de Saúde", "Gympass"],
     [("Growth Hacking", "obrigatorio"), ("SQL", "obrigatorio"), ("A/B Testing", "desejavel")]),

    # AERONÁUTICA - Embraer
    ("Engenheiro Aeronáutico", 7, "presencial", "CLT", 16000, False, "aberta", "2026-01-25",
     ["Vale Refeição", "Plano de Saúde", "PLR", "Previdência Privada"],
     [("Engenharia Aeronáutica", "obrigatorio"), ("CATIA V5", "obrigatorio"), ("Inglês Avançado", "obrigatorio")]),

    ("Técnico de Manutenção Aeronáutica", 7, "presencial", "CLT", 8500, False, "aberta", "2026-02-28",
     ["Vale Refeição", "Vale Transporte", "Plano de Saúde"],
     [("Licença ANAC", "obrigatorio"), ("Aviónica", "desejavel")]),

    # COSMÉTICOS - Natura
    ("Analista de Sustentabilidade", 8, "hibrido", "CLT", 8000, False, "aberta", "2026-03-10",
     ["Vale Refeição", "Plano de Saúde", "PLR"],
     [("ESG", "obrigatorio"), ("Inglês Intermediário", "desejavel"), ("Ciências Ambientais", "desejavel")]),

    ("Designer de Embalagens", 8, "hibrido", "CLT", 7000, False, "aberta", "2026-02-15",
     ["Vale Refeição", "Plano de Saúde"],
     [("Adobe Illustrator", "obrigatorio"), ("Packaging Design", "obrigatorio")]),

    # INVESTIMENTOS - XP Inc.
    ("Assessor de Investimentos", 9, "presencial", "CLT", 5000, False, "aberta", "2026-01-10",
     ["Comissão", "Plano de Saúde", "PLR"],
     [("CPA-20", "obrigatorio"), ("CFP", "desejavel"), ("Experiência com Renda Variável", "desejavel")]),

    ("Desenvolvedor Quant", 9, "remoto", "PJ", 25000, False, "aberta", "2026-02-01",
     ["Home Office", "Equipamento fornecido"],
     [("Python", "obrigatorio"), ("Matemática Financeira", "obrigatorio"), ("C++", "desejavel")]),
]

# ─── DISTRIBUIÇÃO DE CANDIDATURAS ───────────────────────────────────────────
# (vaga_idx, candidato_indices, status_list)
CANDIDATURAS = [
    # Vagas tech com muitos candidatos (alta demanda)
    (0,  [0,1,2,4,6,8,11,12,16,18,19], ["em_analise","em_analise","aprovado","reprovado","em_analise","em_analise","aprovado","reprovado","em_analise","em_analise","em_analise"]),
    (1,  [0,2,4,8,12,16,18,19],         ["em_analise","aprovado","em_analise","reprovado","em_analise","em_analise","aprovado","em_analise"]),
    (3,  [1,4,6,11,16,19],              ["em_analise","aprovado","em_analise","em_analise","reprovado","em_analise"]),
    (6,  [0,2,4,8,12,16],              ["em_analise","em_analise","aprovado","reprovado","em_analise","em_analise"]),
    (17, [0,4,8,12,16,18,19],          ["em_analise","aprovado","em_analise","em_analise","reprovado","em_analise","em_analise"]),
    (24, [1,4,6,11,16,19],             ["em_analise","aprovado","em_analise","em_analise","reprovado","em_analise"]),

    # Vagas financeiras com candidatos médios
    (4,  [0,2,8,12,16],               ["em_analise","aprovado","reprovado","em_analise","em_analise"]),
    (14, [0,2,4,8,16],                ["aprovado","em_analise","em_analise","reprovado","em_analise"]),
    (15, [1,6,11,18],                 ["em_analise","em_analise","aprovado","reprovado"]),
    (23, [0,2,4,8,12],               ["em_analise","em_analise","aprovado","em_analise","reprovado"]),

    # Vagas de saúde
    (11, [3,7,9,13,14],              ["em_analise","aprovado","em_analise","em_analise","reprovado"]),
    (12, [0,2,8,16],                 ["em_analise","aprovado","reprovado","em_analise"]),

    # Vagas PcD (foco)
    (8,  [3,7,9,13,14],              ["em_analise","aprovado","em_analise","reprovado","em_analise"]),
    (13, [3,9,14],                   ["aprovado","em_analise","reprovado"]),

    # Marketing e crescimento
    (9,  [2,4,6,12,16,18],          ["em_analise","aprovado","reprovado","em_analise","em_analise","em_analise"]),
    (18, [4,6,12,16],               ["em_analise","aprovado","em_analise","reprovado"]),

    # Vagas presenciais fora SP
    (19, [5,7,10,17],               ["em_analise","aprovado","em_analise","reprovado"]),
    (20, [3,5,7,10],                ["em_analise","em_analise","aprovado","reprovado"]),

    # Vagas remotas PJ (alta remuneração)
    (2,  [0,4,6,8,12,16,18],        ["em_analise","aprovado","em_analise","em_analise","reprovado","em_analise","aprovado"]),
    (21, [8,11,16,18],              ["em_analise","aprovado","reprovado","em_analise"]),
]


def main():
    print("🔐 Fazendo login como admin...")
    token = login_admin()
    print("✅ Login OK\n")

    # 1. Criar empresas
    print("🏢 Criando empresas...")
    empresa_ids = []
    for e in EMPRESAS:
        r = requests.post(f"{API}/empresas/", json=e, headers=h(token))
        if r.status_code in (200, 201):
            eid = r.json()["id"]
            empresa_ids.append(eid)
            print(f"  ✅ {e['nome']} (id={eid})")
        else:
            print(f"  ❌ {e['nome']}: {r.status_code} {r.text}")
            empresa_ids.append(None)

    # 2. Criar candidatos (registro → pega candidato_id)
    import os, secrets as _sec
    SENHA_CAND = os.getenv("SEED_SENHA_PADRAO") or _sec.token_urlsafe(12)
    print(f"\n👤 Criando candidatos (senha: {SENHA_CAND})...")
    candidato_ids = []
    for nome, email, tel, cidade, estado in CANDIDATOS:
        # registrar usuário
        r = requests.post(f"{API}/auth/registro", json={
            "nome": nome, "email": email, "senha": SENHA_CAND,
            "telefone": tel, "cidade": cidade, "estado": estado
        })
        if r.status_code in (200, 201):
            print(f"  ✅ {nome}")
        elif r.status_code == 400 and "já cadastrado" in r.text:
            print(f"  ⚠️  {nome} já existe")
        else:
            print(f"  ❌ {nome}: {r.status_code} {r.text}")

        # buscar candidato pelo email
        rc = requests.get(f"{API}/candidatos/", headers=h(token))
        cands = rc.json()
        cid = next((c["id"] for c in cands if c["email"] == email), None)
        candidato_ids.append(cid)

    # 3. Criar vagas
    print("\n💼 Criando vagas...")
    vaga_ids = []
    for v in VAGAS:
        titulo, emp_idx, modalidade, contrato, salario, pcd, status, data_ab, beneficios, requisitos = v
        eid = empresa_ids[emp_idx] if emp_idx < len(empresa_ids) else None
        if not eid:
            vaga_ids.append(None)
            continue

        payload = {
            "titulo": titulo,
            "empresa_id": eid,
            "modalidade": modalidade,
            "tipo_contrato": contrato,
            "salario": salario,
            "pcd": pcd,
            "status": status,
            "data_abertura": data_ab,
            "descricao": f"Vaga de {titulo} em empresa de referência no setor. Ambiente dinâmico e oportunidades de crescimento.",
            "local": "São Paulo, SP",
            "cidade": "São Paulo",
            "estado": "SP",
            "publico_alvo": "ambos",
            "beneficios": [{"descricao": b} for b in beneficios],
            "requisitos": [{"descricao": desc, "nivel": nivel} for desc, nivel in requisitos],
        }
        r = requests.post(f"{API}/vagas/", json=payload, headers=h(token))
        if r.status_code in (200, 201):
            vid = r.json()["id"]
            vaga_ids.append(vid)
            print(f"  ✅ {titulo} (id={vid})")
        else:
            print(f"  ❌ {titulo}: {r.status_code} {r.text}")
            vaga_ids.append(None)

    # 4. Criar candidaturas
    print("\n📋 Criando candidaturas...")
    total = 0
    for vaga_idx, cand_indices, statuses in CANDIDATURAS:
        vid = vaga_ids[vaga_idx] if vaga_idx < len(vaga_ids) else None
        if not vid:
            continue
        for i, cand_idx in enumerate(cand_indices):
            cid = candidato_ids[cand_idx] if cand_idx < len(candidato_ids) else None
            if not cid:
                continue
            status = statuses[i] if i < len(statuses) else "em_analise"
            r = requests.post(f"{API}/candidaturas/", json={
                "candidato_id": cid,
                "vaga_id": vid,
                "status": status
            }, headers=h(token))
            if r.status_code in (200, 201):
                total += 1
            # ignora duplicatas silenciosamente

    print(f"  ✅ {total} candidaturas criadas")

    print("\n🎉 Seed concluído!")
    print(f"   Empresas: {len([x for x in empresa_ids if x])}")
    print(f"   Candidatos: {len([x for x in candidato_ids if x])}")
    print(f"   Vagas: {len([x for x in vaga_ids if x])}")
    print(f"   Candidaturas: {total}")

if __name__ == "__main__":
    main()

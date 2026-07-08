import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine, SessionLocal
from app import models  # noqa: F401 - registers models
from app.routers import empresas, vagas, candidatos, candidaturas
from app.routers import auth as auth_router
from app.auth import hash_senha

Base.metadata.create_all(bind=engine)

def _seed_admin():
    db = SessionLocal()
    try:
        if db.query(models.Usuario).count() == 0:
            admin_email = os.getenv("ADMIN_EMAIL")
            admin_senha = os.getenv("ADMIN_SENHA")
            admin_nome = os.getenv("ADMIN_NOME", "Admin")
            if not admin_email or not admin_senha:
                return  # skip seed if credentials not configured
            db.add(models.Usuario(
                nome=admin_nome,
                email=admin_email,
                senha_hash=hash_senha(admin_senha),
                perfil=models.PerfilEnum.admin,
            ))
            db.commit()
    finally:
        db.close()

_seed_admin()


def _seed_dados():
    db = SessionLocal()
    try:
        if db.query(models.Empresa).count() > 0:
            return  # já tem dados

        EMPRESAS = [
            ("Google Brasil",          "06.990.590/0001-23", "Tecnologia",               "São Paulo", "SP"),
            ("Nubank",                 "18.236.120/0001-58", "Fintech",                   "São Paulo", "SP"),
            ("Magazine Luiza",         "47.960.950/0001-21", "Varejo",                    "Franca",    "SP"),
            ("Ambev",                  "07.526.557/0001-00", "Bebidas / FMCG",            "São Paulo", "SP"),
            ("Hospital Albert Einstein","60.765.823/0001-30","Saúde",                     "São Paulo", "SP"),
            ("Itaú Unibanco",          "60.872.504/0001-23", "Financeiro",                "São Paulo", "SP"),
            ("iFood",                  "14.380.200/0001-21", "Tecnologia / Delivery",     "Osasco",    "SP"),
            ("Embraer",                "07.689.002/0001-89", "Aeronáutica",               "São José dos Campos", "SP"),
            ("Natura &Co",             "71.673.990/0001-77", "Cosméticos",                "São Paulo", "SP"),
            ("XP Inc.",                "02.332.886/0001-04", "Financeiro / Investimentos","São Paulo", "SP"),
        ]
        emp_map = {}
        for nome, cnpj, setor, cidade, estado in EMPRESAS:
            e = models.Empresa(nome=nome, cnpj=cnpj, setor=setor, cidade=cidade, estado=estado)
            db.add(e)
            db.flush()
            emp_map[nome] = e.id

        from datetime import date as _date
        VAGAS = [
            ("Engenheiro de Software Sênior", "Google Brasil",   "remoto",     "PJ",        22000, False, "aberta",   "2026-01-10",
             ["Vale Refeição","Plano de Saúde","Stock Options","Home Office"],
             [("Python","obrigatorio"),("Cloud GCP","obrigatorio"),("Kubernetes","desejavel")]),
            ("Data Scientist",                "Google Brasil",   "hibrido",    "CLT",       18000, False, "aberta",   "2026-02-05",
             ["Vale Refeição","Plano de Saúde","Gympass"],
             [("Machine Learning","obrigatorio"),("Python","obrigatorio"),("BigQuery","desejavel")]),
            ("UX Designer",                   "Google Brasil",   "remoto",     "CLT",       12000, False, "aberta",   "2026-03-01",
             ["Vale Refeição","Plano de Saúde"],
             [("Figma","obrigatorio"),("Pesquisa de Usuário","obrigatorio")]),
            ("Engenheiro de Backend",         "Nubank",          "remoto",     "CLT",       20000, False, "aberta",   "2025-11-15",
             ["Vale Refeição","Plano de Saúde","Stock Options"],
             [("Clojure","obrigatorio"),("Kafka","desejavel"),("PostgreSQL","obrigatorio")]),
            ("Analista de Risco de Crédito",  "Nubank",          "hibrido",    "CLT",        9000, False, "aberta",   "2026-01-20",
             ["Vale Refeição","Plano de Saúde","PLR"],
             [("SQL","obrigatorio"),("Estatística","obrigatorio"),("Python","desejavel")]),
            ("Product Manager",               "Nubank",          "remoto",     "CLT",       25000, False, "encerrada","2025-10-01",
             ["Vale Refeição","Plano de Saúde","Stock Options"],
             [("Gestão de Produto","obrigatorio"),("Inglês Fluente","obrigatorio")]),
            ("Desenvolvedor Full Stack",       "Magazine Luiza",  "presencial", "CLT",       11000, False, "aberta",   "2026-02-15",
             ["Vale Refeição","Vale Transporte","Plano de Saúde"],
             [("React","obrigatorio"),("Node.js","obrigatorio"),("MySQL","desejavel")]),
            ("Analista de E-commerce",         "Magazine Luiza",  "presencial", "CLT",        6500, False, "aberta",   "2026-03-10",
             ["Vale Refeição","Vale Transporte"],
             [("Google Analytics","obrigatorio"),("SEO","obrigatorio"),("Excel Avançado","desejavel")]),
            ("Assistente Logístico PcD",       "Magazine Luiza",  "presencial", "CLT",        2800, True,  "aberta",   "2026-03-20",
             ["Vale Refeição","Vale Transporte","Plano de Saúde"],
             [("Ensino Médio Completo","obrigatorio")]),
            ("Analista de Marketing Digital",  "Ambev",           "hibrido",    "CLT",        8000, False, "aberta",   "2026-01-05",
             ["Vale Refeição","PLR","Plano de Saúde","Gympass"],
             [("Google Ads","obrigatorio"),("Meta Ads","obrigatorio"),("Inglês Intermediário","desejavel")]),
            ("Gerente de Trade Marketing",     "Ambev",           "presencial", "CLT",       15000, False, "aberta",   "2025-12-01",
             ["Carro Empresa","Plano de Saúde","PLR"],
             [("Gestão de Equipes","obrigatorio"),("Excel Avançado","obrigatorio"),("MBA","desejavel")]),
            ("Enfermeiro(a) UTI",              "Hospital Albert Einstein","presencial","CLT",  7500, False, "aberta",   "2026-02-01",
             ["Plano de Saúde","Vale Refeição","Plantão Noturno Premium"],
             [("COREN Ativo","obrigatorio"),("Experiência em UTI","obrigatorio")]),
            ("Analista de TI Hospitalar",      "Hospital Albert Einstein","presencial","CLT",  9000, False, "aberta",   "2026-03-05",
             ["Plano de Saúde","Vale Refeição","Vale Transporte"],
             [("Suporte a Sistemas Hospitalares","obrigatorio"),("ITIL","desejavel")]),
            ("Auxiliar Administrativo PcD",    "Hospital Albert Einstein","presencial","CLT",  2500, True,  "aberta",   "2026-03-15",
             ["Plano de Saúde","Vale Refeição","Vale Transporte"],
             [("Ensino Médio Completo","obrigatorio"),("Pacote Office","obrigatorio")]),
            ("Analista de Dados Financeiros",  "Itaú Unibanco",   "hibrido",    "CLT",       13000, False, "aberta",   "2026-01-15",
             ["Vale Refeição","Plano de Saúde","PLR","Previdência Privada"],
             [("SQL","obrigatorio"),("Power BI","obrigatorio"),("Python","desejavel")]),
            ("Especialista em Crédito",        "Itaú Unibanco",   "presencial", "CLT",       11000, False, "aberta",   "2026-02-20",
             ["Vale Refeição","Plano de Saúde","PLR"],
             [("Análise de Crédito","obrigatorio"),("Excel Avançado","obrigatorio")]),
            ("Desenvolvedor Mobile",           "iFood",           "remoto",     "CLT",       16000, False, "aberta",   "2026-01-25",
             ["Vale Refeição","Plano de Saúde","Stock Options"],
             [("Flutter","obrigatorio"),("Kotlin","desejavel"),("Swift","desejavel")]),
            ("Analista de Operações",          "iFood",           "hibrido",    "CLT",        7000, False, "encerrada","2025-09-01",
             ["Vale Refeição","Plano de Saúde"],
             [("Logística","obrigatorio"),("Excel Avançado","obrigatorio")]),
            ("Engenheiro Aeronáutico Sênior",  "Embraer",         "presencial", "CLT",       18000, False, "aberta",   "2026-02-10",
             ["Plano de Saúde","Vale Refeição","PLR","Previdência Privada"],
             [("Engenharia Aeronáutica","obrigatorio"),("Inglês Fluente","obrigatorio"),("CATIA","desejavel")]),
            ("Técnico de Manutenção",          "Embraer",         "presencial", "CLT",        6500, False, "aberta",   "2026-03-01",
             ["Plano de Saúde","Vale Refeição","Vale Transporte"],
             [("Eletromecânica","obrigatorio"),("NR-10","obrigatorio")]),
            ("Analista de Sustentabilidade",   "Natura &Co",      "hibrido",    "CLT",        8500, False, "aberta",   "2026-01-10",
             ["Vale Refeição","Plano de Saúde","Gympass"],
             [("Meio Ambiente","obrigatorio"),("Inglês Intermediário","desejavel")]),
            ("Analista de Investimentos",      "XP Inc.",         "presencial", "CLT",       15000, False, "aberta",   "2026-02-01",
             ["Vale Refeição","Plano de Saúde","PLR","Bônus"],
             [("CPA-20","obrigatorio"),("Excel Avançado","obrigatorio"),("MBA","desejavel")]),
            ("Assessor de Investimentos PcD",  "XP Inc.",         "hibrido",    "CLT",        9000, True,  "aberta",   "2026-03-10",
             ["Vale Refeição","Plano de Saúde","PLR"],
             [("CPA-10","obrigatorio"),("Inglês Básico","desejavel")]),
        ]

        ben_cache = {}
        for titulo, emp_nome, modal, contrato, sal, pcd, status, data_ab, bens, reqs in VAGAS:
            eid = emp_map.get(emp_nome)
            if not eid:
                continue
            vaga = models.Vaga(
                titulo=titulo, empresa_id=eid, modalidade=modal,
                tipo_contrato=contrato, salario=sal, vaga_pcd=pcd,
                status=status, data_abertura=_date.fromisoformat(data_ab),
                data_publicacao=_date.fromisoformat(data_ab),
                local="São Paulo, SP", publico_alvo="ambos", quantidade_vagas=1,
            )
            db.add(vaga)
            db.flush()
            for nome_b in bens:
                if nome_b not in ben_cache:
                    b = models.Beneficio(nome=nome_b)
                    db.add(b); db.flush()
                    ben_cache[nome_b] = b
                vaga.beneficios.append(ben_cache[nome_b])
            for desc_r, nivel_r in reqs:
                r = models.Requisito(descricao=desc_r, nivel=nivel_r)
                db.add(r); db.flush()
                vaga.requisitos.append(r)

        CANDIDATOS = [
            ("Ana Lima","ana.lima@email.com","11912340001","São Paulo","SP"),
            ("Carlos Souza","carlos.souza@email.com","11912340002","Campinas","SP"),
            ("Beatriz Santos","beatriz.santos@email.com","11912340003","Rio de Janeiro","RJ"),
            ("Lucas Ferreira","lucas.ferreira@email.com","11912340004","Belo Horizonte","MG"),
            ("Mariana Costa","mariana.costa@email.com","11912340005","São Paulo","SP"),
            ("Rafael Oliveira","rafael.oliveira@email.com","11912340006","Curitiba","PR"),
            ("Juliana Pereira","juliana.pereira@email.com","11912340007","São Paulo","SP"),
            ("Diego Almeida","diego.almeida@email.com","11912340008","Porto Alegre","RS"),
            ("Fernanda Rocha","fernanda.rocha@email.com","11912340009","São Paulo","SP"),
            ("Pedro Martins","pedro.martins@email.com","11912340010","Fortaleza","CE"),
            ("Isabela Nunes","isabela.nunes@email.com","11912340011","Recife","PE"),
            ("Thiago Barbosa","thiago.barbosa@email.com","11912340012","São Paulo","SP"),
            ("Camila Dias","camila.dias@email.com","11912340013","São Paulo","SP"),
            ("Bruno Carvalho","bruno.carvalho@email.com","11912340014","Salvador","BA"),
            ("Leticia Moura","leticia.moura@email.com","11912340015","Manaus","AM"),
            ("Rodrigo Teixeira","rodrigo.teixeira@email.com","11912340016","São Paulo","SP"),
            ("Amanda Lopes","amanda.lopes@email.com","11912340017","São Paulo","SP"),
            ("Felipe Nascimento","felipe.nascimento@email.com","11912340018","Brasília","DF"),
            ("Vanessa Ribeiro","vanessa.ribeiro@email.com","11912340019","São Paulo","SP"),
            ("Gabriel Silva","gabriel.silva@email.com","11912340020","Campinas","SP"),
        ]
        cand_ids = []
        for nome, email, tel, cidade, estado in CANDIDATOS:
            c = models.Candidato(nome=nome, email=email, telefone=tel, cidade=cidade, estado=estado)
            db.add(c); db.flush()
            cand_ids.append(c.id)

        import random as _random
        vagas_db = db.query(models.Vaga).all()
        status_opts = ["em_analise", "entrevista", "aprovado", "reprovado"]
        seen = set()
        for vaga in vagas_db[:15]:
            for cid in _random.sample(cand_ids, min(3, len(cand_ids))):
                if (vaga.id, cid) in seen:
                    continue
                seen.add((vaga.id, cid))
                db.add(models.Candidatura(
                    vaga_id=vaga.id, candidato_id=cid,
                    status=_random.choice(status_opts),
                ))

        db.commit()
        print("[seed] Dados iniciais inseridos com sucesso.")
    except Exception as exc:
        db.rollback()
        print(f"[seed] Erro ao inserir dados iniciais: {exc}")
    finally:
        db.close()


_seed_dados()

app = FastAPI(title="Agência de Empregos API")

_cors_origins_env = os.getenv("CORS_ORIGINS", "")
_allowed_origins = (
    [o.strip() for o in _cors_origins_env.split(",") if o.strip()]
    if _cors_origins_env
    else [
        "https://projeto-integrador-senac.streamlit.app",
        "http://localhost:8501",
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
app.include_router(empresas.router, prefix="/empresas", tags=["Empresas"])
app.include_router(vagas.router, prefix="/vagas", tags=["Vagas"])
app.include_router(candidatos.router, prefix="/candidatos", tags=["Candidatos"])
app.include_router(candidaturas.router, prefix="/candidaturas", tags=["Candidaturas"])


@app.get("/")
def root():
    return {"message": "Agência de Empregos API", "docs": "/docs"}

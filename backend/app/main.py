import os
import random
import secrets
from datetime import date, timedelta

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine, SessionLocal
from app import models
from app.routers import empresas, vagas, candidatos, candidaturas
from app.routers import auth as auth_router
from app.auth import hash_senha

Base.metadata.create_all(bind=engine)


def _migrate():
    from sqlalchemy import text
    with engine.connect() as conn:
        for sql in [
            "ALTER TABLE candidatos ADD COLUMN curriculo_path TEXT",
            "ALTER TABLE vagas ADD COLUMN recrutador_id INTEGER REFERENCES usuarios(id)",
        ]:
            try:
                conn.execute(text(sql))
                conn.commit()
            except Exception:
                pass


def _seed_admin():
    db = SessionLocal()
    try:
        if db.query(models.Usuario).count() > 0:
            return
        email = os.getenv("ADMIN_EMAIL")
        senha = os.getenv("ADMIN_SENHA")
        nome  = os.getenv("ADMIN_NOME", "Admin")
        if not email or not senha:
            return
        db.add(models.Usuario(
            nome=nome, email=email,
            senha_hash=hash_senha(senha),
            perfil=models.PerfilEnum.admin,
        ))
        db.commit()
    finally:
        db.close()


def _seed_usuarios_fixos():
    """Cria um admin extra via env vars EXTRA_ADMIN_EMAIL / EXTRA_ADMIN_SENHA (idempotente)."""
    email = os.getenv("EXTRA_ADMIN_EMAIL")
    nome  = os.getenv("EXTRA_ADMIN_NOME", "Admin Extra")
    senha = os.getenv("EXTRA_ADMIN_SENHA")
    if not email or not senha:
        return
    db = SessionLocal()
    try:
        if not db.query(models.Usuario).filter(models.Usuario.email == email).first():
            db.add(models.Usuario(
                nome=nome, email=email,
                senha_hash=hash_senha(senha),
                perfil=models.PerfilEnum.admin,
            ))
            db.commit()
    finally:
        db.close()


def _seed_dados():
    db = SessionLocal()
    try:
        if db.query(models.Empresa).count() > 0:
            return  # já tem dados

        from datetime import date as _date

        # ── Recrutadoras (senhas aleatórias geradas uma única vez no seed) ────
        RECRUTADORAS = [
            ("Juliana", "juliana@agencia.com"),
            ("Manu",    "manu@agencia.com"),
            ("Mel",     "mel@agencia.com"),
            ("Sara",    "sara@agencia.com"),
            ("Silvia",  "silvia@agencia.com"),
            ("Thais",   "thais@agencia.com"),
            ("Ully",    "ully@agencia.com"),
            ("Yasmin",  "yasmin@agencia.com"),
            ("Yumi",    "yumi@agencia.com"),
        ]
        rec_map = {}
        print("[seed] Contas de demonstração — recrutadoras:")
        for nome_r, email_r in RECRUTADORAS:
            u = db.query(models.Usuario).filter(models.Usuario.email == email_r).first()
            if not u:
                senha_r = secrets.token_urlsafe(12)
                u = models.Usuario(
                    nome=nome_r, email=email_r,
                    senha_hash=hash_senha(senha_r),
                    perfil=models.PerfilEnum.recrutador,
                )
                db.add(u)
                db.flush()
                print(f"  {email_r}  →  {senha_r}")
            rec_map[nome_r.upper()] = u.id

        # ── Empresas (dados fictícios de demonstração) ────────────────────────
        EMPRESAS_DEMO = [
            ("Ambev",           "Bebidas",      "São Paulo",         "SP"),
            ("Bradesco",        "Financeiro",   "Osasco",            "SP"),
            ("Embraer",         "Aeronáutica",  "São José dos Campos","SP"),
            ("Magazine Luiza",  "Varejo",       "Franca",            "SP"),
            ("Natura",          "Cosméticos",   "São Paulo",         "SP"),
            ("Petrobras",       "Energia",      "Rio de Janeiro",    "RJ"),
            ("Vale",            "Mineração",    "Belo Horizonte",    "MG"),
            ("Vivo",            "Telecom",      "São Paulo",         "SP"),
            ("Itaú",            "Financeiro",   "São Paulo",         "SP"),
            ("Nubank",          "Fintech",      "São Paulo",         "SP"),
            ("iFood",           "Tecnologia",   "São Paulo",         "SP"),
            ("Totvs",           "Software",     "São Paulo",         "SP"),
            ("Localiza",        "Mobilidade",   "Belo Horizonte",    "MG"),
            ("WEG",             "Elétrico",     "Jaraguá do Sul",    "SC"),
            ("JBS",             "Alimentos",    "São Paulo",         "SP"),
        ]
        emp_map = {}
        for nome_e, setor_e, cidade_e, estado_e in EMPRESAS_DEMO:
            e = models.Empresa(nome=nome_e, setor=setor_e, cidade=cidade_e, estado=estado_e)
            db.add(e)
            db.flush()
            emp_map[nome_e] = e.id

        # ── Vagas de demonstração ─────────────────────────────────────────────
        # (titulo, empresa, modalidade, status, qtd, data_abertura, recrutador)
        VAGAS = [
            ("Analista de RH",              "Ambev",          "presencial", "aberta",   2, "2026-04-07", "JULIANA"),
            ("Técnico de Segurança",        "Ambev",          "presencial", "aberta",   1, "2026-05-11", "MEL"),
            ("Auxiliar Administrativo",     "Bradesco",       "presencial", "aberta",   3, "2026-04-13", "SARA"),
            ("Analista Financeiro",         "Bradesco",       "hibrido",    "aberta",   1, "2026-04-13", "SARA"),
            ("Engenheiro de Materiais",     "Embraer",        "presencial", "aberta",   1, "2026-04-23", "ULLY"),
            ("Técnico de Manutenção",       "Embraer",        "presencial", "aberta",   2, "2026-05-08", "YASMIN"),
            ("Vendedor Interno",            "Magazine Luiza", "presencial", "aberta",   5, "2026-04-08", "MANU"),
            ("Consultor de Vendas",         "Magazine Luiza", "hibrido",    "aberta",   3, "2026-05-12", "YUMI"),
            ("Analista de Marketing",       "Natura",         "remoto",     "aberta",   2, "2026-05-04", "SILVIA"),
            ("Designer UX/UI",              "Natura",         "hibrido",    "aberta",   1, "2026-06-01", "JULIANA"),
            ("Engenheiro de Petróleo",      "Petrobras",      "presencial", "aberta",   1, "2026-04-07", "SARA"),
            ("Técnico de Campo",            "Petrobras",      "presencial", "aberta",   4, "2026-05-07", "YASMIN"),
            ("Geólogo Jr",                  "Vale",           "presencial", "aberta",   1, "2026-04-24", "ULLY"),
            ("Operador de Equipamentos",    "Vale",           "presencial", "aberta",   6, "2026-05-26", "MEL"),
            ("Técnico de TI",               "Vivo",           "hibrido",    "aberta",   2, "2026-05-13", "THAIS"),
            ("Analista de Suporte N2",      "Vivo",           "remoto",     "aberta",   3, "2026-06-15", "THAIS"),
            ("Analista de Crédito",         "Itaú",           "hibrido",    "aberta",   2, "2026-06-18", "JULIANA"),
            ("Gerente de Conta PJ",         "Itaú",           "presencial", "aberta",   1, "2026-06-24", "SARA"),
            ("Desenvolvedor Python",        "Nubank",         "remoto",     "aberta",   3, "2026-06-11", "SILVIA"),
            ("Engenheiro de Software Sr",   "Nubank",         "remoto",     "aberta",   2, "2026-07-01", "ULLY"),
            ("Analista de Dados",           "iFood",          "hibrido",    "aberta",   2, "2026-06-16", "JULIANA"),
            ("Product Manager",             "iFood",          "hibrido",    "aberta",   1, "2026-06-22", "YASMIN"),
            ("DevOps Engineer",             "Totvs",          "remoto",     "aberta",   2, "2026-05-25", "ULLY"),
            ("Scrum Master",                "Totvs",          "hibrido",    "aberta",   1, "2026-06-29", "SILVIA"),
            ("Assistente Administrativo",   "Localiza",       "presencial", "aberta",   2, "2026-05-18", "MANU"),
            ("Coordenador de Logística",    "Localiza",       "presencial", "aberta",   1, "2026-06-30", "SARA"),
            ("Eletricista de Manutenção",   "WEG",            "presencial", "aberta",   2, "2026-06-22", "YASMIN"),
            ("Engenheiro Elétrico",         "WEG",            "presencial", "aberta",   1, "2026-07-02", "ULLY"),
            ("Operador de Produção",        "JBS",            "presencial", "aberta",   8, "2026-05-03", "MANU"),
            ("Técnico de Qualidade",        "JBS",            "presencial", "encerrada",1, "2026-04-13", "SARA"),
        ]

        # ── Benefícios (pool comum) ───────────────────────────────────────────
        BENEF_NOMES = [
            "Vale-refeição", "Vale-transporte", "Plano de saúde", "Plano odontológico",
            "Gympass", "Home office", "Bônus anual", "PLR", "Seguro de vida",
            "Auxílio creche", "Auxílio educação", "Day off aniversário",
        ]
        beneficios_db = []
        for bn in BENEF_NOMES:
            b = models.Beneficio(nome=bn)
            db.add(b)
            beneficios_db.append(b)
        db.flush()

        # ── Inserção das vagas ────────────────────────────────────────────────
        random.seed(42)
        vagas_inseridas = []

        for titulo_v, emp_nome, mod_v, status_v, qtd_v, data_v, rec_nome in VAGAS:
            eid = emp_map.get(emp_nome)
            if not eid:
                continue
            rid = rec_map.get(rec_nome.upper()) if rec_nome else None
            salario = round(random.uniform(2500, 15000), 2)
            vaga = models.Vaga(
                titulo=titulo_v, empresa_id=eid, modalidade=mod_v,
                tipo_contrato="CLT", status=status_v,
                quantidade_vagas=qtd_v, recrutador_id=rid,
                local="São Paulo, SP", publico_alvo="ambos",
                salario=salario,
                data_abertura=_date.fromisoformat(data_v),
                data_publicacao=_date.fromisoformat(data_v),
            )
            vaga.beneficios = random.sample(beneficios_db, k=random.randint(3, 6))
            for desc_r, nivel_r in [
                ("Ensino Superior Completo ou cursando", models.NivelRequisitoEnum.obrigatorio),
                ("Experiência na área", models.NivelRequisitoEnum.obrigatorio),
                ("Inglês intermediário", models.NivelRequisitoEnum.desejavel),
            ]:
                r = models.Requisito(descricao=desc_r, nivel=nivel_r)
                db.add(r)
                vaga.requisitos.append(r)
            db.add(vaga)
            db.flush()
            vagas_inseridas.append(vaga)

        # ── Candidatos fictícios ───────────────────────────────────────────────
        CANDIDATOS = [
            ("Ana Paula Ferreira",   "ana.ferreira@email.com",   "11987650001", "São Paulo",    "SP", "1998-03-12"),
            ("Bruno Souza Lima",     "bruno.lima@email.com",     "11987650002", "Santo André",  "SP", "1995-07-22"),
            ("Carla Mendes Silva",   "carla.mendes@email.com",   "11987650003", "São Bernardo", "SP", "2000-01-05"),
            ("Diego Rodrigues",      "diego.rodrigues@email.com","11987650004", "Diadema",      "SP", "1993-11-30"),
            ("Eduarda Costa",        "eduarda.costa@email.com",  "11987650005", "Mauá",         "SP", "2001-06-18"),
            ("Felipe Martins",       "felipe.martins@email.com", "11987650006", "São Caetano",  "SP", "1997-09-03"),
            ("Gabriela Oliveira",    "gabriela.oli@email.com",   "11987650007", "São Paulo",    "SP", "1999-04-25"),
            ("Henrique Alves",       "henrique.alv@email.com",   "11987650008", "Guarulhos",    "SP", "1994-12-14"),
            ("Isabella Nascimento",  "isabella.nasc@email.com",  "11987650009", "Osasco",       "SP", "2002-08-09"),
            ("João Pedro Araújo",    "joaopedro.araujo@email.com","11987650010","São Paulo",    "SP", "1996-02-28"),
            ("Karen Santos",         "karen.santos@email.com",   "11987650011", "Taboão da Serra","SP","1998-05-17"),
            ("Lucas Pereira",        "lucas.pereira@email.com",  "11987650012", "São Paulo",    "SP", "2000-10-31"),
            ("Mariana Gonçalves",    "mariana.gon@email.com",    "11987650013", "São Bernardo", "SP", "1995-03-08"),
            ("Nathan Lima",          "nathan.lima@email.com",    "11987650014", "Diadema",      "SP", "1999-07-19"),
            ("Olivia Teixeira",      "olivia.teix@email.com",    "11987650015", "Santo André",  "SP", "2001-12-02"),
            ("Paulo Henrique Ramos", "ph.ramos@email.com",       "11987650016", "Mauá",         "SP", "1992-06-11"),
            ("Rafaela Cardoso",      "rafaela.card@email.com",   "11987650017", "São Paulo",    "SP", "1997-01-24"),
            ("Samuel Barbosa",       "samuel.barb@email.com",    "11987650018", "Guarulhos",    "SP", "2000-09-06"),
            ("Thaís Moreira",        "thais.moreira@email.com",  "11987650019", "Osasco",       "SP", "1996-04-13"),
            ("Victor Hugo Pinto",    "victor.pinto@email.com",   "11987650020", "São Paulo",    "SP", "1998-11-27"),
        ]
        cands_inseridos = []
        STATUS_CAND = list(models.StatusCandidaturaEnum)
        for nome_c, email_c, tel_c, cidade_c, estado_c, nasc_c in CANDIDATOS:
            c = models.Candidato(
                nome=nome_c, email=email_c, telefone=tel_c,
                cidade=cidade_c, estado=estado_c,
                data_nascimento=_date.fromisoformat(nasc_c),
            )
            db.add(c)
            db.flush()
            cands_inseridos.append(c)

        # ── Candidaturas aleatórias (3-6 por candidato, nas primeiras 40 vagas) ─
        vagas_para_cand = vagas_inseridas[:40]
        for cand in cands_inseridos:
            qtd = random.randint(3, 6)
            vagas_escolhidas = random.sample(vagas_para_cand, min(qtd, len(vagas_para_cand)))
            for vaga in vagas_escolhidas:
                status_c = random.choice(STATUS_CAND)
                candidatura = models.Candidatura(
                    candidato_id=cand.id, vaga_id=vaga.id,
                    status=status_c,
                    data_candidatura=vaga.data_abertura,
                )
                db.add(candidatura)

        db.commit()
        print("[seed] Dados iniciais inseridos com sucesso.")
    except Exception as exc:
        db.rollback()
        print(f"[seed] Erro ao inserir dados iniciais: {exc}")
    finally:
        db.close()


_migrate()
_seed_admin()
_seed_usuarios_fixos()
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
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(auth_router.router,    prefix="/auth",         tags=["Auth"])
app.include_router(empresas.router,       prefix="/empresas",     tags=["Empresas"])
app.include_router(vagas.router,          prefix="/vagas",        tags=["Vagas"])
app.include_router(candidatos.router,     prefix="/candidatos",   tags=["Candidatos"])
app.include_router(candidaturas.router,   prefix="/candidaturas", tags=["Candidaturas"])


@app.get("/")
def root():
    return {"message": "Agência de Empregos API", "docs": "/docs"}

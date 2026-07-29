import os
import random
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
    FIXOS = [
        ("Paulo", "devoluap@gmail.com", "devoluap123", models.PerfilEnum.admin),
    ]
    db = SessionLocal()
    try:
        for nome, email, senha, perfil in FIXOS:
            if not db.query(models.Usuario).filter(models.Usuario.email == email).first():
                db.add(models.Usuario(
                    nome=nome, email=email,
                    senha_hash=hash_senha(senha),
                    perfil=perfil,
                ))
        db.commit()
    finally:
        db.close()


def _seed_dados():
    db = SessionLocal()
    try:
        if db.query(models.Empresa).count() > 0:
            return

        # Recrutadoras
        recrutadoras = []
        for i, nome in enumerate(["Ana Lima", "Beatriz Costa", "Carla Souza", "Diana Rocha",
                                   "Eduardo Melo", "Fernanda Alves", "Gustavo Pinto",
                                   "Helena Cruz", "Igor Nunes"], 1):
            u = models.Usuario(
                nome=nome,
                email=f"recrutador{i}@agencia.com",
                senha_hash=hash_senha("Senha@123"),
                perfil=models.PerfilEnum.recrutador,
            )
            db.add(u)
            recrutadoras.append(u)
        db.flush()

        # Empresas
        dados_empresas = [
            ("Ambev", "Bebidas", "São Paulo", "SP"),
            ("Bradesco", "Financeiro", "Osasco", "SP"),
            ("Embraer", "Aeronáutica", "São José dos Campos", "SP"),
            ("Magazine Luiza", "Varejo", "Franca", "SP"),
            ("Natura", "Cosméticos", "São Paulo", "SP"),
            ("Petrobras", "Energia", "Rio de Janeiro", "RJ"),
            ("Vale", "Mineração", "Belo Horizonte", "MG"),
            ("Vivo", "Telecom", "São Paulo", "SP"),
            ("Itaú", "Financeiro", "São Paulo", "SP"),
            ("Nubank", "Fintech", "São Paulo", "SP"),
            ("iFood", "Tecnologia", "São Paulo", "SP"),
            ("Totvs", "Software", "São Paulo", "SP"),
            ("Localiza", "Mobilidade", "Belo Horizonte", "MG"),
            ("WEG", "Elétrico", "Jaraguá do Sul", "SC"),
            ("JBS", "Alimentos", "São Paulo", "SP"),
        ]
        empresas_db = []
        for nome, setor, cidade, estado in dados_empresas:
            e = models.Empresa(nome=nome, setor=setor, cidade=cidade, estado=estado)
            db.add(e)
            empresas_db.append(e)
        db.flush()

        # Benefícios
        nomes_benef = ["Vale-refeição", "Vale-transporte", "Plano de saúde", "Plano odontológico",
                       "Gympass", "Home office", "Bônus anual", "PLR", "Seguro de vida", "Auxílio creche",
                       "Auxílio educação", "Day off aniversário"]
        beneficios_db = []
        for nome in nomes_benef:
            b = models.Beneficio(nome=nome)
            db.add(b)
            beneficios_db.append(b)
        db.flush()

        # Vagas
        titulos = [
            "Analista de RH", "Desenvolvedor Python", "Gerente Comercial", "Designer UX/UI",
            "Assistente Administrativo", "Analista Financeiro", "Coordenador de Logística",
            "Engenheiro de Software", "Analista de Marketing", "Técnico de TI",
            "Analista de Dados", "Product Manager", "DevOps Engineer", "Scrum Master",
            "Analista de Suporte",
        ]
        modalidades = list(models.ModalidadeEnum)
        contratos   = list(models.TipoContratoEnum)
        random.seed(42)

        vagas_db = []
        for i, titulo in enumerate(titulos):
            abertura = date.today() - timedelta(days=random.randint(1, 60))
            v = models.Vaga(
                titulo=titulo,
                local=random.choice(["São Paulo, SP", "Rio de Janeiro, RJ", "Remoto", "Belo Horizonte, MG"]),
                descricao=f"Vaga para {titulo} em empresa de destaque.",
                salario=round(random.uniform(2500, 15000), 2),
                modalidade=random.choice(modalidades),
                tipo_contrato=random.choice(contratos),
                vaga_pcd=random.random() < 0.2,
                status=models.StatusVagaEnum.aberta,
                data_abertura=abertura,
                quantidade_vagas=random.randint(1, 5),
                empresa_id=random.choice(empresas_db).id,
                recrutador_id=random.choice(recrutadoras).id,
            )
            v.beneficios = random.sample(beneficios_db, k=random.randint(3, 6))
            for desc, nivel in [
                ("Ensino superior completo", models.NivelRequisitoEnum.obrigatorio),
                ("Experiência na área", models.NivelRequisitoEnum.obrigatorio),
                ("Inglês intermediário", models.NivelRequisitoEnum.desejavel),
            ]:
                r = models.Requisito(descricao=desc, nivel=nivel)
                db.add(r)
                v.requisitos.append(r)
            db.add(v)
            vagas_db.append(v)
        db.flush()

        # Candidatos e candidaturas
        for i in range(1, 21):
            c = models.Candidato(
                nome=f"Candidato {i}",
                email=f"candidato{i}@email.com",
                telefone=f"1199{i:07d}",
                cidade="São Paulo",
                estado="SP",
            )
            db.add(c)
            db.flush()
            for v in random.sample(vagas_db, k=random.randint(2, 5)):
                db.add(models.Candidatura(
                    candidato_id=c.id,
                    vaga_id=v.id,
                    status=random.choice(list(models.StatusCandidaturaEnum)),
                ))

        db.commit()
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
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
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

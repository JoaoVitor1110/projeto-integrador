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

        from datetime import date as _date

        # ── Recrutadoras ──────────────────────────────────────────────────────
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
        for nome_r, email_r in RECRUTADORAS:
            u = db.query(models.Usuario).filter(models.Usuario.email == email_r).first()
            if not u:
                u = models.Usuario(
                    nome=nome_r, email=email_r,
                    senha_hash=hash_senha("Senha@123"),
                    perfil=models.PerfilEnum.recrutador,
                )
                db.add(u)
                db.flush()
            rec_map[nome_r.upper()] = u.id

        # ── Empresas ──────────────────────────────────────────────────────────
        EMPRESAS = [
            "ACRIMET", "ALFA ALIMENTOS", "ALFA ALIMENTOS (CIBELE)", "ART TÉCNICA",
            "ASTECH BOMBAS", "AURA HOME", "AUTOMETAL", "AUTOMETAL / SAARGUMI",
            "AXXIS - ITUPEVA", "BRASA BAR", "COMPONENT DIADEMA", "CSI CARGO",
            "FORTE FIXADORES", "G2B PRODUÇÕES", "GALVANOPLASTIA DIADEMA",
            "GRUPO LUKSCOLOR", "IAM", "IBAB RUBBER", "INYLBRA", "ITEB",
            "MARTE BALANÇAS", "MIKROVAL", "OMEGA -MEGA LIGHT DIADEMA",
            "ORUOM - SBCAMPO", "PAPEIS SAFRA", "PLASFIL", "PRODUFLEX",
            "RASSINI", "REAL CESTAS", "RUFATO", "SEFAR", "SER GLASS",
            "SPRAYING", "TECNOBRASIL", "TECNOCON", "TUBOS IPIRANGA",
            "TW ESPUMA", "TW ESPUMAS", "VIVA COR", "VK MOLAS",
            "WORLD LABEL", "ZEPPINI", "ZHS IND e COMERCIO",
        ]
        emp_map = {}
        for nome_e in EMPRESAS:
            e = models.Empresa(nome=nome_e, cnpj="", setor="Indústria", cidade="São Paulo", estado="SP")
            db.add(e)
            db.flush()
            emp_map[nome_e] = e.id

        # ── Vagas (backlog real TGA) ───────────────────────────────────────────
        # (titulo, empresa, modalidade, status, qtd, data_abertura, recrutador, descricao)
        VAGAS = [
            ("Ajudante De Produção", "ZEPPINI", "presencial", "aberta", 4, "2026-04-07", "YASMIN", ""),
            ("Manutencista Predial (Tipo Pedreiro)", "RUFATO", "presencial", "aberta", 1, "2026-05-11", "MEL", ""),
            ("Auxiliar De Almoxarifado", "RUFATO", "presencial", "aberta", 70, "2026-06-24", "MEL", ""),
            ("Vendedora Interna", "PAPEIS SAFRA", "presencial", "aberta", 10, "2026-04-13", "SARA", "VAGA DIFÍCIL DE FECHAR"),
            ("Operador Multifuncional", "ZHS IND e COMERCIO", "presencial", "aberta", 1, "2026-05-08", "YUMI", ""),
            ("Vendedor Interno", "MARTE BALANÇAS", "presencial", "aberta", 2, "2026-04-08", "MANU", ""),
            ("Auxiliar De Produção", "VK MOLAS", "presencial", "aberta", 2, "2026-04-29", "SARA", "CLIENTE NÃO RESPONDE"),
            ("Auxiliar De Enfermagem Do Trabalho", "RASSINI", "presencial", "aberta", 1, "2026-04-07", "SARA", "ENVIAR MAIS CANDIDATOS"),
            ("Eletricista De Manutenção", "AUTOMETAL", "presencial", "aberta", 1, "2026-06-22", "YASMIN", ""),
            ("Auxiliar De Produção", "AUTOMETAL", "presencial", "aberta", 10, "2026-06-29", "YASMIN", ""),
            ("Ajudante Geral", "GRUPO LUKSCOLOR", "presencial", "aberta", 10, "2026-07-07", "YASMIN", "PRAZO 17/07"),
            ("Ajudante Geral Pcd", "GRUPO LUKSCOLOR", "presencial", "aberta", 1, "2026-05-11", "YUMI", "PRAZO 16/07"),
            ("Auxiliar De Laboratório", "GRUPO LUKSCOLOR", "presencial", "aberta", 1, "2026-06-11", "JULIANA", ""),
            ("Auxiliar De Controle Qualidade", "GRUPO LUKSCOLOR", "presencial", "aberta", 2, "2026-05-11", "JULIANA", ""),
            ("Separador C", "GRUPO LUKSCOLOR", "presencial", "aberta", 1, "2026-06-16", "YUMI", "PRAZO 17/07"),
            ("Consultor De Vendas", "REAL CESTAS", "presencial", "aberta", 2, "2026-05-12", "YUMI", ""),
            ("Ajudante Geral", "PAPEIS SAFRA", "presencial", "aberta", 5, "2026-04-13", "YASMIN", "VAGA DIFÍCIL DE FECHAR"),
            ("Almoxarifado De Ferramentas", "SPRAYING", "presencial", "aberta", 1, "2026-04-13", "YASMIN", ""),
            ("Auxiliar De Limpeza Masculino", "ALFA ALIMENTOS (CIBELE)", "presencial", "aberta", 2, "2026-06-08", "SILVIA", ""),
            ("Operador De Empilhadeira", "CSI CARGO", "presencial", "aberta", 1, "2026-05-05", "YUMI", "REABRIR A VAGA"),
            ("Auxiliar De Serviços Gerais", "CSI CARGO", "presencial", "aberta", 1, "2026-05-11", "YUMI", ""),
            ("Auxiliar Operacional", "CSI CARGO", "presencial", "aberta", 20, "2026-05-27", "YUMI", "FERNANDA INFORMOU 20 VAGAS"),
            ("Operador De Máquina Multifuncional", "ORUOM - SBCAMPO", "presencial", "aberta", 1, "2026-05-11", "YUMI", ""),
            ("Especialista Em Pintura Líquida", "AUTOMETAL / SAARGUMI", "presencial", "aberta", 1, "2026-04-08", "ULLY", ""),
            ("Mecânico De Manutenção", "PLASFIL", "presencial", "aberta", 1, "2026-04-13", "MANU", ""),
            ("Laminador", "PLASFIL", "presencial", "aberta", 1, "2026-04-13", "MANU", ""),
            ("Auxiliar De Produção", "PLASFIL", "presencial", "aberta", 4, "2026-04-24", "MANU", "CANDIDATOS ENVIADOS SEM RETORNO"),
            ("Rebobinador", "PLASFIL", "presencial", "aberta", 2, "2026-04-15", "MANU", ""),
            ("Televendas", "ACRIMET", "presencial", "aberta", 1, "2026-04-13", "MEL", "VAGAS TRAVADAS"),
            ("Motorista", "ACRIMET", "presencial", "aberta", 1, "2026-04-13", "MEL", "VAGAS TRAVADAS"),
            ("Vendedor Interno", "ACRIMET", "presencial", "aberta", 1, "2026-04-13", "MEL", "VAGAS TRAVADAS"),
            ("Engenheiro De Materiais Jr", "AUTOMETAL / SAARGUMI", "presencial", "aberta", 1, "2026-04-23", "ULLY", ""),
            ("Auxiliar De Laboratório", "VIVA COR", "presencial", "aberta", 1, "2026-04-23", "MANU", "CLIENTE NÃO RESPONDE"),
            ("Ajudante De Produção", "INYLBRA", "presencial", "aberta", 15, "2026-05-04", "SARA", ""),
            ("Inspetor Da Qualidade", "INYLBRA", "presencial", "aberta", 1, "2026-04-24", "SARA", "CANDIDATO NÃO COMPARECEU"),
            ("Ajudante De Produção (Masc) T= M E T", "SPRAYING", "presencial", "aberta", 2, "2026-05-04", "MANU", ""),
            ("Garçon", "BRASA BAR", "presencial", "encerrada", 1, "2026-04-13", "MANU", ""),
            ("Cozinheiro", "BRASA BAR", "presencial", "encerrada", 1, "2026-04-13", "MANU", ""),
            ("Auxiliar De Almoxarifado", "TECNOCON", "presencial", "aberta", 1, "2026-05-08", "MEL", ""),
            ("Ajudante De Produção", "IBAB RUBBER", "presencial", "aberta", 2, "2026-05-08", "YUMI", ""),
            ("Auxiliar De Produção", "ITEB", "presencial", "aberta", 4, "2026-05-07", "", ""),
            ("Auxiliar De Produção", "TW ESPUMA", "presencial", "aberta", 10, "2026-05-25", "", "CLIENTE VAI AVISAR QUANDO FOR CONTRATAR"),
            ("Auxiliar De Almoxarifado", "AUTOMETAL", "presencial", "aberta", 1, "2026-05-13", "YASMIN", ""),
            ("Ferramenteiro Moldes", "AUTOMETAL", "presencial", "aberta", 1, "2026-06-24", "YASMIN", ""),
            ("Abastecedor De Produção", "AUTOMETAL", "presencial", "aberta", 10, "2026-05-07", "YASMIN", ""),
            ("Fresador Ferramenteiro", "FORTE FIXADORES", "presencial", "aberta", 1, "2026-06-29", "YASMIN", ""),
            ("Preparador E Op Torno CNC", "FORTE FIXADORES", "presencial", "aberta", 2, "2026-06-29", "YASMIN", ""),
            ("Operador De Prensa De Fricção", "FORTE FIXADORES", "presencial", "aberta", 1, "2026-06-29", "YASMIN", ""),
            ("Mecânico Manutenção De Máquinas", "SPRAYING", "presencial", "aberta", 1, "2026-06-10", "SARA", ""),
            ("Soldador", "SPRAYING", "presencial", "aberta", 1, "2026-06-24", "ULLY", ""),
            ("Projetista Com Conhecimento Em Mecatrônica", "SPRAYING", "presencial", "aberta", 1, "2026-05-03", "YASMIN", ""),
            ("Auxiliar De Produção", "TECNOBRASIL", "presencial", "aberta", 3, "2026-05-11", "MANU", ""),
            ("Analista De Recursos Humanos", "RASSINI", "presencial", "aberta", 1, "2026-06-26", "SARA", ""),
            ("Auxiliar De Almoxarifado", "RASSINI", "presencial", "aberta", 1, "2026-05-08", "SARA", "ENVIAR MAIS CANDIDATOS"),
            ("Auxiliar De Limpeza Fem", "ALFA ALIMENTOS (CIBELE)", "presencial", "aberta", 2, "2026-06-08", "SILVIA", ""),
            ("Auxiliar De Produção", "ALFA ALIMENTOS", "presencial", "aberta", 10, "2026-06-18", "SILVIA", ""),
            ("Auxiliar De Almoxarifado", "OMEGA -MEGA LIGHT DIADEMA", "presencial", "aberta", 3, "2026-06-19", "YASMIN", ""),
            ("Auxiliar De Montagem - Fem", "OMEGA -MEGA LIGHT DIADEMA", "presencial", "aberta", 2, "2026-06-19", "YASMIN", ""),
            ("Auxiliar De Produção (Masc/Fem)", "AXXIS - ITUPEVA", "presencial", "aberta", 1, "2026-05-25", "YASMIN", ""),
            ("Ajudante De Expedição", "ZEPPINI", "presencial", "aberta", 2, "2026-06-17", "YASMIN", ""),
            ("Ajudante De Produção (Coquilha)", "ZEPPINI", "presencial", "aberta", 1, "2026-04-07", "YASMIN", ""),
            ("Aux Serviços Gerais (Limpeza)", "PRODUFLEX", "presencial", "aberta", 3, "2026-04-28", "", ""),
            ("Porteiro Com CNH B", "PRODUFLEX", "presencial", "aberta", 1, "2026-04-28", "SARA", "EMPRESA NÃO DEU RETORNO"),
            ("Operador De Caixa", "BRASA BAR", "presencial", "encerrada", 1, "2026-04-13", "MANU", ""),
            ("Assistente Adm Fiscal", "AXXIS - ITUPEVA", "presencial", "aberta", 1, "2026-04-07", "MEL", ""),
            ("Eletricista", "AXXIS - ITUPEVA", "presencial", "aberta", 1, "2026-05-18", "YASMIN", ""),
            ("Mecânico De Manutenção", "AXXIS - ITUPEVA", "presencial", "aberta", 1, "2026-05-18", "YASMIN", ""),
            ("Oficial Mecânico De Manutenção", "AXXIS - ITUPEVA", "presencial", "aberta", 1, "2026-05-18", "YASMIN", ""),
            ("Mecânico Hidráulico", "INYLBRA", "presencial", "aberta", 1, "2026-04-24", "SARA", ""),
            ("Programador De Robô", "INYLBRA", "presencial", "aberta", 1, "2026-05-11", "SARA", ""),
            ("Assistente De Recursos Humanos", "RUFATO", "presencial", "aberta", 1, "2026-07-07", "MEL", ""),
            ("Operador De Empilhadeira", "RUFATO", "presencial", "aberta", 4, "2026-05-26", "MEL", "ENVIADOS PARA VALIDAÇÃO INTERNA DA RUFATO EM 29/05"),
            ("Analista De Engenharia", "INYLBRA", "presencial", "aberta", 1, "2026-05-26", "ULLY", "CANDIDATO 2ª ETAPA NA EMPRESA"),
            ("Operador De Máquina", "ZHS IND e COMERCIO", "presencial", "aberta", 1, "2026-05-22", "YUMI", ""),
            ("Auxiliar De Galvanoplastia", "GALVANOPLASTIA DIADEMA", "presencial", "aberta", 3, "2026-05-27", "SARA", ""),
            ("Auxiliar De Manutenção Predial", "SER GLASS", "presencial", "aberta", 1, "2026-06-30", "SARA", ""),
            ("Auxiliar De Produção", "SER GLASS", "presencial", "aberta", 10, "2026-06-01", "MEL", ""),
            ("Auxiliar De Manufatura", "SEFAR", "presencial", "aberta", 4, "2026-06-18", "SILVIA", "4 VAGAS"),
            ("Costureira", "SEFAR", "presencial", "aberta", 1, "2026-06-01", "SILVIA", "REPOSIÇÃO DE 1 FUNCIONÁRIA"),
            ("Suporte De Operações", "AURA HOME", "presencial", "aberta", 1, "2026-06-02", "THAIS", "2 ETAPA"),
            ("Analista De Qualidade", "TW ESPUMAS", "presencial", "aberta", 1, "2026-06-12", "JULIANA", ""),
            ("Assistente Administrativo", "AXXIS - ITUPEVA", "presencial", "aberta", 1, "2026-06-15", "YASMIN", ""),
            ("Técnico Em Desenvolvimento De Produtos", "ART TÉCNICA", "presencial", "aberta", 1, "2026-06-18", "JULIANA", ""),
            ("Selecionadora De Peças", "ART TÉCNICA", "presencial", "aberta", 1, "2026-06-18", "JULIANA", ""),
            ("Auxiliar De Produção", "ART TÉCNICA", "presencial", "aberta", 3, "2026-06-18", "JULIANA", ""),
            ("Assistente De PCP", "ART TÉCNICA", "presencial", "aberta", 1, "2026-06-18", "JULIANA", ""),
            ("Vendedor Interno", "ART TÉCNICA", "presencial", "aberta", 1, "2026-06-18", "JULIANA", ""),
            ("Técnico De Segurança Do Trabalho", "COMPONENT DIADEMA", "presencial", "aberta", 1, "2026-06-24", "YASMIN", ""),
            ("Auxiliar De Produção - Setor Montagem", "IAM", "presencial", "aberta", 2, "2026-06-26", "YASMIN", ""),
            ("Inspetor De Qualidade – Setor Trefila", "TUBOS IPIRANGA", "presencial", "aberta", 1, "2026-06-23", "SARA", ""),
            ("Operador Máquina I Ou Ajudante – Ponte Rolante", "TUBOS IPIRANGA", "presencial", "aberta", 3, "2026-06-23", "SARA", ""),
            ("Soldador I – Setor Manutenção Trefila", "TUBOS IPIRANGA", "presencial", "aberta", 1, "2026-06-23", "SARA", ""),
            ("Mecânico De Manutenção II – Manutenção", "TUBOS IPIRANGA", "presencial", "aberta", 1, "2026-06-23", "SARA", ""),
            ("Auxiliar Administrativo PCP", "TUBOS IPIRANGA", "presencial", "aberta", 1, "2026-06-23", "SARA", "Sem retorno"),
            ("Operador De Máquina I – Usinagem", "TUBOS IPIRANGA", "presencial", "aberta", 3, "2026-06-23", "SARA", ""),
            ("Analista De Custos (Pleno Ou Sênior)", "PRODUFLEX", "presencial", "aberta", 1, "2026-06-29", "JULIANA", ""),
            ("Laminador", "FORTE FIXADORES", "presencial", "aberta", 1, "2026-06-29", "YUMI", ""),
            ("Assistente/Analista Adm Jr", "FORTE FIXADORES", "presencial", "aberta", 1, "2026-06-29", "YUMI", ""),
            ("Auxiliar De Compras", "FORTE FIXADORES", "presencial", "aberta", 1, "2026-06-29", "YUMI", ""),
            ("Caldeireiro Industrial", "FORTE FIXADORES", "presencial", "aberta", 1, "2026-06-29", "YUMI", ""),
            ("Técnico Eletrônico - Pós Vendas", "RASSINI", "presencial", "aberta", 1, "2026-06-25", "SARA", ""),
            ("Auxiliar De Almoxarifado", "WORLD LABEL", "presencial", "aberta", 1, "2026-07-01", "SILVIA", ""),
            ("Auxiliar De Acabamento", "WORLD LABEL", "presencial", "aberta", 1, "2026-07-01", "SILVIA", ""),
            ("Rebobinador E Revisor", "WORLD LABEL", "presencial", "aberta", 1, "2026-07-01", "SILVIA", ""),
            ("Troquelador Revisor", "WORLD LABEL", "presencial", "aberta", 1, "2026-07-01", "SILVIA", ""),
            ("Assistente De Roteiro", "GRUPO LUKSCOLOR", "presencial", "aberta", 1, "2026-07-01", "YASMIN", ""),
            ("Pintor", "GRUPO LUKSCOLOR", "presencial", "aberta", 1, "2026-07-01", "YASMIN", ""),
            ("Ajudante Geral PcD Almoxarifado", "GRUPO LUKSCOLOR", "presencial", "aberta", 1, "2026-07-01", "YASMIN", ""),
            ("Assistente Adm", "ASTECH BOMBAS", "presencial", "aberta", 1, "2026-07-02", "MANU", ""),
            ("Assistente Adm (Nazaré Pta)", "MIKROVAL", "presencial", "aberta", 1, "2026-07-02", "MANU", ""),
            ("Ajudante Geral (SBC)", "MIKROVAL", "presencial", "aberta", 3, "2026-07-02", "MANU", ""),
            ("Encarregado De Expedição", "G2B PRODUÇÕES", "presencial", "aberta", 1, "2026-07-03", "YUMI", ""),
        ]

        for titulo_v, emp_nome, mod_v, status_v, qtd_v, data_v, rec_nome, desc_v in VAGAS:
            eid = emp_map.get(emp_nome)
            if not eid:
                continue
            rid = rec_map.get(rec_nome.upper()) if rec_nome else None
            vaga = models.Vaga(
                titulo=titulo_v, empresa_id=eid, modalidade=mod_v,
                tipo_contrato="CLT", status=status_v,
                quantidade_vagas=qtd_v, recrutador_id=rid,
                local="São Paulo, SP", publico_alvo="ambos",
                descricao=desc_v or None,
                data_abertura=_date.fromisoformat(data_v),
                data_publicacao=_date.fromisoformat(data_v),
            )
            db.add(vaga)

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
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
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

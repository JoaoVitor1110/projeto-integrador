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


def _seed_usuarios_fixos():
    """Garante usuários fixos a cada redeploy (idempotente por email)."""
    USUARIOS = [
        ("Paulo", "devoluap@gmail.com", "devoluap123", models.PerfilEnum.admin),
    ]
    db = SessionLocal()
    try:
        for nome_u, email_u, senha_u, perfil_u in USUARIOS:
            if not db.query(models.Usuario).filter(models.Usuario.email == email_u).first():
                db.add(models.Usuario(
                    nome=nome_u, email=email_u,
                    senha_hash=hash_senha(senha_u),
                    perfil=perfil_u,
                ))
        db.commit()
    finally:
        db.close()


_seed_usuarios_fixos()


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

        # ── Benefícios (pool comum) ───────────────────────────────────────────
        BENEF_NOMES = [
            "Vale Refeição", "Vale Transporte", "Plano de Saúde",
            "Plano Odontológico", "EPI Completo", "Seguro de Vida",
            "Vale Alimentação", "Cesta Básica", "Adiantamento Salarial",
            "PPR / PLR", "Convênio Farmácia", "Uniforme",
        ]
        benef_map = {}
        for bn in BENEF_NOMES:
            b = models.Beneficio(nome=bn)
            db.add(b)
            db.flush()
            benef_map[bn] = b

        def _benefs_para(titulo: str):
            t = titulo.lower()
            base = ["Vale Refeição", "Vale Transporte", "Seguro de Vida"]
            if any(k in t for k in ["produç", "ajudante", "operador", "manutenç", "soldador",
                                     "laminador", "caldeireiro", "ferramenteiro", "galvanoplastia",
                                     "rebobinador", "troquelador", "costureira", "pintor"]):
                base += ["EPI Completo", "Uniforme", "Plano de Saúde"]
            elif any(k in t for k in ["assistente", "analista", "auxiliar adm", "adm", "compras",
                                       "fiscal", "pcp", "recursos humanos", "custos", "roteiro"]):
                base += ["Plano de Saúde", "Plano Odontológico", "PPR / PLR"]
            elif any(k in t for k in ["vendedor", "vendas", "consultor", "televendas"]):
                base += ["Vale Alimentação", "Convênio Farmácia", "PPR / PLR"]
            elif any(k in t for k in ["motorista", "porteiro", "almoxarife", "almoxarifado",
                                       "expedição", "encarregado"]):
                base += ["Cesta Básica", "Adiantamento Salarial", "Uniforme"]
            elif any(k in t for k in ["técnico", "engenheiro", "analista", "programador",
                                       "projetista", "inspetor", "especialista"]):
                base += ["Plano de Saúde", "Plano Odontológico", "PPR / PLR", "Convênio Farmácia"]
            else:
                base += ["Cesta Básica", "Plano de Saúde"]
            return list(dict.fromkeys(base))  # dedupe preservando ordem

        # ── Requisitos (pool reutilizável) ────────────────────────────────────
        REQ_POOL: dict = {}
        def _get_req(desc: str, nivel: str):
            key = (desc, nivel)
            if key not in REQ_POOL:
                r = models.Requisito(descricao=desc, nivel=models.NivelRequisitoEnum(nivel))
                db.add(r)
                db.flush()
                REQ_POOL[key] = r
            return REQ_POOL[key]

        def _reqs_para(titulo: str):
            t = titulo.lower()
            reqs = []
            # Ensino médio é base para quase todos
            reqs.append(("Ensino Médio Completo", "obrigatorio"))
            if any(k in t for k in ["produç", "ajudante", "operador de máquina", "laminador",
                                     "rebobinador", "troquelador", "costureira", "pintor"]):
                reqs += [("Experiência anterior na função", "desejavel"),
                         ("Disponibilidade para trabalho em turnos", "desejavel")]
            elif any(k in t for k in ["eletricista", "mecânico", "manutenção", "caldeireiro",
                                       "ferramenteiro", "soldador"]):
                reqs[0] = ("Ensino Técnico ou Superior em área correlata", "obrigatorio")
                reqs += [("Experiência comprovada na função", "obrigatorio"),
                         ("NR-10 ou NR-12 atualizada", "desejavel")]
            elif any(k in t for k in ["assistente", "auxiliar adm", "adm", "pcp", "compras",
                                       "fiscal", "roteiro"]):
                reqs += [("Pacote Office (Excel intermediário)", "obrigatorio"),
                         ("Experiência em rotinas administrativas", "desejavel")]
            elif any(k in t for k in ["analista", "engenheiro", "especialista", "técnico"]):
                reqs[0] = ("Ensino Superior Completo ou cursando", "obrigatorio")
                reqs += [("Experiência mínima de 2 anos na área", "obrigatorio"),
                         ("Excel avançado / ERP", "desejavel")]
            elif any(k in t for k in ["vendedor", "vendas", "consultor", "televendas"]):
                reqs += [("Experiência em vendas internas ou externas", "obrigatorio"),
                         ("Boa comunicação e perfil comercial", "obrigatorio"),
                         ("Conhecimento em CRM", "desejavel")]
            elif any(k in t for k in ["motorista",]):
                reqs += [("CNH B ou superior válida", "obrigatorio"),
                         ("Experiência como motorista", "obrigatorio")]
            elif any(k in t for k in ["almoxarifado", "almoxarife", "expedição"]):
                reqs += [("Experiência em almoxarifado ou logística", "desejavel"),
                         ("Conhecimento em WMS ou sistema de estoque", "desejavel")]
            elif any(k in t for k in ["programador", "projetista"]):
                reqs[0] = ("Ensino Técnico ou Superior em Mecatrônica/Automação", "obrigatorio")
                reqs += [("Programação de CLP/Robô", "obrigatorio"),
                         ("Leitura de desenho técnico", "desejavel")]
            elif any(k in t for k in ["enfermagem",]):
                reqs[0] = ("Técnico de Enfermagem com COREN ativo", "obrigatorio")
                reqs += [("Experiência em medicina do trabalho", "desejavel")]
            elif any(k in t for k in ["limpeza", "serviços gerais", "aux serviços"]):
                reqs = [("Experiência em limpeza industrial ou comercial", "desejavel"),
                        ("Disponibilidade de horário", "obrigatorio")]
            elif any(k in t for k in ["inspetor", "qualidade", "laboratório"]):
                reqs += [("Experiência em controle de qualidade ou laboratório", "obrigatorio"),
                         ("Conhecimento em normas ISO ou BPF", "desejavel")]
            return reqs

        # ── Inserção das vagas com benefícios e requisitos ────────────────────
        import random
        random.seed(42)
        vagas_inseridas = []

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
            for bn in _benefs_para(titulo_v):
                if bn in benef_map:
                    vaga.beneficios.append(benef_map[bn])
            for desc_r, nivel_r in _reqs_para(titulo_v):
                vaga.requisitos.append(_get_req(desc_r, nivel_r))
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

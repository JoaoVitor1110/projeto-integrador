"""
Agência de Empregos — Interface Streamlit
Consome a API FastAPI do backend.
Configure a URL da API em .streamlit/secrets.toml ou via variável de ambiente API_URL.
"""

import os
from datetime import date, datetime
import streamlit as st
import requests

# ── Configuração ──────────────────────────────────────────────────────────────

API_URL = st.secrets.get("API_URL", os.getenv("API_URL", "http://localhost:8000"))

st.set_page_config(
    page_title="Agência de Empregos",
    page_icon="💼",
    layout="wide",
)

# ── Helpers de API ────────────────────────────────────────────────────────────

def _headers():
    token = st.session_state.get("token")
    return {"Authorization": f"Bearer {token}"} if token else {}


def api_get(path, params=None):
    try:
        r = requests.get(f"{API_URL}{path}", params=params, headers=_headers(), timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        st.error("❌ Não foi possível conectar ao backend. Verifique se a API está rodando.")
        return None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            st.warning("Sessão expirada. Faça login novamente.")
            st.session_state.clear()
            st.rerun()
        return None


def api_post(path, json=None, form=None):
    try:
        kwargs = {"headers": _headers(), "timeout": 10}
        if json is not None:
            kwargs["json"] = json
        if form is not None:
            kwargs["data"] = form
            kwargs["headers"] = {}
        r = requests.post(f"{API_URL}{path}", **kwargs)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        detail = e.response.json().get("detail", str(e)) if e.response else str(e)
        st.error(f"Erro: {detail}")
        return None


def api_put(path, json=None):
    try:
        r = requests.put(f"{API_URL}{path}", json=json, headers=_headers(), timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        detail = e.response.json().get("detail", str(e)) if e.response else str(e)
        st.error(f"Erro: {detail}")
        return None


def api_delete(path):
    try:
        r = requests.delete(f"{API_URL}{path}", headers=_headers(), timeout=10)
        r.raise_for_status()
        return True
    except requests.exceptions.HTTPError as e:
        detail = e.response.json().get("detail", str(e)) if e.response else str(e)
        st.error(f"Erro: {detail}")
        return False


# ── Estado de sessão ──────────────────────────────────────────────────────────

if "token" not in st.session_state:
    st.session_state.token = None
if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "pagina" not in st.session_state:
    st.session_state.pagina = "vagas"

# ── Labels ────────────────────────────────────────────────────────────────────

MODALIDADE_LABEL = {"presencial": "🏢 Presencial", "remoto": "🏠 Remoto", "hibrido": "🔄 Híbrido"}
CONTRATO_LABEL   = {"CLT": "CLT", "PJ": "PJ", "temporario": "Temporário", "estagio": "Estágio"}
PERFIL_LABEL     = {"admin": "👑 Admin", "recrutador": "📋 Recrutador", "visualizador": "👁 Visualizador"}

# ── Tela de Login ─────────────────────────────────────────────────────────────

def tela_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("## 💼 Agência de Empregos")
        st.markdown("### Acesse sua conta")

        with st.form("form_login"):
            email = st.text_input("Email")
            senha = st.text_input("Senha", type="password")
            entrar = st.form_submit_button("Entrar", use_container_width=True, type="primary")

        if entrar:
            if not email or not senha:
                st.warning("Preencha email e senha.")
            else:
                data = api_post("/auth/login", form={"username": email, "password": senha})
                if data:
                    st.session_state.token = data["access_token"]
                    st.session_state.usuario = data["usuario"]
                    st.rerun()


# ── Sidebar ───────────────────────────────────────────────────────────────────

def _sidebar():
    usuario = st.session_state.usuario
    perfil = usuario["perfil"]
    pode_escrever = perfil in ("admin", "recrutador")

    with st.sidebar:
        st.markdown(f"**{usuario['nome']}**")
        st.caption(PERFIL_LABEL.get(perfil, perfil))
        st.divider()

        st.markdown("### 📌 Menu")
        if st.button("💼 Vagas", use_container_width=True):
            st.session_state.pagina = "vagas"
            st.session_state.pop("vaga_aberta", None)
            st.rerun()

        if pode_escrever:
            if st.button("📊 Dashboard", use_container_width=True):
                st.session_state.pagina = "dashboard"
                st.rerun()

        if perfil == "admin":
            if st.button("🏭 Empresas", use_container_width=True):
                st.session_state.pagina = "empresas"
                st.rerun()
            if st.button("👥 Usuários", use_container_width=True):
                st.session_state.pagina = "usuarios"
                st.rerun()

        st.divider()

        if perfil in ("admin", "recrutador"):
            st.markdown("### 🔍 Filtros")
        else:
            st.markdown("### 🔍 Filtros")

        modalidade = st.selectbox(
            "Modalidade",
            ["", "presencial", "remoto", "hibrido"],
            format_func=lambda x: "Todas" if x == "" else MODALIDADE_LABEL.get(x, x),
        )
        contrato = st.selectbox(
            "Tipo de contrato",
            ["", "CLT", "PJ", "temporario", "estagio"],
            format_func=lambda x: "Todos" if x == "" else CONTRATO_LABEL.get(x, x),
        )
        status_filtro = st.selectbox(
            "Status",
            ["", "aberta", "encerrada"],
            format_func=lambda x: "Qualquer" if x == "" else x.capitalize(),
        )
        apenas_pcd = st.checkbox("Somente vagas PcD ♿")

        st.divider()
        if st.button("🚪 Sair", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    return modalidade, contrato, status_filtro, apenas_pcd


# ── Painel de Vagas ───────────────────────────────────────────────────────────

def tela_painel():
    usuario = st.session_state.usuario
    perfil = usuario["perfil"]
    pode_escrever = perfil in ("admin", "recrutador")

    modalidade, contrato, status_filtro, apenas_pcd = _sidebar()

    st.markdown("# 💼 Painel de Vagas")

    if pode_escrever:
        with st.expander("➕ Cadastrar nova vaga"):
            _form_nova_vaga()

    params = {}
    if modalidade:    params["modalidade"] = modalidade
    if contrato:      params["tipo_contrato"] = contrato
    if status_filtro: params["status"] = status_filtro
    if apenas_pcd:    params["vaga_pcd"] = True

    vagas = api_get("/vagas/", params=params)
    if vagas is None:
        return

    st.caption(f"{len(vagas)} vaga(s) encontrada(s)")
    st.divider()

    if not vagas:
        st.info("Nenhuma vaga encontrada para os filtros selecionados.")
        return

    cols = st.columns(3)
    for i, vaga in enumerate(vagas):
        with cols[i % 3]:
            _card_vaga(vaga, pode_escrever)


def _card_vaga(vaga, pode_escrever=False):
    salario = (
        f"R$ {vaga['salario']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        if vaga.get("salario") else "A combinar"
    )
    status_color = "🟢" if vaga["status"] == "aberta" else "⚫"
    modalidade_icon = {"presencial": "🏢", "remoto": "🏠", "hibrido": "🔄"}.get(vaga["modalidade"], "")

    with st.container(border=True):
        col_title, col_status = st.columns([4, 1])
        with col_title:
            st.markdown(f"**{vaga['titulo']}**")
        with col_status:
            st.markdown(status_color)

        st.caption(f"🏭 {vaga['empresa']['nome']}")
        qtd = vaga.get("quantidade_vagas", 1)
        if qtd and qtd > 1:
            st.caption(f"📌 {qtd} vagas disponíveis")
        st.markdown(
            f"`📍 {vaga['local']}` &nbsp; `{modalidade_icon} {MODALIDADE_LABEL.get(vaga['modalidade'], '')}` &nbsp; "
            f"`{CONTRATO_LABEL.get(vaga['tipo_contrato'], '')}` "
            + ("`♿ PcD`" if vaga.get("vaga_pcd") else ""),
            unsafe_allow_html=True,
        )
        st.markdown(f"**{salario}**")

        col_btn1, col_btn2 = st.columns(2) if pode_escrever else (st, None)
        with col_btn1:
            if st.button("Ver detalhes", key=f"det_{vaga['id']}", use_container_width=True):
                st.session_state["vaga_aberta"] = vaga["id"]
                st.rerun()
        if pode_escrever and col_btn2:
            with col_btn2:
                if st.button("✏️ Editar", key=f"edit_{vaga['id']}", use_container_width=True):
                    st.session_state["vaga_editar"] = vaga["id"]
                    st.rerun()


def _form_nova_vaga():
    empresas = api_get("/empresas/")
    if not empresas:
        st.warning("Nenhuma empresa cadastrada.")
        return

    with st.form("form_nova_vaga"):
        col1, col2 = st.columns(2)
        with col1:
            titulo = st.text_input("Título da vaga *")
            local  = st.text_input("Local *")
            salario = st.number_input("Salário (R$)", min_value=0.0, step=100.0)
            quantidade_vagas = st.number_input("Quantidade de vagas", min_value=1, step=1, value=1)
            empresa_opcoes = {e["nome"]: e["id"] for e in empresas}
            empresa_nome = st.selectbox("Empresa *", list(empresa_opcoes.keys()))
        with col2:
            modalidade    = st.selectbox("Modalidade", ["presencial", "remoto", "hibrido"])
            tipo_contrato = st.selectbox("Tipo de contrato", ["CLT", "PJ", "temporario", "estagio"])
            publico_alvo  = st.selectbox("Público-alvo", ["ambos", "masculino", "feminino"])
            horario       = st.text_input("Horário")
        vaga_pcd = st.checkbox("Vaga PcD")
        salvar = st.form_submit_button("Salvar vaga", type="primary")

    if salvar:
        if not titulo or not local or not empresa_nome:
            st.error("Preencha título, local e empresa.")
            return
        dados = {
            "titulo": titulo, "local": local, "salario": salario or None,
            "modalidade": modalidade, "tipo_contrato": tipo_contrato,
            "publico_alvo": publico_alvo, "horario": horario or None,
            "vaga_pcd": vaga_pcd, "status": "aberta",
            "quantidade_vagas": int(quantidade_vagas),
            "empresa_id": empresa_opcoes[empresa_nome],
        }
        resp = api_post("/vagas/", json=dados)
        if resp:
            st.success(f"✅ Vaga '{resp['titulo']}' criada com sucesso!")
            st.rerun()


# ── Detalhe da Vaga ───────────────────────────────────────────────────────────

def tela_detalhe(vaga_id):
    usuario = st.session_state.usuario
    perfil = usuario["perfil"]
    pode_escrever = perfil in ("admin", "recrutador")

    _sidebar()

    vaga = api_get(f"/vagas/{vaga_id}")
    if not vaga:
        st.session_state.pop("vaga_aberta", None)
        st.rerun()

    if st.button("← Voltar ao painel"):
        st.session_state.pop("vaga_aberta", None)
        st.rerun()

    st.markdown(f"# {vaga['titulo']}")
    st.markdown(f"**{vaga['empresa']['nome']}** — {vaga['local']}")

    status_badge = "🟢 Aberta" if vaga["status"] == "aberta" else "⚫ Encerrada"
    st.markdown(f"**Status:** {status_badge}")

    col1, col2, col3, col4, col5 = st.columns(5)
    salario = (
        f"R$ {vaga['salario']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        if vaga.get("salario") else "A combinar"
    )
    col1.metric("Salário", salario)
    col2.metric("Modalidade", MODALIDADE_LABEL.get(vaga["modalidade"], vaga["modalidade"]))
    col3.metric("Contrato", CONTRATO_LABEL.get(vaga["tipo_contrato"], vaga["tipo_contrato"]))
    col4.metric("PcD", "Sim ♿" if vaga.get("vaga_pcd") else "Não")
    col5.metric("Vagas", vaga.get("quantidade_vagas", 1))

    if vaga.get("horario"):
        st.markdown(f"**Horário:** {vaga['horario']}")

    if vaga.get("data_abertura"):
        abertura = vaga["data_abertura"]
        dias = (date.today() - date.fromisoformat(abertura)).days
        st.caption(f"📅 Aberta desde {abertura} ({dias} dias)")

    st.divider()

    col_ben, col_req = st.columns(2)
    with col_ben:
        st.markdown("### 🎁 Benefícios")
        if vaga.get("beneficios"):
            for b in vaga["beneficios"]:
                st.markdown(f"- {b['nome']}")
        else:
            st.caption("Não informado")

    with col_req:
        st.markdown("### 📋 Requisitos")
        if vaga.get("requisitos"):
            for r in vaga["requisitos"]:
                badge = "🔴 Obrigatório" if r["nivel"] == "obrigatorio" else "🔵 Desejável"
                st.markdown(f"- **{badge}** — {r['descricao']}")
        else:
            st.caption("Não informado")

    if pode_escrever:
        st.divider()
        st.markdown("### ⚙️ Ações")
        col_enc, col_del = st.columns(2)
        with col_enc:
            novo_status = "encerrada" if vaga["status"] == "aberta" else "aberta"
        label_btn = "⚫ Encerrar vaga" if vaga["status"] == "aberta" else "🟢 Reabrir vaga"
        with col_enc:
            if st.button(label_btn, use_container_width=True):
                dados = {k: vaga[k] for k in [
                    "titulo","local","salario","modalidade","horario","tipo_contrato",
                    "publico_alvo","vaga_pcd","empresa_id","quantidade_vagas",
                    "data_publicacao","data_abertura","data_fechamento"
                ] if k in vaga}
                dados["status"] = novo_status
                if novo_status == "encerrada":
                    dados["data_fechamento"] = str(date.today())
                resp = api_put(f"/vagas/{vaga_id}", json=dados)
                if resp:
                    st.success("Status atualizado!")
                    st.rerun()
        with col_del:
            if st.button("🗑️ Excluir vaga", use_container_width=True, type="secondary"):
                if api_delete(f"/vagas/{vaga_id}"):
                    st.success("Vaga excluída.")
                    st.session_state.pop("vaga_aberta", None)
                    st.rerun()


# ── Dashboard ─────────────────────────────────────────────────────────────────

def tela_dashboard():
    _sidebar()

    st.markdown("# 📊 Dashboard")

    vagas = api_get("/vagas/")
    empresas = api_get("/empresas/")
    if vagas is None or empresas is None:
        return

    abertas   = [v for v in vagas if v["status"] == "aberta"]
    encerradas = [v for v in vagas if v["status"] == "encerrada"]
    total_posicoes = sum(v.get("quantidade_vagas", 1) for v in abertas)
    pcd = [v for v in vagas if v.get("vaga_pcd")]

    # KPIs
    st.markdown("### 📈 Visão Geral")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total de Vagas", len(vagas))
    c2.metric("Vagas Abertas", len(abertas))
    c3.metric("Vagas Encerradas", len(encerradas))
    c4.metric("Posições Disponíveis", total_posicoes)
    c5.metric("Vagas PcD", len(pcd))

    st.divider()

    col_a, col_b = st.columns(2)

    # Vagas por modalidade
    with col_a:
        st.markdown("### 🏢 Vagas por Modalidade")
        contagem_mod = {}
        for v in vagas:
            m = MODALIDADE_LABEL.get(v["modalidade"], v["modalidade"])
            contagem_mod[m] = contagem_mod.get(m, 0) + 1
        for mod, qtd in sorted(contagem_mod.items(), key=lambda x: -x[1]):
            pct = qtd / len(vagas) * 100
            st.markdown(f"**{mod}** — {qtd} vaga(s)")
            st.progress(pct / 100)

    # Vagas por tipo de contrato
    with col_b:
        st.markdown("### 📄 Vagas por Contrato")
        contagem_cont = {}
        for v in vagas:
            c = CONTRATO_LABEL.get(v["tipo_contrato"], v["tipo_contrato"])
            contagem_cont[c] = contagem_cont.get(c, 0) + 1
        for cont, qtd in sorted(contagem_cont.items(), key=lambda x: -x[1]):
            pct = qtd / len(vagas) * 100
            st.markdown(f"**{cont}** — {qtd} vaga(s)")
            st.progress(pct / 100)

    st.divider()

    col_c, col_d = st.columns(2)

    # Vagas por empresa
    with col_c:
        st.markdown("### 🏭 Vagas por Empresa")
        contagem_emp = {}
        for v in vagas:
            nome = v["empresa"]["nome"]
            contagem_emp[nome] = contagem_emp.get(nome, 0) + 1
        for emp, qtd in sorted(contagem_emp.items(), key=lambda x: -x[1]):
            st.markdown(f"**{emp}** — {qtd} vaga(s)")

    # Faixa salarial por setor
    with col_d:
        st.markdown("### 💰 Salário Médio por Setor")
        setor_salarios = {}
        for v in vagas:
            if v.get("salario"):
                setor = v["empresa"].get("setor", "Outros")
                if setor not in setor_salarios:
                    setor_salarios[setor] = []
                setor_salarios[setor].append(v["salario"])
        for setor, salarios in sorted(setor_salarios.items()):
            media = sum(salarios) / len(salarios)
            media_fmt = f"R$ {media:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            st.markdown(f"**{setor}** — {media_fmt} (média de {len(salarios)} vaga(s))")

    st.divider()

    # Vagas paradas há muito tempo
    st.markdown("### ⚠️ Vagas Abertas Há Muito Tempo")
    hoje = date.today()
    vagas_antigas = []
    for v in abertas:
        if v.get("data_abertura"):
            dias = (hoje - date.fromisoformat(v["data_abertura"])).days
            vagas_antigas.append((v, dias))
        elif v.get("data_publicacao"):
            dias = (hoje - date.fromisoformat(v["data_publicacao"])).days
            vagas_antigas.append((v, dias))

    vagas_antigas.sort(key=lambda x: -x[1])
    alertas = [(v, d) for v, d in vagas_antigas if d >= 30]

    if alertas:
        for vaga, dias in alertas:
            cor = "🔴" if dias >= 90 else ("🟡" if dias >= 60 else "🟠")
            st.markdown(f"{cor} **{vaga['titulo']}** ({vaga['empresa']['nome']}) — {dias} dias aberta")
    else:
        st.success("✅ Nenhuma vaga aberta há mais de 30 dias.")


# ── Empresas (Admin) ──────────────────────────────────────────────────────────

def tela_empresas():
    _sidebar()

    st.markdown("# 🏭 Gerenciar Empresas")

    with st.expander("➕ Cadastrar nova empresa"):
        with st.form("form_nova_empresa"):
            col1, col2 = st.columns(2)
            with col1:
                nome   = st.text_input("Nome da empresa *")
                cnpj   = st.text_input("CNPJ *")
                setor  = st.text_input("Setor *")
            with col2:
                cidade = st.text_input("Cidade *")
                estado = st.text_input("Estado (UF) *", max_chars=2)
                descricao = st.text_area("Descrição")
            salvar = st.form_submit_button("Salvar empresa", type="primary")

        if salvar:
            if not nome or not cnpj or not setor or not cidade or not estado:
                st.error("Preencha todos os campos obrigatórios.")
            else:
                resp = api_post("/empresas/", json={
                    "nome": nome, "cnpj": cnpj, "setor": setor,
                    "cidade": cidade, "estado": estado.upper(), "descricao": descricao
                })
                if resp:
                    st.success(f"✅ Empresa '{resp['nome']}' cadastrada!")
                    st.rerun()

    empresas = api_get("/empresas/")
    if not empresas:
        st.info("Nenhuma empresa cadastrada.")
        return

    st.divider()
    st.caption(f"{len(empresas)} empresa(s) cadastrada(s)")

    for emp in empresas:
        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.markdown(f"**{emp['nome']}**")
                st.caption(f"CNPJ: {emp['cnpj']} | Setor: {emp['setor']}")
            with col2:
                st.caption(f"📍 {emp['cidade']}/{emp['estado']}")
                if emp.get("descricao"):
                    st.caption(emp["descricao"][:80] + "..." if len(emp.get("descricao","")) > 80 else emp.get("descricao",""))
            with col3:
                if st.button("🗑️ Excluir", key=f"del_emp_{emp['id']}", use_container_width=True):
                    if api_delete(f"/empresas/{emp['id']}"):
                        st.success("Empresa excluída.")
                        st.rerun()


# ── Usuários (Admin) ──────────────────────────────────────────────────────────

def tela_usuarios():
    _sidebar()

    st.markdown("# 👥 Gerenciar Usuários")

    with st.expander("➕ Criar novo usuário"):
        with st.form("form_novo_usuario"):
            col1, col2 = st.columns(2)
            with col1:
                nome_u  = st.text_input("Nome *")
                email_u = st.text_input("Email *")
            with col2:
                senha_u = st.text_input("Senha *", type="password")
                perfil_u = st.selectbox("Perfil", ["visualizador", "recrutador", "admin"])
            salvar_u = st.form_submit_button("Criar usuário", type="primary")

        if salvar_u:
            if not nome_u or not email_u or not senha_u:
                st.error("Preencha todos os campos.")
            else:
                resp = api_post("/auth/usuarios", json={
                    "nome": nome_u, "email": email_u,
                    "senha": senha_u, "perfil": perfil_u
                })
                if resp:
                    st.success(f"✅ Usuário '{resp['nome']}' criado com perfil {resp['perfil']}!")
                    st.rerun()

    st.info("ℹ️ A listagem de usuários requer endpoint adicional na API. Use o banco de dados para consultar diretamente.")


# ── Roteamento ────────────────────────────────────────────────────────────────

if not st.session_state.token:
    tela_login()
elif "vaga_aberta" in st.session_state:
    tela_detalhe(st.session_state["vaga_aberta"])
elif st.session_state.pagina == "dashboard":
    tela_dashboard()
elif st.session_state.pagina == "empresas":
    tela_empresas()
elif st.session_state.pagina == "usuarios":
    tela_usuarios()
else:
    tela_painel()

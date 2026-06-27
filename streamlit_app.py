"""
Agência de Empregos — Interface Streamlit
Consome a API FastAPI do backend.
Configure a URL da API em .streamlit/secrets.toml ou via variável de ambiente API_URL.
"""

import os
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
            kwargs["headers"] = {}  # form-urlencoded não usa JSON header
        r = requests.post(f"{API_URL}{path}", **kwargs)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        detail = e.response.json().get("detail", str(e)) if e.response else str(e)
        st.error(f"Erro: {detail}")
        return None


# ── Estado de sessão ──────────────────────────────────────────────────────────

if "token" not in st.session_state:
    st.session_state.token = None
if "usuario" not in st.session_state:
    st.session_state.usuario = None

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


# ── Painel de Vagas ───────────────────────────────────────────────────────────

def tela_painel():
    usuario = st.session_state.usuario
    perfil = usuario["perfil"]
    pode_escrever = perfil in ("admin", "recrutador")

    # Sidebar
    with st.sidebar:
        st.markdown(f"**{usuario['nome']}**")
        st.caption(PERFIL_LABEL.get(perfil, perfil))
        st.divider()

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

    # Header
    st.markdown("# 💼 Painel de Vagas")

    # Formulário de nova vaga (admin/recrutador)
    if pode_escrever:
        with st.expander("➕ Cadastrar nova vaga"):
            _form_nova_vaga()

    # Buscar vagas
    params = {}
    if modalidade:   params["modalidade"] = modalidade
    if contrato:     params["tipo_contrato"] = contrato
    if status_filtro: params["status"] = status_filtro
    if apenas_pcd:   params["vaga_pcd"] = True

    vagas = api_get("/vagas/", params=params)
    if vagas is None:
        return

    st.caption(f"{len(vagas)} vaga(s) encontrada(s)")
    st.divider()

    if not vagas:
        st.info("Nenhuma vaga encontrada para os filtros selecionados.")
        return

    # Grid de vagas
    cols = st.columns(3)
    for i, vaga in enumerate(vagas):
        with cols[i % 3]:
            _card_vaga(vaga)


def _card_vaga(vaga):
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
        st.markdown(
            f"`📍 {vaga['local']}` &nbsp; `{modalidade_icon} {MODALIDADE_LABEL.get(vaga['modalidade'], '')}` &nbsp; "
            f"`{CONTRATO_LABEL.get(vaga['tipo_contrato'], '')}` "
            + ("`♿ PcD`" if vaga.get("vaga_pcd") else ""),
            unsafe_allow_html=True,
        )
        st.markdown(f"**{salario}**")

        if st.button("Ver detalhes", key=f"vaga_{vaga['id']}", use_container_width=True):
            st.session_state["vaga_aberta"] = vaga["id"]
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
            empresa_opcoes = {e["nome"]: e["id"] for e in empresas}
            empresa_nome = st.selectbox("Empresa *", list(empresa_opcoes.keys()))
        with col2:
            modalidade   = st.selectbox("Modalidade", ["presencial", "remoto", "hibrido"])
            tipo_contrato = st.selectbox("Tipo de contrato", ["CLT", "PJ", "temporario", "estagio"])
            publico_alvo = st.selectbox("Público-alvo", ["ambos", "masculino", "feminino"])
            horario      = st.text_input("Horário")
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
            "empresa_id": empresa_opcoes[empresa_nome],
        }
        resp = api_post("/vagas/", json=dados)
        if resp:
            st.success(f"✅ Vaga '{resp['titulo']}' criada com sucesso!")
            st.rerun()


# ── Modal de Detalhe ──────────────────────────────────────────────────────────

def tela_detalhe(vaga_id):
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

    col1, col2, col3, col4 = st.columns(4)
    salario = (
        f"R$ {vaga['salario']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        if vaga.get("salario") else "A combinar"
    )
    col1.metric("Salário", salario)
    col2.metric("Modalidade", MODALIDADE_LABEL.get(vaga["modalidade"], vaga["modalidade"]))
    col3.metric("Contrato", CONTRATO_LABEL.get(vaga["tipo_contrato"], vaga["tipo_contrato"]))
    col4.metric("PcD", "Sim ♿" if vaga.get("vaga_pcd") else "Não")

    if vaga.get("horario"):
        st.markdown(f"**Horário:** {vaga['horario']}")

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


# ── Roteamento ────────────────────────────────────────────────────────────────

if not st.session_state.token:
    tela_login()
elif "vaga_aberta" in st.session_state:
    tela_detalhe(st.session_state["vaga_aberta"])
else:
    tela_painel()

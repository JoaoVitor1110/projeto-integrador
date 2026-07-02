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

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"], .stApp, .stMarkdown, .stButton, .stSelectbox,
.stTextInput, .stTextArea, .stNumberInput, .stDateInput, .stCheckbox,
.stRadio, .stMetric, h1, h2, h3, h4, h5, h6, p, div, span, label {
    font-family: 'Poppins', sans-serif !important;
}
/* Esconde a sidebar completamente */
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
/* Remove padding lateral padrão do Streamlit */
.block-container { padding-top: 0 !important; max-width: 100% !important; }
/* Navbar topo */
.navbar {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    background: #1565C0 !important;
    padding: 0 24px !important;
    height: 52px !important;
    margin-bottom: 0 !important;
}
.navbar-brand {
    color: #ffffff !important;
    font-size: 17px !important;
    font-weight: 700 !important;
    white-space: nowrap !important;
}
.navbar-user {
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
    color: #ffffff !important;
    font-size: 13px !important;
    white-space: nowrap !important;
}
.user-badge {
    background: rgba(255,255,255,0.25) !important;
    padding: 3px 10px !important;
    border-radius: 20px !important;
    font-size: 12px !important;
    color: #ffffff !important;
}
/* Faixa de colunas de navegação — identificada pelo marcador #navbar-btns */
[data-testid="stMarkdownContainer"]:has(#navbar-btns) + div[data-testid="stHorizontalBlock"],
[data-testid="stMarkdownContainer"]:has(#navbar-btns) ~ div > div[data-testid="stHorizontalBlock"]:first-child {
    background: #1565C0 !important;
    padding: 4px 16px 12px !important;
    border-radius: 0 0 12px 12px !important;
    box-shadow: 0 3px 10px rgba(0,0,0,0.18) !important;
    margin-bottom: 20px !important;
}
[data-testid="stMarkdownContainer"]:has(#navbar-btns) + div[data-testid="stHorizontalBlock"] button,
[data-testid="stMarkdownContainer"]:has(#navbar-btns) ~ div > div[data-testid="stHorizontalBlock"]:first-child button {
    background: transparent !important;
    color: rgba(255,255,255,0.88) !important;
    border-color: transparent !important;
    box-shadow: none !important;
}
[data-testid="stMarkdownContainer"]:has(#navbar-btns) + div[data-testid="stHorizontalBlock"] button[data-testid="stBaseButton-primary"],
[data-testid="stMarkdownContainer"]:has(#navbar-btns) ~ div > div[data-testid="stHorizontalBlock"]:first-child button[data-testid="stBaseButton-primary"] {
    background: rgba(255,255,255,0.25) !important;
    color: #ffffff !important;
}
/* Cards com tema compatível (dark/light) */
.card-info { background: #1565C020; border-radius: 12px; padding: 16px 20px; margin-bottom: 16px; }
.card-info .card-title { font-size: 18px; font-weight: 700; }
.card-info .card-sub { font-size: 13px; opacity: 0.75; margin-top: 4px; }
.cand-card { border-left: 4px solid; border-radius: 8px; padding: 12px 16px; margin-bottom: 10px; }
.cand-card-inner { display: flex; justify-content: space-between; align-items: center; }
.cand-titulo { font-weight: 700; font-size: 15px; }
.cand-sub { font-size: 13px; opacity: 0.7; margin-top: 2px; }
.cand-badge { padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600; color: #fff; white-space: nowrap; }
</style>
""", unsafe_allow_html=True)

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
PERFIL_LABEL     = {"admin": "👑 Admin", "recrutador": "📋 Recrutador", "visualizador": "🙋 Candidato"}

# ── Tela de Login ─────────────────────────────────────────────────────────────

def tela_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align:center;padding:20px 0 10px">
          <div style="font-size:48px">💼</div>
          <div style="font-size:28px;font-weight:700;color:#1565C0">Agência de Empregos</div>
          <div style="color:#666;margin-top:4px">Plataforma de gestão de vagas</div>
        </div>
        """, unsafe_allow_html=True)

        aba_login, aba_cadastro = st.tabs(["🔑 Entrar", "📝 Criar conta"])

        with aba_login:
            with st.form("form_login"):
                email = st.text_input("Email", placeholder="seu@email.com")
                senha = st.text_input("Senha", type="password", placeholder="••••••••")
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

        with aba_cadastro:
            st.caption("Crie sua conta gratuitamente para visualizar e se candidatar às vagas.")
            with st.form("form_cadastro"):
                nome_c  = st.text_input("Nome completo *", placeholder="João Silva")
                email_c = st.text_input("Email *", placeholder="seu@email.com")
                senha_c = st.text_input("Senha *", type="password", placeholder="Mínimo 6 caracteres")
                senha2  = st.text_input("Confirmar senha *", type="password")
                cadastrar = st.form_submit_button("Criar conta", use_container_width=True, type="primary")
            if cadastrar:
                if not nome_c or not email_c or not senha_c:
                    st.error("Preencha todos os campos.")
                elif senha_c != senha2:
                    st.error("As senhas não coincidem.")
                elif len(senha_c) < 6:
                    st.error("A senha deve ter pelo menos 6 caracteres.")
                else:
                    data = api_post("/auth/registro", json={"nome": nome_c, "email": email_c, "senha": senha_c, "perfil": "visualizador"})
                    if data:
                        st.session_state.token = data["access_token"]
                        st.session_state.usuario = data["usuario"]
                        st.success(f"Bem-vindo(a), {nome_c}!")
                        st.rerun()


# ── Navbar ────────────────────────────────────────────────────────────────────

def _navbar():
    usuario = st.session_state.usuario
    perfil = usuario["perfil"]
    pode_escrever = perfil in ("admin", "recrutador")
    pagina_atual = st.session_state.get("pagina", "vagas")
    badge = PERFIL_LABEL.get(perfil, perfil)

    itens = [("💼 Vagas", "vagas")]
    if pode_escrever:
        itens.append(("📊 Dashboard", "dashboard"))
    if perfil == "admin":
        itens.append(("🏭 Empresas", "empresas"))
        itens.append(("👤 Candidatos", "candidatos"))
        itens.append(("👥 Usuários", "usuarios"))
    if perfil == "visualizador":
        itens.append(("📋 Candidaturas", "candidaturas"))
    itens.append(("🤖 Assistente", "assistente"))

    # Renderiza navbar e botões em um único container azul
    st.markdown(f"""
    <div class="navbar">
        <div class="navbar-brand">💼 Agência de Empregos</div>
        <div class="navbar-user">
            <span>{usuario['nome']}</span>
            <span class="user-badge">{badge}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<span id="navbar-btns"></span>', unsafe_allow_html=True)

    cols = st.columns(len(itens) + 1)
    for i, (label, pagina) in enumerate(itens):
        with cols[i]:
            ativo = pagina == pagina_atual
            if st.button(label, key=f"nav_{pagina}", use_container_width=True,
                         type="primary" if ativo else "secondary"):
                st.session_state.pagina = pagina
                for k in ("vaga_aberta", "vaga_editar", "empresa_editar", "candidato_editar"):
                    st.session_state.pop(k, None)
                st.rerun()
    with cols[-1]:
        if st.button("🚪 Sair", key="nav_sair", use_container_width=True):
            st.session_state.clear()
            st.rerun()


def _filtros_inline():
    with st.expander("🔍 Filtros", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            modalidade = st.selectbox(
                "Modalidade",
                ["", "presencial", "remoto", "hibrido"],
                format_func=lambda x: "Todas" if x == "" else MODALIDADE_LABEL.get(x, x),
                key="filtro_modalidade",
            )
        with col2:
            contrato = st.selectbox(
                "Tipo de contrato",
                ["", "CLT", "PJ", "temporario", "estagio"],
                format_func=lambda x: "Todos" if x == "" else CONTRATO_LABEL.get(x, x),
                key="filtro_contrato",
            )
        with col3:
            status_filtro = st.selectbox(
                "Status",
                ["", "aberta", "encerrada"],
                format_func=lambda x: "Qualquer" if x == "" else x.capitalize(),
                key="filtro_status",
            )
        with col4:
            apenas_pcd = st.checkbox("Somente vagas PcD ♿", key="filtro_pcd")
    return modalidade, contrato, status_filtro, apenas_pcd


# ── Painel de Vagas ───────────────────────────────────────────────────────────

def tela_painel():
    usuario = st.session_state.usuario
    perfil = usuario["perfil"]
    pode_escrever = perfil in ("admin", "recrutador")

    _navbar()
    modalidade, contrato, status_filtro, apenas_pcd = _filtros_inline()

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

        if pode_escrever:
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("Ver detalhes", key=f"det_{vaga['id']}", use_container_width=True):
                    st.session_state["vaga_aberta"] = vaga["id"]
                    st.rerun()
            with col_btn2:
                if st.button("✏️ Editar", key=f"edit_{vaga['id']}", use_container_width=True):
                    st.session_state["vaga_editar"] = vaga["id"]
                    st.rerun()
        else:
            if st.button("Ver detalhes", key=f"det_{vaga['id']}", use_container_width=True):
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
            quantidade_vagas = st.number_input("Quantidade de vagas", min_value=1, step=1, value=1)
            empresa_opcoes = {e["nome"]: e["id"] for e in empresas}
            empresa_nome = st.selectbox("Empresa *", list(empresa_opcoes.keys()))
        with col2:
            modalidade    = st.selectbox("Modalidade", ["presencial", "remoto", "hibrido"])
            tipo_contrato = st.selectbox("Tipo de contrato", ["CLT", "PJ", "temporario", "estagio"])
            publico_alvo  = st.selectbox("Público-alvo", ["ambos", "masculino", "feminino"])
            horario       = st.text_input("Horário")
        descricao = st.text_area("Descrição da vaga", placeholder="Descreva as responsabilidades, o que a pessoa vai fazer no dia a dia...")
        vaga_pcd = st.checkbox("Vaga PcD")
        salvar = st.form_submit_button("Salvar vaga", type="primary")

    if salvar:
        if not titulo or not local or not empresa_nome:
            st.error("Preencha título, local e empresa.")
            return
        dados = {
            "titulo": titulo, "local": local, "descricao": descricao or None,
            "salario": salario or None,
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

    _navbar()

    vaga = api_get(f"/vagas/{vaga_id}")
    if not vaga:
        st.session_state.pop("vaga_aberta", None)
        st.rerun()

    if st.button("← Voltar ao painel"):
        st.session_state.pop("vaga_aberta", None)
        st.rerun()

    st.markdown(f"### {vaga['titulo']}")
    st.caption(f"{vaga['empresa']['nome']} — {vaga['local']}")

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

    # Descrição
    if vaga.get("descricao"):
        st.markdown("**📝 Sobre a vaga**")
        st.markdown(vaga["descricao"])
        st.divider()

    col_ben, col_req = st.columns(2)
    with col_ben:
        st.markdown("**🎁 Benefícios**")
        if vaga.get("beneficios"):
            for b in vaga["beneficios"]:
                st.caption(f"• {b['nome']}")
        else:
            st.caption("Não informado")

    with col_req:
        st.markdown("**📋 Requisitos**")
        if vaga.get("requisitos"):
            for r in vaga["requisitos"]:
                badge = "🔴 Obrigatório" if r["nivel"] == "obrigatorio" else "🔵 Desejável"
                st.caption(f"{badge} — {r['descricao']}")
        else:
            st.caption("Não informado")

    st.divider()

    if pode_escrever:
        # Candidatos que se inscreveram nessa vaga
        st.markdown("### 👥 Candidatos Inscritos")
        candidaturas_vaga = api_get("/candidaturas/", params={"vaga_id": vaga_id})
        if not candidaturas_vaga:
            st.info("Nenhum candidato inscrito ainda.")
        else:
            STATUS_COR = {"pendente": "#F9A825", "em_analise": "#1565C0", "aprovado": "#2E7D32", "reprovado": "#B71C1C"}
            STATUS_LABEL = {"pendente": "⏳ Pendente", "em_analise": "🔍 Em análise", "aprovado": "✅ Aprovado", "reprovado": "❌ Reprovado"}
            st.caption(f"{len(candidaturas_vaga)} candidato(s) inscrito(s)")
            for cand in candidaturas_vaga:
                c = cand.get("candidato", {})
                status = cand.get("status", "pendente")
                cor = STATUS_COR.get(status, "#555")
                with st.container(border=True):
                    col_info, col_status, col_acao = st.columns([3, 2, 2])
                    with col_info:
                        st.markdown(f"**{c.get('nome', '—')}**")
                        st.caption(f"✉️ {c.get('email', '—')}")
                        if c.get("telefone"):
                            st.caption(f"📞 {c['telefone']}")
                        if c.get("cidade"):
                            st.caption(f"📍 {c['cidade']}/{c.get('estado','')}")
                    with col_status:
                        st.markdown(f"<span style='background:{cor};color:white;padding:4px 10px;border-radius:12px;font-size:12px'>{STATUS_LABEL.get(status, status)}</span>", unsafe_allow_html=True)
                        st.caption(f"📅 {cand.get('data_candidatura', '')}")
                    with col_acao:
                        novo = st.selectbox(
                            "Atualizar",
                            ["pendente", "em_analise", "aprovado", "reprovado"],
                            index=["pendente", "em_analise", "aprovado", "reprovado"].index(status),
                            key=f"sel_status_{cand['id']}",
                            format_func=lambda x: STATUS_LABEL.get(x, x),
                            label_visibility="collapsed",
                        )
                        if st.button("Salvar", key=f"btn_status_{cand['id']}", use_container_width=True):
                            r = api_put(f"/candidaturas/{cand['id']}/status", json={"status": novo})
                            if r:
                                st.success("Status atualizado!")
                                st.rerun()

        st.divider()
        st.markdown("**⚙️ Ações**")
        col_enc, col_del = st.columns(2)
        novo_status = "encerrada" if vaga["status"] == "aberta" else "aberta"
        label_btn = "⚫ Encerrar vaga" if vaga["status"] == "aberta" else "🟢 Reabrir vaga"
        with col_enc:
            if st.button(label_btn, use_container_width=True):
                dados = {k: vaga[k] for k in [
                    "titulo","local","descricao","salario","modalidade","horario","tipo_contrato",
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

    elif perfil == "visualizador" and vaga["status"] == "aberta":
        st.markdown("### 🚀 Candidatar-se")
        candidatos = api_get("/candidatos/")
        usuario = st.session_state.usuario
        candidato_id = None
        ja_inscrito = False
        if candidatos:
            for c in candidatos:
                if c.get("email") == usuario.get("email"):
                    candidato_id = c["id"]
                    break

        if candidato_id:
            # Verifica se já está inscrito
            candidaturas_existentes = api_get("/candidaturas/", params={"vaga_id": vaga_id}) or []
            ja_inscrito = any(c.get("candidato_id") == candidato_id for c in candidaturas_existentes)

            if ja_inscrito:
                st.success("✅ Você já está inscrito nessa vaga!")
            else:
                if st.button("✅ Candidatar-se a esta vaga", use_container_width=True, type="primary"):
                    resp = api_post("/candidaturas/", json={
                        "candidato_id": candidato_id,
                        "vaga_id": vaga_id,
                    })
                    if resp:
                        st.success("Candidatura enviada com sucesso!")
                        st.rerun()
        else:
            st.info("Complete seu perfil de candidato para se candidatar.")
            if st.button("📝 Completar perfil", use_container_width=True, type="primary"):
                st.session_state.pagina = "candidaturas"
                st.session_state.pop("vaga_aberta", None)
                st.rerun()


# ── Dashboard ─────────────────────────────────────────────────────────────────

def _barra_horizontal(label, valor, total, cor="#1f77b4"):
    pct = valor / total * 100 if total else 0
    st.markdown(f"""
    <div style="margin-bottom:8px">
      <div style="display:flex;justify-content:space-between;margin-bottom:2px">
        <span style="font-size:13px">{label}</span>
        <span style="font-size:13px;font-weight:600">{valor} ({pct:.0f}%)</span>
      </div>
      <div style="background:#e0e0e0;border-radius:6px;height:18px">
        <div style="background:{cor};width:{pct}%;height:18px;border-radius:6px;transition:width 0.3s"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)


def _kpi(label, valor, cor_fundo, emoji):
    st.markdown(f"""
    <div style="background:{cor_fundo};border-radius:12px;padding:16px 20px;text-align:center;margin-bottom:8px">
      <div style="font-size:28px">{emoji}</div>
      <div style="font-size:28px;font-weight:700;color:#111">{valor}</div>
      <div style="font-size:12px;color:#555;margin-top:4px">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def tela_dashboard():
    _navbar()

    st.markdown("# 📊 Dashboard")

    vagas = api_get("/vagas/")
    empresas = api_get("/empresas/")
    if vagas is None or empresas is None:
        return

    abertas    = [v for v in vagas if v["status"] == "aberta"]
    encerradas = [v for v in vagas if v["status"] == "encerrada"]
    total_posicoes = sum(v.get("quantidade_vagas", 1) for v in abertas)
    pcd = [v for v in vagas if v.get("vaga_pcd")]

    # KPIs coloridos
    st.markdown("### 📈 Visão Geral")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: _kpi("Total de Vagas",        len(vagas),         "#e3f2fd", "💼")
    with c2: _kpi("Vagas Abertas",         len(abertas),       "#e8f5e9", "🟢")
    with c3: _kpi("Vagas Encerradas",      len(encerradas),    "#fce4ec", "⚫")
    with c4: _kpi("Posições Disponíveis",  total_posicoes,     "#fff8e1", "📌")
    with c5: _kpi("Vagas PcD",             len(pcd),           "#f3e5f5", "♿")

    st.divider()

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("### 🏢 Vagas por Modalidade")
        contagem_mod = {}
        for v in vagas:
            m = MODALIDADE_LABEL.get(v["modalidade"], v["modalidade"])
            contagem_mod[m] = contagem_mod.get(m, 0) + 1
        total_mod = sum(contagem_mod.values())
        for label, val in sorted(contagem_mod.items(), key=lambda x: -x[1]):
            _barra_horizontal(label, val, total_mod, "#1565C0")

    with col_b:
        st.markdown("### 📄 Vagas por Contrato")
        contagem_cont = {}
        for v in vagas:
            c = CONTRATO_LABEL.get(v["tipo_contrato"], v["tipo_contrato"])
            contagem_cont[c] = contagem_cont.get(c, 0) + 1
        total_cont = sum(contagem_cont.values())
        for label, val in sorted(contagem_cont.items(), key=lambda x: -x[1]):
            _barra_horizontal(label, val, total_cont, "#2E7D32")

    st.divider()

    col_c, col_d = st.columns(2)

    with col_c:
        st.markdown("### 🏭 Vagas por Empresa")
        contagem_emp = {}
        for v in vagas:
            nome = v["empresa"]["nome"]
            contagem_emp[nome] = contagem_emp.get(nome, 0) + 1
        total_emp = sum(contagem_emp.values())
        for label, val in sorted(contagem_emp.items(), key=lambda x: -x[1]):
            _barra_horizontal(label, val, total_emp, "#6A1B9A")

    with col_d:
        st.markdown("### 💰 Salário Médio por Setor")
        setor_salarios = {}
        for v in vagas:
            if v.get("salario"):
                setor = v["empresa"].get("setor", "Outros")
                setor_salarios.setdefault(setor, []).append(v["salario"])

        if setor_salarios:
            maior = max(sum(s)/len(s) for s in setor_salarios.values())
            for setor, salarios in sorted(setor_salarios.items(), key=lambda x: -sum(x[1])/len(x[1])):
                media = sum(salarios) / len(salarios)
                media_fmt = f"R$ {media:,.0f}".replace(",", ".")
                pct = media / maior * 100
                st.markdown(f"""
                <div style="margin-bottom:8px">
                  <div style="display:flex;justify-content:space-between;margin-bottom:2px">
                    <span style="font-size:13px">{setor}</span>
                    <span style="font-size:13px;font-weight:600">{media_fmt}</span>
                  </div>
                  <div style="background:#e0e0e0;border-radius:6px;height:18px">
                    <div style="background:#E65100;width:{pct:.0f}%;height:18px;border-radius:6px"></div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

    st.divider()

    # Status aberta vs encerrada — mini visual
    st.markdown("### 📉 Status das Vagas")
    col_s1, col_s2, col_s3 = st.columns([2, 2, 3])
    with col_s1:
        pct_ab = len(abertas) / len(vagas) * 100 if vagas else 0
        st.markdown(f"""
        <div style="background:#e8f5e9;border-radius:12px;padding:16px;text-align:center">
          <div style="font-size:36px;font-weight:700;color:#2E7D32">{pct_ab:.0f}%</div>
          <div style="color:#555">das vagas estão abertas</div>
          <div style="font-size:12px;color:#888">{len(abertas)} de {len(vagas)}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_s2:
        pct_enc = len(encerradas) / len(vagas) * 100 if vagas else 0
        st.markdown(f"""
        <div style="background:#fce4ec;border-radius:12px;padding:16px;text-align:center">
          <div style="font-size:36px;font-weight:700;color:#B71C1C">{pct_enc:.0f}%</div>
          <div style="color:#555">das vagas estão encerradas</div>
          <div style="font-size:12px;color:#888">{len(encerradas)} de {len(vagas)}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_s3:
        pct_pcd = len(pcd) / len(vagas) * 100 if vagas else 0
        st.markdown(f"""
        <div style="background:#f3e5f5;border-radius:12px;padding:16px;text-align:center">
          <div style="font-size:36px;font-weight:700;color:#6A1B9A">{pct_pcd:.0f}%</div>
          <div style="color:#555">das vagas são PcD</div>
          <div style="font-size:12px;color:#888">{len(pcd)} de {len(vagas)} vagas inclusivas</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Alertas de vagas paradas
    st.markdown("### ⚠️ Vagas Abertas Há Muito Tempo")
    hoje = date.today()
    vagas_antigas = []
    for v in abertas:
        ref = v.get("data_abertura") or v.get("data_publicacao")
        if ref:
            dias = (hoje - date.fromisoformat(ref)).days
            vagas_antigas.append((v, dias))

    vagas_antigas.sort(key=lambda x: -x[1])
    alertas = [(v, d) for v, d in vagas_antigas if d >= 60][:10]

    if alertas:
        for vaga, dias in alertas:
            if dias >= 90:
                cor, bg, icone = "#B71C1C", "#fce4ec", "🔴"
            elif dias >= 60:
                cor, bg, icone = "#E65100", "#fff3e0", "🟠"
            else:
                cor, bg, icone = "#F9A825", "#fffde7", "🟡"
            st.markdown(f"""
            <div style="background:{bg};border-left:4px solid {cor};border-radius:6px;padding:10px 14px;margin-bottom:8px">
              {icone} <strong>{vaga['titulo']}</strong> — {vaga['empresa']['nome']}
              <span style="float:right;color:{cor};font-weight:600">{dias} dias aberta</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ Nenhuma vaga aberta há mais de 30 dias.")


# ── Empresas (Admin) ──────────────────────────────────────────────────────────

def tela_empresas():
    _navbar()

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
                if st.button("✏️", key=f"edit_emp_{emp['id']}", use_container_width=True, help="Editar empresa"):
                    st.session_state["empresa_editar"] = emp["id"]
                    st.rerun()
                if st.button("🗑️", key=f"del_emp_{emp['id']}", use_container_width=True, help="Excluir empresa"):
                    if api_delete(f"/empresas/{emp['id']}"):
                        st.success("Empresa excluída.")
                        st.rerun()


# ── Usuários (Admin) ──────────────────────────────────────────────────────────

def tela_usuarios():
    _navbar()

    st.markdown("# 👥 Gerenciar Usuários")

    with st.expander("➕ Criar novo usuário"):
        with st.form("form_novo_usuario"):
            col1, col2 = st.columns(2)
            with col1:
                nome_u  = st.text_input("Nome *")
                email_u = st.text_input("Email *")
            with col2:
                senha_u = st.text_input("Senha *", type="password")
                perfil_u = st.selectbox(
                    "Perfil",
                    ["visualizador", "recrutador", "admin"],
                    format_func=lambda x: {"visualizador": "Candidato", "recrutador": "Recrutador", "admin": "Admin"}.get(x, x),
                )
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

    usuarios = api_get("/auth/usuarios")
    if not usuarios:
        st.info("Nenhum usuário cadastrado.")
        return

    st.divider()
    st.caption(f"{len(usuarios)} usuário(s) cadastrado(s)")

    usuario_atual = st.session_state.usuario

    PERFIL_COR = {"admin": "#6A1B9A", "recrutador": "#1565C0", "visualizador": "#2E7D32"}

    for u in usuarios:
        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.markdown(f"**{u['nome']}**")
                st.caption(u["email"])
            with col2:
                cor = PERFIL_COR.get(u["perfil"], "#555")
                st.markdown(f"<span style='background:{cor};color:white;padding:2px 10px;border-radius:12px;font-size:12px'>{PERFIL_LABEL.get(u['perfil'], u['perfil'])}</span>", unsafe_allow_html=True)
            with col3:
                eh_voce = u["id"] == usuario_atual["id"]
                if eh_voce:
                    st.caption("(você)")
                else:
                    if st.button("🗑️", key=f"del_usr_{u['id']}", help="Excluir usuário", use_container_width=True):
                        ok = api_delete(f"/auth/usuarios/{u['id']}")
                        if ok:
                            st.success(f"Usuário '{u['nome']}' excluído.")
                            st.rerun()


# ── Candidaturas (Visualizador) ───────────────────────────────────────────────

def tela_candidaturas():
    _navbar()
    usuario = st.session_state.usuario

    st.markdown("# 📋 Meu Perfil de Candidato")

    candidatos = api_get("/candidatos/")
    candidato = None
    if candidatos:
        for c in candidatos:
            if c.get("email") == usuario.get("email"):
                candidato = c
                break

    def _form_perfil_candidato(candidato=None):
        is_edit = candidato is not None
        label_btn = "Salvar alterações" if is_edit else "Salvar perfil"
        with st.form("form_candidato"):
            col1, col2 = st.columns(2)
            with col1:
                telefone = st.text_input("Telefone", value=candidato.get("telefone") or "" if is_edit else "")
            with col2:
                cidade = st.text_input("Cidade", value=candidato.get("cidade") or "" if is_edit else "")
                estado = st.text_input("Estado (UF)", max_chars=2, value=candidato.get("estado") or "" if is_edit else "")
            nasc_val = None
            if is_edit and candidato.get("data_nascimento"):
                try:
                    from datetime import date as _d
                    nasc_val = _d.fromisoformat(candidato["data_nascimento"])
                except Exception:
                    pass
            nasc = st.date_input("Data de nascimento", value=nasc_val)
            salvar = st.form_submit_button(label_btn, type="primary")
        return telefone, cidade, estado, nasc, salvar

    if not candidato:
        st.info("Complete seu perfil com dados de contato para se candidatar às vagas.")
        telefone, cidade, estado, nasc, salvar = _form_perfil_candidato()
        if salvar:
            resp = api_post("/candidatos/", json={
                "nome": usuario.get("nome"),
                "email": usuario.get("email"),
                "telefone": telefone or None,
                "cidade": cidade or None,
                "estado": estado.upper() if estado else None,
                "data_nascimento": str(nasc) if nasc else None,
            })
            if resp:
                st.success("Perfil criado! Agora você pode se candidatar às vagas.")
                st.rerun()
        return

    # Perfil existente
    loc = f"📍 {candidato['cidade']}/{candidato['estado']}" if candidato.get("cidade") else ""
    tel = f"📞 {candidato['telefone']}" if candidato.get("telefone") else ""
    sub = "  ·  ".join(filter(None, [candidato["email"], tel, loc]))
    st.markdown(f"""
    <div class="card-info">
      <div class="card-title">👤 {candidato['nome']}</div>
      <div class="card-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("✏️ Editar dados de contato"):
        telefone, cidade, estado, nasc, salvar = _form_perfil_candidato(candidato)
        if salvar:
            resp = api_put(f"/candidatos/{candidato['id']}", json={
                "nome": candidato["nome"],
                "email": candidato["email"],
                "telefone": telefone or None,
                "cidade": cidade or None,
                "estado": estado.upper() if estado else None,
                "data_nascimento": str(nasc) if nasc else None,
            })
            if resp:
                st.success("Dados atualizados!")
                st.rerun()

    st.markdown("### 📄 Minhas Candidaturas")
    candidaturas = api_get("/candidaturas/")
    minhas = [c for c in (candidaturas or []) if c.get("candidato_id") == candidato["id"]]

    STATUS_COR = {
        "pendente":   "#F9A825",
        "em_analise": "#1565C0",
        "aprovado":   "#2E7D32",
        "reprovado":  "#B71C1C",
    }
    STATUS_LABEL = {
        "pendente": "⏳ Pendente",
        "em_analise": "🔍 Em análise",
        "aprovado": "✅ Aprovado",
        "reprovado": "❌ Reprovado",
    }

    if not minhas:
        st.info("Você ainda não se candidatou a nenhuma vaga. Explore as vagas disponíveis!")
        if st.button("💼 Ver vagas", type="primary"):
            st.session_state.pagina = "vagas"
            st.rerun()
        return

    # Cache de vagas para evitar múltiplas requisições
    _vagas_cache = {}
    def _get_vaga(vaga_id):
        if vaga_id not in _vagas_cache:
            v = api_get(f"/vagas/{vaga_id}")
            _vagas_cache[vaga_id] = v or {}
        return _vagas_cache[vaga_id]

    for cand in minhas:
        vaga_id = cand.get("vaga_id")
        vaga_inline = cand.get("vaga") or {}
        titulo = vaga_inline.get("titulo")
        empresa_nome = (vaga_inline.get("empresa") or {}).get("nome")
        # Se faltou título, busca a vaga completa
        if not titulo and vaga_id:
            vaga_full = _get_vaga(vaga_id)
            titulo = vaga_full.get("titulo", "—")
            empresa_nome = empresa_nome or (vaga_full.get("empresa") or {}).get("nome", "—")
        status = cand.get("status", "pendente")
        cor = STATUS_COR.get(status, "#555")
        st.markdown(f"""
        <div class="cand-card" style="border-color:{cor}">
          <div class="cand-card-inner">
            <div>
              <div class="cand-titulo">{titulo or '—'}</div>
              <div class="cand-sub">🏭 {empresa_nome or '—'} &nbsp;|&nbsp; 📅 {cand.get('data_candidatura','')}</div>
            </div>
            <div class="cand-badge" style="background:{cor}">{STATUS_LABEL.get(status, status)}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)


# ── Editar Vaga ───────────────────────────────────────────────────────────────

def tela_editar_vaga(vaga_id):
    _navbar()

    vaga = api_get(f"/vagas/{vaga_id}")
    if not vaga:
        st.session_state.pop("vaga_editar", None)
        st.rerun()

    if st.button("← Voltar"):
        st.session_state.pop("vaga_editar", None)
        st.rerun()

    st.markdown(f"### ✏️ Editar: {vaga['titulo']}")

    empresas = api_get("/empresas/") or []
    empresa_opcoes = {e["nome"]: e["id"] for e in empresas}
    empresa_atual = next((e["nome"] for e in empresas if e["id"] == vaga["empresa_id"]), None)

    with st.form("form_editar_vaga"):
        col1, col2 = st.columns(2)
        with col1:
            titulo   = st.text_input("Título *", value=vaga["titulo"])
            local    = st.text_input("Local *", value=vaga["local"])
            salario  = st.number_input("Salário (R$)", min_value=0.0, step=100.0, value=float(vaga["salario"] or 0))
            qtd      = st.number_input("Quantidade de vagas", min_value=1, step=1, value=vaga.get("quantidade_vagas", 1))
            empresa_nome = st.selectbox("Empresa *", list(empresa_opcoes.keys()),
                                        index=list(empresa_opcoes.keys()).index(empresa_atual) if empresa_atual else 0)
        with col2:
            modalidades = ["presencial", "remoto", "hibrido"]
            contratos   = ["CLT", "PJ", "temporario", "estagio"]
            publicos    = ["ambos", "masculino", "feminino"]
            modalidade    = st.selectbox("Modalidade", modalidades,
                                         index=modalidades.index(vaga["modalidade"]))
            tipo_contrato = st.selectbox("Tipo de contrato", contratos,
                                         index=contratos.index(vaga["tipo_contrato"]))
            publico_alvo  = st.selectbox("Público-alvo", publicos,
                                         index=publicos.index(vaga.get("publico_alvo", "ambos")))
            horario = st.text_input("Horário", value=vaga.get("horario") or "")
        descricao = st.text_area("Descrição da vaga", value=vaga.get("descricao") or "")
        vaga_pcd = st.checkbox("Vaga PcD", value=vaga.get("vaga_pcd", False))
        status   = st.selectbox("Status", ["aberta", "encerrada"],
                                 index=0 if vaga["status"] == "aberta" else 1)
        salvar = st.form_submit_button("Salvar alterações", type="primary")

    if salvar:
        dados = {
            "titulo": titulo, "local": local, "descricao": descricao or None,
            "salario": salario or None,
            "modalidade": modalidade, "tipo_contrato": tipo_contrato,
            "publico_alvo": publico_alvo, "horario": horario or None,
            "vaga_pcd": vaga_pcd, "status": status,
            "quantidade_vagas": int(qtd),
            "empresa_id": empresa_opcoes[empresa_nome],
        }
        resp = api_put(f"/vagas/{vaga_id}", json=dados)
        if resp:
            st.success("✅ Vaga atualizada!")
            st.session_state.pop("vaga_editar", None)
            st.rerun()


# ── Roteamento ────────────────────────────────────────────────────────────────

# ── Editar Empresa ────────────────────────────────────────────────────────────

def tela_editar_empresa(empresa_id):
    _navbar()

    emp = api_get(f"/empresas/{empresa_id}")
    if not emp:
        st.session_state.pop("empresa_editar", None)
        st.rerun()

    if st.button("← Voltar"):
        st.session_state.pop("empresa_editar", None)
        st.rerun()

    st.markdown(f"### ✏️ Editar: {emp['nome']}")

    with st.form("form_editar_empresa"):
        col1, col2 = st.columns(2)
        with col1:
            nome   = st.text_input("Nome *", value=emp["nome"])
            cnpj   = st.text_input("CNPJ *", value=emp["cnpj"])
            setor  = st.text_input("Setor *", value=emp["setor"])
        with col2:
            cidade = st.text_input("Cidade *", value=emp["cidade"])
            estado = st.text_input("Estado (UF) *", value=emp["estado"], max_chars=2)
            descricao = st.text_area("Descrição", value=emp.get("descricao") or "")
        salvar = st.form_submit_button("Salvar alterações", type="primary")

    if salvar:
        if not nome or not cnpj or not setor or not cidade or not estado:
            st.error("Preencha todos os campos obrigatórios.")
        else:
            resp = api_put(f"/empresas/{empresa_id}", json={
                "nome": nome, "cnpj": cnpj, "setor": setor,
                "cidade": cidade, "estado": estado.upper(), "descricao": descricao or None,
            })
            if resp:
                st.success("✅ Empresa atualizada!")
                st.session_state.pop("empresa_editar", None)
                st.rerun()


# ── Candidatos (Admin) ────────────────────────────────────────────────────────

def tela_candidatos():
    _navbar()

    st.markdown("# 👤 Candidatos")

    candidatos = api_get("/candidatos/")
    if not candidatos:
        st.info("Nenhum candidato cadastrado.")
        return

    st.caption(f"{len(candidatos)} candidato(s) cadastrado(s)")
    st.divider()

    for c in candidatos:
        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.markdown(f"**{c['nome']}**")
                st.caption(c["email"])
            with col2:
                info = []
                if c.get("telefone"): info.append(f"📞 {c['telefone']}")
                if c.get("cidade"):   info.append(f"📍 {c['cidade']}/{c['estado']}")
                st.caption("  |  ".join(info) if info else "Sem dados de contato")
            with col3:
                if st.button("✏️", key=f"edit_cand_{c['id']}", use_container_width=True, help="Editar"):
                    st.session_state["candidato_editar"] = c["id"]
                    st.rerun()


def tela_editar_candidato(candidato_id):
    _navbar()

    c = api_get(f"/candidatos/{candidato_id}")
    if not c:
        st.session_state.pop("candidato_editar", None)
        st.rerun()

    if st.button("← Voltar"):
        st.session_state.pop("candidato_editar", None)
        st.rerun()

    st.markdown(f"### ✏️ Editar: {c['nome']}")

    with st.form("form_editar_candidato"):
        col1, col2 = st.columns(2)
        with col1:
            nome     = st.text_input("Nome *", value=c["nome"])
            email    = st.text_input("Email *", value=c["email"])
            telefone = st.text_input("Telefone", value=c.get("telefone") or "")
        with col2:
            cidade  = st.text_input("Cidade", value=c.get("cidade") or "")
            estado  = st.text_input("Estado (UF)", value=c.get("estado") or "", max_chars=2)
            nasc_val = None
            if c.get("data_nascimento"):
                try:
                    from datetime import date as _date
                    nasc_val = _date.fromisoformat(c["data_nascimento"])
                except Exception:
                    pass
            nasc = st.date_input("Data de nascimento", value=nasc_val)
        salvar = st.form_submit_button("Salvar alterações", type="primary")

    if salvar:
        resp = api_put(f"/candidatos/{candidato_id}", json={
            "nome": nome, "email": email,
            "telefone": telefone or None,
            "cidade": cidade or None,
            "estado": estado.upper() if estado else None,
            "data_nascimento": str(nasc) if nasc else None,
        })
        if resp:
            st.success("✅ Candidato atualizado!")
            st.session_state.pop("candidato_editar", None)
            st.rerun()


# ── Assistente IA ─────────────────────────────────────────────────────────────

def _contexto_sistema():
    """Busca dados do backend para montar contexto da IA."""
    token = st.session_state.token
    h = {"Authorization": f"Bearer {token}"}
    linhas = []
    try:
        vagas = requests.get(f"{API}/vagas/", headers=h, timeout=10).json()
        abertas = [v for v in vagas if v.get("status") == "aberta"]
        linhas.append(f"Total de vagas cadastradas: {len(vagas)} ({len(abertas)} abertas, {len(vagas)-len(abertas)} encerradas).")
        for v in abertas[:15]:
            empresa = v.get("empresa", {}).get("nome", "N/A") if isinstance(v.get("empresa"), dict) else "N/A"
            linhas.append(
                f"- Vaga: {v['titulo']} | Empresa: {empresa} | "
                f"Modalidade: {v.get('modalidade','')} | Contrato: {v.get('tipo_contrato','')} | "
                f"Salário: R$ {v.get('salario', 0):,.0f} | PcD: {'Sim' if v.get('vaga_pcd') else 'Não'}"
            )
    except Exception:
        linhas.append("Não foi possível obter dados de vagas.")
    try:
        cands = requests.get(f"{API}/candidaturas/", headers=h, timeout=10).json()
        linhas.append(f"\nTotal de candidaturas no sistema: {len(cands)}.")
        from collections import Counter
        status_count = Counter(c.get("status") for c in cands)
        for s, n in status_count.items():
            linhas.append(f"  - {s}: {n}")
    except Exception:
        pass
    return "\n".join(linhas)


def tela_assistente():
    _navbar()
    st.title("🤖 Assistente IA")
    st.caption("Tire dúvidas sobre as vagas do sistema ou sobre carreira e emprego em geral.")

    api_key = st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        st.warning("Configure a secret `GEMINI_API_KEY` no Streamlit Cloud para usar o assistente.")
        return

    if "chat_historico" not in st.session_state:
        st.session_state.chat_historico = []

    for msg in st.session_state.chat_historico:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    pergunta = st.chat_input("Digite sua pergunta...")
    if pergunta:
        st.session_state.chat_historico.append({"role": "user", "content": pergunta})
        with st.chat_message("user"):
            st.markdown(pergunta)

        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                contexto = _contexto_sistema()
                system_prompt = f"""Você é um assistente especializado em recrutamento e emprego da Agência de Empregos.
Responda em português, de forma clara e objetiva.
Você tem acesso aos dados atuais do sistema:

{contexto}

Use esses dados para responder perguntas sobre vagas disponíveis, candidaturas e estatísticas.
Para perguntas gerais sobre carreira, mercado de trabalho, currículo, entrevistas ou emprego, responda com base no seu conhecimento."""

                contents = [{"role": "user", "parts": [{"text": system_prompt}]},
                            {"role": "model", "parts": [{"text": "Entendido! Estou pronto para ajudar."}]}]
                for m in st.session_state.chat_historico[:-1][-10:]:
                    role = "user" if m["role"] == "user" else "model"
                    contents.append({"role": role, "parts": [{"text": m["content"]}]})
                contents.append({"role": "user", "parts": [{"text": pergunta}]})

                try:
                    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}"
                    payload = {"contents": contents, "generationConfig": {"maxOutputTokens": 800, "temperature": 0.7}}
                    r = requests.post(url, json=payload, timeout=30)
                    r.raise_for_status()
                    resposta = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                except Exception as e:
                    resposta = f"Erro ao consultar a IA: {e}"

                st.markdown(resposta)
                st.session_state.chat_historico.append({"role": "assistant", "content": resposta})

    if st.session_state.chat_historico:
        if st.button("🗑️ Limpar conversa", key="limpar_chat"):
            st.session_state.chat_historico = []
            st.rerun()


# ── Roteamento ────────────────────────────────────────────────────────────────

if not st.session_state.token:
    tela_login()
elif "vaga_editar" in st.session_state:
    tela_editar_vaga(st.session_state["vaga_editar"])
elif "empresa_editar" in st.session_state:
    tela_editar_empresa(st.session_state["empresa_editar"])
elif "candidato_editar" in st.session_state:
    tela_editar_candidato(st.session_state["candidato_editar"])
elif "vaga_aberta" in st.session_state:
    tela_detalhe(st.session_state["vaga_aberta"])
elif st.session_state.pagina == "dashboard":
    tela_dashboard()
elif st.session_state.pagina == "empresas":
    tela_empresas()
elif st.session_state.pagina == "candidatos":
    tela_candidatos()
elif st.session_state.pagina == "usuarios":
    tela_usuarios()
elif st.session_state.pagina == "candidaturas":
    tela_candidaturas()
elif st.session_state.pagina == "assistente":
    tela_assistente()
else:
    tela_painel()

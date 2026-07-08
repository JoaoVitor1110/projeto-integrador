"""
Agência de Empregos — Interface Streamlit  (v2 · visual TGA SISTEMAS)
"""

import os
import io
import csv
from datetime import date
import streamlit as st
import requests

# ── Config ───────────────────────────────────────────────────────────────────

API_URL = st.secrets.get("API_URL", os.getenv("API_URL", "http://localhost:8000"))
LOGO_URL = "https://tgaempregos.com.br/wp-content/uploads/elementor/thumbs/cropped-tga-empregos-1-plj70pvsrsnrqdqgv2j3x6wrprqw46jo0l2h7r88o8.webp"

st.set_page_config(
    page_title="TGA Empregos",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS Global ────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Arial:wght@400;700&display=swap');

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#083B7A 0%,#0E63C7 58%,#1895FF 100%) !important;
    min-width: 270px !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }
[data-testid="stSidebar"] * { color: #fff !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.2) !important; }

/* Nav buttons na sidebar */
[data-testid="stSidebar"] button {
    width: 100% !important;
    text-align: left !important;
    background: rgba(255,255,255,.10) !important;
    border: 1px solid rgba(255,255,255,.18) !important;
    border-radius: 14px !important;
    color: #fff !important;
    font-weight: 700 !important;
    padding: 12px 14px !important;
    margin-bottom: 4px !important;
    transition: .15s ease !important;
    box-shadow: 0 4px 12px rgba(0,0,0,.08) !important;
}
[data-testid="stSidebar"] button:hover,
[data-testid="stSidebar"] button[kind="primary"] {
    background: #fff !important;
    color: #083B7A !important;
    transform: translateX(3px) !important;
}
[data-testid="stSidebar"] button[kind="primary"] * { color: #083B7A !important; }
[data-testid="stSidebar"] button p { color: inherit !important; }

/* Logo box */
.logo-box {
    background: linear-gradient(135deg,#fff,#eef7ff);
    border-radius: 20px;
    padding: 12px;
    margin: 16px 16px 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 12px 30px rgba(0,0,0,.22);
    overflow: hidden;
    min-height: 120px;
}
.logo-box img { width:100%; max-height:116px; object-fit:contain; }

.sidebar-info {
    background: rgba(255,255,255,.12);
    border: 1px solid rgba(255,255,255,.2);
    border-radius: 14px;
    padding: 12px 14px;
    margin: 0 12px 12px;
    font-size: 12px;
    line-height: 1.5;
}

/* ── Main ── */
.block-container { padding-top: 16px !important; padding-bottom: 40px !important; max-width: 100% !important; }

/* Topbar */
.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(244,247,250,.85);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(220,231,243,.8);
    border-radius: 20px;
    padding: 16px 22px;
    margin-bottom: 20px;
    box-shadow: 0 10px 30px rgba(8,59,122,.09);
}
.topbar-title { font-size: 26px; font-weight: 900; color: #083B7A; letter-spacing: .8px; }
.topbar-user { font-size: 13px; color: #4a5a6a; }
.user-badge {
    display: inline-block;
    background: linear-gradient(135deg,#083B7A,#1895FF);
    color: #fff !important;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    margin-left: 8px;
}

/* ── Cards KPI ── */
.kpi-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 14px; margin-bottom: 18px; }
.kpi-card {
    background: rgba(255,255,255,.94);
    border: 1px solid rgba(220,231,243,.95);
    border-radius: 22px;
    padding: 18px 20px;
    box-shadow: 0 14px 36px rgba(8,59,122,.09);
    transition: .15s ease;
}
.kpi-card:hover { transform: translateY(-2px); box-shadow: 0 20px 48px rgba(8,59,122,.14); }
.kpi-label { font-size: 11px; text-transform: uppercase; letter-spacing: .7px; color: #68788e; font-weight: 700; margin-bottom: 6px; }
.kpi-value { font-size: 38px; font-weight: 900; letter-spacing: -1px; }
.kpi-val-blue   { color: #0A3D91; }
.kpi-val-red    { color: #E53935; }
.kpi-val-orange { color: #FB8C00; }
.kpi-val-green  { color: #43A047; }
.kpi-val-gray   { color: #757575; }
.kpi-val-teal   { color: #00897B; }
.kpi-val-purple { color: #7B1FA2; }
.kpi-border-red    { border-left: 7px solid #E53935; }
.kpi-border-orange { border-left: 7px solid #FB8C00; }
.kpi-border-green  { border-left: 7px solid #43A047; }
.kpi-border-blue   { border-left: 7px solid #0A3D91; }
.kpi-border-gray   { border-left: 7px solid #90A4AE; }
.kpi-border-teal   { border-left: 7px solid #00897B; }
.kpi-border-purple { border-left: 7px solid #7B1FA2; }

/* ── Vaga card ── */
.vaga-card {
    background: rgba(255,255,255,.96);
    border: 1px solid rgba(220,231,243,.9);
    border-radius: 18px;
    padding: 16px 18px;
    margin-bottom: 12px;
    box-shadow: 0 8px 22px rgba(8,59,122,.07);
    transition: .15s ease;
    border-left-width: 7px;
}
.vaga-card:hover { transform: translateY(-1px); box-shadow: 0 14px 36px rgba(8,59,122,.12); }
.vaga-card-alta   { border-left-color: #E53935; }
.vaga-card-media  { border-left-color: #FB8C00; }
.vaga-card-baixa  { border-left-color: #43A047; }
.vaga-card-none   { border-left-color: #90A4AE; }
.vaga-titulo { font-size: 15px; font-weight: 800; color: #0A3D91; margin-bottom: 2px; }
.vaga-empresa { font-size: 12px; color: #68788e; margin-bottom: 8px; }

/* ── Pills ── */
.pill {
    display: inline-block;
    border-radius: 999px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 800;
    margin-right: 4px;
    margin-bottom: 4px;
}
.pill-alta    { background: #ffe1e1; color: #9f2222; }
.pill-media   { background: #fff3c4; color: #7a5b00; }
.pill-baixa   { background: #dff5e7; color: #146c38; }
.pill-aberta  { background: #e7f1ff; color: #0f4c81; }
.pill-enc     { background: #eceff3; color: #4d5b6a; }
.pill-moe     { background: #e8f5e9; color: #1b5e20; }
.pill-mot     { background: #fce4ec; color: #880e4f; }
.pill-pcd     { background: #f3e5f5; color: #4a148c; }
.pill-pend    { background: #fff8e1; color: #7a5b00; }
.pill-analise { background: #e3f2fd; color: #0d47a1; }
.pill-aprov   { background: #e8f5e9; color: #1b5e20; }
.pill-reprov  { background: #ffebee; color: #b71c1c; }

/* ── Tabela ── */
.tabela-wrap { overflow-x: auto; border-radius: 16px; border: 1px solid #dce7f3; box-shadow: 0 6px 20px rgba(8,59,122,.06); margin-bottom: 14px; }
.tabela-wrap table { width: 100%; border-collapse: collapse; background: #fff; min-width: 700px; font-size: 13px; }
.tabela-wrap th { background: linear-gradient(135deg,#eaf4ff,#dff0ff); color: #083B7A; padding: 10px 12px; text-align: left; font-size: 11px; text-transform: uppercase; letter-spacing: .6px; font-weight: 700; border-bottom: 2px solid #d0e6fb; position: sticky; top: 0; }
.tabela-wrap td { padding: 9px 12px; border-bottom: 1px solid #e8f0f8; vertical-align: top; }
.tabela-wrap tr:hover td { background: #f5f9ff; }
.tabela-wrap tr:last-child td { border-bottom: none; }
.linha-atrasada td { background: #fff1f1 !important; }
.linha-atrasada:hover td { background: #ffe5e5 !important; }

/* ── Barra de progresso ── */
.bar-row { margin: 10px 0; }
.bar-label { display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 5px; }
.bar-bg { height: 12px; background: #e8f0f8; border-radius: 999px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 999px; min-width: 2%; }

/* ── Status line ── */
.status-line { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px dashed #dce7f3; font-size: 13px; }
.status-line:last-child { border-bottom: none; }

/* Seção bloco */
.bloco {
    background: rgba(255,255,255,.94);
    border: 1px solid rgba(220,231,243,.9);
    border-radius: 18px;
    padding: 20px 22px;
    box-shadow: 0 8px 24px rgba(8,59,122,.07);
    margin-bottom: 16px;
}
.bloco-title { font-size: 14px; font-weight: 800; color: #083B7A; text-transform: uppercase; letter-spacing: .5px; margin-bottom: 14px; border-bottom: 1px solid #e0eaf5; padding-bottom: 10px; }

/* Alert */
.alerta-atrasada { background: #fff1f1; border-left: 4px solid #E53935; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; font-size: 13px; }
.alerta-warn { background: #fff8e1; border-left: 4px solid #FB8C00; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; font-size: 13px; }

/* Login page */
.login-box { max-width: 420px; margin: 60px auto; }

/* Hide streamlit elements */
#MainMenu { display: none !important; }
footer { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── Labels ───────────────────────────────────────────────────────────────────

MODALIDADE_LABEL = {
    "presencial": "🏢 Presencial",
    "remoto":     "🏠 Remoto",
    "hibrido":    "🔄 Híbrido",
    "MOE":        "⚙️ MOE",
    "MOT":        "🔩 MOT",
}
CONTRATO_LABEL = {"CLT": "CLT", "PJ": "PJ", "temporario": "Temporário", "estagio": "Estágio"}
PERFIL_LABEL   = {"admin": "👑 Admin", "recrutador": "📋 Recrutador", "visualizador": "🙋 Candidato"}
PRIO_LABEL     = {"alta": "🔴 Alta", "media": "🟡 Média", "baixa": "🟢 Baixa"}
STATUS_LABEL   = {"pendente": "⏳ Pendente", "em_analise": "🔍 Em análise", "aprovado": "✅ Aprovado", "reprovado": "❌ Reprovado"}
STATUS_COR     = {"pendente": "#F9A825", "em_analise": "#1565C0", "aprovado": "#2E7D32", "reprovado": "#B71C1C"}

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
        st.error("❌ Não foi possível conectar ao backend.")
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


def api_patch(path, json=None):
    try:
        r = requests.patch(f"{API_URL}{path}", json=json, headers=_headers(), timeout=10)
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

# ── Estado ───────────────────────────────────────────────────────────────────

if "token"   not in st.session_state: st.session_state.token   = None
if "usuario" not in st.session_state: st.session_state.usuario = None
if "pagina"  not in st.session_state: st.session_state.pagina  = "dashboard"

# ── Helpers visuais ───────────────────────────────────────────────────────────

def _prio_class(p):
    return {"alta": "vaga-card-alta", "media": "vaga-card-media", "baixa": "vaga-card-baixa"}.get(p or "", "vaga-card-none")

def _prio_pill(p):
    css = {"alta": "pill-alta", "media": "pill-media", "baixa": "pill-baixa"}.get(p or "", "")
    return f'<span class="pill {css}">{PRIO_LABEL.get(p, "—")}</span>' if p else ""

def _fmt_salario(v):
    if not v.get("salario"): return "A combinar"
    return f"R$ {v['salario']:,.0f}".replace(",", ".")

def _dias_aberta(v):
    ref = v.get("data_abertura") or v.get("data_publicacao")
    return (date.today() - date.fromisoformat(ref)).days if ref else 0

def _barra(label, valor, total, cor):
    pct = valor / total * 100 if total else 0
    st.markdown(f"""
    <div class="bar-row">
      <div class="bar-label"><span>{label}</span><span><b>{valor}</b> ({pct:.0f}%)</span></div>
      <div class="bar-bg"><div class="bar-fill" style="width:{pct}%;background:{cor}"></div></div>
    </div>""", unsafe_allow_html=True)

def _kpi(label, valor, val_class, border_class):
    st.markdown(f"""
    <div class="kpi-card {border_class}">
      <div class="kpi-label">{label}</div>
      <div class="kpi-value {val_class}">{valor}</div>
    </div>""", unsafe_allow_html=True)

def _csv_download(vagas, nome_arquivo):
    if not vagas:
        return
    buf = io.StringIO()
    campos = ["id","titulo","empresa","local","modalidade","tipo_contrato","salario",
              "prioridade","quantidade_vagas","encaminhados","recrutador_responsavel",
              "status","data_abertura","data_fechamento","vaga_pcd"]
    w = csv.DictWriter(buf, fieldnames=campos, extrasaction="ignore")
    w.writeheader()
    for v in vagas:
        row = {**v, "empresa": v.get("empresa", {}).get("nome", "")}
        w.writerow(row)
    st.download_button(
        label="⬇ Exportar CSV",
        data=buf.getvalue().encode("utf-8-sig"),
        file_name=nome_arquivo,
        mime="text/csv",
        use_container_width=True,
    )

# ── Sidebar ───────────────────────────────────────────────────────────────────

def _sidebar():
    usuario  = st.session_state.usuario
    perfil   = usuario["perfil"]
    pode_escrever = perfil in ("admin", "recrutador")
    pagina_atual  = st.session_state.get("pagina", "dashboard")

    with st.sidebar:
        st.markdown(f'<div class="logo-box"><img src="{LOGO_URL}" alt="TGA Empregos"/></div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="sidebar-info">
            <b>{usuario['nome']}</b><br>
            <span style="opacity:.8;font-size:11px">{PERFIL_LABEL.get(perfil, perfil)}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Itens de navegação por perfil
        itens = []
        if pode_escrever:
            itens.append(("📊 Dashboard",            "dashboard"))
        itens.append(    ("💼 Vagas abertas",         "vagas"))
        if pode_escrever:
            itens.append(("✅ Vagas encerradas",       "encerradas"))
            itens.append(("🔎 Pesquisa por recrutador","recrutador"))
        if perfil == "visualizador":
            itens.append(("📋 Minhas candidaturas",    "candidaturas"))
        if perfil == "admin":
            itens.append(("🏭 Empresas",              "empresas"))
            itens.append(("👤 Candidatos",            "candidatos"))
            itens.append(("👥 Usuários",              "usuarios"))
        itens.append(    ("🤖 Assistente IA",         "assistente"))

        for label, pagina in itens:
            ativo = pagina == pagina_atual
            if st.button(label, key=f"nav_{pagina}", use_container_width=True,
                         type="primary" if ativo else "secondary"):
                st.session_state.pagina = pagina
                for k in ("vaga_aberta","vaga_editar","empresa_editar","candidato_editar"):
                    st.session_state.pop(k, None)
                st.rerun()

        st.markdown("---")
        if st.button("🚪 Sair", key="nav_sair", use_container_width=True):
            st.session_state.clear()
            st.rerun()


def _topbar(titulo):
    usuario = st.session_state.usuario
    perfil  = usuario["perfil"]
    badge   = PERFIL_LABEL.get(perfil, perfil)
    st.markdown(f"""
    <div class="topbar">
      <div class="topbar-title">{titulo}</div>
      <div class="topbar-user">{usuario['nome']} <span class="user-badge">{badge}</span></div>
    </div>
    """, unsafe_allow_html=True)


# ── Login ─────────────────────────────────────────────────────────────────────

def tela_login():
    col1, col2, col3 = st.columns([1, 1.6, 1])
    with col2:
        st.markdown(f'<div style="text-align:center;margin-bottom:20px"><img src="{LOGO_URL}" style="max-height:140px;border-radius:16px;box-shadow:0 8px 24px rgba(0,0,0,.18)"/></div>', unsafe_allow_html=True)
        st.markdown('<div style="text-align:center;font-size:22px;font-weight:900;color:#083B7A;margin-bottom:4px">TGA Empregos</div>', unsafe_allow_html=True)
        st.markdown('<div style="text-align:center;color:#68788e;margin-bottom:24px;font-size:14px">Plataforma de gestão de vagas</div>', unsafe_allow_html=True)

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
                        st.session_state.token   = data["access_token"]
                        st.session_state.usuario = data["usuario"]
                        perfil = data["usuario"]["perfil"]
                        st.session_state.pagina = "dashboard" if perfil in ("admin","recrutador") else "vagas"
                        st.rerun()

        with aba_cadastro:
            st.caption("Crie sua conta para visualizar e se candidatar às vagas.")
            with st.form("form_cadastro"):
                nome_c  = st.text_input("Nome completo *")
                email_c = st.text_input("Email *")
                senha_c = st.text_input("Senha *", type="password")
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
                        st.session_state.token   = data["access_token"]
                        st.session_state.usuario = data["usuario"]
                        st.session_state.pagina  = "vagas"
                        st.success(f"Bem-vindo(a), {nome_c}!")
                        st.rerun()


# ── Dashboard ─────────────────────────────────────────────────────────────────

def tela_dashboard():
    _sidebar()
    _topbar("📊 DASHBOARD")

    vagas = api_get("/vagas/")
    if vagas is None:
        return

    hoje       = date.today()
    abertas    = [v for v in vagas if v["status"] == "aberta"]
    encerradas = [v for v in vagas if v["status"] == "encerrada"]
    alta       = [v for v in abertas if v.get("prioridade") == "alta"]
    media      = [v for v in abertas if v.get("prioridade") == "media"]
    baixa      = [v for v in abertas if v.get("prioridade") == "baixa"]
    enc_total  = sum(v.get("encaminhados") or 0 for v in vagas)
    mais7      = [v for v in abertas if _dias_aberta(v) >= 7]
    pcd        = [v for v in vagas if v.get("vaga_pcd")]

    # KPIs linha 1
    c1,c2,c3,c4 = st.columns(4)
    with c1: _kpi("Vagas abertas",     len(abertas),   "kpi-val-blue",   "kpi-border-blue")
    with c2: _kpi("Prioridade alta",   len(alta),      "kpi-val-red",    "kpi-border-red")
    with c3: _kpi("Prioridade média",  len(media),     "kpi-val-orange", "kpi-border-orange")
    with c4: _kpi("Prioridade baixa",  len(baixa),     "kpi-val-green",  "kpi-border-green")

    c5,c6,c7,c8 = st.columns(4)
    with c5: _kpi("Encerradas",        len(encerradas),"kpi-val-gray",   "kpi-border-gray")
    with c6: _kpi("Encaminhados",      enc_total,      "kpi-val-teal",   "kpi-border-teal")
    with c7: _kpi("Vagas +7 dias",     len(mais7),     "kpi-val-red",    "kpi-border-red")
    with c8: _kpi("Vagas PcD",         len(pcd),       "kpi-val-purple", "kpi-border-purple")

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="bloco">', unsafe_allow_html=True)
        st.markdown('<div class="bloco-title">Resumo por status</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="status-line"><span>Abertas</span><b style="color:#0A3D91">{len(abertas)}</b></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="status-line"><span>Encerradas</span><b style="color:#757575">{len(encerradas)}</b></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="status-line"><span>Prioridade alta</span><b style="color:#E53935">{len(alta)}</b></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="status-line"><span>Prioridade média</span><b style="color:#FB8C00">{len(media)}</b></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="status-line"><span>Prioridade baixa</span><b style="color:#43A047">{len(baixa)}</b></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="status-line"><span>Total encaminhados</span><b style="color:#00897B">{enc_total}</b></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="status-line"><span>PcD</span><b style="color:#7B1FA2">{len(pcd)}</b></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="bloco">', unsafe_allow_html=True)
        st.markdown('<div class="bloco-title">Encaminhados por recrutador</div>', unsafe_allow_html=True)
        recrutadores: dict = {}
        for v in vagas:
            r = v.get("recrutador_responsavel") or "Sem recrutador"
            recrutadores[r] = recrutadores.get(r, 0) + (v.get("encaminhados") or 0)
        total_r = sum(recrutadores.values()) or 1
        for rec, qtd in sorted(recrutadores.items(), key=lambda x: -x[1]):
            _barra(rec, qtd, total_r, "#0A3D91")
        st.markdown('</div>', unsafe_allow_html=True)

    col_c, col_d = st.columns(2)

    with col_c:
        st.markdown('<div class="bloco">', unsafe_allow_html=True)
        st.markdown('<div class="bloco-title">Vagas por modalidade</div>', unsafe_allow_html=True)
        mod_count: dict = {}
        for v in vagas:
            m = MODALIDADE_LABEL.get(v["modalidade"], v["modalidade"])
            mod_count[m] = mod_count.get(m, 0) + 1
        total_m = sum(mod_count.values()) or 1
        for lbl, val in sorted(mod_count.items(), key=lambda x: -x[1]):
            _barra(lbl, val, total_m, "#1565C0")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_d:
        st.markdown('<div class="bloco">', unsafe_allow_html=True)
        st.markdown('<div class="bloco-title">Vagas por tipo de contrato</div>', unsafe_allow_html=True)
        cont_count: dict = {}
        for v in vagas:
            c = CONTRATO_LABEL.get(v["tipo_contrato"], v["tipo_contrato"])
            cont_count[c] = cont_count.get(c, 0) + 1
        total_c = sum(cont_count.values()) or 1
        for lbl, val in sorted(cont_count.items(), key=lambda x: -x[1]):
            _barra(lbl, val, total_c, "#2E7D32")
        st.markdown('</div>', unsafe_allow_html=True)

    # Vagas abertas há mais de 7 dias
    if mais7:
        st.markdown('<div class="bloco">', unsafe_allow_html=True)
        st.markdown('<div class="bloco-title">⚠️ Vagas abertas há mais de 7 dias</div>', unsafe_allow_html=True)
        mais7_ord = sorted(mais7, key=lambda v: -_dias_aberta(v))
        rows = ""
        for v in mais7_ord[:15]:
            dias = _dias_aberta(v)
            cls = "linha-atrasada" if dias >= 30 else ""
            prio_pill = _prio_pill(v.get("prioridade"))
            enc = v.get("encaminhados") or 0
            rows += f"""<tr class="{cls}">
              <td><b>{v['titulo']}</b></td>
              <td>{v['empresa']['nome']}</td>
              <td>{prio_pill}</td>
              <td style="color:#E53935;font-weight:700">{dias} dias</td>
              <td>{enc}</td>
              <td>{v.get('recrutador_responsavel') or '—'}</td>
            </tr>"""
        st.markdown(f"""
        <div class="tabela-wrap"><table>
          <thead><tr><th>Vaga</th><th>Cliente</th><th>Prioridade</th><th>Tempo aberta</th><th>Encaminhados</th><th>Recrutador</th></tr></thead>
          <tbody>{rows}</tbody>
        </table></div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ── Vagas abertas ─────────────────────────────────────────────────────────────

def _form_vaga(vaga_existente=None, key_prefix="nova"):
    """Formulário unificado de criação/edição de vaga."""
    empresas = api_get("/empresas/") or []
    usuarios = api_get("/auth/usuarios") or []
    recrutadores = [u["nome"] for u in usuarios if u["perfil"] in ("admin","recrutador")]

    is_edit = vaga_existente is not None
    v = vaga_existente or {}
    empresa_opcoes = {e["nome"]: e["id"] for e in empresas}
    empresa_atual  = next((e["nome"] for e in empresas if e["id"] == v.get("empresa_id")), None)

    modalidades = ["presencial","remoto","hibrido","MOE","MOT"]
    contratos   = ["CLT","PJ","temporario","estagio"]
    publicos    = ["ambos","masculino","feminino"]
    prioridades = ["alta","media","baixa"]

    with st.form(f"form_vaga_{key_prefix}"):
        col1, col2 = st.columns(2)
        with col1:
            titulo   = st.text_input("Título *", value=v.get("titulo",""))
            local    = st.text_input("Local *", value=v.get("local",""))
            salario  = st.number_input("Salário (R$)", min_value=0.0, step=100.0, value=float(v.get("salario") or 0))
            qtd      = st.number_input("Quantidade de vagas", min_value=1, step=1, value=v.get("quantidade_vagas",1))
            empresa_nome = st.selectbox("Cliente/Empresa *", list(empresa_opcoes.keys()),
                index=list(empresa_opcoes.keys()).index(empresa_atual) if empresa_atual and empresa_atual in empresa_opcoes else 0)
        with col2:
            prio_idx = prioridades.index(v["prioridade"]) if v.get("prioridade") in prioridades else 1
            prioridade    = st.selectbox("Prioridade", prioridades, index=prio_idx,
                                         format_func=lambda x: PRIO_LABEL.get(x,x))
            mod_idx = modalidades.index(v["modalidade"]) if v.get("modalidade") in modalidades else 0
            modalidade    = st.selectbox("Modalidade", modalidades, index=mod_idx,
                                         format_func=lambda x: MODALIDADE_LABEL.get(x,x))
            cont_idx = contratos.index(v["tipo_contrato"]) if v.get("tipo_contrato") in contratos else 0
            tipo_contrato = st.selectbox("Tipo de contrato", contratos, index=cont_idx,
                                         format_func=lambda x: CONTRATO_LABEL.get(x,x))
            pub_idx = publicos.index(v.get("publico_alvo","ambos")) if v.get("publico_alvo") in publicos else 0
            publico_alvo  = st.selectbox("Público-alvo", publicos, index=pub_idx)
            horario       = st.text_input("Horário", value=v.get("horario") or "")
        col3, col4 = st.columns(2)
        with col3:
            rec_opts = [""] + recrutadores
            rec_atual = v.get("recrutador_responsavel") or ""
            rec_idx   = rec_opts.index(rec_atual) if rec_atual in rec_opts else 0
            recrutador = st.selectbox("Recrutador responsável", rec_opts, index=rec_idx,
                                       format_func=lambda x: x if x else "— Selecione —")
        with col4:
            enc_val = v.get("encaminhados") or 0
            encaminhados = st.number_input("Encaminhados", min_value=0, step=1, value=int(enc_val))
        descricao = st.text_area("Descrição / Observações", value=v.get("descricao") or "",
                                  placeholder="Responsabilidades, perfil solicitado, urgência...")
        col5, col6 = st.columns(2)
        with col5:
            vaga_pcd = st.checkbox("Vaga PcD ♿", value=v.get("vaga_pcd", False))
        with col6:
            if is_edit:
                status = st.selectbox("Status", ["aberta","encerrada"],
                                       index=0 if v.get("status","aberta") == "aberta" else 1)
            else:
                status = "aberta"
        salvar = st.form_submit_button("Salvar" if is_edit else "Lançar vaga", type="primary", use_container_width=True)

    if salvar:
        if not titulo or not local or not empresa_nome:
            st.error("Preencha título, local e cliente.")
            return None
        return {
            "titulo": titulo, "local": local,
            "descricao": descricao or None,
            "salario": salario or None,
            "modalidade": modalidade, "tipo_contrato": tipo_contrato,
            "publico_alvo": publico_alvo, "horario": horario or None,
            "vaga_pcd": vaga_pcd, "status": status,
            "quantidade_vagas": int(qtd),
            "prioridade": prioridade,
            "encaminhados": int(encaminhados),
            "recrutador_responsavel": recrutador or None,
            "empresa_id": empresa_opcoes[empresa_nome],
        }
    return None


def tela_vagas(apenas_encerradas=False):
    _sidebar()
    titulo_pg = "✅ Vagas Encerradas" if apenas_encerradas else "📌 Vagas Abertas"
    _topbar(titulo_pg)

    usuario = st.session_state.usuario
    perfil  = usuario["perfil"]
    pode_escrever = perfil in ("admin","recrutador")

    if pode_escrever and not apenas_encerradas:
        with st.expander("➕ Lançar nova vaga"):
            dados = _form_vaga(key_prefix="nova")
            if dados:
                resp = api_post("/vagas/", json=dados)
                if resp:
                    st.success(f"✅ Vaga '{resp['titulo']}' lançada!")
                    st.rerun()

    # Filtros
    with st.expander("🔍 Filtros", expanded=False):
        col1,col2,col3,col4,col5 = st.columns(5)
        with col1:
            busca = st.text_input("Buscar cargo/cliente", placeholder="Buscar...", key="filtro_busca")
        with col2:
            modalidade = st.selectbox("Modalidade", ["","presencial","remoto","hibrido","MOE","MOT"],
                format_func=lambda x: "Todas" if x=="" else MODALIDADE_LABEL.get(x,x), key="filtro_mod")
        with col3:
            contrato = st.selectbox("Contrato", ["","CLT","PJ","temporario","estagio"],
                format_func=lambda x: "Todos" if x=="" else CONTRATO_LABEL.get(x,x), key="filtro_cont")
        with col4:
            prioridade_f = st.selectbox("Prioridade", ["","alta","media","baixa"],
                format_func=lambda x: "Todas" if x=="" else PRIO_LABEL.get(x,x), key="filtro_prio")
        with col5:
            apenas_pcd = st.checkbox("Somente PcD ♿", key="filtro_pcd")

    params: dict = {}
    if modalidade:  params["modalidade"]  = modalidade
    if contrato:    params["tipo_contrato"] = contrato
    if apenas_pcd:  params["vaga_pcd"]    = True
    params["status"] = "encerrada" if apenas_encerradas else "aberta"

    vagas = api_get("/vagas/", params=params)
    if vagas is None:
        return

    # Filtros locais
    if busca:
        b = busca.lower()
        vagas = [v for v in vagas if b in v["titulo"].lower() or b in v["empresa"]["nome"].lower()]
    if prioridade_f:
        vagas = [v for v in vagas if v.get("prioridade") == prioridade_f]

    col_info, col_export = st.columns([3,1])
    with col_info:
        st.caption(f"{len(vagas)} vaga(s) encontrada(s)")
    with col_export:
        _csv_download(vagas, "vagas_abertas_tga.csv" if not apenas_encerradas else "vagas_encerradas_tga.csv")

    if not vagas:
        st.info("Nenhuma vaga encontrada para os filtros selecionados.")
        return

    # Tabela de vagas
    rows = ""
    for v in vagas:
        dias = _dias_aberta(v)
        cls  = "linha-atrasada" if dias >= 30 and not apenas_encerradas else ""
        prio = _prio_pill(v.get("prioridade"))
        mod  = MODALIDADE_LABEL.get(v["modalidade"], v["modalidade"])
        sal  = _fmt_salario(v)
        enc  = v.get("encaminhados") or 0
        pcd  = '♿' if v.get("vaga_pcd") else ""
        rec  = v.get("recrutador_responsavel") or "—"
        qtd  = v.get("quantidade_vagas",1)
        rows += f"""<tr class="{cls}">
          <td><b>{v['titulo']}</b>{pcd}</td>
          <td>{v['empresa']['nome']}</td>
          <td>{prio}</td>
          <td>{mod}</td>
          <td>{sal}</td>
          <td>{qtd}</td>
          <td style="color:#00897B;font-weight:700">{enc}</td>
          <td style="{'color:#E53935;font-weight:700' if dias>=30 else ''}">{dias}d</td>
          <td>{rec}</td>
        </tr>"""

    st.markdown(f"""
    <div class="tabela-wrap"><table>
      <thead><tr>
        <th>Cargo/Vaga</th><th>Cliente</th><th>Prioridade</th><th>Modalidade</th>
        <th>Salário</th><th>Qtd</th><th>Encam.</th><th>Tempo</th><th>Recrutador</th>
      </tr></thead>
      <tbody>{rows}</tbody>
    </table></div>
    """, unsafe_allow_html=True)

    # Cards de ação (editar/detalhes) abaixo da tabela
    if pode_escrever:
        st.markdown("#### Ações por vaga")
        for v in vagas[:20]:
            with st.expander(f"⚡ {v['titulo']} — {v['empresa']['nome']}"):
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    if st.button("👁 Ver detalhes / candidatos", key=f"det_{v['id']}", use_container_width=True):
                        st.session_state["vaga_aberta"] = v["id"]
                        st.rerun()
                with col_b:
                    if st.button("✏️ Editar vaga", key=f"edit_{v['id']}", use_container_width=True):
                        st.session_state["vaga_editar"] = v["id"]
                        st.rerun()
                with col_c:
                    label_toggle = "⚫ Encerrar" if v["status"]=="aberta" else "🟢 Reabrir"
                    if st.button(label_toggle, key=f"tog_{v['id']}", use_container_width=True):
                        novo_status = "encerrada" if v["status"]=="aberta" else "aberta"
                        dados = {k: v[k] for k in ["titulo","local","descricao","salario","modalidade",
                                 "horario","tipo_contrato","publico_alvo","vaga_pcd","empresa_id",
                                 "quantidade_vagas","data_publicacao","data_abertura","data_fechamento",
                                 "prioridade","encaminhados","recrutador_responsavel"] if k in v}
                        dados["status"] = novo_status
                        if novo_status == "encerrada":
                            dados["data_fechamento"] = str(date.today())
                        if api_put(f"/vagas/{v['id']}", json=dados):
                            st.success("Status atualizado!")
                            st.rerun()
    else:
        # Candidato: botão ver detalhes
        for v in vagas:
            col_a, _ = st.columns([1,3])
            with col_a:
                if st.button(f"Ver {v['titulo']}", key=f"det_{v['id']}"):
                    st.session_state["vaga_aberta"] = v["id"]
                    st.rerun()


# ── Pesquisa por recrutador ───────────────────────────────────────────────────

def tela_recrutador():
    _sidebar()
    _topbar("🔎 Pesquisa por Recrutador")

    vagas_all = api_get("/vagas/")
    if vagas_all is None:
        return

    usuarios = api_get("/auth/usuarios") or []
    recrutadores_sistema = sorted({u["nome"] for u in usuarios if u["perfil"] in ("admin","recrutador")})
    recrutadores_vagas   = sorted({v["recrutador_responsavel"] for v in vagas_all if v.get("recrutador_responsavel")})
    todos_recs = sorted(set(recrutadores_sistema) | set(recrutadores_vagas))

    col1, col2, col3 = st.columns(3)
    with col1:
        rec_sel = st.selectbox("Selecione o recrutador", [""] + todos_recs,
                               format_func=lambda x: "— Todos —" if x=="" else x)
    with col2:
        status_f = st.selectbox("Status", ["","aberta","encerrada"],
                                 format_func=lambda x: "Qualquer" if x=="" else x.capitalize())
    with col3:
        prio_f = st.selectbox("Prioridade", ["","alta","media","baixa"],
                               format_func=lambda x: "Todas" if x=="" else PRIO_LABEL.get(x,x))

    vagas = vagas_all
    if rec_sel:
        vagas = [v for v in vagas if v.get("recrutador_responsavel") == rec_sel]
    if status_f:
        vagas = [v for v in vagas if v["status"] == status_f]
    if prio_f:
        vagas = [v for v in vagas if v.get("prioridade") == prio_f]

    col_i, col_e = st.columns([3,1])
    with col_i:
        st.caption(f"{len(vagas)} vaga(s) encontrada(s){' para ' + rec_sel if rec_sel else ''}")
    with col_e:
        _csv_download(vagas, f"pesquisa_recrutador_{rec_sel or 'todos'}.csv")

    if not vagas:
        st.info("Nenhuma vaga encontrada.")
        return

    # KPIs do recrutador selecionado
    if rec_sel:
        ab  = [v for v in vagas if v["status"]=="aberta"]
        enc = sum(v.get("encaminhados") or 0 for v in vagas)
        alt = [v for v in ab if v.get("prioridade")=="alta"]
        c1,c2,c3,c4 = st.columns(4)
        with c1: _kpi("Abertas",    len(ab),  "kpi-val-blue",  "kpi-border-blue")
        with c2: _kpi("Alta prio.", len(alt),  "kpi-val-red",   "kpi-border-red")
        with c3: _kpi("Encaminhados",enc,      "kpi-val-teal",  "kpi-border-teal")
        with c4: _kpi("Total vagas",len(vagas),"kpi-val-gray",  "kpi-border-gray")

    rows = ""
    for v in sorted(vagas, key=lambda x: (x["status"]!="aberta", -(v.get("prioridade")=="alta"))):
        dias = _dias_aberta(v)
        prio = _prio_pill(v.get("prioridade"))
        mod  = MODALIDADE_LABEL.get(v["modalidade"], v["modalidade"])
        sal  = _fmt_salario(v)
        status_pill = '<span class="pill pill-aberta">Aberta</span>' if v["status"]=="aberta" else '<span class="pill pill-enc">Encerrada</span>'
        enc_v = v.get("encaminhados") or 0
        rows += f"""<tr>
          <td><b>{v['titulo']}</b></td>
          <td>{v['empresa']['nome']}</td>
          <td>{prio}</td>
          <td>{status_pill}</td>
          <td>{mod}</td>
          <td>{sal}</td>
          <td style="color:#00897B;font-weight:700">{enc_v}</td>
          <td>{dias}d</td>
        </tr>"""

    st.markdown(f"""
    <div class="tabela-wrap"><table>
      <thead><tr>
        <th>Cargo/Vaga</th><th>Cliente</th><th>Prioridade</th><th>Status</th>
        <th>Modalidade</th><th>Salário</th><th>Encam.</th><th>Tempo</th>
      </tr></thead>
      <tbody>{rows}</tbody>
    </table></div>
    """, unsafe_allow_html=True)


# ── Detalhe da Vaga ───────────────────────────────────────────────────────────

def tela_detalhe(vaga_id):
    _sidebar()

    vaga = api_get(f"/vagas/{vaga_id}")
    if not vaga:
        st.session_state.pop("vaga_aberta", None)
        st.rerun()

    usuario = st.session_state.usuario
    perfil  = usuario["perfil"]
    pode_escrever = perfil in ("admin","recrutador")

    _topbar(f"💼 {vaga['titulo']}")

    if st.button("← Voltar"):
        st.session_state.pop("vaga_aberta", None)
        st.rerun()

    prio_cls = _prio_class(vaga.get("prioridade"))
    prio_pill = _prio_pill(vaga.get("prioridade"))
    dias = _dias_aberta(vaga)
    sal  = _fmt_salario(vaga)
    mod  = MODALIDADE_LABEL.get(vaga["modalidade"], vaga["modalidade"])

    st.markdown(f"""
    <div class="vaga-card {prio_cls}">
      <div class="vaga-titulo">{vaga['titulo']} {prio_pill}</div>
      <div class="vaga-empresa">🏭 {vaga['empresa']['nome']} &nbsp;·&nbsp; 📍 {vaga['local']}</div>
      <span class="pill {'pill-aberta' if vaga['status']=='aberta' else 'pill-enc'}">
        {'🟢 Aberta' if vaga['status']=='aberta' else '⚫ Encerrada'}
      </span>
      {'<span class="pill pill-pcd">♿ PcD</span>' if vaga.get('vaga_pcd') else ''}
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    c1.metric("Salário",     sal)
    c2.metric("Modalidade",  mod)
    c3.metric("Contrato",    CONTRATO_LABEL.get(vaga["tipo_contrato"], vaga["tipo_contrato"]))
    c4.metric("Vagas",       vaga.get("quantidade_vagas",1))
    c5.metric("Encaminhados", vaga.get("encaminhados") or 0)
    c6.metric("Dias aberta", dias)

    if vaga.get("recrutador_responsavel"):
        st.caption(f"👤 Recrutador: **{vaga['recrutador_responsavel']}**")
    if vaga.get("horario"):
        st.caption(f"🕐 Horário: {vaga['horario']}")

    if vaga.get("descricao"):
        st.divider()
        st.markdown("**📝 Descrição / Observações**")
        st.markdown(vaga["descricao"])

    col_ben, col_req = st.columns(2)
    with col_ben:
        st.markdown("**🎁 Benefícios**")
        if vaga.get("beneficios"):
            for b in vaga["beneficios"]: st.caption(f"• {b['nome']}")
        else:
            st.caption("Não informado")
    with col_req:
        st.markdown("**📋 Requisitos**")
        if vaga.get("requisitos"):
            for r in vaga["requisitos"]:
                badge = "🔴 Obrigatório" if r["nivel"]=="obrigatorio" else "🔵 Desejável"
                st.caption(f"{badge} — {r['descricao']}")
        else:
            st.caption("Não informado")

    st.divider()

    if pode_escrever:
        st.markdown("### 👥 Candidatos Inscritos")

        candidaturas_vaga = api_get("/candidaturas/", params={"vaga_id": vaga_id})
        if not candidaturas_vaga:
            st.info("Nenhum candidato inscrito ainda.")
        else:
            st.caption(f"{len(candidaturas_vaga)} candidato(s) inscrito(s)")
            rows = ""
            for cand in candidaturas_vaga:
                c = cand.get("candidato", {})
                s = cand.get("status","pendente")
                pill_map = {"pendente":"pill-pend","em_analise":"pill-analise","aprovado":"pill-aprov","reprovado":"pill-reprov"}
                rows += f"""<tr>
                  <td><b>{c.get('nome','—')}</b></td>
                  <td>{c.get('email','—')}</td>
                  <td>{c.get('telefone') or '—'}</td>
                  <td>{c.get('cidade') or '—'}/{c.get('estado') or ''}</td>
                  <td><span class="pill {pill_map.get(s,'')}">{STATUS_LABEL.get(s,s)}</span></td>
                  <td>{cand.get('data_candidatura','')}</td>
                </tr>"""
            st.markdown(f"""
            <div class="tabela-wrap"><table>
              <thead><tr><th>Nome</th><th>Email</th><th>Telefone</th><th>Cidade</th><th>Status</th><th>Data</th></tr></thead>
              <tbody>{rows}</tbody>
            </table></div>
            """, unsafe_allow_html=True)

            st.markdown("**Atualizar status de candidatura:**")
            for cand in candidaturas_vaga:
                c = cand.get("candidato", {})
                s = cand.get("status","pendente")
                with st.container(border=True):
                    col_nm, col_sel, col_btn = st.columns([3,2,1])
                    with col_nm:
                        st.markdown(f"**{c.get('nome','—')}**")
                        st.caption(c.get("email",""))
                    with col_sel:
                        novo = st.selectbox("Status", ["pendente","em_analise","aprovado","reprovado"],
                            index=["pendente","em_analise","aprovado","reprovado"].index(s),
                            key=f"sel_{cand['id']}", format_func=lambda x: STATUS_LABEL.get(x,x),
                            label_visibility="collapsed")
                    with col_btn:
                        if st.button("✔", key=f"btn_{cand['id']}", use_container_width=True):
                            if api_put(f"/candidaturas/{cand['id']}/status", json={"status": novo}):
                                st.success("Atualizado!")
                                st.rerun()

        # Atualizar encaminhados
        st.divider()
        st.markdown("**📤 Atualizar encaminhados:**")
        col_enc, col_btn_enc = st.columns([2,1])
        with col_enc:
            novo_enc = st.number_input("Qtd encaminhados", min_value=0, step=1,
                                        value=int(vaga.get("encaminhados") or 0),
                                        key="enc_update", label_visibility="collapsed")
        with col_btn_enc:
            if st.button("Salvar encaminhados", use_container_width=True):
                if api_patch(f"/vagas/{vaga_id}/encaminhados", json={"encaminhados": int(novo_enc)}):
                    st.success("Encaminhados atualizados!")
                    st.rerun()

        st.divider()
        st.markdown("**⚙️ Ações da vaga:**")
        col_tog, col_del = st.columns(2)
        novo_status = "encerrada" if vaga["status"]=="aberta" else "aberta"
        label_tog   = "⚫ Encerrar vaga" if vaga["status"]=="aberta" else "🟢 Reabrir vaga"
        with col_tog:
            if st.button(label_tog, use_container_width=True, type="primary"):
                dados = {k: vaga[k] for k in ["titulo","local","descricao","salario","modalidade","horario",
                         "tipo_contrato","publico_alvo","vaga_pcd","empresa_id","quantidade_vagas",
                         "data_publicacao","data_abertura","data_fechamento","prioridade",
                         "encaminhados","recrutador_responsavel"] if k in vaga}
                dados["status"] = novo_status
                if novo_status == "encerrada":
                    dados["data_fechamento"] = str(date.today())
                if api_put(f"/vagas/{vaga_id}", json=dados):
                    st.success("Status atualizado!")
                    st.rerun()
        with col_del:
            if st.button("🗑️ Excluir vaga", use_container_width=True):
                if api_delete(f"/vagas/{vaga_id}"):
                    st.success("Vaga excluída.")
                    st.session_state.pop("vaga_aberta", None)
                    st.rerun()

    elif perfil == "visualizador" and vaga["status"] == "aberta":
        st.markdown("### 🚀 Candidatar-se")
        candidatos = api_get("/candidatos/")
        candidato_id = None
        if candidatos:
            for c in candidatos:
                if c.get("email") == usuario.get("email"):
                    candidato_id = c["id"]
                    break
        if candidato_id:
            existentes = api_get("/candidaturas/", params={"vaga_id": vaga_id}) or []
            ja_inscrito = any(c.get("candidato_id")==candidato_id for c in existentes)
            if ja_inscrito:
                st.success("✅ Você já está inscrito nessa vaga!")
            else:
                if st.button("✅ Candidatar-se", use_container_width=True, type="primary"):
                    resp = api_post("/candidaturas/", json={"candidato_id": candidato_id, "vaga_id": vaga_id})
                    if resp:
                        st.success("Candidatura enviada!")
                        st.rerun()
        else:
            st.info("Complete seu perfil para se candidatar.")
            if st.button("📝 Completar perfil", type="primary"):
                st.session_state.pagina = "candidaturas"
                st.session_state.pop("vaga_aberta", None)
                st.rerun()


# ── Editar Vaga ───────────────────────────────────────────────────────────────

def tela_editar_vaga(vaga_id):
    _sidebar()

    vaga = api_get(f"/vagas/{vaga_id}")
    if not vaga:
        st.session_state.pop("vaga_editar", None)
        st.rerun()

    _topbar(f"✏️ Editar: {vaga['titulo']}")

    if st.button("← Voltar"):
        st.session_state.pop("vaga_editar", None)
        st.rerun()

    dados = _form_vaga(vaga_existente=vaga, key_prefix=f"edit_{vaga_id}")
    if dados:
        resp = api_put(f"/vagas/{vaga_id}", json=dados)
        if resp:
            st.success("✅ Vaga atualizada!")
            st.session_state.pop("vaga_editar", None)
            st.rerun()


# ── Empresas (Admin) ──────────────────────────────────────────────────────────

def tela_empresas():
    _sidebar()
    _topbar("🏭 Gerenciar Empresas")

    with st.expander("➕ Cadastrar nova empresa"):
        with st.form("form_nova_empresa"):
            col1, col2 = st.columns(2)
            with col1:
                nome  = st.text_input("Nome *")
                cnpj  = st.text_input("CNPJ *")
                setor = st.text_input("Setor *")
            with col2:
                cidade    = st.text_input("Cidade *")
                estado    = st.text_input("Estado (UF) *", max_chars=2)
                descricao = st.text_area("Descrição")
            salvar = st.form_submit_button("Salvar", type="primary")
        if salvar:
            if not all([nome, cnpj, setor, cidade, estado]):
                st.error("Preencha todos os campos obrigatórios.")
            else:
                resp = api_post("/empresas/", json={"nome":nome,"cnpj":cnpj,"setor":setor,
                                                     "cidade":cidade,"estado":estado.upper(),"descricao":descricao})
                if resp:
                    st.success(f"✅ {resp['nome']} cadastrada!")
                    st.rerun()

    empresas = api_get("/empresas/") or []
    st.caption(f"{len(empresas)} empresa(s)")

    for emp in empresas:
        with st.container(border=True):
            c1, c2, c3 = st.columns([3,2,1])
            with c1:
                st.markdown(f"**{emp['nome']}**")
                st.caption(f"CNPJ: {emp['cnpj']} | {emp['setor']}")
            with c2:
                st.caption(f"📍 {emp['cidade']}/{emp['estado']}")
            with c3:
                if st.button("✏️", key=f"ed_emp_{emp['id']}", use_container_width=True):
                    st.session_state["empresa_editar"] = emp["id"]
                    st.rerun()
                if st.button("🗑️", key=f"dl_emp_{emp['id']}", use_container_width=True):
                    if api_delete(f"/empresas/{emp['id']}"):
                        st.success("Empresa excluída.")
                        st.rerun()


def tela_editar_empresa(empresa_id):
    _sidebar()
    emp = api_get(f"/empresas/{empresa_id}")
    if not emp:
        st.session_state.pop("empresa_editar", None)
        st.rerun()

    _topbar(f"✏️ Editar: {emp['nome']}")

    if st.button("← Voltar"):
        st.session_state.pop("empresa_editar", None)
        st.rerun()

    with st.form("form_edit_emp"):
        c1,c2 = st.columns(2)
        with c1:
            nome   = st.text_input("Nome *", value=emp["nome"])
            cnpj   = st.text_input("CNPJ *", value=emp["cnpj"])
            setor  = st.text_input("Setor *", value=emp["setor"])
        with c2:
            cidade = st.text_input("Cidade *", value=emp["cidade"])
            estado = st.text_input("UF *", value=emp["estado"], max_chars=2)
            desc   = st.text_area("Descrição", value=emp.get("descricao") or "")
        salvar = st.form_submit_button("Salvar", type="primary")
    if salvar:
        resp = api_put(f"/empresas/{empresa_id}", json={"nome":nome,"cnpj":cnpj,"setor":setor,
                                                          "cidade":cidade,"estado":estado.upper(),"descricao":desc or None})
        if resp:
            st.success("✅ Empresa atualizada!")
            st.session_state.pop("empresa_editar", None)
            st.rerun()


# ── Usuários (Admin) ──────────────────────────────────────────────────────────

def tela_usuarios():
    _sidebar()
    _topbar("👥 Gerenciar Usuários")

    with st.expander("➕ Criar novo usuário"):
        with st.form("form_novo_usr"):
            c1,c2 = st.columns(2)
            with c1:
                nome_u  = st.text_input("Nome *")
                email_u = st.text_input("Email *")
            with c2:
                senha_u  = st.text_input("Senha *", type="password")
                perfil_u = st.selectbox("Perfil", ["visualizador","recrutador","admin"],
                    format_func=lambda x: {"visualizador":"Candidato","recrutador":"Recrutador","admin":"Admin"}.get(x,x))
            salvar_u = st.form_submit_button("Criar", type="primary")
        if salvar_u:
            if not all([nome_u, email_u, senha_u]):
                st.error("Preencha todos os campos.")
            else:
                resp = api_post("/auth/usuarios", json={"nome":nome_u,"email":email_u,"senha":senha_u,"perfil":perfil_u})
                if resp:
                    st.success(f"✅ {resp['nome']} criado!")
                    st.rerun()

    usuarios = api_get("/auth/usuarios") or []
    st.caption(f"{len(usuarios)} usuário(s)")
    usuario_atual = st.session_state.usuario
    PCOR = {"admin":"#6A1B9A","recrutador":"#1565C0","visualizador":"#2E7D32"}

    for u in usuarios:
        with st.container(border=True):
            c1,c2,c3 = st.columns([3,2,1])
            with c1:
                st.markdown(f"**{u['nome']}**")
                st.caption(u["email"])
            with c2:
                cor = PCOR.get(u["perfil"],"#555")
                st.markdown(f"<span style='background:{cor};color:white;padding:2px 10px;border-radius:12px;font-size:12px'>{PERFIL_LABEL.get(u['perfil'],u['perfil'])}</span>", unsafe_allow_html=True)
            with c3:
                if u["id"] == usuario_atual["id"]:
                    st.caption("(você)")
                else:
                    if st.button("🗑️", key=f"dl_usr_{u['id']}", use_container_width=True):
                        if api_delete(f"/auth/usuarios/{u['id']}"):
                            st.success(f"'{u['nome']}' excluído.")
                            st.rerun()


# ── Candidaturas (Candidato) ──────────────────────────────────────────────────

def tela_candidaturas():
    _sidebar()
    _topbar("📋 Meu Perfil de Candidato")

    usuario  = st.session_state.usuario
    candidatos = api_get("/candidatos/")
    candidato  = next((c for c in (candidatos or []) if c.get("email")==usuario.get("email")), None)

    def _form_cand(c=None):
        is_e = c is not None
        with st.form("form_cand"):
            col1, col2 = st.columns(2)
            with col1:
                tel = st.text_input("Telefone", value=c.get("telefone") or "" if is_e else "")
            with col2:
                cid = st.text_input("Cidade", value=c.get("cidade") or "" if is_e else "")
                uf  = st.text_input("Estado (UF)", max_chars=2, value=c.get("estado") or "" if is_e else "")
            nasc_v = None
            if is_e and c.get("data_nascimento"):
                try: nasc_v = date.fromisoformat(c["data_nascimento"])
                except Exception: pass
            nasc = st.date_input("Data de nascimento", value=nasc_v)
            btn  = st.form_submit_button("Salvar alterações" if is_e else "Criar perfil", type="primary")
        return tel, cid, uf, nasc, btn

    if not candidato:
        st.info("Complete seu perfil para se candidatar às vagas.")
        tel, cid, uf, nasc, btn = _form_cand()
        if btn:
            resp = api_post("/candidatos/", json={"nome":usuario.get("nome"),"email":usuario.get("email"),
                "telefone":tel or None,"cidade":cid or None,"estado":uf.upper() if uf else None,
                "data_nascimento":str(nasc) if nasc else None})
            if resp:
                st.success("Perfil criado!")
                st.rerun()
        return

    st.markdown(f"""
    <div class="bloco">
      <div class="bloco-title">👤 {candidato['nome']}</div>
      <div style="font-size:13px;color:#68788e">
        ✉️ {candidato['email']}
        {' · 📞 ' + candidato['telefone'] if candidato.get('telefone') else ''}
        {' · 📍 ' + candidato['cidade'] + '/' + (candidato.get('estado') or '') if candidato.get('cidade') else ''}
      </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("✏️ Editar dados de contato"):
        tel, cid, uf, nasc, btn = _form_cand(candidato)
        if btn:
            resp = api_put(f"/candidatos/{candidato['id']}", json={
                "nome":candidato["nome"],"email":candidato["email"],
                "telefone":tel or None,"cidade":cid or None,
                "estado":uf.upper() if uf else None,
                "data_nascimento":str(nasc) if nasc else None})
            if resp:
                st.success("Dados atualizados!")
                st.rerun()

    st.markdown("### 📄 Minhas Candidaturas")
    candidaturas = api_get("/candidaturas/")
    minhas = [c for c in (candidaturas or []) if c.get("candidato_id")==candidato["id"]]

    if not minhas:
        st.info("Você ainda não se candidatou a nenhuma vaga.")
        if st.button("💼 Ver vagas", type="primary"):
            st.session_state.pagina = "vagas"
            st.rerun()
        return

    for cand in minhas:
        v_inline = cand.get("vaga") or {}
        titulo   = v_inline.get("titulo","—")
        empresa  = (v_inline.get("empresa") or {}).get("nome","—")
        s = cand.get("status","pendente")
        cor = STATUS_COR.get(s,"#555")
        st.markdown(f"""
        <div style="border-left:4px solid {cor};border-radius:8px;padding:10px 14px;margin-bottom:8px;background:#fff;border:1px solid #e8f0f8;border-left-width:4px">
          <div style="display:flex;justify-content:space-between;align-items:center">
            <div>
              <div style="font-weight:700;font-size:14px">{titulo}</div>
              <div style="font-size:12px;color:#68788e">🏭 {empresa} &nbsp;·&nbsp; 📅 {cand.get('data_candidatura','')}</div>
            </div>
            <span class="pill {'pill-pend' if s=='pendente' else 'pill-analise' if s=='em_analise' else 'pill-aprov' if s=='aprovado' else 'pill-reprov'}">{STATUS_LABEL.get(s,s)}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)


# ── Candidatos (Admin) ────────────────────────────────────────────────────────

def tela_candidatos():
    _sidebar()
    _topbar("👤 Candidatos")

    candidatos = api_get("/candidatos/") or []
    st.caption(f"{len(candidatos)} candidato(s)")

    for c in candidatos:
        with st.container(border=True):
            c1,c2,c3 = st.columns([3,2,1])
            with c1:
                st.markdown(f"**{c['nome']}**")
                st.caption(c["email"])
            with c2:
                info = []
                if c.get("telefone"): info.append(f"📞 {c['telefone']}")
                if c.get("cidade"):   info.append(f"📍 {c['cidade']}/{c.get('estado','')}")
                st.caption("  ·  ".join(info) or "Sem dados de contato")
            with c3:
                if st.button("✏️", key=f"ed_cand_{c['id']}", use_container_width=True):
                    st.session_state["candidato_editar"] = c["id"]
                    st.rerun()


def tela_editar_candidato(candidato_id):
    _sidebar()
    c = api_get(f"/candidatos/{candidato_id}")
    if not c:
        st.session_state.pop("candidato_editar", None)
        st.rerun()

    _topbar(f"✏️ Editar: {c['nome']}")

    if st.button("← Voltar"):
        st.session_state.pop("candidato_editar", None)
        st.rerun()

    with st.form("form_ed_cand"):
        col1,col2 = st.columns(2)
        with col1:
            nome  = st.text_input("Nome *", value=c["nome"])
            email = st.text_input("Email *", value=c["email"])
            tel   = st.text_input("Telefone", value=c.get("telefone") or "")
        with col2:
            cid = st.text_input("Cidade", value=c.get("cidade") or "")
            uf  = st.text_input("UF", value=c.get("estado") or "", max_chars=2)
            nasc_v = None
            if c.get("data_nascimento"):
                try: nasc_v = date.fromisoformat(c["data_nascimento"])
                except Exception: pass
            nasc = st.date_input("Data de nascimento", value=nasc_v)
        salvar = st.form_submit_button("Salvar", type="primary")

    if salvar:
        resp = api_put(f"/candidatos/{candidato_id}", json={
            "nome":nome,"email":email,"telefone":tel or None,
            "cidade":cid or None,"estado":uf.upper() if uf else None,
            "data_nascimento":str(nasc) if nasc else None})
        if resp:
            st.success("✅ Atualizado!")
            st.session_state.pop("candidato_editar", None)
            st.rerun()


# ── Assistente IA ─────────────────────────────────────────────────────────────

def _contexto_sistema():
    token = st.session_state.token
    h = {"Authorization": f"Bearer {token}"}
    linhas = []
    try:
        vagas = requests.get(f"{API_URL}/vagas/", headers=h, timeout=10).json()
        abertas = [v for v in vagas if v.get("status")=="aberta"]
        linhas.append(f"Total de vagas: {len(vagas)} ({len(abertas)} abertas, {len(vagas)-len(abertas)} encerradas).")
        for v in abertas[:15]:
            empresa = v.get("empresa",{}).get("nome","N/A")
            enc = v.get("encaminhados") or 0
            prio = v.get("prioridade") or "—"
            linhas.append(f"- {v['titulo']} | Empresa: {empresa} | Modalidade: {v.get('modalidade','')} | "
                          f"Contrato: {v.get('tipo_contrato','')} | Salário: R$ {v.get('salario',0):,.0f} | "
                          f"Prioridade: {prio} | Encaminhados: {enc} | PcD: {'Sim' if v.get('vaga_pcd') else 'Não'}")
    except Exception:
        linhas.append("Não foi possível obter dados de vagas.")
    try:
        cands = requests.get(f"{API_URL}/candidaturas/", headers=h, timeout=10).json()
        linhas.append(f"\nTotal de candidaturas: {len(cands)}.")
        from collections import Counter
        for s, n in Counter(c.get("status") for c in cands).items():
            linhas.append(f"  - {s}: {n}")
    except Exception:
        pass
    return "\n".join(linhas)


def tela_assistente():
    _sidebar()
    _topbar("🤖 Assistente IA")

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
                system_prompt = f"""Você é um assistente especializado em recrutamento da TGA Empregos.
Responda em português, de forma clara e objetiva. Máximo 300 palavras.
Dados atuais do sistema:

{contexto}

Use esses dados para responder sobre vagas, candidaturas, encaminhamentos e estatísticas.
Para perguntas gerais sobre carreira, currículo e emprego, responda com base no seu conhecimento."""

                contents = [{"role":"user","parts":[{"text":system_prompt}]},
                            {"role":"model","parts":[{"text":"Entendido! Pronto para ajudar."}]}]
                for m in st.session_state.chat_historico[:-1][-10:]:
                    contents.append({"role":"user" if m["role"]=="user" else "model","parts":[{"text":m["content"]}]})
                contents.append({"role":"user","parts":[{"text":pergunta}]})

                try:
                    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"
                    r = requests.post(url, json={"contents":contents,"generationConfig":{"maxOutputTokens":2048,"temperature":0.7}}, timeout=30)
                    r.raise_for_status()
                    resposta = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                except Exception as e:
                    resposta = f"Erro ao consultar a IA: {e}"

                st.markdown(resposta)
                st.session_state.chat_historico.append({"role":"assistant","content":resposta})

    if st.session_state.chat_historico:
        if st.button("🗑️ Limpar conversa"):
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
elif st.session_state.pagina == "vagas":
    tela_vagas(apenas_encerradas=False)
elif st.session_state.pagina == "encerradas":
    tela_vagas(apenas_encerradas=True)
elif st.session_state.pagina == "recrutador":
    tela_recrutador()
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
    tela_vagas()

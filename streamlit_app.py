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

        if perfil == "visualizador":
            if st.button("📋 Minhas Candidaturas", use_container_width=True):
                st.session_state.pagina = "candidaturas"
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

    st.divider()

    if pode_escrever:
        st.markdown("### ⚙️ Ações")
        col_enc, col_del = st.columns(2)
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

    elif perfil == "visualizador" and vaga["status"] == "aberta":
        st.markdown("### 🚀 Candidatar-se")
        candidatos = api_get("/candidatos/")
        usuario = st.session_state.usuario
        candidato_id = None
        if candidatos:
            for c in candidatos:
                if c.get("email") == usuario.get("email"):
                    candidato_id = c["id"]
                    break

        if candidato_id:
            if st.button("✅ Candidatar-se a esta vaga", use_container_width=True, type="primary"):
                resp = api_post("/candidaturas/", json={
                    "candidato_id": candidato_id,
                    "vaga_id": vaga_id,
                })
                if resp:
                    st.success("Candidatura enviada com sucesso!")
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
    _sidebar()

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
        if contagem_mod:
            st.bar_chart(contagem_mod, color="#1565C0", height=200)

    with col_b:
        st.markdown("### 📄 Vagas por Contrato")
        contagem_cont = {}
        for v in vagas:
            c = CONTRATO_LABEL.get(v["tipo_contrato"], v["tipo_contrato"])
            contagem_cont[c] = contagem_cont.get(c, 0) + 1
        if contagem_cont:
            st.bar_chart(contagem_cont, color="#2E7D32", height=200)

    st.divider()

    col_c, col_d = st.columns(2)

    with col_c:
        st.markdown("### 🏭 Vagas por Empresa")
        contagem_emp = {}
        for v in vagas:
            nome = v["empresa"]["nome"]
            contagem_emp[nome] = contagem_emp.get(nome, 0) + 1
        if contagem_emp:
            st.bar_chart(contagem_emp, color="#6A1B9A", height=250)

    with col_d:
        st.markdown("### 💰 Salário Médio por Setor")
        setor_salarios = {}
        for v in vagas:
            if v.get("salario"):
                setor = v["empresa"].get("setor", "Outros")
                setor_salarios.setdefault(setor, []).append(v["salario"])

        if setor_salarios:
            medias = {s: round(sum(vals)/len(vals)) for s, vals in setor_salarios.items()}
            st.bar_chart(medias, color="#E65100", height=250)
            maior = max(sum(s)/len(s) for s in setor_salarios.values())
            cores_sal = ["#E65100","#F57C00","#FB8C00","#FFA726","#FFCC80"]
            for i, (setor, salarios) in enumerate(sorted(setor_salarios.items(), key=lambda x: -sum(x[1])/len(x[1]))):
                media = sum(salarios) / len(salarios)
                media_fmt = f"R$ {media:,.0f}".replace(",", ".")
                pct = media / maior * 100
                st.markdown(f"""
                <div style="margin-bottom:6px">
                  <div style="display:flex;justify-content:space-between">
                    <span style="font-size:12px;color:#555">{setor}</span>
                    <span style="font-size:12px;font-weight:600">{media_fmt}</span>
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
    alertas = [(v, d) for v, d in vagas_antigas if d >= 30]

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
    _sidebar()
    usuario = st.session_state.usuario

    st.markdown("# 📋 Meu Perfil de Candidato")

    candidatos = api_get("/candidatos/")
    candidato = None
    if candidatos:
        for c in candidatos:
            if c.get("email") == usuario.get("email"):
                candidato = c
                break

    if not candidato:
        st.info("Você ainda não tem um perfil de candidato. Preencha abaixo para poder se candidatar às vagas.")
        with st.form("form_candidato"):
            col1, col2 = st.columns(2)
            with col1:
                nome_c   = st.text_input("Nome completo *", value=usuario.get("nome", ""))
                email_c  = st.text_input("Email *", value=usuario.get("email", ""), disabled=True)
                telefone = st.text_input("Telefone")
            with col2:
                cidade   = st.text_input("Cidade")
                estado   = st.text_input("Estado (UF)", max_chars=2)
                nasc     = st.date_input("Data de nascimento", value=None)
            salvar = st.form_submit_button("Salvar perfil", type="primary")

        if salvar:
            resp = api_post("/candidatos/", json={
                "nome": nome_c,
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
    st.markdown(f"""
    <div style="background:#e3f2fd;border-radius:12px;padding:16px 20px;margin-bottom:16px">
      <div style="font-size:18px;font-weight:700">👤 {candidato['nome']}</div>
      <div style="color:#555;font-size:13px">✉️ {candidato['email']}
      {"&nbsp;&nbsp;📞 " + candidato['telefone'] if candidato.get('telefone') else ""}
      {"&nbsp;&nbsp;📍 " + candidato['cidade'] + "/" + candidato['estado'] if candidato.get('cidade') else ""}
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📄 Minhas Candidaturas")
    candidaturas = api_get("/candidaturas/")
    minhas = [c for c in (candidaturas or []) if c.get("candidato_id") == candidato["id"]]

    STATUS_COR = {
        "pendente":   ("#F9A825", "#fffde7"),
        "em_analise": ("#1565C0", "#e3f2fd"),
        "aprovado":   ("#2E7D32", "#e8f5e9"),
        "reprovado":  ("#B71C1C", "#fce4ec"),
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

    for cand in minhas:
        vaga = cand.get("vaga", {})
        status = cand.get("status", "pendente")
        cor, bg = STATUS_COR.get(status, ("#555", "#f5f5f5"))
        st.markdown(f"""
        <div style="background:{bg};border-left:4px solid {cor};border-radius:8px;padding:12px 16px;margin-bottom:10px">
          <div style="display:flex;justify-content:space-between;align-items:center">
            <div>
              <div style="font-weight:700;font-size:15px">{vaga.get('titulo','—')}</div>
              <div style="color:#555;font-size:13px">🏭 {vaga.get('empresa',{}).get('nome','—')} &nbsp;|&nbsp; 📅 {cand.get('data_candidatura','')}</div>
            </div>
            <div style="background:{cor};color:white;padding:4px 12px;border-radius:12px;font-size:12px;font-weight:600">
              {STATUS_LABEL.get(status, status)}
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)


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
elif st.session_state.pagina == "candidaturas":
    tela_candidaturas()
else:
    tela_painel()

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function getToken() {
  return localStorage.getItem("token");
}

async function request(path, options = {}) {
  const token = getToken();
  const headers = { "Content-Type": "application/json", ...options.headers };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${BASE_URL}${path}`, { ...options, headers });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw Object.assign(new Error(body.detail || `Erro ${res.status}`), { status: res.status });
  }
  if (res.status === 204) return null;
  return res.json();
}

export const api = {
  // Auth
  login: async (email, senha) => {
    const form = new URLSearchParams({ username: email, password: senha });
    const res = await fetch(`${BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: form,
    });
    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      throw new Error(body.detail || "Credenciais inválidas");
    }
    return res.json();
  },
  me: () => request("/auth/me"),

  // Vagas (leitura pública)
  getVagas: (filters = {}) => {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([k, v]) => {
      if (v !== "" && v !== null && v !== undefined) params.append(k, v);
    });
    const qs = params.toString();
    return request(`/vagas/${qs ? `?${qs}` : ""}`);
  },
  getVaga: (id) => request(`/vagas/${id}`),

  // Vagas (escrita — requer admin/recrutador)
  criarVaga: (dados) => request("/vagas/", { method: "POST", body: JSON.stringify(dados) }),
  deletarVaga: (id) => request(`/vagas/${id}`, { method: "DELETE" }),

  // Empresas
  getEmpresas: () => request("/empresas/"),
};

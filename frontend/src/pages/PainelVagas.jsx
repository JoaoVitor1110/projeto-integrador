import { useState, useEffect, useCallback } from "react";
import { api } from "../services/api";
import VagaCard from "../components/VagaCard";
import VagaDetalhe from "../components/VagaDetalhe";
import Filtros from "../components/Filtros";

const FILTROS_INICIAIS = {
  modalidade: "",
  tipo_contrato: "",
  status: "",
  vaga_pcd: "",
};

const PERFIL_LABEL = { admin: "Admin", recrutador: "Recrutador", visualizador: "Visualizador" };

export default function PainelVagas({ usuario, onLogout }) {
  const [vagas, setVagas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState(null);
  const [filtros, setFiltros] = useState(FILTROS_INICIAIS);
  const [vagaSelecionada, setVagaSelecionada] = useState(null);

  const podeEscrever = usuario && ["admin", "recrutador"].includes(usuario.perfil);

  const carregarVagas = useCallback(async () => {
    setLoading(true);
    setErro(null);
    try {
      setVagas(await api.getVagas(filtros));
    } catch {
      setErro("Não foi possível carregar as vagas. Verifique se o backend está rodando.");
    } finally {
      setLoading(false);
    }
  }, [filtros]);

  useEffect(() => { carregarVagas(); }, [carregarVagas]);

  const abrirDetalhe = async (id) => {
    try {
      setVagaSelecionada(await api.getVaga(id));
    } catch {
      setVagaSelecionada(vagas.find((v) => v.id === id) ?? null);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    onLogout();
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navbar */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <span className="text-2xl">💼</span>
            <h1 className="text-xl font-bold text-gray-900">Agência de Empregos</h1>
          </div>

          <div className="flex items-center gap-3">
            {usuario && (
              <span className="text-sm text-gray-600 hidden sm:block">
                {usuario.nome}
                <span className="ml-1.5 bg-blue-100 text-blue-700 text-xs px-1.5 py-0.5 rounded">
                  {PERFIL_LABEL[usuario.perfil]}
                </span>
              </span>
            )}
            {podeEscrever && (
              <span className="text-xs text-green-700 bg-green-50 border border-green-200 px-2 py-1 rounded hidden sm:block">
                + pode criar vagas
              </span>
            )}
            <button
              onClick={handleLogout}
              className="text-sm text-gray-500 hover:text-gray-800 border border-gray-200 px-3 py-1.5 rounded-lg hover:bg-gray-50 transition"
            >
              Sair
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 py-6 space-y-5">
        <div className="flex items-center justify-between gap-4">
          <p className="text-sm text-gray-500">
            {!loading && `${vagas.length} vaga${vagas.length !== 1 ? "s" : ""} encontrada${vagas.length !== 1 ? "s" : ""}`}
          </p>
        </div>

        <Filtros filtros={filtros} onChange={setFiltros} />

        {loading && (
          <div className="text-center py-16 text-gray-400">
            <div className="animate-spin text-4xl mb-3">⟳</div>
            <p>Carregando vagas...</p>
          </div>
        )}

        {!loading && erro && (
          <div className="bg-red-50 border border-red-200 text-red-700 rounded-xl p-4 text-sm">{erro}</div>
        )}

        {!loading && !erro && vagas.length === 0 && (
          <div className="text-center py-16 text-gray-400">
            <p className="text-4xl mb-3">🔍</p>
            <p>Nenhuma vaga encontrada para os filtros selecionados.</p>
          </div>
        )}

        {!loading && !erro && vagas.length > 0 && (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {vagas.map((vaga) => (
              <VagaCard key={vaga.id} vaga={vaga} onClick={() => abrirDetalhe(vaga.id)} />
            ))}
          </div>
        )}
      </main>

      {vagaSelecionada && (
        <VagaDetalhe vaga={vagaSelecionada} onClose={() => setVagaSelecionada(null)} />
      )}
    </div>
  );
}

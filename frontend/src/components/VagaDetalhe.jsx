import StatusBadge from "./StatusBadge";

const MODALIDADE_LABEL = {
  presencial: "Presencial",
  remoto: "Remoto",
  hibrido: "Híbrido",
};

const CONTRATO_LABEL = {
  CLT: "CLT",
  PJ: "PJ",
  temporario: "Temporário",
  estagio: "Estágio",
};

const PUBLICO_LABEL = {
  masculino: "Masculino",
  feminino: "Feminino",
  ambos: "Ambos",
};

export default function VagaDetalhe({ vaga, onClose }) {
  const salario = vaga.salario
    ? vaga.salario.toLocaleString("pt-BR", { style: "currency", currency: "BRL" })
    : "A combinar";

  const dataPublicacao = vaga.data_publicacao
    ? new Date(vaga.data_publicacao + "T00:00:00").toLocaleDateString("pt-BR")
    : "—";

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      style={{ backgroundColor: "rgba(0,0,0,0.5)" }}
      onClick={onClose}
    >
      <div
        className="bg-white rounded-2xl shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="sticky top-0 bg-white border-b border-gray-100 px-6 py-4 flex items-start justify-between gap-4 rounded-t-2xl">
          <div>
            <h2 className="text-xl font-bold text-gray-900">{vaga.titulo}</h2>
            <p className="text-blue-700 font-medium text-sm mt-0.5">{vaga.empresa?.nome}</p>
          </div>
          <div className="flex items-center gap-3 shrink-0">
            <StatusBadge status={vaga.status} />
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-700 text-xl leading-none"
              aria-label="Fechar"
            >
              ✕
            </button>
          </div>
        </div>

        {/* Body */}
        <div className="px-6 py-5 space-y-5">
          {/* Infos rápidas */}
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            {[
              ["📍 Local", vaga.local],
              ["🏢 Modalidade", MODALIDADE_LABEL[vaga.modalidade] ?? vaga.modalidade],
              ["📄 Contrato", CONTRATO_LABEL[vaga.tipo_contrato] ?? vaga.tipo_contrato],
              ["💰 Salário", salario],
              ["🕐 Horário", vaga.horario ?? "—"],
              ["👤 Público", PUBLICO_LABEL[vaga.publico_alvo] ?? vaga.publico_alvo],
              ["♿ PcD", vaga.vaga_pcd ? "Sim" : "Não"],
              ["📅 Publicação", dataPublicacao],
            ].map(([label, val]) => (
              <div key={label} className="bg-gray-50 rounded-lg p-3">
                <p className="text-xs text-gray-500 mb-0.5">{label}</p>
                <p className="text-sm font-medium text-gray-800">{val}</p>
              </div>
            ))}
          </div>

          {/* Benefícios */}
          {vaga.beneficios?.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-gray-700 mb-2">Benefícios</h3>
              <div className="flex flex-wrap gap-2">
                {vaga.beneficios.map((b) => (
                  <span key={b.id} className="bg-green-50 text-green-800 text-xs px-3 py-1 rounded-full">
                    {b.nome}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Requisitos */}
          {vaga.requisitos?.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-gray-700 mb-2">Requisitos</h3>
              <ul className="space-y-1.5">
                {vaga.requisitos.map((r) => (
                  <li key={r.id} className="flex items-start gap-2 text-sm text-gray-700">
                    <span className={`mt-0.5 shrink-0 text-xs font-medium px-1.5 py-0.5 rounded ${
                      r.nivel === "obrigatorio"
                        ? "bg-red-50 text-red-700"
                        : "bg-blue-50 text-blue-700"
                    }`}>
                      {r.nivel === "obrigatorio" ? "Obrigatório" : "Desejável"}
                    </span>
                    {r.descricao}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

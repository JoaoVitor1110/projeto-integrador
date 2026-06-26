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

export default function VagaCard({ vaga, onClick }) {
  const salario = vaga.salario
    ? vaga.salario.toLocaleString("pt-BR", { style: "currency", currency: "BRL" })
    : "A combinar";

  return (
    <button
      onClick={onClick}
      className="w-full text-left bg-white border border-gray-200 rounded-xl p-5 hover:shadow-md hover:border-blue-300 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-400"
    >
      <div className="flex items-start justify-between gap-3 mb-3">
        <h2 className="text-lg font-semibold text-gray-900 leading-tight">{vaga.titulo}</h2>
        <StatusBadge status={vaga.status} />
      </div>

      <p className="text-sm font-medium text-blue-700 mb-3">{vaga.empresa?.nome}</p>

      <div className="flex flex-wrap gap-2 text-xs">
        <span className="bg-blue-50 text-blue-700 px-2 py-1 rounded-md">
          📍 {vaga.local}
        </span>
        <span className="bg-purple-50 text-purple-700 px-2 py-1 rounded-md">
          {MODALIDADE_LABEL[vaga.modalidade] ?? vaga.modalidade}
        </span>
        <span className="bg-amber-50 text-amber-700 px-2 py-1 rounded-md">
          {CONTRATO_LABEL[vaga.tipo_contrato] ?? vaga.tipo_contrato}
        </span>
        {vaga.vaga_pcd && (
          <span className="bg-teal-50 text-teal-700 px-2 py-1 rounded-md">♿ PcD</span>
        )}
      </div>

      <p className="mt-3 text-sm font-semibold text-gray-700">{salario}</p>
    </button>
  );
}

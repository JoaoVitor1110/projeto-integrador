const MODALIDADES = [
  { value: "", label: "Todas modalidades" },
  { value: "presencial", label: "Presencial" },
  { value: "remoto", label: "Remoto" },
  { value: "hibrido", label: "Híbrido" },
];

const CONTRATOS = [
  { value: "", label: "Todos os contratos" },
  { value: "CLT", label: "CLT" },
  { value: "PJ", label: "PJ" },
  { value: "temporario", label: "Temporário" },
  { value: "estagio", label: "Estágio" },
];

const STATUS_OPTIONS = [
  { value: "", label: "Qualquer status" },
  { value: "aberta", label: "Abertas" },
  { value: "encerrada", label: "Encerradas" },
];

export default function Filtros({ filtros, onChange }) {
  const set = (key) => (e) => onChange({ ...filtros, [key]: e.target.value });
  const setCheck = (key) => (e) =>
    onChange({ ...filtros, [key]: e.target.checked ? "true" : "" });

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-4 flex flex-wrap gap-3 items-center">
      <select
        value={filtros.modalidade}
        onChange={set("modalidade")}
        className="text-sm border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
      >
        {MODALIDADES.map((o) => (
          <option key={o.value} value={o.value}>{o.label}</option>
        ))}
      </select>

      <select
        value={filtros.tipo_contrato}
        onChange={set("tipo_contrato")}
        className="text-sm border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
      >
        {CONTRATOS.map((o) => (
          <option key={o.value} value={o.value}>{o.label}</option>
        ))}
      </select>

      <select
        value={filtros.status}
        onChange={set("status")}
        className="text-sm border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
      >
        {STATUS_OPTIONS.map((o) => (
          <option key={o.value} value={o.value}>{o.label}</option>
        ))}
      </select>

      <label className="flex items-center gap-2 text-sm text-gray-700 cursor-pointer select-none">
        <input
          type="checkbox"
          checked={filtros.vaga_pcd === "true"}
          onChange={setCheck("vaga_pcd")}
          className="w-4 h-4 rounded accent-blue-600"
        />
        Somente PcD
      </label>
    </div>
  );
}

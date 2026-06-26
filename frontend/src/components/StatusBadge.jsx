export default function StatusBadge({ status }) {
  const isAberta = status === "aberta";
  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium ${
        isAberta
          ? "bg-green-100 text-green-800"
          : "bg-gray-100 text-gray-600"
      }`}
    >
      <span
        className={`w-1.5 h-1.5 rounded-full ${
          isAberta ? "bg-green-500" : "bg-gray-400"
        }`}
      />
      {isAberta ? "Aberta" : "Encerrada"}
    </span>
  );
}

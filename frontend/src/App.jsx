import { useState, useEffect } from "react";
import Login from "./pages/Login";
import PainelVagas from "./pages/PainelVagas";
import { api } from "./services/api";

export default function App() {
  const [usuario, setUsuario] = useState(undefined); // undefined = carregando

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) { setUsuario(null); return; }
    api.me()
      .then(setUsuario)
      .catch(() => { localStorage.removeItem("token"); setUsuario(null); });
  }, []);

  if (usuario === undefined) {
    return (
      <div className="min-h-screen flex items-center justify-center text-gray-400">
        Carregando...
      </div>
    );
  }

  if (!usuario) {
    return <Login onLogin={setUsuario} />;
  }

  return <PainelVagas usuario={usuario} onLogout={() => setUsuario(null)} />;
}

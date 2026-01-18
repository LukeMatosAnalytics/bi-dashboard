import { useEffect, useState } from "react";
import { getSelosPendentesFnc } from "../services/bi.service";
import type { SeloPendente } from "../types/bi.types";
import { useAuthStore } from "../../../auth/auth.store";

export function SelosPendentesPage() {
  const user = useAuthStore(state => state.user);

  const [data, setData] = useState<SeloPendente[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!user) return;

    async function load() {
      setLoading(true);
      setError(null);

      try {
        const result = await getSelosPendentesFnc({
          contrato_id: user.contrato_id,
          data_inicio: "2025-12-01",
          data_fim: "2025-12-31",
        });

        setData(result.registros || []);
      } catch (err: any) {
        setError(err?.error?.message || "Erro ao carregar dados");
      } finally {
        setLoading(false);
      }
    }

    load();
  }, [user]);

  return (
    <div>
      <h2>Selos pendentes no FNC</h2>

      {loading && <p>Carregando...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {!loading && !error && data.length === 0 && (
        <p>Nenhum selo pendente encontrado.</p>
      )}

      {!loading && data.length > 0 && (
        <table border={1} cellPadding={6}>
          <thead>
            <tr>
              <th>Selo</th>
              <th>Tipo Ato</th>
              <th>Cód. Ato</th>
              <th>Descrição</th>
              <th>Data Ato</th>
            </tr>
          </thead>
          <tbody>
            {data.map((row, idx) => (
              <tr key={idx}>
                <td>{row.selo_principal}</td>
                <td>{row.tipo_ato}</td>
                <td>{row.id_codigo_ato}</td>
                <td>{row.descricao_codigo_ato ?? "-"}</td>
                <td>{row.dataato}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

import { useEffect, useState } from "react";
import { useAuthStore } from "../../auth/auth.store";
import {
  getSelosDuplicadosMesmoSistema,
  getSelosDuplicadosSistemasDiferentes,
  SelosDuplicadosMesmoSistema,
  SelosDuplicadosSistemasDiferentes
} from "./inconsistencias.service";

type TipoVisual = "MESMO_SISTEMA" | "SISTEMAS_DIFERENTES";

export function InconsistenciasPage() {
  const user = useAuthStore(state => state.user);

  const [dataInicio, setDataInicio] = useState("");
  const [dataFim, setDataFim] = useState("");

  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState<string | null>(null);

  const [mesmoSistema, setMesmoSistema] =
    useState<SelosDuplicadosMesmoSistema | null>(null);

  const [sistemasDiferentes, setSistemasDiferentes] =
    useState<SelosDuplicadosSistemasDiferentes | null>(null);

  const [visualAtivo, setVisualAtivo] =
    useState<TipoVisual>("MESMO_SISTEMA");

  async function carregarDados() {
    if (!user || !dataInicio || !dataFim) return;

    setErro(null);
    setLoading(true);

    try {
      const [ms, sd] = await Promise.all([
        getSelosDuplicadosMesmoSistema({
          contrato_id: user.contrato_id,
          data_inicio: dataInicio,
          data_fim: dataFim,
        }),
        getSelosDuplicadosSistemasDiferentes({
          contrato_id: user.contrato_id,
          data_inicio: dataInicio,
          data_fim: dataFim,
        }),
      ]);

      setMesmoSistema(ms);
      setSistemasDiferentes(sd);
    } catch (e: any) {
      setErro(e?.error?.message || "Erro ao carregar inconsistências");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    carregarDados();
  }, []);

  return (
    <div style={{ padding: 24 }}>
      <h1>Inconsistências de Selos</h1>

      {/* Filtros */}
      <div style={{ display: "flex", gap: 12, marginBottom: 20 }}>
        <input
          type="date"
          value={dataInicio}
          onChange={e => setDataInicio(e.target.value)}
        />
        <input
          type="date"
          value={dataFim}
          onChange={e => setDataFim(e.target.value)}
        />
        <button onClick={carregarDados}>Buscar</button>
      </div>

      {erro && <p style={{ color: "red" }}>{erro}</p>}
      {loading && <p>Carregando...</p>}

      {/* KPIs */}
      <div style={{ display: "flex", gap: 20, marginBottom: 20 }}>
        <div
          style={{ cursor: "pointer" }}
          onClick={() => setVisualAtivo("MESMO_SISTEMA")}
        >
          <strong>Mesmo sistema</strong>
          <div>{mesmoSistema?.total_selos ?? "-"}</div>
        </div>

        <div
          style={{ cursor: "pointer", color: "darkred" }}
          onClick={() => setVisualAtivo("SISTEMAS_DIFERENTES")}
        >
          <strong>Sistemas diferentes</strong>
          <div>{sistemasDiferentes?.total_selos ?? "-"}</div>
        </div>
      </div>

      {/* Tabela */}
      {visualAtivo === "MESMO_SISTEMA" && mesmoSistema && (
        <table border={1} cellPadding={6}>
          <thead>
            <tr>
              <th>Selo</th>
              <th>Sistema</th>
              <th>Tipo Ato</th>
              <th>Livro</th>
              <th>Folha</th>
              <th>Data</th>
              <th>Ocorrências</th>
            </tr>
          </thead>
          <tbody>
            {mesmoSistema.registros.map((r, i) => (
              <tr key={i}>
                <td>{r.selo_principal}</td>
                <td>{r.sistema_origem_id}</td>
                <td>{r.tipo_ato}</td>
                <td>{r.livro}</td>
                <td>{r.folha}</td>
                <td>{r.dataato}</td>
                <td>{r.total_ocorrencias}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {visualAtivo === "SISTEMAS_DIFERENTES" && sistemasDiferentes && (
        <table border={1} cellPadding={6}>
          <thead>
            <tr>
              <th>Selo</th>
              <th>Sistemas</th>
              <th>Primeira ocorrência</th>
              <th>Última ocorrência</th>
            </tr>
          </thead>
          <tbody>
            {sistemasDiferentes.registros.map((r, i) => (
              <tr key={i}>
                <td>{r.selo_principal}</td>
                <td>{r.sistemas_origem.join(", ")}</td>
                <td>{r.primeira_ocorrencia}</td>
                <td>{r.ultima_ocorrencia}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

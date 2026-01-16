import { useEffect, useState } from "react";
import { getMetrics } from "./Services/Metrics";
import type { Metric } from "./types/Metrics";
import { MetricsTable } from "./components/MetricsTable";
import { KpiCard } from "./components/KpiCard";

function App() {
  const [metrics, setMetrics] = useState<Metric[]>([]);

  useEffect(() => {
    getMetrics().then(setMetrics);
  }, []);

  const latestByName = (name: string) => {
    return metrics
      .filter((m) => m.name === name)
      .sort(
        (a, b) =>
          new Date(b.created_at).getTime() -
          new Date(a.created_at).getTime()
      )[0];
  };

  const atendimentos = latestByName("Atendimentos")?.value ?? "-";
  const receita = latestByName("Receita")?.value ?? "-";
  const satisfacao = latestByName("Satisfação")?.value ?? "-";

  return (
    <div style={{ padding: 24 }}>
      <h1>BI Dashboard</h1>

      <div style={{ display: "flex", gap: 16, marginBottom: 24 }}>
        <KpiCard title="Atendimentos" value={atendimentos} />
        <KpiCard title="Receita (R$)" value={receita} />
        <KpiCard title="Satisfação" value={satisfacao} />
      </div>

      <MetricsTable metrics={metrics} />
    </div>
  );
}

export default App;

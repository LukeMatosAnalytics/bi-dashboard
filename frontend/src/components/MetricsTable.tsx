import type { Metric } from "../types/Metrics";

interface MetricsTableProps {
  metrics: Metric[];
}

export function MetricsTable({ metrics }: MetricsTableProps) {
  return (
    <table border={1} cellPadding={8}>
      <thead>
        <tr>
          <th>ID</th>
          <th>Nome</th>
          <th>Valor</th>
          <th>Categoria</th>
          <th>Data</th>
        </tr>
      </thead>
      <tbody>
        {metrics.map((metric) => (
          <tr key={metric.id}>
            <td>{metric.id}</td>
            <td>{metric.name}</td>
            <td>{metric.value}</td>
            <td>{metric.category}</td>
            <td>
              {new Date(metric.created_at).toLocaleDateString("pt-BR")}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

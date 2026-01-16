interface KpiCardProps {
  title: string;
  value: string | number;
}

export function KpiCard({ title, value }: KpiCardProps) {
  return (
    <div
      style={{
        border: "1px solid #ccc",
        borderRadius: 8,
        padding: 16,
        minWidth: 200,
      }}
    >
      <h3>{title}</h3>
      <strong style={{ fontSize: 24 }}>{value}</strong>
    </div>
  );
}

import { useAuthStore } from "../auth/auth.store";

export function Header() {
  const user = useAuthStore((state) => state.user);

  return (
    <header
      style={{
        height: 56,
        borderBottom: "1px solid #ddd",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "0 16px",
      }}
    >
      <strong>BI Dashboard</strong>

      {user && (
        <div style={{ fontSize: 14 }}>
          {user.email} ({user.role}) — contrato {user.contrato_id}
        </div>
      )}
    </header>
  );
}

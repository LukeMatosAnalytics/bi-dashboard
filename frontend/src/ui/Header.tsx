import { useAuthStore } from "../auth/auth.store";

export function Header() {
  const user = useAuthStore(state => state.user);

  return (
    <header
      style={{
        height: 56,
        borderBottom: "1px solid #e5e7eb",
        padding: "0 24px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        background: "#fff",
      }}
    >
      <strong>BI Dashboard</strong>

      <div style={{ display: "flex", gap: 16, alignItems: "center" }}>
        {user && (
          <span style={{ fontSize: 14 }}>
            {user.email} ({user.role})
          </span>
        )}
      </div>
    </header>
  );
}

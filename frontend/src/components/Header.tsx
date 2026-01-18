import { useAuthStore } from "../auth/auth.store";

export function Header() {
  const user = useAuthStore((state) => state.user);

  return (
    <header
      style={{
        height: 56,
        background: "#fff",
        borderBottom: "1px solid #ddd",
        padding: "0 16px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
      }}
    >
      <strong>BI Dashboard</strong>

      {user && (
        <span>
          {user.email} ({user.role})
        </span>
      )}
    </header>
  );
}

import { NavLink } from "react-router-dom";
import { useAuthStore } from "../auth/auth.store";

export function Sidebar() {
  const user = useAuthStore(state => state.user);

  return (
    <aside
      style={{
        width: 220,
        borderRight: "1px solid #e5e7eb",
        padding: 16,
        background: "#f9fafb",
      }}
    >
      <nav style={{ display: "flex", flexDirection: "column", gap: 8 }}>
        <NavLink to="/">Dashboard</NavLink>

        {(user?.role === "ADMIN" || user?.role === "MASTER") && (
          <>
            <NavLink to="/importacao">Importação</NavLink>
            <NavLink to="/logs">Logs</NavLink>
          </>
        )}
      </nav>
    </aside>
  );
}

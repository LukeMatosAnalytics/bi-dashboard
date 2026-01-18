import { NavLink } from "react-router-dom";

export function Sidebar() {
  return (
    <aside
      style={{
        width: 220,
        background: "#f5f5f5",
        padding: 16,
        borderRight: "1px solid #ddd",
      }}
    >
      <h3>Dashboard</h3>

      <nav style={{ display: "flex", flexDirection: "column", gap: 8 }}>
        <NavLink to="/">Home</NavLink>
        <NavLink to="/importacao">Importação</NavLink>
        <NavLink to="/logs">Logs</NavLink>
      </nav>
    </aside>
  );
}

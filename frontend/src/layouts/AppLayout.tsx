import { Outlet } from "react-router-dom";
import { Sidebar } from "../components/Sidebar";
import { Header } from "../components/Header";

export function AppLayout() {
  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <Sidebar />

      <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
        <Header />

        <main style={{ padding: 16, flex: 1 }}>
          <Outlet />
        </main>
      </div>
    </div>
  );
}

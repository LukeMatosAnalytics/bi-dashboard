import { Outlet } from "react-router-dom";
import { Header } from "../ui/Header";
import { Sidebar } from "../ui/Sidebar";

export function MainLayout() {
  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <Sidebar />
      <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
        <Header />
        <main style={{ flex: 1, padding: 24, overflow: "auto" }}>
          <Outlet />
        </main>
      </div>
    </div>
  );
}

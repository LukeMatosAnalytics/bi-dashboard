import { Navigate, Outlet } from "react-router-dom";
import { useAuthStore } from "./auth.store";

export function RequireAuth() {
  const token = useAuthStore(state => state.token);
  const user = useAuthStore(state => state.user);

  if (!token || !user) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}

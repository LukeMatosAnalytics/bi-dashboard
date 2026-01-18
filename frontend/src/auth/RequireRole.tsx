import { Navigate, Outlet } from "react-router-dom";
import { useAuthStore } from "./auth.store";
import type { UserRole } from "./auth.types";

interface RequireRoleProps {
  roles: UserRole[];
}

export function RequireRole({ roles }: RequireRoleProps) {
  const user = useAuthStore(state => state.user);

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (!roles.includes(user.role)) {
    return <Navigate to="/" replace />;
  }

  return <Outlet />;
}
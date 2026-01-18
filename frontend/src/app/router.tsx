import { createBrowserRouter } from "react-router-dom";

import { LoginPage } from "../auth/LoginPage";
import { RequireAuth } from "../auth/RequireAuth";
import { RequireRole } from "../auth/RequireRole";

// Layout base
import { AppLayout } from "../layouts/AppLayout";

// Página de BI – Opção 1
import { SelosPendentesPage } from "../features/bi/pages/SelosPendentesPage";

export const router = createBrowserRouter([
  // ==========================
  // LOGIN (rota pública)
  // ==========================
  {
    path: "/login",
    element: <LoginPage />,
  },

  // ==========================
  // ROTAS PROTEGIDAS (logado)
  // ==========================
  {
    element: <RequireAuth />,
    children: [
      {
        // Layout base da aplicação
        element: <AppLayout />,
        children: [
          // --------------------------
          // HOME
          // --------------------------
          {
            path: "/",
            element: <div>Home</div>,
          },

          // ==========================
          // ROTAS ADMIN / MASTER
          // ==========================
          {
            element: <RequireRole roles={["ADMIN", "MASTER"]} />,
            children: [
              {
                // 👉 BI - Selos Pendentes no FNC
                path: "/importacao",
                element: <SelosPendentesPage />,
              },
              {
                path: "/logs",
                element: <div>Logs</div>,
              },
            ],
          },
        ],
      },
    ],
  },
]);

import { create } from "zustand";
import type { AuthUser } from "./auth.types";
import { getMe } from "./auth.service";

interface AuthState {
  token: string | null;
  user: (AuthUser & { contrato_id: string }) | null;
  setToken: (token: string) => void;
  loadUser: () => Promise<void>;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  token: null,
  user: null,

  setToken: (token) => {
    set({ token });
  },

  loadUser: async () => {
    const token = get().token;
    if (!token) return;

    const user = await getMe();
    set({ user });
  },

  logout: () => {
    set({ token: null, user: null });
  },
}));

import { api } from "../api/axios";
import { AuthUser } from "./auth.types";

interface LoginRequest {
  email: string;
  senha: string;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
}

export async function login(
  payload: LoginRequest
): Promise<LoginResponse> {
  const formData = new URLSearchParams();
  formData.append("username", payload.email);
  formData.append("password", payload.senha);

  const response = await api.post<LoginResponse>(
    "/auth/login",
    formData,
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    }
  );

  return response.data;
}

export async function getMe(): Promise<AuthUser & { contrato_id: string }> {
  const response = await api.get("/auth/me");
  return response.data;
}

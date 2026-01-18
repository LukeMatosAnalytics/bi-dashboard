export type UserRole = "ADMIN" | "MASTER" | "USUARIO";

export interface AuthUser {
  email: string;
  role: UserRole;
}

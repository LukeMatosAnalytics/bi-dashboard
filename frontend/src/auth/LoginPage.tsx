import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "./auth.service";
import { useAuthStore } from "./auth.store";

export function LoginPage() {
  const navigate = useNavigate();

  const setToken = useAuthStore(state => state.setToken);
  const loadUser = useAuthStore(state => state.loadUser);

  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErro(null);
    setLoading(true);

    try {
      const response = await login({ email, senha });

      // 1️⃣ salva o token
      setToken(response.access_token);

      // 2️⃣ carrega o usuário real via /auth/me
      await loadUser();

      // 3️⃣ redireciona
      navigate("/");
    } catch (err: any) {
      setErro(err?.error?.message || "Usuário ou senha inválidos");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 400, margin: "100px auto" }}>
      <h2>Login</h2>

      <form onSubmit={handleSubmit}>
        <div>
          <label>Email</label>
          <input
            value={email}
            onChange={e => setEmail(e.target.value)}
            type="email"
            required
          />
        </div>

        <div>
          <label>Senha</label>
          <input
            value={senha}
            onChange={e => setSenha(e.target.value)}
            type="password"
            required
          />
        </div>

        {erro && <p style={{ color: "red" }}>{erro}</p>}

        <button type="submit" disabled={loading}>
          {loading ? "Entrando..." : "Entrar"}
        </button>
      </form>
    </div>
  );
}

from sqlalchemy import text
from app.core.database import engine
from app.utils.security import verificar_senha
from app.utils.jwt import criar_token


def login(email: str, senha: str):
    sql = """
    SELECT
        u.usuario_id,
        u.email,
        u.role,
        u.ativo AS usuario_ativo,
        u.contrato_id,
        u.senha_hash,
        c.status AS contrato_status
    FROM control.usuarios u
    LEFT JOIN control.contratos c
        ON c.contrato_id = u.contrato_id
    WHERE u.email = :email
    """

    with engine.connect() as conn:
        result = conn.execute(
            text(sql),
            {"email": email}
        ).fetchone()

    if not result:
        return {"sucesso": False, "erro": "Usuário ou senha inválidos"}

    if not verificar_senha(senha, result.senha_hash):
        return {"sucesso": False, "erro": "Usuário ou senha inválidos"}

    if not result.usuario_ativo:
        return {"sucesso": False, "erro": "Usuário inativo"}

    if result.role != "MASTER":
        if not result.contrato_id:
            return {"sucesso": False, "erro": "Usuário sem contrato"}
        if result.contrato_status != "ATIVO":
            return {"sucesso": False, "erro": "Contrato inativo"}

    token = criar_token({
        "sub": result.email,
        "role": result.role,
        "contrato_id": result.contrato_id
    })

    return {
        "sucesso": True,
        "email": result.email,
        "role": result.role,
        "contrato_id": result.contrato_id,
        "access_token": token,
        "token_type": "bearer"
    }

-- ============================================
-- SCRIPT 04: SEED DE DADOS INICIAIS
-- ============================================
-- IMPORTANTE: Execute após criar as tabelas
-- Senhas hasheadas com bcrypt
-- ============================================

-- Inserir Contratos
INSERT INTO control.contratos (contrato_id, nome, nome_fantasia, cidade, uf, vertical, status)
VALUES 
    ('000000', 'SioC Analytics', 'SIOC', 'Curitiba', 'PR', 'Tecnologia', 'ATIVO'),
    ('041619', 'Serviço Distrital do Cajuru', 'Cartório do Cajuru', 'Cajuru', 'PR', 'Cartório', 'ATIVO')
ON CONFLICT (contrato_id) DO NOTHING;

-- Inserir Usuários
-- Senha Master@2024 (hash bcrypt)
-- Senha Admin@2024 (hash bcrypt)
-- NOTA: Gere os hashes reais usando o script Python abaixo

-- Para gerar os hashes, execute em Python:
-- from passlib.context import CryptContext
-- pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
-- print(pwd_context.hash("Master@2024"))
-- print(pwd_context.hash("Admin@2024"))

INSERT INTO control.usuarios (email, senha_hash, nome, role, contrato_id, ativo, status)
VALUES 
    ('lucas.sioc@gmail.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.M8K8HL0N/Q0Kxm', 'Lucas Matos', 'MASTER', '000000', TRUE, 'ATIVO'),
    ('lucas@ansata.com', '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Usuário Teste', 'ADMIN', '041619', TRUE, 'ATIVO')
ON CONFLICT (email) DO NOTHING;

-- Inserir Tipos de Ato FUNARPEN (Referência)
INSERT INTO data_pr.tipo_lancamento (codlcto, descricao, tipo_lanc, grupo_de_contas) VALUES
    ('101', 'Nascimento - Registro', 'REGISTRO_CIVIL', 'NASCIMENTO'),
    ('102', 'Nascimento - 2ª Via', 'REGISTRO_CIVIL', 'NASCIMENTO'),
    ('103', 'Nascimento - Averbação', 'REGISTRO_CIVIL', 'NASCIMENTO'),
    ('117', 'Casamento - 2ª Via', 'REGISTRO_CIVIL', 'CASAMENTO'),
    ('120', 'Casamento - Certidão Inteiro Teor', 'REGISTRO_CIVIL', 'CASAMENTO'),
    ('124', 'Casamento - Separação/Divórcio', 'REGISTRO_CIVIL', 'CASAMENTO'),
    ('130', 'Óbito - Registro', 'REGISTRO_CIVIL', 'OBITO'),
    ('402', 'Escritura Pública', 'TABELIONATO', 'NOTAS'),
    ('403', 'Procuração', 'TABELIONATO', 'NOTAS'),
    ('404', 'Substabelecimento', 'TABELIONATO', 'NOTAS'),
    ('430', 'Inventário Extrajudicial', 'TABELIONATO', 'NOTAS'),
    ('437', 'Declaração Diversa', 'TABELIONATO', 'NOTAS')
ON CONFLICT (codlcto) DO NOTHING;

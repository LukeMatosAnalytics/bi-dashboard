-- ============================================
-- SCRIPT 02: TABELAS DO SCHEMA CONTROL
-- ============================================

-- Tabela de Contratos (Multi-tenant)
CREATE TABLE IF NOT EXISTS control.contratos (
    contrato_id VARCHAR(6) PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    nome_fantasia VARCHAR(255),
    cidade VARCHAR(100),
    uf VARCHAR(2),
    vertical VARCHAR(100),
    status VARCHAR(50) DEFAULT 'ATIVO',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Usuários
CREATE TABLE IF NOT EXISTS control.usuarios (
    usuario_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    nome VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('MASTER', 'ADMIN', 'USER')),
    contrato_id VARCHAR(6) REFERENCES control.contratos(contrato_id),
    ativo BOOLEAN DEFAULT TRUE,
    status VARCHAR(50) DEFAULT 'ATIVO',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Log de Importações
CREATE TABLE IF NOT EXISTS control.importacoes (
    importacao_id SERIAL PRIMARY KEY,
    contrato_id VARCHAR(6) REFERENCES control.contratos(contrato_id),
    email_usuario VARCHAR(255),
    nome_arquivo VARCHAR(255),
    tipo_arquivo VARCHAR(100),
    quantidade_registros INTEGER,
    status VARCHAR(50),
    mensagem_erro TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_usuarios_email ON control.usuarios(email);
CREATE INDEX IF NOT EXISTS idx_usuarios_contrato ON control.usuarios(contrato_id);
CREATE INDEX IF NOT EXISTS idx_importacoes_contrato ON control.importacoes(contrato_id);
CREATE INDEX IF NOT EXISTS idx_importacoes_data ON control.importacoes(criado_em);

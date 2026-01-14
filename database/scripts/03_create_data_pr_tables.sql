-- ============================================
-- SCRIPT 03: TABELAS DO SCHEMA DATA_PR
-- ============================================

-- Tabela de Tipos de Lançamento (Dimensão/Referência)
CREATE TABLE IF NOT EXISTS data_pr.tipo_lancamento (
    codlcto VARCHAR(20) PRIMARY KEY,
    descricao VARCHAR(255),
    tipo_lanc VARCHAR(50),
    grupo_de_contas VARCHAR(100),
    status_inativo BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Situações (Dimensão)
CREATE TABLE IF NOT EXISTS data_pr.dim_situacao (
    situacao_id INTEGER PRIMARY KEY,
    descricao VARCHAR(50) NOT NULL
);

-- Inserir situações padrão
INSERT INTO data_pr.dim_situacao (situacao_id, descricao) VALUES
    (0, 'ABERTO'),
    (1, 'BAIXADO'),
    (2, 'EM COBRANÇA'),
    (3, 'CANCELADO'),
    (4, 'ESTORNADO'),
    (5, 'FECHADO'),
    (6, 'PENDENTE')
ON CONFLICT (situacao_id) DO NOTHING;

-- Tabela Fato OS Lançamentos
CREATE TABLE IF NOT EXISTS data_pr.fato_os_lanc (
    lancamento_id SERIAL PRIMARY KEY,
    contrato_id VARCHAR(6) NOT NULL,
    id_origem VARCHAR(50),
    os VARCHAR(50),
    sequencia INTEGER,
    situacao INTEGER,
    lcto VARCHAR(20),
    quantidade DECIMAL(18,4),
    valor DECIMAL(18,4),
    valor_abs DECIMAL(18,4),
    operacao VARCHAR(1),
    natureza VARCHAR(50),
    capa VARCHAR(50),
    livro VARCHAR(50),
    folha VARCHAR(50),
    selo_principal VARCHAR(100),
    dt_lancou TIMESTAMP,
    data_lancamento_date DATE,
    recibo VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(contrato_id, os, sequencia)
);

-- Tabela OS Selo (Associativa)
CREATE TABLE IF NOT EXISTS data_pr.os_selo (
    os_selo_id SERIAL PRIMARY KEY,
    contrato_id VARCHAR(6) NOT NULL,
    id_origem VARCHAR(50),
    os VARCHAR(50),
    codigo_selo VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(contrato_id, os, codigo_selo)
);

-- Tabela Histórico de Selos
CREATE TABLE IF NOT EXISTS data_pr.his_selo (
    his_selo_id SERIAL PRIMARY KEY,
    contrato_id VARCHAR(6) NOT NULL,
    id_origem VARCHAR(50),
    auto_inc VARCHAR(50),
    ativ_sel VARCHAR(50),
    data DATE,
    hora DECIMAL(18,15),
    operador VARCHAR(20),
    tipo_ato VARCHAR(10),
    capa VARCHAR(50),
    livro VARCHAR(50),
    folha VARCHAR(50),
    servico VARCHAR(10),
    tipo_his VARCHAR(10),
    tipo_selo VARCHAR(20),
    selo VARCHAR(100),
    validador VARCHAR(100),
    qtd INTEGER,
    data_envio DATE,
    data_compra VARCHAR(50),
    finalizado BOOLEAN DEFAULT FALSE,
    baixado_postgres BOOLEAN DEFAULT FALSE,
    data_locacao DATE,
    hora_locacao DECIMAL(18,15),
    id_status INTEGER,
    id_natureza_funapen INTEGER,
    id_usuario VARCHAR(50),
    numero_pedido INTEGER,
    tem_erro BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela Histórico Selo Detalhe PR
CREATE TABLE IF NOT EXISTS data_pr.his_selo_detalhe_pr (
    his_selo_detalhe_id SERIAL PRIMARY KEY,
    contrato_id VARCHAR(6) NOT NULL,
    id_origem VARCHAR(50),
    record_number VARCHAR(50),
    selo_principal VARCHAR(100),
    selo_retificacao VARCHAR(100),
    selo_anulacao VARCHAR(100),
    selo_cancelamento VARCHAR(100),
    cod_tipo_ato INTEGER,
    num_pedido VARCHAR(100),
    chave_digital VARCHAR(100),
    protocolo VARCHAR(50),
    selo_retificado VARCHAR(100),
    documento VARCHAR(50),
    valor_base DECIMAL(18,4),
    divisor INTEGER,
    quantidade INTEGER,
    idap VARCHAR(100),
    data_ato TIMESTAMP,
    tipo_envolvido VARCHAR(100),
    nome_razao VARCHAR(255),
    cpf_cnpj VARCHAR(20),
    rg_emissor_estado VARCHAR(50),
    rg_pessoa VARCHAR(50),
    tipo_arquivamento VARCHAR(100),
    entidade_convenio VARCHAR(100),
    tipo_averbacao VARCHAR(100),
    numero_apostilamento VARCHAR(50),
    tipo_documento VARCHAR(50),
    placa VARCHAR(20),
    crv VARCHAR(50),
    renavam VARCHAR(50),
    cartorio DECIMAL(18,4),
    funrejus DECIMAL(18,4),
    iss DECIMAL(18,4),
    fadep DECIMAL(18,4),
    funarpen DECIMAL(18,4),
    distribuidor DECIMAL(18,4),
    status INTEGER,
    mensagem TEXT,
    qrcode TEXT,
    caminho_imagem VARCHAR(255),
    json TEXT,
    id_tipo_gratuidade VARCHAR(50),
    id_codigo_ato INTEGER,
    id_usuario VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Lançamentos (Referência/Dimensão)
CREATE TABLE IF NOT EXISTS data_pr.tabela_de_lancamentos (
    id SERIAL PRIMARY KEY,
    contrato_id VARCHAR(6) NOT NULL,
    codlcto VARCHAR(20),
    descricao VARCHAR(255),
    tipo_lanc VARCHAR(50),
    grupo_de_contas VARCHAR(100),
    status_inativo BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(contrato_id, codlcto)
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_fato_os_lanc_contrato ON data_pr.fato_os_lanc(contrato_id);
CREATE INDEX IF NOT EXISTS idx_fato_os_lanc_os ON data_pr.fato_os_lanc(os);
CREATE INDEX IF NOT EXISTS idx_fato_os_lanc_data ON data_pr.fato_os_lanc(data_lancamento_date);

CREATE INDEX IF NOT EXISTS idx_os_selo_contrato ON data_pr.os_selo(contrato_id);
CREATE INDEX IF NOT EXISTS idx_os_selo_codigo ON data_pr.os_selo(codigo_selo);

CREATE INDEX IF NOT EXISTS idx_his_selo_contrato ON data_pr.his_selo(contrato_id);
CREATE INDEX IF NOT EXISTS idx_his_selo_selo ON data_pr.his_selo(selo);

CREATE INDEX IF NOT EXISTS idx_his_selo_detalhe_contrato ON data_pr.his_selo_detalhe_pr(contrato_id);
CREATE INDEX IF NOT EXISTS idx_his_selo_detalhe_selo ON data_pr.his_selo_detalhe_pr(selo_principal);
CREATE INDEX IF NOT EXISTS idx_his_selo_detalhe_data ON data_pr.his_selo_detalhe_pr(data_ato);

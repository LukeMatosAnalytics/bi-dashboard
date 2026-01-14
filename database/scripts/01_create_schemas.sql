-- ============================================
-- SCRIPT 01: CRIAÇÃO DOS SCHEMAS
-- ============================================
-- Plataforma BI Dashboard Web
-- Data: 2026-01-14
-- ============================================

-- Schema de controle (usuários, contratos, logs)
CREATE SCHEMA IF NOT EXISTS control;

-- Schema de dados do Paraná
CREATE SCHEMA IF NOT EXISTS data_pr;

-- Schema para dados brutos (futuro)
CREATE SCHEMA IF NOT EXISTS raw;

-- Schema para dados consolidados (futuro)
CREATE SCHEMA IF NOT EXISTS trusted;

-- Confirmar criação
SELECT schema_name 
FROM information_schema.schemata 
WHERE schema_name IN ('control', 'data_pr', 'raw', 'trusted');

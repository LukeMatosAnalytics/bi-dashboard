from enum import Enum


class ErrorCode(str, Enum):
    # =========================
    # IMPORTAÇÃO — VALIDAÇÃO
    # =========================
    INVALID_FILE_TYPE = "IMPORT_001"
    MISSING_REQUIRED_COLUMNS = "IMPORT_002"
    INVALID_IMPORT_MODE = "IMPORT_003"
    INVALID_PASSWORD = "IMPORT_004"
    PASSWORD_REQUIRED = "IMPORT_005"
    EMPTY_FILE = "IMPORT_006"
    IMPORT_TYPE_NOT_CONFIGURED = "IMPORT_007"

    # =========================
    # BANCO DE DADOS
    # =========================
    DATABASE_ERROR = "DB_001"
    DUPLICATE_KEY = "DB_002"

    # =========================
    # SISTEMA
    # =========================
    UNEXPECTED_ERROR = "SYS_001"


ERROR_CATALOG = {
    # =========================
    # IMPORTAÇÃO
    # =========================
    ErrorCode.INVALID_FILE_TYPE: {
        "message": "Tipo de arquivo inválido. Utilize um arquivo .xlsx",
        "http_status": 400,
        "action": "Solicitar novo arquivo ao cliente"
    },
    ErrorCode.MISSING_REQUIRED_COLUMNS: {
        "message": "Arquivo não contém todas as colunas obrigatórias",
        "http_status": 400,
        "action": "Validar layout do arquivo com o cliente"
    },
    ErrorCode.INVALID_IMPORT_MODE: {
        "message": "Modo de importação inválido para este tipo de arquivo",
        "http_status": 400,
        "action": "Verificar configuração do tipo de importação"
    },
    ErrorCode.PASSWORD_REQUIRED: {
        "message": "Confirmação de senha obrigatória para carga inicial",
        "http_status": 400,
        "action": "Solicitar confirmação de senha ao usuário"
    },
    ErrorCode.INVALID_PASSWORD: {
        "message": "Senha de confirmação inválida",
        "http_status": 403,
        "action": "Solicitar nova confirmação ao usuário"
    },
    ErrorCode.EMPTY_FILE: {
        "message": "Arquivo enviado não possui registros válidos",
        "http_status": 200,
        "action": "Orientar cliente a revisar o conteúdo do arquivo"
    },
    ErrorCode.IMPORT_TYPE_NOT_CONFIGURED: {
        "message": "Tipo de importação não configurado no sistema",
        "http_status": 500,
        "action": "Encaminhar para N3"
    },

    # =========================
    # BANCO DE DADOS
    # =========================
    ErrorCode.DATABASE_ERROR: {
        "message": "Erro ao persistir dados no banco",
        "http_status": 500,
        "action": "Encaminhar para N3 / DBA"
    },
    ErrorCode.DUPLICATE_KEY: {
        "message": "Registro duplicado identificado",
        "http_status": 409,
        "action": "Validar chave única e dados do arquivo"
    },

    # =========================
    # SISTEMA
    # =========================
    ErrorCode.UNEXPECTED_ERROR: {
        "message": "Erro inesperado no sistema",
        "http_status": 500,
        "action": "Encaminhar para N3"
    },
}

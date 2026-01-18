from app.core.success_codes import SuccessCode


SUCCESS_CATALOG = {
    # =========================
    # IMPORTAÇÃO
    # =========================
    SuccessCode.IMPORT_SUCCESS: {
        "message": "Importação realizada com sucesso"
    },
    SuccessCode.IMPORT_NO_DATA: {
        "message": "Arquivo processado, mas nenhum registro válido foi encontrado"
    },

    # =========================
    # BI
    # =========================
    SuccessCode.BI_001: {
        "message": "Consulta de selos pendentes realizada com sucesso"
    },
    SuccessCode.BI_002: {
        "message": "Consulta de selos duplicados no mesmo sistema realizada com sucesso"
    },
    SuccessCode.BI_003: {
        "message": "Consulta de selos duplicados em sistemas de origem diferentes realizada com sucesso"
    },
}

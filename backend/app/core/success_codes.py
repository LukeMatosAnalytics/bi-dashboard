from enum import Enum


class SuccessCode(str, Enum):
    # =========================
    # IMPORTAÇÃO
    # =========================
    IMPORT_SUCCESS = "IMPORT_SUCCESS"
    IMPORT_NO_DATA = "IMPORT_NO_DATA"

    # =========================
    # BI
    # =========================
    BI_001 = "BI_001"
    BI_002 = "BI_002"
    BI_003 = "BI_003"

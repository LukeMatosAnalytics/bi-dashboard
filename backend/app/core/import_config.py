from enum import Enum


class ModoImportacao(str, Enum):
    INITIAL = "INITIAL"
    INCREMENTAL = "INCREMENTAL"


TIPOS_IMPORTACAO = {
    "os_selo": {
        "permite_incremental": True,
        "descricao": "Ordem de Serviço - Selos"
    },
    "os_lanc": {
        "permite_incremental": True,
        "descricao": "Ordem de Serviço - Lançamentos"
    },
    "his_selo": {
        "permite_incremental": True,
        "descricao": "Histórico de Selos"
    },
    "his_selo_detalhe_pr": {
        "permite_incremental": True,
        "descricao": "Histórico de Selos Detalhado (PR)"
    },
    "tabela_lancamentos": {
        "permite_incremental": False,
        "descricao": "Tabela de Tipos de Lançamentos (Dimensão)"
    }
}

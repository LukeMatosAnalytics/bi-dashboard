from fastapi import APIRouter, Depends, Query

from app.core.permissions import somente_admin_ou_master
from app.core.responses import success_response
from app.core.success_codes import SuccessCode

from app.services.bi_selos_pendentes_service import obter_selos_pendentes_fnc
from app.services.bi_selos_duplicados_service import (
    obter_selos_duplicados_mesmo_sistema,
    obter_selos_duplicados_sistemas_diferentes
)

router = APIRouter(prefix="/bi", tags=["BI"])


@router.get(
    "/selos/pendentes-fnc",
    dependencies=[Depends(somente_admin_ou_master)]
)
def selos_pendentes_fnc(
    contrato_id: str = Query(...),
    data_inicio: str = Query(...),
    data_fim: str = Query(...)
):
    resultado = obter_selos_pendentes_fnc(
        contrato_id=contrato_id,
        data_inicio=data_inicio,
        data_fim=data_fim
    )

    return success_response(
        code=SuccessCode.BI_001,
        data=resultado
    )


@router.get(
    "/selos/duplicados/mesmo-sistema",
    dependencies=[Depends(somente_admin_ou_master)]
)
def selos_duplicados_mesmo_sistema(
    contrato_id: str = Query(...),
    data_inicio: str = Query(...),
    data_fim: str = Query(...)
):
    resultado = obter_selos_duplicados_mesmo_sistema(
        contrato_id=contrato_id,
        data_inicio=data_inicio,
        data_fim=data_fim
    )

    return success_response(
        code=SuccessCode.BI_002,
        data=resultado
    )


@router.get(
    "/selos/duplicados/sistemas-diferentes",
    dependencies=[Depends(somente_admin_ou_master)]
)
def selos_duplicados_sistemas_diferentes(
    contrato_id: str = Query(...),
    data_inicio: str = Query(...),
    data_fim: str = Query(...)
):
    resultado = obter_selos_duplicados_sistemas_diferentes(
        contrato_id=contrato_id,
        data_inicio=data_inicio,
        data_fim=data_fim
    )

    return success_response(
        code=SuccessCode.BI_003,
        data=resultado
    )

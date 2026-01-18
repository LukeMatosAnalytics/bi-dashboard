import { api } from "../../../api/axios";

export interface SelosPendentesParams {
  contrato_id: string;
  data_inicio: string; // YYYY-MM-DD
  data_fim: string;    // YYYY-MM-DD
}

export async function getSelosPendentesFnc(
  params: SelosPendentesParams
) {
  const response = await api.get("/bi/selos/pendentes-fnc", {
    params,
  });

  return response.data.data;
}

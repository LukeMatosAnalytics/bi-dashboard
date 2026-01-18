import { api } from "../../api/axios";

/* ============================
 * Tipos
 * ============================ */

export interface SelosDuplicadosMesmoSistema {
  tipo_duplicidade: "MESMO_SISTEMA";
  total_selos: number;
  registros: {
    selo_principal: string;
    sistema_origem_id: number;
    tipo_ato: string | null;
    livro: string | null;
    folha: string | null;
    dataato: string;
    total_ocorrencias: number;
  }[];
}

export interface SelosDuplicadosSistemasDiferentes {
  tipo_duplicidade: "SISTEMAS_DIFERENTES";
  total_selos: number;
  registros: {
    selo_principal: string;
    total_sistemas: number;
    sistemas_origem: number[];
    primeira_ocorrencia: string;
    ultima_ocorrencia: string;
  }[];
}

/* ============================
 * Services
 * ============================ */

export async function getSelosDuplicadosMesmoSistema(
  params: {
    contrato_id: string;
    data_inicio: string;
    data_fim: string;
  }
): Promise<SelosDuplicadosMesmoSistema> {
  const response = await api.get(
    "/bi/selos/duplicados/mesmo-sistema",
    { params }
  );

  return response.data.data;
}

export async function getSelosDuplicadosSistemasDiferentes(
  params: {
    contrato_id: string;
    data_inicio: string;
    data_fim: string;
  }
): Promise<SelosDuplicadosSistemasDiferentes> {
  const response = await api.get(
    "/bi/selos/duplicados/sistemas-diferentes",
    { params }
  );

  return response.data.data;
}

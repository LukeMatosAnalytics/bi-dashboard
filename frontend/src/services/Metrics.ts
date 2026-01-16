import { api } from "./api";
import type { Metric } from "../types/Metrics";

export async function getMetrics(): Promise<Metric[]> {
  const response = await api.get<Metric[]>("/metrics");
  return response.data;
}

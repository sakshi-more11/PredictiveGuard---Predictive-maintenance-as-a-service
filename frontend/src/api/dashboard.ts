import api from "./api";

export type DashboardSummary = {
  monitored_assets: number;
  fleet_health: number;
  high_risk_assets: number;
  average_rul_days: number;
  latest_predictions: Array<{
    id: number;
    machine_id: number;
    machine_name: string;
    rul_estimate: number;
    failure_probability: number;
    created_at: string;
  }>;
  active_alerts: Array<{
    id: number;
    machine_id: number;
    machine_name: string;
    failure_probability_threshold: number;
    rul_threshold_days: number;
    is_active: boolean;
  }>;
};

export type ModelRecord = {
  id: number;
  name: string;
  version: string;
  model_type: string;
  metrics?: Record<string, number | string> | null;
  is_active: boolean;
  created_at: string;
};

export async function getDashboardSummary() {
  const response = await api.get<DashboardSummary>("/api/v1/dashboard");
  return response.data;
}

export async function listModels() {
  const response = await api.get<ModelRecord[]>("/api/v1/models");
  return response.data;
}

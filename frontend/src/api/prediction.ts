import api from "./api";

export type Prediction = {
  id: number;
  machine_id: number;
  model_id: number;
  rul_estimate: number;
  failure_probability: number;
  lower_confidence_interval: number;
  upper_confidence_interval: number;
  confidence_level: number;
  top_features?: Array<Record<string, number>> | null;
  prediction_horizon_days: number;
  created_at: string;
};

export async function runPrediction(machineId: number, horizonDays: number) {
  const response = await api.post<Prediction>("/api/v1/predict/", {
    machine_id: machineId,
    horizon_days: horizonDays,
  });

  return response.data;
}

export async function listPredictions() {
  const response = await api.get<Prediction[]>("/api/v1/predict");
  return response.data;
}

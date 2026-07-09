import api from "./api";

export type AlertConfig = {
  id: number;
  machine_id: number;
  failure_probability_threshold: number;
  rul_threshold_days: number;
  webhook_url?: string | null;
  email_recipients?: string[] | null;
  is_active: boolean;
  created_at: string;
};

export async function listAlerts() {
  const response = await api.get<AlertConfig[]>("/api/v1/alerts");
  return response.data;
}

export async function createAlert(machineId: number, failureThreshold: number, rulThreshold: number) {
  const response = await api.post<AlertConfig>("/api/v1/alerts/", {
    machine_id: machineId,
    failure_probability_threshold: failureThreshold,
    rul_threshold_days: rulThreshold,
  });

  return response.data;
}

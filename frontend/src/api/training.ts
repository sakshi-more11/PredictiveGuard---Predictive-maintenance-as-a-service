import api from "./api";

export type TrainingJob = {
  id: number;
  machine_id: number;
  celery_task_id: string | null;
  model_type: string;
  status: string;
  started_at?: string | null;
  completed_at?: string | null;
  model_id?: number | null;
  error_message?: string | null;
  created_at: string;
};

export async function startTraining(machineId: number, modelType: string) {
  const response = await api.post<TrainingJob>("/api/v1/train/", {
    machine_id: machineId,
    model_type: modelType,
    parameters: {},
  });

  return response.data;
}

export async function listJobs(machineId?: number) {
  const path = machineId
    ? `/api/v1/jobs/machine/${machineId}`
    : "/api/v1/jobs";
  const response = await api.get<TrainingJob[]>(path);
  return response.data;
}

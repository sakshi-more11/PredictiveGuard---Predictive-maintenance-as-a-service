import api from "./api";

export type Machine = {
  id: number;
  name: string;
  machine_type: string;
  description?: string | null;
  location?: string | null;
  created_at: string;
  updated_at: string;
};

export type UploadResponse = {
  machine_id: number;
  task_id: string;
  status: string;
  message: string;
  rows_uploaded: number;
};

export type CreateMachinePayload = {
  name: string;
  machine_type: string;
  description?: string;
  location?: string;
};

export async function listMachines() {
  const response = await api.get<Machine[]>("/api/v1/ingest/machines");
  return response.data;
}

export async function createMachine(payload: CreateMachinePayload) {
  const response = await api.post<Machine>("/api/v1/ingest/machines", payload);
  return response.data;
}

export async function uploadDataset(machineId: number, file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post<UploadResponse>(
    `/api/v1/ingest/upload?machine_id=${machineId}`,
    formData,
    { headers: { "Content-Type": "multipart/form-data" } },
  );

  return response.data;
}

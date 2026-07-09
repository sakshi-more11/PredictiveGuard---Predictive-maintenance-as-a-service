import { useEffect, useState } from "react";
import { BrainCircuit, Play, RefreshCcw } from "lucide-react";
import { listMachines, type Machine } from "../../api/upload";
import { listJobs, startTraining, type TrainingJob } from "../../api/training";

export default function Training() {
  const [machines, setMachines] = useState<Machine[]>([]);
  const [jobs, setJobs] = useState<TrainingJob[]>([]);
  const [machineId, setMachineId] = useState("");
  const [modelType, setModelType] = useState("prophet");
  const [status, setStatus] = useState("Select an asset and queue a model training job.");

  async function refresh() {
    const [machineList, jobList] = await Promise.all([listMachines(), listJobs()]);
    setMachines(machineList);
    setJobs(jobList);
    if (!machineId && machineList[0]) {
      setMachineId(String(machineList[0].id));
    }
  }

  useEffect(() => {
    Promise.all([listMachines(), listJobs()])
      .then(([machineList, jobList]) => {
        setMachines(machineList);
        setJobs(jobList);
        if (machineList[0]) {
          setMachineId(String(machineList[0].id));
        }
      })
      .catch(() => setStatus("Backend unavailable. Start FastAPI on port 8000."));
  }, []);

  async function handleTrain() {
    if (!machineId) {
      setStatus("Create or select a machine first.");
      return;
    }

    try {
      const job = await startTraining(Number(machineId), modelType);
      setJobs((current) => [job, ...current]);
      setStatus(`Training job ${job.id} queued with task ${job.celery_task_id ?? "pending"}.`);
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Training request failed.");
    }
  }

  return (
    <div className="workspace">
      <section className="surface chart-card">
        <div className="section-title">
          <div><BrainCircuit size={18} /><h2>Model Training</h2></div>
          <button className="ghost-button" type="button" onClick={() => refresh()}><RefreshCcw size={16} />Refresh</button>
        </div>

        <div className="grid gap-4 lg:grid-cols-[1fr_1fr_auto]">
          <select className="h-12 rounded-lg border border-slate-700 bg-slate-900 px-3 text-white" value={machineId} onChange={(event) => setMachineId(event.target.value)}>
            <option value="">Select asset</option>
            {machines.map((machine) => <option key={machine.id} value={machine.id}>{machine.name}</option>)}
          </select>
          <select className="h-12 rounded-lg border border-slate-700 bg-slate-900 px-3 text-white" value={modelType} onChange={(event) => setModelType(event.target.value)}>
            <option value="prophet">Prophet</option>
            <option value="degradation">Degradation</option>
            <option value="tft">Temporal Fusion</option>
          </select>
          <button className="primary-button" type="button" onClick={handleTrain}><Play size={18} />Start Training</button>
        </div>

        <div className="job-status"><span>Training Status</span><strong>{status}</strong></div>
      </section>

      <section className="surface table-card mt-4">
        <div className="section-title"><div><BrainCircuit size={18} /><h2>Recent Jobs</h2></div></div>
        <div className="asset-table">
          <div className="table-row table-head"><span>Job</span><span>Machine</span><span>Model</span><span>Status</span><span>Model ID</span></div>
          {jobs.map((job) => (
            <div className="table-row" key={job.id}>
              <span><strong>training_{job.id}</strong><small>{job.celery_task_id ?? "No task yet"}</small></span>
              <span>{job.machine_id}</span>
              <span>{job.model_type}</span>
              <span className="risk-pill text-cyan-200 bg-cyan-950/70 border-cyan-700/50">{job.status}</span>
              <span>{job.model_id ?? "-"}</span>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

import { useEffect, useState } from "react";
import { Database, HardDriveUpload, Plus, UploadCloud } from "lucide-react";
import { createMachine, listMachines, type Machine, uploadDataset } from "../../api/upload";

export default function Upload() {
  const [machines, setMachines] = useState<Machine[]>([]);
  const [machineId, setMachineId] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState("Ready for sensor CSV ingestion.");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    listMachines()
      .then((items) => {
        setMachines(items);
        if (items[0]) {
          setMachineId(String(items[0].id));
        }
      })
      .catch(() => setStatus("Backend unavailable. Start FastAPI on port 8000."));
  }, []);

  async function handleCreateMachine() {
    setIsLoading(true);
    try {
      const machine = await createMachine({
        name: `Asset-${Date.now().toString().slice(-4)}`,
        machine_type: "Compressor",
        description: "Created from the PredictiveGuard upload workflow",
        location: "Plant A",
      });
      setMachines((current) => [machine, ...current]);
      setMachineId(String(machine.id));
      setStatus(`Created machine ${machine.name}.`);
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Machine creation failed.");
    } finally {
      setIsLoading(false);
    }
  }

  async function handleUpload() {
    if (!machineId || !file) {
      setStatus("Select a machine and CSV file before uploading.");
      return;
    }

    setIsLoading(true);
    try {
      const result = await uploadDataset(Number(machineId), file);
      setStatus(`${result.message}. ${result.rows_uploaded} rows queued as task ${result.task_id}.`);
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Upload failed.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="workspace">
      <section className="surface chart-card">
        <div className="section-title">
          <div>
            <HardDriveUpload size={18} />
            <h2>Upload Dataset</h2>
          </div>
          <button className="ghost-button" type="button" onClick={handleCreateMachine} disabled={isLoading}>
            <Plus size={16} />
            New Asset
          </button>
        </div>

        <div className="grid gap-4 lg:grid-cols-[1fr_1fr_auto]">
          <label className="grid gap-2 text-sm text-slate-300">
            Machine
            <select className="h-12 rounded-lg border border-slate-700 bg-slate-900 px-3 text-white" value={machineId} onChange={(event) => setMachineId(event.target.value)}>
              <option value="">Select asset</option>
              {machines.map((machine) => (
                <option key={machine.id} value={machine.id}>
                  {machine.name} - {machine.machine_type}
                </option>
              ))}
            </select>
          </label>

          <label className="grid gap-2 text-sm text-slate-300">
            CSV File
            <input className="h-12 rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-white" type="file" accept=".csv,text/csv" onChange={(event) => setFile(event.target.files?.[0] ?? null)} />
          </label>

          <button className="primary-button self-end" type="button" onClick={handleUpload} disabled={isLoading}>
            <UploadCloud size={18} />
            Upload
          </button>
        </div>

        <div className="job-status">
          <span>Pipeline Status</span>
          <strong>{status}</strong>
        </div>
      </section>

      <section className="surface table-card mt-4">
        <div className="section-title">
          <div>
            <Database size={18} />
            <h2>Registered Assets</h2>
          </div>
        </div>
        <div className="asset-table">
          <div className="table-row table-head"><span>Asset</span><span>Type</span><span>Location</span><span>Status</span><span>ID</span></div>
          {machines.map((machine) => (
            <div className="table-row" key={machine.id}>
              <span><strong>{machine.name}</strong><small>{machine.description ?? "No description"}</small></span>
              <span>{machine.machine_type}</span>
              <span>{machine.location ?? "Unassigned"}</span>
              <span className="risk-pill text-emerald-300 bg-emerald-950/70 border-emerald-700/50">Active</span>
              <span>{machine.id}</span>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

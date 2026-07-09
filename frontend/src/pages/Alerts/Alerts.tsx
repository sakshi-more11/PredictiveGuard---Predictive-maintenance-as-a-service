import { useEffect, useState } from "react";
import { Bell, Plus } from "lucide-react";
import { createAlert, listAlerts, type AlertConfig } from "../../api/alerts";
import { listMachines, type Machine } from "../../api/upload";

export default function Alerts() {
  const [alerts, setAlerts] = useState<AlertConfig[]>([]);
  const [machines, setMachines] = useState<Machine[]>([]);
  const [machineId, setMachineId] = useState("");
  const [status, setStatus] = useState("Configure alert thresholds for active assets.");

  useEffect(() => {
    Promise.all([listAlerts(), listMachines()])
      .then(([alertList, machineList]) => {
        setAlerts(alertList);
        setMachines(machineList);
        if (machineList[0]) {
          setMachineId(String(machineList[0].id));
        }
      })
      .catch(() => setStatus("Backend unavailable. Alerts will load when the API is running."));
  }, []);

  async function handleCreateAlert() {
    if (!machineId) {
      setStatus("Select a machine first.");
      return;
    }

    try {
      const alert = await createAlert(Number(machineId), 0.7, 14);
      setAlerts((current) => [alert, ...current]);
      setStatus(`Alert ${alert.id} created.`);
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Alert creation failed.");
    }
  }

  return (
    <div className="workspace">
      <section className="surface chart-card">
        <div className="section-title"><div><Bell size={18} /><h2>Alerts</h2></div></div>
        <div className="grid gap-4 lg:grid-cols-[1fr_auto]">
          <select className="h-12 rounded-lg border border-slate-700 bg-slate-900 px-3 text-white" value={machineId} onChange={(event) => setMachineId(event.target.value)}>
            <option value="">Select asset</option>
            {machines.map((machine) => <option key={machine.id} value={machine.id}>{machine.name}</option>)}
          </select>
          <button className="primary-button" type="button" onClick={handleCreateAlert}><Plus size={18} />Create Alert</button>
        </div>
        <div className="job-status"><span>Alert Status</span><strong>{status}</strong></div>
      </section>

      <section className="surface table-card mt-4">
        <div className="section-title"><div><Bell size={18} /><h2>Active Alert Rules</h2></div></div>
        <div className="asset-table">
          <div className="table-row table-head"><span>Alert</span><span>Machine</span><span>Failure Threshold</span><span>RUL Threshold</span><span>Status</span></div>
          {alerts.map((alert) => (
            <div className="table-row" key={alert.id}>
              <span><strong>alert_{alert.id}</strong><small>{new Date(alert.created_at).toLocaleString()}</small></span>
              <span>{alert.machine_id}</span>
              <span>{Math.round(alert.failure_probability_threshold * 100)}%</span>
              <span>{alert.rul_threshold_days} days</span>
              <span className="alert-level warning">{alert.is_active ? "Active" : "Paused"}</span>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

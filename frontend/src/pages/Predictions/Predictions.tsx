import { useEffect, useState } from "react";
import { Activity, LineChart, Play } from "lucide-react";
import { listMachines, type Machine } from "../../api/upload";
import { listPredictions, runPrediction, type Prediction } from "../../api/prediction";

export default function Predictions() {
  const [machines, setMachines] = useState<Machine[]>([]);
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [machineId, setMachineId] = useState("");
  const [horizon, setHorizon] = useState(30);
  const [status, setStatus] = useState("Run a remaining useful life prediction.");

  useEffect(() => {
    Promise.all([listMachines(), listPredictions()])
      .then(([machineList, predictionList]) => {
        setMachines(machineList);
        setPredictions(predictionList);
        if (machineList[0]) {
          setMachineId(String(machineList[0].id));
        }
      })
      .catch(() => setStatus("Backend unavailable or no trained model exists yet."));
  }, []);

  async function handlePredict() {
    if (!machineId) {
      setStatus("Select an asset before running inference.");
      return;
    }

    try {
      const prediction = await runPrediction(Number(machineId), horizon);
      setPredictions((current) => [prediction, ...current]);
      setStatus(`Prediction complete: ${prediction.rul_estimate.toFixed(1)} days RUL.`);
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Prediction failed.");
    }
  }

  return (
    <div className="workspace">
      <section className="surface chart-card">
        <div className="section-title"><div><Activity size={18} /><h2>Predictions</h2></div></div>
        <div className="grid gap-4 lg:grid-cols-[1fr_1fr_auto]">
          <select className="h-12 rounded-lg border border-slate-700 bg-slate-900 px-3 text-white" value={machineId} onChange={(event) => setMachineId(event.target.value)}>
            <option value="">Select asset</option>
            {machines.map((machine) => <option key={machine.id} value={machine.id}>{machine.name}</option>)}
          </select>
          <input className="h-12 rounded-lg border border-slate-700 bg-slate-900 px-3 text-white" type="number" min={1} max={365} value={horizon} onChange={(event) => setHorizon(Number(event.target.value))} />
          <button className="primary-button" type="button" onClick={handlePredict}><Play size={18} />Run Prediction</button>
        </div>
        <div className="job-status"><span>Inference Status</span><strong>{status}</strong></div>
      </section>

      <section className="surface table-card mt-4">
        <div className="section-title"><div><LineChart size={18} /><h2>Prediction History</h2></div></div>
        <div className="asset-table">
          <div className="table-row table-head"><span>Prediction</span><span>Machine</span><span>RUL</span><span>Risk</span><span>Horizon</span></div>
          {predictions.map((prediction) => (
            <div className="table-row" key={prediction.id}>
              <span><strong>prediction_{prediction.id}</strong><small>{new Date(prediction.created_at).toLocaleString()}</small></span>
              <span>{prediction.machine_id}</span>
              <span>{prediction.rul_estimate.toFixed(1)} days</span>
              <span className="risk-pill text-amber-200 bg-amber-950/70 border-amber-600/50">{Math.round(prediction.failure_probability * 100)}%</span>
              <span>{prediction.prediction_horizon_days} days</span>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

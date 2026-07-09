import { useEffect, useState } from "react";
import { Save, Settings as SettingsIcon, ShieldCheck } from "lucide-react";
import api from "../../api/api";

type HealthResponse = {
  status: string;
  service: string;
  version: string;
};

export default function Settings() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [apiUrl, setApiUrl] = useState(import.meta.env.VITE_API_URL ?? "http://localhost:8000");
  const [status, setStatus] = useState("Runtime settings are stored in environment variables.");

  useEffect(() => {
    api.get<HealthResponse>("/health")
      .then((response) => setHealth(response.data))
      .catch(() => setStatus("Backend health check failed."));
  }, []);

  return (
    <div className="workspace">
      <section className="surface chart-card">
        <div className="section-title"><div><SettingsIcon size={18} /><h2>Settings</h2></div></div>
        <div className="grid gap-4 lg:grid-cols-2">
          <label className="grid gap-2 text-sm text-slate-300">
            API URL
            <input className="h-12 rounded-lg border border-slate-700 bg-slate-900 px-3 text-white" value={apiUrl} onChange={(event) => setApiUrl(event.target.value)} />
          </label>
          <label className="grid gap-2 text-sm text-slate-300">
            Service
            <input className="h-12 rounded-lg border border-slate-700 bg-slate-900 px-3 text-white" value={health?.service ?? "PredictiveGuard"} readOnly />
          </label>
        </div>
        <div className="control-list mt-4">
          <button type="button" onClick={() => setStatus("Set VITE_API_URL in frontend/.env to persist API URL changes.")}>
            <Save size={18} />
            Save Runtime Note
          </button>
        </div>
        <div className="job-status"><span>System Status</span><strong>{status}</strong></div>
      </section>

      <section className="surface stat-card mt-4">
        <div className="icon-box green"><ShieldCheck size={20} /></div>
        <div>
          <p className="panel-label">Backend Health</p>
          <strong className="stat-value">{health?.status ?? "offline"}</strong>
          <span className="stat-helper">FastAPI port 8000, version {health?.version ?? "unknown"}</span>
        </div>
      </section>
    </div>
  );
}

import { useEffect, useState } from "react";
import { Database, ShieldCheck } from "lucide-react";
import { listModels, type ModelRecord } from "../../api/dashboard";

export default function Models() {
  const [models, setModels] = useState<ModelRecord[]>([]);
  const [status, setStatus] = useState("Model registry is ready.");

  useEffect(() => {
    listModels()
      .then(setModels)
      .catch(() => setStatus("Backend unavailable. Trained models will appear once the API is running."));
  }, []);

  return (
    <div className="workspace">
      <section className="surface table-card">
        <div className="section-title">
          <div><Database size={18} /><h2>Model Registry</h2></div>
        </div>
        <div className="job-status"><span>Registry Status</span><strong>{status}</strong></div>
        <div className="asset-table mt-4">
          <div className="table-row table-head"><span>Model</span><span>Type</span><span>Version</span><span>Status</span><span>Created</span></div>
          {models.map((model) => (
            <div className="table-row" key={model.id}>
              <span><strong>{model.name}</strong><small>model_{model.id}</small></span>
              <span>{model.model_type}</span>
              <span>{model.version}</span>
              <span className="risk-pill text-emerald-300 bg-emerald-950/70 border-emerald-700/50"><ShieldCheck size={14} />{model.is_active ? "Active" : "Inactive"}</span>
              <span>{new Date(model.created_at).toLocaleDateString()}</span>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

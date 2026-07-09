import { useEffect, useState } from "react";
import { BarChart3, Gauge, ShieldAlert, Timer } from "lucide-react";
import { getDashboardSummary, type DashboardSummary } from "../../api/dashboard";

export default function Analytics() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);

  useEffect(() => {
    getDashboardSummary().then(setSummary).catch(() => setSummary(null));
  }, []);

  return (
    <div className="workspace">
      <section className="stat-grid">
        <section className="surface stat-card"><div className="icon-box cyan"><BarChart3 size={20} /></div><div><p className="panel-label">Assets</p><strong className="stat-value">{summary?.monitored_assets ?? 0}</strong><span className="stat-helper">Monitored fleet</span></div></section>
        <section className="surface stat-card"><div className="icon-box green"><Gauge size={20} /></div><div><p className="panel-label">Fleet Health</p><strong className="stat-value">{summary?.fleet_health ?? 0}%</strong><span className="stat-helper">Calculated from latest risk</span></div></section>
        <section className="surface stat-card"><div className="icon-box red"><ShieldAlert size={20} /></div><div><p className="panel-label">High Risk</p><strong className="stat-value">{summary?.high_risk_assets ?? 0}</strong><span className="stat-helper">Failure probability over 70%</span></div></section>
        <section className="surface stat-card"><div className="icon-box amber"><Timer size={20} /></div><div><p className="panel-label">Average RUL</p><strong className="stat-value">{summary?.average_rul_days ?? 0}</strong><span className="stat-helper">Days remaining</span></div></section>
      </section>

      <section className="surface table-card">
        <div className="section-title"><div><BarChart3 size={18} /><h2>Latest Prediction Analytics</h2></div></div>
        <div className="asset-table">
          <div className="table-row table-head"><span>Asset</span><span>Machine</span><span>RUL</span><span>Risk</span><span>Created</span></div>
          {(summary?.latest_predictions ?? []).map((prediction) => (
            <div className="table-row" key={prediction.id}>
              <span><strong>{prediction.machine_name}</strong><small>prediction_{prediction.id}</small></span>
              <span>{prediction.machine_id}</span>
              <span>{prediction.rul_estimate.toFixed(1)} days</span>
              <span className="risk-pill text-amber-200 bg-amber-950/70 border-amber-600/50">{Math.round(prediction.failure_probability * 100)}%</span>
              <span>{new Date(prediction.created_at).toLocaleDateString()}</span>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

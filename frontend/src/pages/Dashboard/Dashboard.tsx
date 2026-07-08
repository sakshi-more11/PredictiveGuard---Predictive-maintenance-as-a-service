import {
  Activity,
  AlertTriangle,
  ArrowUpRight,
  Bell,
  BrainCircuit,
  CheckCircle2,
  ChevronRight,
  CircuitBoard,
  Clock3,
  Cpu,
  Database,
  Gauge,
  HardDriveUpload,
  LineChart as LineChartIcon,
  MapPin,
  RadioTower,
  RefreshCcw,
  Search,
  Settings,
  ShieldCheck,
  Thermometer,
  Upload,
  Wrench,
  Zap,
} from "lucide-react";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ComposedChart,
  Line,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const telemetry = [
  { time: "06:00", temp: 61, vibration: 1.8, pressure: 41, risk: 18 },
  { time: "08:00", temp: 64, vibration: 2.1, pressure: 43, risk: 24 },
  { time: "10:00", temp: 68, vibration: 2.4, pressure: 47, risk: 31 },
  { time: "12:00", temp: 74, vibration: 3.2, pressure: 51, risk: 46 },
  { time: "14:00", temp: 82, vibration: 4.8, pressure: 57, risk: 63 },
  { time: "16:00", temp: 79, vibration: 4.2, pressure: 54, risk: 58 },
  { time: "18:00", temp: 72, vibration: 3.1, pressure: 49, risk: 39 },
];

const rulForecast = [
  { day: "D+1", rul: 132, lower: 118, upper: 151 },
  { day: "D+7", rul: 108, lower: 92, upper: 129 },
  { day: "D+14", rul: 86, lower: 64, upper: 105 },
  { day: "D+21", rul: 63, lower: 42, upper: 84 },
  { day: "D+30", rul: 41, lower: 24, upper: 68 },
];

const modelMetrics = [
  { name: "Pump", score: 92 },
  { name: "Turbine", score: 88 },
  { name: "Compressor", score: 84 },
  { name: "Conveyor", score: 79 },
];

const fleet = [
  {
    id: "PX-204",
    asset: "Centrifugal Pump",
    site: "Plant A / Line 2",
    health: 94,
    risk: "Low",
    rul: "132 days",
    status: "Nominal",
  },
  {
    id: "TB-117",
    asset: "Steam Turbine",
    site: "Plant B / Unit 4",
    health: 77,
    risk: "Medium",
    rul: "64 days",
    status: "Watch",
  },
  {
    id: "CP-330",
    asset: "Air Compressor",
    site: "Plant C / Bay 1",
    health: 58,
    risk: "High",
    rul: "29 days",
    status: "Service",
  },
  {
    id: "CN-082",
    asset: "Conveyor Drive",
    site: "Plant A / Packing",
    health: 83,
    risk: "Medium",
    rul: "91 days",
    status: "Watch",
  },
];

const alerts = [
  {
    title: "Vibration drift above learned baseline",
    asset: "CP-330",
    time: "12 min ago",
    level: "Critical",
  },
  {
    title: "Temperature confidence interval widening",
    asset: "TB-117",
    time: "38 min ago",
    level: "Warning",
  },
  {
    title: "Scheduled retraining completed",
    asset: "Fleet segment A",
    time: "1 hr ago",
    level: "Info",
  },
];

const recommendations = [
  "Inspect compressor bearing assembly within 48 hours.",
  "Reduce Line 2 pump load by 8% during peak cycle.",
  "Retrain turbine model after next 5,000 sensor samples.",
];

const navItems = [
  { label: "Overview", icon: Gauge, active: true },
  { label: "Ingest", icon: Upload },
  { label: "Training", icon: BrainCircuit },
  { label: "Predictions", icon: LineChartIcon },
  { label: "Alerts", icon: Bell },
  { label: "Models", icon: Database },
  { label: "Settings", icon: Settings },
];

const riskColor: Record<string, string> = {
  Low: "text-emerald-300 bg-emerald-950/70 border-emerald-700/50",
  Medium: "text-amber-200 bg-amber-950/70 border-amber-600/50",
  High: "text-rose-200 bg-rose-950/70 border-rose-600/50",
};

function StatCard({
  icon: Icon,
  label,
  value,
  helper,
  tone,
}: {
  icon: typeof Activity;
  label: string;
  value: string;
  helper: string;
  tone: string;
}) {
  return (
    <section className="surface stat-card">
      <div className={`icon-box ${tone}`}>
        <Icon size={20} aria-hidden="true" />
      </div>
      <div>
        <p className="panel-label">{label}</p>
        <strong className="stat-value">{value}</strong>
        <span className="stat-helper">{helper}</span>
      </div>
    </section>
  );
}

function SectionTitle({
  icon: Icon,
  title,
  action,
}: {
  icon: typeof Activity;
  title: string;
  action?: string;
}) {
  return (
    <div className="section-title">
      <div>
        <Icon size={18} aria-hidden="true" />
        <h2>{title}</h2>
      </div>
      {action ? (
        <button className="ghost-button" type="button">
          {action}
          <ChevronRight size={16} aria-hidden="true" />
        </button>
      ) : null}
    </div>
  );
}

export default function Dashboard() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-lockup">
          <div className="brand-mark">
            <ShieldCheck size={24} aria-hidden="true" />
          </div>
          <div>
            <strong>PredictiveGuard</strong>
            <span>Industrial AI Operations</span>
          </div>
        </div>

        <nav className="nav-list" aria-label="Primary">
          {navItems.map((item) => (
            <button
              className={item.active ? "nav-item active" : "nav-item"}
              key={item.label}
              type="button"
            >
              <item.icon size={18} aria-hidden="true" />
              <span>{item.label}</span>
            </button>
          ))}
        </nav>

        <div className="edge-card">
          <RadioTower size={18} aria-hidden="true" />
          <div>
            <strong>Edge gateway</strong>
            <span>24 machines streaming</span>
          </div>
        </div>
      </aside>

      <main className="workspace">
        <header className="topbar">
          <div>
            <p className="eyebrow">Fleet Command Center</p>
            <h1>PredictiveGuard</h1>
          </div>

          <div className="topbar-actions">
            <label className="search-box">
              <Search size={17} aria-hidden="true" />
              <input aria-label="Search assets" placeholder="Search assets" />
            </label>
            <button className="icon-button" type="button" aria-label="Refresh telemetry">
              <RefreshCcw size={18} />
            </button>
            <button className="primary-button" type="button">
              <Upload size={18} aria-hidden="true" />
              Ingest CSV
            </button>
          </div>
        </header>

        <section className="hero-panel">
          <div className="hero-copy">
            <div className="status-pill">
              <CheckCircle2 size={16} aria-hidden="true" />
              Live inference online
            </div>
            <h2>Probabilistic maintenance intelligence for critical assets</h2>
            <p>
              Sensor streams, model jobs, RUL forecasts, confidence bands, and
              alert actions are unified in one operations-grade control plane.
            </p>
            <div className="hero-actions">
              <button className="primary-button" type="button">
                <BrainCircuit size={18} aria-hidden="true" />
                Start Training
              </button>
              <button className="secondary-button" type="button">
                <Wrench size={18} aria-hidden="true" />
                Create Ticket
              </button>
            </div>
          </div>

          <div className="twin-panel" aria-label="Digital twin status">
            <div className="twin-header">
              <span>Compressor CP-330</span>
              <strong>58%</strong>
            </div>
            <div className="machine-visual">
              <div className="machine-node node-a" />
              <div className="machine-node node-b" />
              <div className="machine-node node-c" />
              <div className="machine-core">
                <Cpu size={44} aria-hidden="true" />
              </div>
              <div className="sensor-line line-a" />
              <div className="sensor-line line-b" />
              <div className="sensor-line line-c" />
            </div>
            <div className="twin-metrics">
              <span>
                <Thermometer size={15} aria-hidden="true" />
                82 C
              </span>
              <span>
                <Activity size={15} aria-hidden="true" />
                4.8 mm/s
              </span>
              <span>
                <Zap size={15} aria-hidden="true" />
                63% risk
              </span>
            </div>
          </div>
        </section>

        <section className="stat-grid">
          <StatCard
            icon={CircuitBoard}
            label="Monitored Assets"
            value="24"
            helper="+3 onboarded this week"
            tone="cyan"
          />
          <StatCard
            icon={Gauge}
            label="Fleet Health"
            value="86%"
            helper="4.2% above target"
            tone="green"
          />
          <StatCard
            icon={AlertTriangle}
            label="High Risk"
            value="1"
            helper="CP-330 needs action"
            tone="red"
          />
          <StatCard
            icon={Clock3}
            label="Avg RUL"
            value="94d"
            helper="30 day horizon"
            tone="amber"
          />
        </section>

        <section className="content-grid">
          <section className="surface chart-card wide">
            <SectionTitle icon={Activity} title="Sensor Telemetry" action="View stream" />
            <div className="chart-frame">
              <ResponsiveContainer width="100%" height={300}>
                <ComposedChart data={telemetry}>
                  <CartesianGrid stroke="#253244" strokeDasharray="4 4" vertical={false} />
                  <XAxis dataKey="time" stroke="#8b9bb4" tickLine={false} axisLine={false} />
                  <YAxis stroke="#8b9bb4" tickLine={false} axisLine={false} />
                  <Tooltip contentStyle={{ background: "#101820", border: "1px solid #2b3b4f" }} />
                  <Area type="monotone" dataKey="risk" fill="#7f1d1d" stroke="#f97316" fillOpacity={0.24} />
                  <Line type="monotone" dataKey="temp" stroke="#22d3ee" strokeWidth={3} dot={false} />
                  <Line type="monotone" dataKey="pressure" stroke="#34d399" strokeWidth={2} dot={false} />
                  <Bar dataKey="vibration" barSize={16} fill="#f59e0b" radius={[4, 4, 0, 0]} />
                </ComposedChart>
              </ResponsiveContainer>
            </div>
          </section>

          <section className="surface chart-card">
            <SectionTitle icon={BrainCircuit} title="RUL Forecast" />
            <div className="chart-frame compact">
              <ResponsiveContainer width="100%" height={250}>
                <AreaChart data={rulForecast}>
                  <CartesianGrid stroke="#253244" strokeDasharray="4 4" vertical={false} />
                  <XAxis dataKey="day" stroke="#8b9bb4" tickLine={false} axisLine={false} />
                  <YAxis stroke="#8b9bb4" tickLine={false} axisLine={false} />
                  <Tooltip contentStyle={{ background: "#101820", border: "1px solid #2b3b4f" }} />
                  <Area dataKey="upper" fill="#155e75" stroke="#0891b2" fillOpacity={0.18} />
                  <Area dataKey="rul" fill="#0f766e" stroke="#2dd4bf" fillOpacity={0.4} />
                  <Line dataKey="lower" stroke="#f59e0b" strokeWidth={2} dot={false} />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </section>
        </section>

        <section className="content-grid lower">
          <section className="surface table-card">
            <SectionTitle icon={MapPin} title="Fleet Assets" action="Open registry" />
            <div className="asset-table">
              <div className="table-row table-head">
                <span>Asset</span>
                <span>Site</span>
                <span>Health</span>
                <span>Risk</span>
                <span>RUL</span>
              </div>
              {fleet.map((machine) => (
                <div className="table-row" key={machine.id}>
                  <span>
                    <strong>{machine.id}</strong>
                    <small>{machine.asset}</small>
                  </span>
                  <span>{machine.site}</span>
                  <span>
                    <div className="health-bar" aria-label={`${machine.health}% health`}>
                      <i style={{ width: `${machine.health}%` }} />
                    </div>
                    {machine.health}%
                  </span>
                  <span className={`risk-pill ${riskColor[machine.risk]}`}>{machine.risk}</span>
                  <span>{machine.rul}</span>
                </div>
              ))}
            </div>
          </section>

          <section className="surface model-card">
            <SectionTitle icon={Database} title="Model Registry" action="Metrics" />
            <div className="chart-frame compact">
              <ResponsiveContainer width="100%" height={220}>
                <BarChart data={modelMetrics} layout="vertical">
                  <CartesianGrid stroke="#253244" strokeDasharray="4 4" horizontal={false} />
                  <XAxis type="number" domain={[0, 100]} hide />
                  <YAxis dataKey="name" type="category" stroke="#9fb0c7" tickLine={false} axisLine={false} width={88} />
                  <Tooltip contentStyle={{ background: "#101820", border: "1px solid #2b3b4f" }} />
                  <Bar dataKey="score" radius={[0, 5, 5, 0]}>
                    {modelMetrics.map((entry) => (
                      <Cell key={entry.name} fill={entry.score > 85 ? "#22c55e" : entry.score > 80 ? "#06b6d4" : "#f59e0b"} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div className="pipeline">
              <span>Validated</span>
              <ChevronRight size={15} aria-hidden="true" />
              <span>Versioned</span>
              <ChevronRight size={15} aria-hidden="true" />
              <span>Deployed</span>
            </div>
          </section>

          <section className="surface action-card">
            <SectionTitle icon={HardDriveUpload} title="Data Pipeline" />
            <div className="control-list">
              <button type="button">
                <Upload size={18} aria-hidden="true" />
                Upload sensor CSV
              </button>
              <button type="button">
                <BrainCircuit size={18} aria-hidden="true" />
                Queue DeepAR training
              </button>
              <button type="button">
                <LineChartIcon size={18} aria-hidden="true" />
                Run 30 day prediction
              </button>
            </div>
            <div className="job-status">
              <span>Current job</span>
              <strong>training_1042</strong>
              <div className="progress-track">
                <i />
              </div>
            </div>
          </section>

          <section className="surface alert-card">
            <SectionTitle icon={Bell} title="Alert Governance" />
            <div className="alert-list">
              {alerts.map((alert) => (
                <article key={`${alert.asset}-${alert.time}`}>
                  <div>
                    <strong>{alert.title}</strong>
                    <span>{alert.asset} / {alert.time}</span>
                  </div>
                  <span className={`alert-level ${alert.level.toLowerCase()}`}>{alert.level}</span>
                </article>
              ))}
            </div>
          </section>

          <section className="surface recommendation-card">
            <SectionTitle icon={Wrench} title="AI Recommendations" />
            <ul>
              {recommendations.map((item) => (
                <li key={item}>
                  <ArrowUpRight size={16} aria-hidden="true" />
                  {item}
                </li>
              ))}
            </ul>
          </section>
        </section>
      </main>
    </div>
  );
}

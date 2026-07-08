import {
  LayoutDashboard,
  Upload,
  BrainCircuit,
  Activity,
  Bell,
  BarChart3,
  Database,
  Settings,
} from "lucide-react";

import { NavLink } from "react-router-dom";

const items = [
  {
    icon: LayoutDashboard,
    title: "Dashboard",
    path: "/",
  },
  {
    icon: Upload,
    title: "Upload Dataset",
    path: "/upload",
  },
  {
    icon: BrainCircuit,
    title: "Train Model",
    path: "/training",
  },
  {
    icon: Activity,
    title: "Predictions",
    path: "/predictions",
  },
  {
    icon: BarChart3,
    title: "Analytics",
    path: "/analytics",
  },
  {
    icon: Bell,
    title: "Alerts",
    path: "/alerts",
  },
  {
    icon: Database,
    title: "Models",
    path: "/models",
  },
  {
    icon: Settings,
    title: "Settings",
    path: "/settings",
  },
];

export default function Sidebar() {
  return (
    <aside className="w-64 h-screen bg-slate-900 border-r border-slate-800 flex flex-col">
      {/* Logo */}
      <div className="p-6 border-b border-slate-800">
        <h1 className="text-2xl font-bold text-cyan-400">
          PredictiveGuard
        </h1>

        <p className="text-slate-400 text-sm mt-2">
          AI Maintenance Platform
        </p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4">
        {items.map((item) => (
          <NavLink
            key={item.title}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 p-3 rounded-lg mb-2 transition-all duration-200 ${
                isActive
                  ? "bg-cyan-600 text-white shadow-lg"
                  : "text-slate-300 hover:bg-slate-800 hover:text-white"
              }`
            }
          >
            <item.icon size={20} />
            <span>{item.title}</span>
          </NavLink>
        ))}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-slate-800 text-xs text-slate-500">
        PredictiveGuard v1.0
      </div>
    </aside>
  );
}
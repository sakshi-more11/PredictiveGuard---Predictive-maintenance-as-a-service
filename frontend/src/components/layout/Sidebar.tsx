import {
  LayoutDashboard,
  Upload,
  BrainCircuit,
  Activity,
  BarChart3,
  Bell,
  Database,
  Settings,
  ShieldCheck,
} from "lucide-react";

import { NavLink } from "react-router-dom";

const menu = [
  {
    name: "Dashboard",
    path: "/",
    icon: LayoutDashboard,
  },
  {
    name: "Upload Dataset",
    path: "/upload",
    icon: Upload,
  },
  {
    name: "Train Model",
    path: "/training",
    icon: BrainCircuit,
  },
  {
    name: "Predictions",
    path: "/predictions",
    icon: Activity,
  },
  {
    name: "Analytics",
    path: "/analytics",
    icon: BarChart3,
  },
  {
    name: "Alerts",
    path: "/alerts",
    icon: Bell,
  },
  {
    name: "Models",
    path: "/models",
    icon: Database,
  },
  {
    name: "Settings",
    path: "/settings",
    icon: Settings,
  },
];

export default function Sidebar() {
  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 h-screen sticky top-0 flex flex-col">

      <div className="p-6 border-b border-slate-800">

        <div className="flex items-center gap-3">

          <div className="bg-cyan-600 rounded-xl p-2">
            <ShieldCheck className="text-white" size={26} />
          </div>

          <div>
            <h1 className="text-xl font-bold text-white">
              PredictiveGuard
            </h1>

            <p className="text-slate-400 text-sm">
              AI Maintenance
            </p>

          </div>

        </div>

      </div>

      <nav className="flex-1 p-4">

        {menu.map((item) => (

          <NavLink
            key={item.name}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-xl mb-2 transition ${
                isActive
                  ? "bg-cyan-600 text-white"
                  : "text-slate-300 hover:bg-slate-800"
              }`
            }
          >
            <item.icon size={20} />

            <span>{item.name}</span>

          </NavLink>

        ))}

      </nav>

      <div className="p-5 border-t border-slate-800">

        <div className="rounded-xl bg-slate-800 p-4">

          <p className="text-xs text-slate-400">

            Edge Gateway

          </p>

          <p className="font-semibold text-white">

            24 Machines Online

          </p>

        </div>

      </div>

    </aside>
  );
}
import {
  Search,
  Bell,
  RefreshCcw,
  UserCircle,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();

  return (
    <header className="h-20 border-b border-slate-800 bg-slate-950 px-8 flex items-center justify-between">

      <div>

        <p className="text-cyan-400 text-sm">

          Fleet Command Center

        </p>

        <h1 className="text-3xl font-bold text-white">

          PredictiveGuard Dashboard

        </h1>

      </div>

      <div className="flex items-center gap-4">

        <div className="relative">

          <Search
            size={18}
            className="absolute left-3 top-3 text-slate-400"
          />

          <input
            placeholder="Search..."
            className="bg-slate-900 border border-slate-700 rounded-xl pl-10 pr-4 py-2 text-white w-72 outline-none"
          />

        </div>

        <button
          className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700"
          type="button"
          aria-label="Refresh page data"
          onClick={() => window.location.reload()}
        >

          <RefreshCcw size={20} />

        </button>

        <button
          className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700"
          type="button"
          aria-label="Open alerts"
          onClick={() => navigate("/alerts")}
        >

          <Bell size={20} />

        </button>

        <UserCircle
          size={36}
          className="text-cyan-400"
        />

      </div>

    </header>
  );
}

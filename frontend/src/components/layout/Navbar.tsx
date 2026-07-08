import { Bell, Search, UserCircle } from "lucide-react";

export default function Navbar() {
  return (
    <header className="h-16 border-b border-slate-800 bg-slate-900 flex justify-between items-center px-8">
      <h2 className="text-xl font-semibold">
        Dashboard
      </h2>

      <div className="flex items-center gap-5">
        <Search />

        <Bell />

        <UserCircle size={34} />
      </div>
    </header>
  );
}
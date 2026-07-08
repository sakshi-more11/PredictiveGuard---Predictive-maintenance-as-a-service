import type { ReactNode } from "react";

import Sidebar from "./SideBar";
import Navbar from "./Navbar";

interface Props {
  children: ReactNode;
}

export default function Layout({ children }: Props) {
  return (
    <div className="flex min-h-screen bg-slate-950">
      <Sidebar />

      <div className="flex flex-col flex-1">
        <Navbar />

        <main className="p-8">
          {children}
        </main>
      </div>
    </div>
  );
}
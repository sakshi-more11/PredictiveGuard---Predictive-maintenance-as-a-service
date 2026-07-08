import { BrowserRouter, Routes, Route } from "react-router-dom";

import Dashboard from "../pages/Dashboard/Dashboard";
import Upload from "../pages/Upload/Upload";
import Training from "../pages/Training/Training";
import Predictions from "../pages/Predictions/Predictions";
import Analytics from "../pages/Analytics/Analytics";
import Alerts from "../pages/Alerts/Alerts";
import Models from "../pages/Models/Models";
import Settings from "../pages/Settings/Settings";

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/upload" element={<Upload />} />
        <Route path="/training" element={<Training />} />
        <Route path="/predictions" element={<Predictions />} />
        <Route path="/analytics" element={<Analytics />} />
        <Route path="/alerts" element={<Alerts />} />
        <Route path="/models" element={<Models />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </BrowserRouter>
  );
}
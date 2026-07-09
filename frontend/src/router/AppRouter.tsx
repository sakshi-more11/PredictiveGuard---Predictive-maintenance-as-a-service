import { Routes, Route } from "react-router-dom";

import Layout from "../components/layout/Layout";

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
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="upload" element={<Upload />} />
        <Route path="training" element={<Training />} />
        <Route path="predictions" element={<Predictions />} />
        <Route path="analytics" element={<Analytics />} />
        <Route path="alerts" element={<Alerts />} />
        <Route path="models" element={<Models />} />
        <Route path="settings" element={<Settings />} />
      </Route>
    </Routes>
  );
}
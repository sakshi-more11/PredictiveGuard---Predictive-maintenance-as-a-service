import Layout from "../../components/layout/Layout";

export default function Upload() {
  return (
    <Layout>
      <h1 className="text-4xl font-bold">Upload Dataset</h1>

      <p className="text-slate-400 mt-2">
        Upload sensor CSV files for training.
      </p>
    </Layout>
  );
}
import { useEffect, useState } from "react";

export default function Dashboard() {
  const [user, setUser] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) return;

    try {
      const payload = JSON.parse(atob(token.split(".")[1]));
      if (payload.name) {
        // Defer state update to avoid React cascading render warning
        setTimeout(() => setUser(payload.name), 0);
      }
    } catch {
      console.error("Invalid token");
    }
  }, []);

  return (
    <div className="max-w-6xl mx-auto p-6">

      {/* ===== HERO HEADER ===== */}
      <div className="mb-12 p-8 rounded-3xl bg-gradient-to-r from-blue-50 to-teal-50 border shadow-sm">

        {user && (
          <h2 className="text-lg text-gray-500 mb-2">
            Hi {user} 👋
          </h2>
        )}

        <h1 className="text-3xl font-bold text-gray-800 mb-3">
          AI-Based Diabetic Medical Report Analysis System
        </h1>

        <p className="text-gray-600 max-w-3xl leading-relaxed">
          This intelligent healthcare system helps patients and clinicians understand
          diabetic lab reports by enhancing images, extracting clinical information,
          predicting risks, and providing multilingual explanations.
        </p>
      </div>

      {/* ===== FEATURES ===== */}
      <div className="grid grid-cols-2 gap-8 mb-14">

        <Feature
          icon="🖼️"
          title="Medical Report Image Enhancement"
          desc="Improves clarity of scanned or blurred medical reports to support accurate analysis."
        />

        <Feature
          icon="🧪"
          title="AI Clause Extraction & Interpretation"
          desc="Extracts diabetic test values and provides meaningful clinical explanations."
        />

        <Feature
          icon="⚠️"
          title="Risk Prediction & Recommendation"
          desc="Identifies potential diabetic risks and provides personalized lifestyle guidance."
        />

        <Feature
          icon="🌍"
          title="Multilingual Report Translation"
          desc="Generates simplified explanations in multiple languages for better understanding."
        />

      </div>

      {/* ===== WORKFLOW ===== */}
      <div className="bg-white p-10 rounded-3xl shadow-lg border max-w-4xl mx-auto">
        <h2 className="font-bold text-xl mb-10 text-gray-800">
          How Your Report Is Analyzed
        </h2>

        <div className="flex justify-between items-center relative">
          <div className="absolute top-5 left-10 right-10 h-1 bg-gradient-to-r from-blue-200 to-teal-200 rounded-full" />
          <Step emoji="📤" label="Upload" />
          <Step emoji="✨" label="Enhancement" />
          <Step emoji="🔎" label="Extraction" />
          <Step emoji="🧠" label="Interpretation" />
          <Step emoji="📊" label="Risk Analysis" />
          <Step emoji="🌍" label="Translation" />
        </div>
      </div>
    </div>
  );
}

/* ===== FEATURE CARD ===== */
function Feature({ icon, title, desc }) {
  return (
    <div className="bg-white p-8 rounded-3xl border shadow-sm hover:shadow-xl hover:-translate-y-1 transition duration-300 group">
      <div className="text-4xl mb-4 group-hover:scale-110 transition">{icon}</div>
      <h3 className="font-semibold text-lg mb-2 text-gray-800 leading-snug">{title}</h3>
      <p className="text-gray-600 text-sm leading-relaxed">{desc}</p>
    </div>
  );
}

/* ===== STEP ===== */
function Step({ emoji, label }) {
  return (
    <div className="flex flex-col items-center relative z-10">
      <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-blue-500 to-teal-500 text-white flex items-center justify-center text-xl shadow-md mb-2">
        {emoji}
      </div>
      <p className="text-sm font-medium text-gray-600">{label}</p>
    </div>
  );
}
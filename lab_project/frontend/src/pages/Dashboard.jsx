export default function Dashboard() {
  return (
    <div className="max-w-6xl">

      {/* Header */}
      <h1 className="text-3xl font-bold text-gray-800 mb-2">
        AI-Based Diabetic Medical Report Analysis System
      </h1>

      <p className="text-gray-500 mb-10 max-w-3xl">
        This intelligent healthcare system helps patients and clinicians understand
        diabetic lab reports by enhancing images, extracting clinical information,
        predicting risks, and providing multilingual explanations.
      </p>

      {/* Feature modules */}
      <div className="grid grid-cols-2 gap-8 mb-12">

        <Feature
          icon="🖼️"
          title="Medical Report Image Enhancement"
          desc="Improves clarity of scanned or blurred medical reports to support accurate analysis."
        />

        <Feature
          icon="🧪"
          title="AI Clause Extraction and Interpretation Engine for Diabetes Medical Reports"
          desc="Extracts diabetic test values and provides meaningful clinical explanations."
        />

        <Feature
          icon="⚠️"
          title="AI-Powered Risk Prediction & Recommendation Engine for Diabetes Management"
          desc="Identifies potential diabetic risks and provides lifestyle recommendations."
        />

        <Feature
          icon="🌍"
          title="Multilingual Diabetic Medical Report Summarization and Translation"
          desc="Generates simplified medical explanations in multiple languages for better understanding."
        />

      </div>

      {/* Workflow */}
      <div className="bg-white p-8 rounded-2xl shadow-lg max-w-4xl">
         <h2 className="font-bold text-xl mb-6">How Your Report Is Analyzed</h2>

       
      <div className="flex justify-between text-center">
        <Step emoji="📤" label="Upload Report" />
        <Step emoji="✨" label="Image Enhancement" />
        <Step emoji="🔍" label="Extraction and Interpretation" />
        <Step emoji="📊" label="Risk Detection" />
        <Step emoji="🌍" label="Translation" />
      </div>
    </div>

    </div>
  );
}

function Feature({ icon, title, desc }) {
  return (
    <div className="bg-white p-8 rounded-2xl shadow-md hover:shadow-xl transition">
      <div className="text-4xl mb-4">{icon}</div>
      <h3 className="font-bold text-lg mb-2 text-gray-800 leading-snug">{title}</h3>
      <p className="text-gray-600 text-sm">{desc}</p>
    </div>
  );
}

function Step({ emoji, label }) {
  return (
    <div className="flex flex-col items-center">
      <div className="text-3xl mb-2">{emoji}</div>
      <p className="text-sm font-medium text-gray-600">{label}</p>
    </div>
  );
}
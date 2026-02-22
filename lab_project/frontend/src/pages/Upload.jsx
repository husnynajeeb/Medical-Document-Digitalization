import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Upload() {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const upload = async () => {
    if (!files.length) return alert("Please select a report");

    const form = new FormData();
    files.forEach((f) => form.append("files", f));

    try {
      setLoading(true);
      const res = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: form,
      });

      const data = await res.json();
      console.log("Backend response:", data);

      // Save results in localStorage
      localStorage.setItem("results", JSON.stringify(data.results || []));

      // Navigate to results page
      navigate("/results");
    } catch (err) {
      console.error("Upload error:", err);
      alert("Upload failed. See console for details.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full min-h-screen p-6 md:p-10 bg-gray-50">
      <div className="mb-10">
        <h1 className="text-3xl md:text-4xl font-bold text-gray-800">
          Upload Medical Report
        </h1>
        <p className="text-gray-500 mt-2">
          Upload your diabetic lab report for AI analysis and explanation
        </p>
      </div>

      <div className="grid lg:grid-cols-2 gap-10 w-full">
        {/* Upload Card */}
        <div className="bg-white rounded-2xl shadow-xl p-10 flex flex-col justify-center">
          <div className="flex justify-center mb-8">
            <div className="w-52 h-52 bg-gradient-to-br from-blue-100 to-teal-100 rounded-full flex items-center justify-center text-8xl">
              🏥
            </div>
          </div>

          <input
            type="file"
            multiple
            accept="image/*,.pdf"
            onChange={(e) => setFiles(Array.from(e.target.files))}
            className="mb-5"
          />

          {files.length > 0 && (
            <div className="mb-5 text-sm text-gray-600 space-y-1">
              {files.map((f, i) => (
                <div key={i}>📄 {f.name}</div>
              ))}
            </div>
          )}

          <button
            onClick={upload}
            disabled={loading}
            className="w-full bg-blue-600 text-white py-4 rounded-xl font-semibold text-lg shadow-lg hover:bg-blue-700 transition"
          >
            {loading ? "Analyzing..." : "Analyze Report"}
          </button>
        </div>

        {/* How it works */}
        <div className="bg-gradient-to-br from-blue-500 to-teal-500 rounded-2xl shadow-xl p-10 text-white flex flex-col justify-center">
          <h2 className="text-3xl font-bold mb-6">How It Works</h2>
          <div className="space-y-4">
            <Step
              n="1"
              title="Upload Your Report"
              desc="Take a photo or upload an image of your lab report"
            />
            <Step
              n="2"
              title="AI Analysis"
              desc="Our system extracts and analyzes your test values"
            />
            <Step
              n="3"
              title="Get Insights"
              desc="Receive clear explanations and health advice"
            />
          </div>
        </div>
      </div>
    </div>
  );
}

function Step({ n, title, desc }) {
  return (
    <div className="flex items-start space-x-3">
      <div className="w-8 h-8 bg-white bg-opacity-20 rounded-full flex items-center justify-center flex-shrink-0 mt-1 font-bold">
        {n}
      </div>
      <div>
        <h3 className="font-semibold mb-1">{title}</h3>
        <p className="text-sm text-blue-100">{desc}</p>
      </div>
    </div>
  );
}
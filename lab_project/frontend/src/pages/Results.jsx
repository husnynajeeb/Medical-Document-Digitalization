import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Results() {
  const [results, setResults] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const data = localStorage.getItem("results");
    if (!data) {
      navigate("/upload"); // No results, redirect
      return;
    }

    // Wrap in setTimeout to avoid synchronous setState warning
    setTimeout(() => {
      try {
        setResults(JSON.parse(data));
      } catch (err) {
        console.error("Failed to parse results:", err);
        navigate("/upload");
      }
    }, 0);
  }, [navigate]);

  if (!results || results.length === 0) {
    return (
      <div className="p-10 text-gray-700 text-lg font-semibold">
        No test results found.
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl w-full space-y-6 mx-auto">
        {results.map((test, i) => (
          <div key={i} className="bg-white rounded-2xl shadow-xl overflow-hidden">
            {/* Test Header */}
            <div className="p-8 border-b border-gray-100 flex justify-between items-center">
              <h2 className="text-3xl font-bold text-gray-800">{test.test}</h2>
              <span
                className={`px-4 py-2 rounded-full font-semibold flex items-center space-x-2 ${
                  test.status === "High"
                    ? "bg-red-100 text-red-700"
                    : "bg-green-100 text-green-700"
                }`}
              >
                <span
                  className={`w-2.5 h-2.5 rounded-full ${
                    test.status === "High" ? "bg-red-600" : "bg-green-600"
                  }`}
                ></span>
                <span>{test.status}</span>
              </span>
            </div>

            {/* Test Value */}
            <div className="p-8 bg-gradient-to-br from-gray-50 to-white">
              <div className="flex items-baseline space-x-3 mb-3">
                <span className="text-6xl font-bold text-gray-800">{test.value}</span>
                <span className="text-2xl text-gray-600 font-medium">{test.unit}</span>
              </div>
              <p className="text-base text-gray-500">
                Normal Range: <span className="font-semibold text-gray-700">{test.range}</span>
              </p>
            </div>

            {/* Meaning Section */}
            <div className="p-8 border-t border-gray-100 flex items-start space-x-4">
              <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center flex-shrink-0">
                <svg
                  className="w-6 h-6 text-blue-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-bold text-gray-800 mb-2">What This Means</h3>
                <p className="text-base text-gray-600 leading-relaxed">{test.meaning}</p>
              </div>
            </div>

            {/* Advice Section */}
            <div className="p-8 bg-red-50 border-t border-red-100 flex items-start space-x-4">
              <div className="w-12 h-12 bg-red-100 rounded-xl flex items-center justify-center flex-shrink-0">
                <svg
                  className="w-6 h-6 text-red-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                  />
                </svg>
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-bold text-red-800 mb-3">Health Advice</h3>
                <p className="text-base text-gray-700 leading-relaxed">{test.advice}</p>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="p-8 flex gap-4">
              <button className="flex-1 bg-blue-600 text-white py-4 rounded-xl font-semibold shadow-lg hover:bg-blue-700 transition">
                Download Report
              </button>
              <button className="flex-1 bg-white text-gray-700 border-2 border-gray-300 py-4 rounded-xl font-semibold shadow hover:bg-gray-50 transition">
                Save to History
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
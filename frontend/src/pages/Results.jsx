import { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { jsPDF } from "jspdf";

export default function Results() {
  const [results, setResults] = useState([]);
  const [combined, setCombined] = useState([]);
  const navigate = useNavigate();
  const location = useLocation();

  // Load results safely from location.state
  useEffect(() => {
    if (location.state && location.state.results) {
      // Wrap in a microtask to avoid synchronous setState warning
      Promise.resolve().then(() => {
        setResults(location.state.results);
        setCombined(location.state.combined_interpretation || []);
      });
    } else {
      // Navigate outside setState to prevent cascading render
      navigate("/upload");
    }
  }, [location.state, navigate]);

  if ((!results || results.length === 0) && (!combined || combined.length === 0)) {
    return (
      <div className="p-10 text-gray-700 text-lg font-semibold">
        No test results found.
      </div>
    );
  }

  const drawWrappedText = (doc, text, x, y, maxWidth, lineHeight = 6) => {
    const lines = doc.splitTextToSize(text, maxWidth);
    lines.forEach((line) => {
      doc.text(line, x, y);
      y += lineHeight;
    });
    return y;
  };

  const downloadPDF = () => {
    const doc = new jsPDF();
    let y = 20;

    doc.setFontSize(20);
    doc.setTextColor("#1E3A8A");
    doc.text("Medical Report Analysis", 105, y, { align: "center" });
    y += 12;

    results.forEach((test) => {
      y += 6;
      doc.setFontSize(16);
      doc.setTextColor("#111827");
      doc.text(`${test.test} (${test.unit})`, 14, y);

      doc.setFontSize(12);
      doc.setTextColor(test.status === "High" ? "#DC2626" : "#16A34A");
      doc.text(`Status: ${test.status}`, 150, y, { align: "right" });

      y += 8;
      doc.setTextColor("#374151");
      doc.text(`Value: ${test.value}`, 14, y);
      doc.text(`Range: ${test.range}`, 14, y + 6);
      y += 14;

      doc.setFontSize(14);
      doc.setTextColor("#1F2937");
      doc.text("What This Means:", 14, y);
      y += 6;
      doc.setFontSize(12);
      y = drawWrappedText(doc, test.meaning, 14, y, 180);

      y += 4;
      doc.setFontSize(14);
      doc.setTextColor("#1F2937");
      doc.text("Interpretation:", 14, y);
      y += 6;
      doc.setFontSize(12);
      y = drawWrappedText(doc, test.advice, 14, y, 180);

      y += 10;
      if (y > 260) {
        doc.addPage();
        y = 20;
      }
    });

    combined.forEach((block) => {
      y += 10;
      doc.setFontSize(16);
      doc.setTextColor("#1E40AF");
      doc.text("Combined Interpretation", 14, y);
      y += 8;

      block.results.forEach((test) => {
        doc.setFontSize(14);
        doc.setTextColor("#111827");
        doc.text(`${test.test} (${test.unit})`, 14, y);

        doc.setFontSize(12);
        doc.setTextColor(test.status === "High" ? "#DC2626" : "#16A34A");
        doc.text(`Status: ${test.status}`, 150, y, { align: "right" });

        y += 6;
        doc.setTextColor("#374151");
        doc.text(`Value: ${test.value}`, 14, y);
        doc.text(`Range: ${test.range}`, 14, y + 6);
        y += 12;

        doc.setFontSize(12);
        doc.setTextColor("#1F2937");
        y = drawWrappedText(doc, test.meaning, 14, y, 180);

        y += 6;
        if (y > 260) {
          doc.addPage();
          y = 20;
        }
      });

      doc.setFontSize(14);
      doc.setTextColor("#1F2937");
      doc.text("Overall Interpretation:", 14, y);
      y += 6;
      doc.setFontSize(12);
      y = drawWrappedText(doc, block.interpretation, 14, y, 180);

      y += 10;
      if (y > 260) {
        doc.addPage();
        y = 20;
      }
    });

    doc.save("Medical_Report.pdf");
  };

  return (
    <div className="flex min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl w-full space-y-6 mx-auto">
        {results.map((test, i) => (
          <div key={i} className="bg-white rounded-2xl shadow-xl overflow-hidden">
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
                />
                <span>{test.status}</span>
              </span>
            </div>

            <div className="p-8 bg-gray-50">
              <div className="flex items-baseline space-x-3 mb-3">
                <span className="text-6xl font-bold text-gray-800">{test.value}</span>
                <span className="text-2xl text-gray-600 font-medium">{test.unit}</span>
              </div>
              <p className="text-base text-gray-500 mb-3">
                Normal Range: <span className="font-semibold text-gray-700">{test.range}</span>
              </p>
              <h3 className="text-lg font-bold text-gray-800 mb-1">What This Means</h3>
              <p className="text-base text-gray-600 mb-3">{test.meaning}</p>
              <h3 className="text-lg font-bold text-gray-800 mb-1">Interpretation</h3>
              <p className="text-base text-gray-600">{test.advice}</p>
            </div>
          </div>
        ))}

        {combined.length > 0 && (
          <div className="bg-white rounded-2xl shadow-xl p-8">
            {combined.map((block, idx) => (
              <div key={idx} className="space-y-4">
                <h2 className="text-2xl font-bold text-blue-700 mb-4">Combined Interpretation</h2>
                {block.results.map((test, i) => (
                  <div key={i} className="p-4 border rounded-xl border-gray-200">
                    <div className="flex justify-between items-center mb-1">
                      <h3 className="font-semibold text-gray-800">{test.test} ({test.unit})</h3>
                      <span
                        className={`px-3 py-1 rounded-full font-semibold text-sm ${
                          test.status === "High" ? "bg-red-100 text-red-700" : "bg-green-100 text-green-700"
                        }`}
                      >
                        {test.status}
                      </span>
                    </div>
                    <p className="text-gray-600 mb-1">{test.meaning}</p>
                    <p className="text-gray-500 text-sm">Range: {test.range}</p>
                    <p className="text-gray-500 text-sm">Value: {test.value}</p>
                  </div>
                ))}
                <h3 className="text-lg font-bold mt-4 text-gray-800">Overall Interpretation</h3>
                <p className="text-gray-600">{block.interpretation}</p>
              </div>
            ))}
          </div>
        )}

        <button
          onClick={downloadPDF}
          className="w-full bg-blue-600 text-white py-4 rounded-xl font-semibold shadow-lg hover:bg-blue-700 transition mt-4"
        >
          Download PDF
        </button>
      </div>
    </div>
  );
}
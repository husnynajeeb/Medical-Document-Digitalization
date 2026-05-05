import { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { jsPDF } from "jspdf";
import MultilingualPanel from "../components/MultilingualPanel";

export default function Results() {
  const [results, setResults] = useState([]);
  const [combined, setCombined] = useState([]);
  const [selectedText, setSelectedText] = useState("");

  const navigate = useNavigate();
  const location = useLocation();

  // ===================================================
  // 🧠 BUILD TEXT FOR MULTILINGUAL PROCESSING
  // ===================================================
  const buildMedicalText = (resultsData, combinedData) => {
    let text = "";

    resultsData.forEach((test) => {
      text += `${test.test}: ${test.value} ${test.unit}. `;
      text += `Status: ${test.status}. `;
      text += `Range: ${test.range}. `;
      text += `${test.meaning}. `;
      text += `${test.advice}. `;
    });

    combinedData.forEach((block) => {
      text += `Overall Interpretation: ${block.interpretation}. `;
    });

    return text;
  };

  // ===================================================
  // LOAD DATA
  // ===================================================
  useEffect(() => {
    if (location.state && location.state.results) {
      Promise.resolve().then(() => {
        const res = location.state.results;
        const comb = location.state.combined_interpretation || [];

        setResults(res);
        setCombined(comb);

        // 🔥 Prepare text for multilingual processing
        const text = buildMedicalText(res, comb);
        setSelectedText(text);
      });
    } else {
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

  // ===================================================
  // PDF GENERATION
  // ===================================================
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

  // ===================================================
  // UI
  // ===================================================
  return (
    <div className="flex min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl w-full space-y-6 mx-auto">

        {/* ================= RESULTS ================= */}
        {results.map((test, i) => (
          <div key={i} className="bg-white rounded-2xl shadow-xl overflow-hidden">
            <div className="p-8 border-b border-gray-100 flex justify-between items-center">
              <h2 className="text-3xl font-bold text-gray-800">{test.test}</h2>
              <span
                className={`px-4 py-2 rounded-full font-semibold ${
                  test.status === "High"
                    ? "bg-red-100 text-red-700"
                    : "bg-green-100 text-green-700"
                }`}
              >
                {test.status}
              </span>
            </div>

            <div className="p-8 bg-gray-50">
              <div className="flex items-baseline space-x-3 mb-3">
                <span className="text-6xl font-bold text-gray-800">{test.value}</span>
                <span className="text-2xl text-gray-600">{test.unit}</span>
              </div>

              <p className="text-gray-600 mb-2">
                Range: <strong>{test.range}</strong>
              </p>

              <p className="text-gray-700 mb-2">{test.meaning}</p>
              <p className="text-gray-500">{test.advice}</p>
            </div>
          </div>
        ))}

        {/* ================= COMBINED ================= */}
        {combined.length > 0 && (
          <div className="bg-white rounded-2xl shadow-xl p-8">
            {combined.map((block, idx) => (
              <div key={idx}>
                <h2 className="text-xl font-bold text-blue-700 mb-3">
                  Combined Interpretation
                </h2>
                <p>{block.interpretation}</p>
              </div>
            ))}
          </div>
        )}

        {/* ================= 🌍 MULTILINGUAL ================= */}
        {selectedText && (
          <div className="bg-white rounded-2xl shadow-xl p-6">
            <h2 className="text-xl font-bold text-blue-700 mb-4">
              🌍 Multilingual Processing
            </h2>

            <MultilingualPanel
              inputType="text"
              text={selectedText}
            />
          </div>
        )}

        {/* ================= DOWNLOAD ================= */}
        <button
          onClick={downloadPDF}
          className="w-full bg-blue-600 text-white py-4 rounded-xl font-semibold hover:bg-blue-700"
        >
          Download PDF
        </button>
      </div>
    </div>
  );
}
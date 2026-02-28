import { useState } from "react";
import { jsPDF } from "jspdf";

export default function History() {
  const [reports] = useState(() => {
    try {
      const data = localStorage.getItem("all_reports");
      if (!data) return [];
      return JSON.parse(data);
    } catch {
      return [];
    }
  });

  // Helper for wrapped text in PDF
  const drawWrappedText = (doc, text, x, y, maxWidth, lineHeight = 6) => {
    const lines = doc.splitTextToSize(text, maxWidth);
    lines.forEach((line) => {
      doc.text(line, x, y);
      y += lineHeight;
    });
    return y;
  };

  const downloadPDF = (report) => {
    const doc = new jsPDF();
    let y = 20;

    doc.setFontSize(20);
    doc.setTextColor("#1E3A8A");
    doc.text("Medical Report Analysis", 105, y, { align: "center" });
    y += 12;

    // Single results
    report.results.forEach((test) => {
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

    // Combined interpretation
    report.combined_interpretation.forEach((block) => {
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

    const safeDate = report.date.replace(/[: ]/g, "_");
    doc.save(`Report_${safeDate}.pdf`);
  };

  const getAbnormalCount = (results, combined) => {
    const singleAbnormal = results.filter((r) => r.status === "High").length;
    const combinedAbnormal = combined.reduce(
      (sum, block) => sum + block.results.filter((r) => r.status === "High").length,
      0
    );
    return singleAbnormal + combinedAbnormal;
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return {
      day: date.toLocaleDateString(),
      time: date.toLocaleTimeString(),
    };
  };

  const getTotalTests = (results, combined) => {
    const single = results.length;
    const combinedCount = combined.reduce((sum, block) => sum + block.results.length, 0);
    return single + combinedCount;
  };

  return (
    <div className="flex-1 p-8 bg-gray-50 min-h-screen">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800">
          Report History
        </h1>
        <p className="text-gray-500 mt-1">
          Your previously analyzed lab reports
        </p>
      </div>

      {/* Table */}
      <div className="bg-white rounded-xl shadow-md overflow-hidden max-w-5xl">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase">
                Date & Time
              </th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase">
                Tests Analyzed
              </th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase">
                Status
              </th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase">
                Actions
              </th>
            </tr>
          </thead>

          <tbody className="divide-y divide-gray-200">
            {reports.length === 0 ? (
              <tr>
                <td colSpan="4" className="text-center py-8 text-gray-500">
                  No reports found
                </td>
              </tr>
            ) : (
              reports
                .slice()
                .reverse()
                .map((report, index) => {
                  const { day, time } = formatDate(report.date);
                  const totalTests = getTotalTests(report.results, report.combined_interpretation);
                  const abnormalCount = getAbnormalCount(report.results, report.combined_interpretation);

                  return (
                    <tr key={index} className="hover:bg-gray-50 transition">
                      <td className="px-6 py-5">
                        <div>
                          <div className="font-semibold text-gray-800">{day}</div>
                          <div className="text-sm text-gray-500">{time}</div>
                        </div>
                      </td>

                      <td className="px-6 py-5">
                        <div className="font-medium text-gray-800">{totalTests} tests</div>
                        <div className="text-sm text-gray-500">Lab Report</div>
                      </td>

                      <td className="px-6 py-5">
                        {abnormalCount > 0 ? (
                          <span className="text-sm font-medium text-orange-700">
                            {abnormalCount} abnormal
                          </span>
                        ) : (
                          <span className="text-sm font-medium text-green-700">All normal</span>
                        )}
                      </td>

                      <td className="px-6 py-5">
                        <div className="flex space-x-2">
                          <button
                            onClick={() => downloadPDF(report)}
                            className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700"
                          >
                            Download
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { jsPDF } from "jspdf";

export default function History() {
  const [reports, setReports] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchReports = async () => {
      const token = localStorage.getItem("token");
      if (!token) return navigate("/login");

      try {
        const res = await fetch("http://127.0.0.1:8000/extraction-interpretation/my-reports", {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (res.status === 401) {
          localStorage.removeItem("token");
          navigate("/login");
          return;
        }

        const data = await res.json();
        setReports(data);
      } catch (err) {
        console.error("Error fetching reports:", err);
      }
    };

    fetchReports();
  }, [navigate]);

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
    doc.text("Medical Report Analysis", 105, y, { align: "center" });
    y += 12;

    report.results.forEach((test) => {
      y += 6;
      doc.setFontSize(14);
      doc.text(`${test.test} (${test.unit})`, 14, y);
      y += 8;
      doc.setFontSize(12);
      doc.text(`Value: ${test.value}`, 14, y);
      doc.text(`Range: ${test.range}`, 14, y + 6);
      y += 12;
      y = drawWrappedText(doc, test.meaning, 14, y, 180);
      y += 6;
      y = drawWrappedText(doc, test.advice, 14, y, 180);
      y += 10;
      if (y > 260) {
        doc.addPage();
        y = 20;
      }
    });

    const safeDate = report.created_at.replace(/[: ]/g, "_");
    doc.save(`Report_${safeDate}.pdf`);
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return {
      day: date.toLocaleDateString("en-GB", { timeZone: "Asia/Colombo" }),
      time: date.toLocaleTimeString("en-GB", { timeZone: "Asia/Colombo", hour12: false }),
    };
  };

  const getAbnormalCount = (results) => results.filter((r) => r.status === "High").length;

  return (
    <div className="flex-1 p-8 bg-gray-50 min-h-screen">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Report History</h1>
        <p className="text-gray-500 mt-1">Your previously analyzed lab reports</p>
      </div>

      <div className="bg-white rounded-xl shadow-md overflow-hidden max-w-5xl">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase">Date & Time</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase">Tests</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase">Status</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase">Actions</th>
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
              reports.slice().reverse().map((report) => {
                const { day, time } = formatDate(report.created_at);
                const abnormalCount = getAbnormalCount(report.results);
                return (
                  <tr key={report._id} className="hover:bg-gray-50 transition">
                    <td className="px-6 py-5">
                      <div>
                        <div className="font-semibold text-gray-800">{day}</div>
                        <div className="text-sm text-gray-500">{time}</div>
                      </div>
                    </td>
                    <td className="px-6 py-5">
                      <div className="font-medium text-gray-800">{report.results.length} tests</div>
                    </td>
                    <td className="px-6 py-5">
                      {abnormalCount > 0 ? (
                        <span className="text-sm font-medium text-orange-700">{abnormalCount} abnormal</span>
                      ) : (
                        <span className="text-sm font-medium text-green-700">All normal</span>
                      )}
                    </td>
                    <td className="px-6 py-5">
                      <button
                        onClick={() => downloadPDF(report)}
                        className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700"
                      >
                        Download
                      </button>
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
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { jsPDF } from "jspdf";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Area,
  AreaChart,
} from "recharts";

export default function History() {
  const [reports, setReports] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchReports = async () => {
      const token = localStorage.getItem("token");
      if (!token) return navigate("/login");

      try {
        const res = await fetch(
          "http://127.0.0.1:8000/extraction-interpretation/my-reports",
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );

        if (res.status === 401) {
          localStorage.removeItem("token");
          navigate("/login");
          return;
        }

        const data = await res.json();
        setReports(data);
      } catch (err) {
        console.error(err);
      }
    };

    fetchReports();
  }, [navigate]);

  const formatDate = (dateString) =>
    new Date(dateString).toLocaleDateString("en-GB");

  const getStatus = (report) => {
    const highs = report.results.filter((r) => r.status === "High").length;
    const total = report.results.length;
    if (highs === 0) return { label: "Normal", score: 0 };
    if (highs < total) return { label: "Partial", score: 1 };
    return { label: "Critical", score: 2 };
  };

  const getColor = (status) => {
    if (status === "Normal") return "#16A34A";
    if (status === "Partial") return "#D97706";
    return "#DC2626";
  };

  const graphData = reports
    .slice()
    .reverse()
    .map((report, idx) => {
      const status = getStatus(report);

      const findVal = (key) => {
        const match = report.results.find((x) =>
          x.test.toLowerCase().includes(key)
        );
        return match ? match.value : null;
      };

      return {
        idx,
        label: `R${idx + 1}`,
        fullLabel: `Report ${idx + 1}`,
        date: formatDate(report.created_at),
        status: status.label,
        score: status.score,
        totalTests: report.results.length,
        highCount: report.results.filter((r) => r.status === "High").length,
        hba1c: findVal("hba1c"),
        fbs: findVal("fasting"),
        ppbs: findVal("post"),
      };
    });

  // Bigger X-axis tick: "R1" + date below, both larger
  const CustomXAxisTick = ({ x, y, payload }) => {
    const point = graphData[payload.value];
    if (!point) return null;
    return (
      <g transform={`translate(${x},${y})`}>
        <text
          x={0} y={0} dy={18}
          textAnchor="middle"
          fill="#374151"
          fontSize={15}
          fontWeight={700}
        >
          {point.label}
        </text>
        <text
          x={0} y={0} dy={36}
          textAnchor="middle"
          fill="#6b7280"
          fontSize={13}
        >
          {point.date}
        </text>
      </g>
    );
  };

  const CustomTooltip = ({ active, payload }) => {
    if (!active || !payload || !payload.length) return null;
    const d = payload[0].payload;
    const color = getColor(d.status);

    return (
      <div style={{
        background: "#fff",
        border: `2px solid ${color}`,
        borderRadius: 12,
        padding: "12px 16px",
        fontSize: 13,
        boxShadow: "0 8px 24px rgba(0,0,0,0.12)",
        minWidth: 180,
      }}>
        <p style={{ fontWeight: 700, color: "#111827", fontSize: 14, marginBottom: 2 }}>
          {d.fullLabel}
        </p>
        <p style={{ color: "#9ca3af", fontSize: 12, marginBottom: 8 }}>{d.date}</p>
        <span style={{
          display: "inline-block",
          background: color + "18",
          color,
          fontWeight: 700,
          fontSize: 12,
          padding: "3px 10px",
          borderRadius: 20,
          marginBottom: 8,
        }}>
          ● {d.status}
        </span>
        <div style={{ borderTop: "1px solid #f3f4f6", paddingTop: 8, marginTop: 4 }}>
          <p style={{ color: "#374151", marginBottom: 2 }}>
            Total tests: <b>{d.totalTests}</b>
          </p>
          <p style={{ color: "#374151" }}>
            Abnormal: <b style={{ color: d.highCount > 0 ? "#DC2626" : "#16A34A" }}>{d.highCount}</b>
          </p>
        </div>
        {(d.hba1c !== null || d.fbs !== null || d.ppbs !== null) && (
          <div style={{ borderTop: "1px solid #f3f4f6", paddingTop: 8, marginTop: 8 }}>
            {d.hba1c !== null && <p style={{ color: "#6b7280" }}>HbA1c: <b style={{ color: "#111827" }}>{d.hba1c}</b></p>}
            {d.fbs !== null && <p style={{ color: "#6b7280" }}>FBS: <b style={{ color: "#111827" }}>{d.fbs}</b></p>}
            {d.ppbs !== null && <p style={{ color: "#6b7280" }}>PPBS: <b style={{ color: "#111827" }}>{d.ppbs}</b></p>}
          </div>
        )}
      </div>
    );
  };

  // ── PDF (same as Results.jsx) ─────────────────────────────────────────────
  const drawWrappedText = (doc, text, x, y, maxWidth, lineHeight = 6) => {
    if (!text) return y;
    const lines = doc.splitTextToSize(text, maxWidth);
    lines.forEach((line) => { doc.text(line, x, y); y += lineHeight; });
    return y;
  };

  const downloadReportPDF = (report, reportNumber) => {
    const doc = new jsPDF();
    let y = 20;

    doc.setFontSize(20);
    doc.setTextColor("#1E3A8A");
    doc.text("Medical Report Analysis", 105, y, { align: "center" });
    y += 12;

    report.results.forEach((test) => {
      y += 6;
      doc.setFontSize(16);
      doc.setTextColor("#111827");
      doc.text(`${test.test}${test.unit ? ` (${test.unit})` : ""}`, 14, y);

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
      if (y > 260) { doc.addPage(); y = 20; }
    });

    if (report.combined_interpretation && report.combined_interpretation.length > 0) {
      report.combined_interpretation.forEach((block) => {
        y += 10;
        doc.setFontSize(16);
        doc.setTextColor("#1E40AF");
        doc.text("Combined Interpretation", 14, y);
        y += 8;

        block.results.forEach((test) => {
          doc.setFontSize(14);
          doc.setTextColor("#111827");
          doc.text(`${test.test}${test.unit ? ` (${test.unit})` : ""}`, 14, y);

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
          if (y > 260) { doc.addPage(); y = 20; }
        });

        doc.setFontSize(14);
        doc.setTextColor("#1F2937");
        doc.text("Overall Interpretation:", 14, y);
        y += 6;
        doc.setFontSize(12);
        y = drawWrappedText(doc, block.interpretation, 14, y, 180);

        y += 10;
        if (y > 260) { doc.addPage(); y = 20; }
      });
    }

    doc.save(`Medical_Report_${reportNumber}.pdf`);
  };

  const statusBadge = (label) => {
    const base = { padding: "4px 14px", borderRadius: 20, fontWeight: 600, fontSize: 13, display: "inline-block" };
    if (label === "Normal")  return { ...base, background: "#DCFCE7", color: "#166534" };
    if (label === "Partial") return { ...base, background: "#FEF3C7", color: "#92400E" };
    return { ...base, background: "#FEE2E2", color: "#991B1B" };
  };

  return (
    <div className="flex min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl w-full space-y-6 mx-auto">

        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-800">Report History</h1>
          <p className="text-gray-500 mt-1">Your previously analyzed lab reports</p>
        </div>

        {/* ── GRAPH ──────────────────────────────────────────────────────── */}
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          <div style={{ background: "linear-gradient(90deg,#2563eb,#3b82f6)", height: 5 }} />

          <div className="p-8">
            {/* Graph header */}
            <div className="flex items-start justify-between mb-6">
              <div>
                <h2 className="text-xl font-bold text-gray-800">Report Trends</h2>
                <p className="text-sm text-gray-400 mt-0.5">Health status across all reports</p>
              </div>
              {/* Legend */}
              <div className="flex gap-5">
                {[
                  ["Normal",   "#16A34A"],
                  ["Partial",  "#D97706"],
                  ["Critical", "#DC2626"],
                ].map(([label, color]) => (
                  <div key={label} className="flex items-center gap-2 text-sm font-medium text-gray-600">
                    <span style={{
                      width: 12, height: 12, borderRadius: "50%",
                      background: color, display: "inline-block",
                    }} />
                    {label}
                  </div>
                ))}
              </div>
            </div>

            {graphData.length === 0 ? (
              <p className="text-gray-400 text-center py-16">No reports yet.</p>
            ) : (
              /* Dynamic: 100px per report, min 420, max 700 */
              <ResponsiveContainer width="100%" height={Math.min(Math.max(graphData.length * 100, 420), 700)}>
                <AreaChart
                  data={graphData}
                  margin={{ top: 20, right: 50, left: 16, bottom: 70 }}
                >
                  <defs>
                    <linearGradient id="scoreGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%"  stopColor="#3b82f6" stopOpacity={0.18} />
                      <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.02} />
                    </linearGradient>
                  </defs>

                  <CartesianGrid strokeDasharray="4 4" stroke="#f1f5f9" vertical={false} />

                  <XAxis
                    dataKey="idx"
                    tick={<CustomXAxisTick />}
                    tickLine={false}
                    axisLine={{ stroke: "#e5e7eb" }}
                    height={70}
                    padding={{ left: 30, right: 30 }}
                  />

                  <YAxis
                    ticks={[0, 1, 2]}
                    tickFormatter={(v) =>
                      v === 0 ? "Normal" : v === 1 ? "Partial" : "Critical"
                    }
                    tick={{ fontSize: 14, fill: "#6b7280", fontWeight: 600 }}
                    tickLine={false}
                    axisLine={false}
                    width={90}
                    tickMargin={12}
                    domain={[-0.3, 2.5]}
                  />

                  <Tooltip content={<CustomTooltip />} cursor={{ stroke: "#e5e7eb", strokeWidth: 1 }} />

                  {/* Soft fill */}
                  <Area
                    type="monotone"
                    dataKey="score"
                    stroke="none"
                    fill="url(#scoreGrad)"
                    isAnimationActive={false}
                  />

                  {/* Main line — thicker for bigger chart */}
                  <Line
                    type="monotone"
                    dataKey="score"
                    stroke="#3b82f6"
                    strokeWidth={4}
                    isAnimationActive={false}
                    dot={(props) => {
                      const { cx, cy, payload } = props;
                      const color = getColor(payload.status);
                      return (
                        <g key={`dot-${payload.idx}`}>
                          <circle cx={cx} cy={cy} r={18} fill={color} opacity={0.1} />
                          <circle cx={cx} cy={cy} r={11} fill="#fff" stroke={color} strokeWidth={3} />
                          <circle cx={cx} cy={cy} r={6}  fill={color} />
                        </g>
                      );
                    }}
                    activeDot={(props) => {
                      const { cx, cy, payload } = props;
                      const color = getColor(payload.status);
                      return (
                        <g key={`adot-${payload.idx}`}>
                          <circle cx={cx} cy={cy} r={22} fill={color} opacity={0.12} />
                          <circle cx={cx} cy={cy} r={14} fill="#fff" stroke={color} strokeWidth={3.5} />
                          <circle cx={cx} cy={cy} r={7}  fill={color} />
                        </g>
                      );
                    }}
                  />
                </AreaChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>

        {/* ── TABLE ─────────────────────────────────────────────────────── */}
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-100">
              <tr>
                <th className="p-4 text-left text-sm font-semibold text-gray-600">Report</th>
                <th className="p-4 text-left text-sm font-semibold text-gray-600">Date</th>
                <th className="p-4 text-left text-sm font-semibold text-gray-600">Tests</th>
                <th className="p-4 text-left text-sm font-semibold text-gray-600">Abnormal</th>
                <th className="p-4 text-left text-sm font-semibold text-gray-600">Status</th>
                <th className="p-4 text-left text-sm font-semibold text-gray-600">Download</th>
              </tr>
            </thead>
            <tbody>
              {reports.length === 0 ? (
                <tr>
                  <td colSpan={6} className="p-6 text-center text-gray-400">No reports found.</td>
                </tr>
              ) : (
                reports.slice().reverse().map((r, i) => {
                  const status = getStatus(r);
                  const highCount = r.results.filter((x) => x.status === "High").length;
                  return (
                    <tr key={i} className="border-t border-gray-50 hover:bg-gray-50 transition">
                      <td className="p-4 font-semibold text-gray-700">Report {i + 1}</td>
                      <td className="p-4 text-gray-600">{formatDate(r.created_at)}</td>
                      <td className="p-4 text-gray-600">{r.results.length}</td>
                      <td className="p-4">
                        {highCount > 0
                          ? <span className="text-red-600 font-semibold">{highCount} high</span>
                          : <span className="text-green-600">None</span>}
                      </td>
                      <td className="p-4">
                        <span style={statusBadge(status.label)}>{status.label}</span>
                      </td>
                      <td className="p-4">
                        <button
                          onClick={() => downloadReportPDF(r, i + 1)}
                          className="bg-blue-600 text-white px-4 py-2 rounded-xl font-semibold shadow hover:bg-blue-700 transition text-sm"
                        >
                          Download PDF
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
    </div>
  );
}
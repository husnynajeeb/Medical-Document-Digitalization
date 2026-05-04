import { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { jsPDF } from "jspdf";
import {
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Area,
  AreaChart,
  ReferenceLine,
} from "recharts";

export default function History() {
  const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";
  const [reports, setReports] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchReports = async () => {
      const token = localStorage.getItem("token");
      if (!token) return navigate("/login");
      try {
        const res = await fetch(
          `${API_BASE_URL}/extraction-interpretation/my-reports`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
          },
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

  const getBgColor = (status) => {
    if (status === "Normal") return "#f0fdf4";
    if (status === "Partial") return "#fffbeb";
    return "#fef2f2";
  };

  const graphData = reports
    .slice()
    .reverse()
    .map((report, idx) => {
      const status = getStatus(report);
      const findVal = (key) => {
        const match = report.results.find((x) =>
          x.test.toLowerCase().includes(key),
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

  // Summary stats
  const normalCount = graphData.filter((d) => d.status === "Normal").length;
  const partialCount = graphData.filter((d) => d.status === "Partial").length;
  const criticalCount = graphData.filter((d) => d.status === "Critical").length;
  const latestStatus = graphData.length
    ? graphData[graphData.length - 1].status
    : null;

  // Custom X tick
  const CustomXAxisTick = ({ x, y, payload }) => {
    const point = graphData[payload.value];
    if (!point) return null;
    const color = getColor(point.status);
    return (
      <g transform={`translate(${x},${y})`}>
        {/* Coloured dot above label */}
        <circle cx={0} cy={4} r={5} fill={color} opacity={0.85} />
        <text
          x={0}
          y={0}
          dy={22}
          textAnchor="middle"
          fill="#374151"
          fontSize={14}
          fontWeight={700}
        >
          {point.label}
        </text>
        <text
          x={0}
          y={0}
          dy={38}
          textAnchor="middle"
          fill="#6b7280"
          fontSize={12}
        >
          {point.date}
        </text>
      </g>
    );
  };

  // Custom dot that renders coloured segments between points via SVG lines
  // We use a custom dot + a custom line via linearGradient trick
  const CustomDot = (props) => {
    const { cx, cy, payload } = props;
    const color = getColor(payload.status);
    return (
      <g key={`dot-${payload.idx}`}>
        <circle cx={cx} cy={cy} r={20} fill={color} opacity={0.08} />
        <circle
          cx={cx}
          cy={cy}
          r={12}
          fill="#fff"
          stroke={color}
          strokeWidth={3}
        />
        <circle cx={cx} cy={cy} r={6} fill={color} />
      </g>
    );
  };

  const CustomActiveDot = (props) => {
    const { cx, cy, payload } = props;
    const color = getColor(payload.status);
    return (
      <g key={`adot-${payload.idx}`}>
        <circle cx={cx} cy={cy} r={26} fill={color} opacity={0.1} />
        <circle
          cx={cx}
          cy={cy}
          r={16}
          fill="#fff"
          stroke={color}
          strokeWidth={3.5}
        />
        <circle cx={cx} cy={cy} r={8} fill={color} />
      </g>
    );
  };

  const CustomTooltip = ({ active, payload }) => {
    if (!active || !payload || !payload.length) return null;
    const d = payload[0].payload;
    const color = getColor(d.status);
    return (
      <div
        style={{
          background: "#fff",
          border: `2px solid ${color}`,
          borderRadius: 14,
          padding: "14px 18px",
          fontSize: 13,
          boxShadow: "0 12px 32px rgba(0,0,0,0.13)",
          minWidth: 190,
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 8,
            marginBottom: 6,
          }}
        >
          <span
            style={{
              width: 10,
              height: 10,
              borderRadius: "50%",
              background: color,
              display: "inline-block",
              flexShrink: 0,
            }}
          />
          <p
            style={{
              fontWeight: 700,
              color: "#111827",
              fontSize: 15,
              margin: 0,
            }}
          >
            {d.fullLabel}
          </p>
        </div>
        <p style={{ color: "#9ca3af", fontSize: 12, marginBottom: 10 }}>
          {d.date}
        </p>
        <span
          style={{
            display: "inline-block",
            background: color + "18",
            color,
            fontWeight: 700,
            fontSize: 12,
            padding: "3px 12px",
            borderRadius: 20,
            marginBottom: 10,
          }}
        >
          {d.status}
        </span>
        <div style={{ borderTop: "1px solid #f3f4f6", paddingTop: 8 }}>
          <p style={{ color: "#374151", marginBottom: 3 }}>
            Total tests: <b>{d.totalTests}</b>
          </p>
          <p style={{ color: "#374151" }}>
            Abnormal:{" "}
            <b style={{ color: d.highCount > 0 ? "#DC2626" : "#16A34A" }}>
              {d.highCount}
            </b>
          </p>
        </div>
        {(d.hba1c !== null || d.fbs !== null || d.ppbs !== null) && (
          <div
            style={{
              borderTop: "1px solid #f3f4f6",
              paddingTop: 8,
              marginTop: 8,
            }}
          >
            {d.hba1c !== null && (
              <p style={{ color: "#6b7280" }}>
                HbA1c: <b style={{ color: "#111827" }}>{d.hba1c}</b>
              </p>
            )}
            {d.fbs !== null && (
              <p style={{ color: "#6b7280" }}>
                FBS: <b style={{ color: "#111827" }}>{d.fbs}</b>
              </p>
            )}
            {d.ppbs !== null && (
              <p style={{ color: "#6b7280" }}>
                PPBS: <b style={{ color: "#111827" }}>{d.ppbs}</b>
              </p>
            )}
          </div>
        )}
      </div>
    );
  };

  // ── PDF ───────────────────────────────────────────────────────────────────
  const drawWrappedText = (doc, text, x, y, maxWidth, lineHeight = 6) => {
    if (!text) return y;
    const lines = doc.splitTextToSize(text, maxWidth);
    lines.forEach((line) => {
      doc.text(line, x, y);
      y += lineHeight;
    });
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
      if (y > 260) {
        doc.addPage();
        y = 20;
      }
    });

    if (report.combined_interpretation?.length > 0) {
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
    }

    doc.save(`Medical_Report_${reportNumber}.pdf`);
  };

  const statusBadge = (label) => {
    const base = {
      padding: "4px 14px",
      borderRadius: 20,
      fontWeight: 600,
      fontSize: 13,
      display: "inline-block",
    };
    if (label === "Normal")
      return { ...base, background: "#DCFCE7", color: "#166534" };
    if (label === "Partial")
      return { ...base, background: "#FEF3C7", color: "#92400E" };
    return { ...base, background: "#FEE2E2", color: "#991B1B" };
  };

  const graphHeight = Math.min(Math.max(graphData.length * 100, 420), 700);

  return (
    <div className="flex min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl w-full space-y-6 mx-auto">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-800">Report History</h1>
          <p className="text-gray-500 mt-1">
            Your previously analyzed lab reports
          </p>
        </div>

        {/* ── SUMMARY CARDS ─────────────────────────────────────────────── */}
        {graphData.length > 0 && (
          <div className="grid grid-cols-4 gap-4">
            {/* Total */}
            <div className="bg-white rounded-2xl shadow p-5 flex flex-col gap-1 border-t-4 border-blue-500">
              <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide">
                Total Reports
              </p>
              <p className="text-3xl font-bold text-gray-800">
                {graphData.length}
              </p>
            </div>
            {/* Normal */}
            <div className="bg-white rounded-2xl shadow p-5 flex flex-col gap-1 border-t-4 border-green-500">
              <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide">
                Normal
              </p>
              <p className="text-3xl font-bold text-green-600">{normalCount}</p>
            </div>
            {/* Partial */}
            <div className="bg-white rounded-2xl shadow p-5 flex flex-col gap-1 border-t-4 border-amber-400">
              <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide">
                Partial
              </p>
              <p className="text-3xl font-bold text-amber-600">
                {partialCount}
              </p>
            </div>
            {/* Critical */}
            <div className="bg-white rounded-2xl shadow p-5 flex flex-col gap-1 border-t-4 border-red-500">
              <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide">
                Critical
              </p>
              <p className="text-3xl font-bold text-red-600">{criticalCount}</p>
            </div>
          </div>
        )}

        {/* ── GRAPH ──────────────────────────────────────────────────────── */}
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          {/* Top accent bar — colour reflects latest status */}
          <div
            style={{
              background: latestStatus
                ? `linear-gradient(90deg, #2563eb, ${getColor(latestStatus)})`
                : "linear-gradient(90deg,#2563eb,#3b82f6)",
              height: 5,
            }}
          />

          <div className="p-8">
            {/* Graph header */}
            <div className="flex items-start justify-between mb-8">
              <div>
                <h2 className="text-xl font-bold text-gray-800">
                  Report Trends
                </h2>
                <p className="text-sm text-gray-400 mt-0.5">
                  Health status across all reports
                </p>
              </div>
              <div className="flex gap-5">
                {[
                  ["Normal", "#16A34A"],
                  ["Partial", "#D97706"],
                  ["Critical", "#DC2626"],
                ].map(([label, color]) => (
                  <div
                    key={label}
                    className="flex items-center gap-2 text-sm font-medium text-gray-600"
                  >
                    <span
                      style={{
                        width: 12,
                        height: 12,
                        borderRadius: "50%",
                        background: color,
                        display: "inline-block",
                      }}
                    />
                    {label}
                  </div>
                ))}
              </div>
            </div>

            {graphData.length === 0 ? (
              <p className="text-gray-400 text-center py-16">No reports yet.</p>
            ) : (
              <ResponsiveContainer width="100%" height={graphHeight}>
                <AreaChart
                  data={graphData}
                  margin={{ top: 20, right: 50, left: 16, bottom: 70 }}
                >
                  <defs>
                    {/* Gradient fill under line */}
                    <linearGradient id="scoreGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop
                        offset="5%"
                        stopColor="#3b82f6"
                        stopOpacity={0.15}
                      />
                      <stop
                        offset="95%"
                        stopColor="#3b82f6"
                        stopOpacity={0.01}
                      />
                    </linearGradient>

                    {/* Zone band fills */}
                    <linearGradient id="normalZone" x1="0" y1="0" x2="0" y2="1">
                      <stop
                        offset="0%"
                        stopColor="#16A34A"
                        stopOpacity={0.06}
                      />
                      <stop
                        offset="100%"
                        stopColor="#16A34A"
                        stopOpacity={0.02}
                      />
                    </linearGradient>
                    <linearGradient
                      id="partialZone"
                      x1="0"
                      y1="0"
                      x2="0"
                      y2="1"
                    >
                      <stop
                        offset="0%"
                        stopColor="#D97706"
                        stopOpacity={0.07}
                      />
                      <stop
                        offset="100%"
                        stopColor="#D97706"
                        stopOpacity={0.02}
                      />
                    </linearGradient>
                    <linearGradient
                      id="criticalZone"
                      x1="0"
                      y1="0"
                      x2="0"
                      y2="1"
                    >
                      <stop
                        offset="0%"
                        stopColor="#DC2626"
                        stopOpacity={0.07}
                      />
                      <stop
                        offset="100%"
                        stopColor="#DC2626"
                        stopOpacity={0.02}
                      />
                    </linearGradient>
                  </defs>

                  {/* Subtle grid */}
                  <CartesianGrid
                    strokeDasharray="4 4"
                    stroke="#f1f5f9"
                    vertical={false}
                  />

                  {/* Zone bands via reference lines with label */}
                  <ReferenceLine
                    y={0}
                    stroke="#16A34A"
                    strokeWidth={1.5}
                    strokeDasharray="6 3"
                    label={{ value: "", position: "insideTopLeft" }}
                  />
                  <ReferenceLine
                    y={1}
                    stroke="#D97706"
                    strokeWidth={1.5}
                    strokeDasharray="6 3"
                    label={{ value: "", position: "insideTopLeft" }}
                  />
                  <ReferenceLine
                    y={2}
                    stroke="#DC2626"
                    strokeWidth={1.5}
                    strokeDasharray="6 3"
                    label={{ value: "", position: "insideTopLeft" }}
                  />

                  <XAxis
                    dataKey="idx"
                    tick={<CustomXAxisTick />}
                    tickLine={false}
                    axisLine={{ stroke: "#e5e7eb" }}
                    height={70}
                    padding={{ left: 40, right: 40 }}
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

                  <Tooltip
                    content={<CustomTooltip />}
                    cursor={{
                      stroke: "#e2e8f0",
                      strokeWidth: 2,
                      strokeDasharray: "4 4",
                    }}
                  />

                  {/* Area fill under line */}
                  <Area
                    type="monotone"
                    dataKey="score"
                    stroke="none"
                    fill="url(#scoreGrad)"
                    isAnimationActive={false}
                  />

                  {/* Main trend line */}
                  <Area
                    type="monotone"
                    dataKey="score"
                    stroke="#3b82f6"
                    strokeWidth={4}
                    fill="none"
                    isAnimationActive={true}
                    animationDuration={800}
                    dot={<CustomDot />}
                    activeDot={<CustomActiveDot />}
                  />
                </AreaChart>
              </ResponsiveContainer>
            )}

            {/* Trend summary pill */}
            {graphData.length >= 2 &&
              (() => {
                const first = graphData[0];
                const last = graphData[graphData.length - 1];
                const diff = last.score - first.score;
                const improved = diff < 0;
                const same = diff === 0;
                return (
                  <div
                    style={{
                      marginTop: 16,
                      display: "inline-flex",
                      alignItems: "center",
                      gap: 8,
                      background: same
                        ? "#f8fafc"
                        : improved
                          ? "#f0fdf4"
                          : "#fef2f2",
                      border: `1px solid ${same ? "#e2e8f0" : improved ? "#bbf7d0" : "#fecaca"}`,
                      borderRadius: 24,
                      padding: "6px 16px",
                      fontSize: 13,
                      fontWeight: 600,
                      color: same
                        ? "#64748b"
                        : improved
                          ? "#16a34a"
                          : "#dc2626",
                    }}
                  >
                    <span style={{ fontSize: 16 }}>
                      {same ? "→" : improved ? "↓" : "↑"}
                    </span>
                    {same
                      ? "Status unchanged across reports"
                      : improved
                        ? `Improved from ${first.status} → ${last.status}`
                        : `Worsened from ${first.status} → ${last.status}`}
                  </div>
                );
              })()}
          </div>
        </div>

        {/* ── TABLE ─────────────────────────────────────────────────────── */}
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-100">
              <tr>
                <th className="p-4 text-left text-sm font-semibold text-gray-600">
                  Report
                </th>
                <th className="p-4 text-left text-sm font-semibold text-gray-600">
                  Date
                </th>
                <th className="p-4 text-left text-sm font-semibold text-gray-600">
                  Tests
                </th>
                <th className="p-4 text-left text-sm font-semibold text-gray-600">
                  Abnormal
                </th>
                <th className="p-4 text-left text-sm font-semibold text-gray-600">
                  Status
                </th>
                <th className="p-4 text-left text-sm font-semibold text-gray-600">
                  Download
                </th>
              </tr>
            </thead>
            <tbody>
              {reports.length === 0 ? (
                <tr>
                  <td colSpan={6} className="p-6 text-center text-gray-400">
                    No reports found.
                  </td>
                </tr>
              ) : (
                reports
                  .slice()
                  .reverse()
                  .map((r, i) => {
                    const status = getStatus(r);
                    const highCount = r.results.filter(
                      (x) => x.status === "High",
                    ).length;
                    return (
                      <tr
                        key={i}
                        className="border-t border-gray-50 hover:bg-gray-50 transition"
                      >
                        <td className="p-4 font-semibold text-gray-700">
                          Report {i + 1}
                        </td>
                        <td className="p-4 text-gray-600">
                          {formatDate(r.created_at)}
                        </td>
                        <td className="p-4 text-gray-600">
                          {r.results.length}
                        </td>
                        <td className="p-4">
                          {highCount > 0 ? (
                            <span className="text-red-600 font-semibold">
                              {highCount} high
                            </span>
                          ) : (
                            <span className="text-green-600">None</span>
                          )}
                        </td>
                        <td className="p-4">
                          <span style={statusBadge(status.label)}>
                            {status.label}
                          </span>
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

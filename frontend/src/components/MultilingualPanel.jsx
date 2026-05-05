import React, { useState } from "react";
import axios from "axios";

const API_URL = "http://localhost:8000/multilingual";

const MultilingualPanel = ({ inputType, text = "", imageBase64 = "" }) => {
  const [targetLang, setTargetLang] = useState("en");
  const [summarize, setSummarize] = useState(true);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleProcess = async () => {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const payload = {
        input_type: inputType,
        text,
        image_base64: imageBase64,
        target_lang: targetLang,
        summarize,
      };

      const response = await axios.post(`${API_URL}/process`, payload);
      setResult(response.data.data || response.data);
    } catch (err) {
      console.error("Processing error:", err);
      setError("Processing failed. Please check backend connection.");
    } finally {
      setLoading(false);
    }
  };

  const hasObjectData = (obj) => obj && Object.keys(obj).length > 0;

  const splitMedicalSections = (content) => {
    if (!content) return [];

    const normalized = content.replace(/\s+/g, " ").trim();

    const patterns = [
      {
        title: "மொத்த கொலஸ்ட்ரோல்",
        regex: /மொத்த கொலஸ்ட்ரோல்/i,
      },
      {
        title: "டிரைகிளிசரைட்கள்",
        regex: /டிரைகிளிசரைட்கள்/i,
      },
      {
        title: "HDL கொலஸ்ட்ரோல்",
        regex: /HDL கொலஸ்ட்ரோல்/i,
      },
      {
        title: "மொத்த பரிசோதனை",
        regex: /மொத்த பரிசோதனை/i,
      },
      {
        title: "TOTAL CHOLESTEROL",
        regex: /TOTAL CHOLESTEROL/i,
      },
      {
        title: "TRIGLYCERIDES",
        regex: /TRIGLYCERIDES/i,
      },
      {
        title: "HDL CHOLESTEROL",
        regex: /HDL CHOLESTEROL/i,
      },
      {
        title: "Overall Interpretation",
        regex: /Overall Interpretation/i,
      },
    ];

    const positions = patterns
      .map((pattern) => {
        const match = normalized.match(pattern.regex);
        return match
          ? {
              title: pattern.title,
              index: match.index,
            }
          : null;
      })
      .filter(Boolean)
      .sort((a, b) => a.index - b.index);

    if (!positions.length) {
      return [{ title: "Output", content: normalized }];
    }

    return positions.map((section, index) => {
      const start = section.index + section.title.length;
      const end =
        index + 1 < positions.length
          ? positions[index + 1].index
          : normalized.length;

      return {
        title: section.title,
        content: normalized.slice(start, end).trim(),
      };
    });
  };

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>🌍 Multilingual Processing</h3>

      <div style={styles.controls}>
        <div style={styles.row}>
          <label style={styles.label}>Language:</label>
          <select
            value={targetLang}
            onChange={(e) => setTargetLang(e.target.value)}
            style={styles.select}
          >
            <option value="en">English</option>
            <option value="si">Sinhala</option>
            <option value="ta">Tamil</option>
          </select>
        </div>

        <label style={styles.checkboxLabel}>
          <input
            type="checkbox"
            checked={summarize}
            onChange={() => setSummarize(!summarize)}
          />
          Enable Summarization
        </label>

        <button
          onClick={handleProcess}
          style={{
            ...styles.button,
            opacity: loading ? 0.7 : 1,
            cursor: loading ? "not-allowed" : "pointer",
          }}
          disabled={loading}
        >
          {loading ? "Processing..." : "Process"}
        </button>
      </div>

      {error && <div style={styles.error}>{error}</div>}

      {result && (
        <div style={styles.output}>
          {result.processing_note && (
            <div style={styles.note}>⚠️ {result.processing_note}</div>
          )}

          {typeof result.confidence === "number" && (
            <div style={styles.confidenceBox}>
              <div style={styles.confidenceHeader}>
                <strong>Confidence Score</strong>
                <span>{Math.round(result.confidence * 100)}%</span>
              </div>
              <div style={styles.progressOuter}>
                <div
                  style={{
                    ...styles.progressInner,
                    width: `${Math.round(result.confidence * 100)}%`,
                  }}
                />
              </div>
            </div>
          )}

          <SectionedOutput
            title="📄 Full Translation"
            content={result.full_translation || "-"}
            splitMedicalSections={splitMedicalSections}
          />

          <Section
            title="🧠 Medical Summary"
            content={result.medical_summary || "-"}
          />

          <Section
            title="👤 Patient Summary"
            content={result.patient_summary || "-"}
          />

          {result.prediction_output && (
            <Section
              title="📊 Prediction Output"
              content={result.prediction_output}
            />
          )}

          {hasObjectData(result.abbreviations) && (
            <div style={styles.card}>
              <h4 style={styles.cardTitle}>🔤 Abbreviations</h4>
              <ul style={styles.list}>
                {Object.entries(result.abbreviations).map(([key, value]) => (
                  <li key={key} style={styles.listItem}>
                    <strong>{key}</strong>: {value}
                  </li>
                ))}
              </ul>
            </div>
          )}

          <div style={styles.aiPanel}>
            <h4 style={styles.aiTitle}>🧠 AI Explanation Panel</h4>

            {hasObjectData(result.explanations) ? (
              <ul style={styles.list}>
                {Object.entries(result.explanations).map(([key, value]) => (
                  <li key={key} style={styles.listItem}>
                    <strong>{key}</strong>: {value}
                  </li>
                ))}
              </ul>
            ) : (
              <p style={styles.muted}>
                No additional medical term explanations detected.
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

const detectStatus = (title, content) => {
  const combined = `${title} ${content}`.toLowerCase();

  if (
    combined.includes("குறைந்த நிலையில்") ||
    combined.includes("low") ||
    combined.includes("குறைவு")
  ) {
    return "Low";
  }

  if (
    combined.includes("உயர் நிலையில்") ||
    combined.includes("high") ||
    combined.includes("அதிக")
  ) {
    return "High";
  }

  return null;
};

const Section = ({ title, content }) => (
  <div style={styles.card}>
    <h4 style={styles.cardTitle}>{title}</h4>
    <p style={styles.text}>{content}</p>
  </div>
);

const SectionedOutput = ({ title, content, splitMedicalSections }) => {
  const sections = splitMedicalSections(content);

  return (
    <div style={styles.card}>
      <h4 style={styles.cardTitle}>{title}</h4>

      {sections.map((section, index) => {
        const status = detectStatus(section.title, section.content);

        return (
          <div key={index} style={styles.reportCard}>
            <div style={styles.reportHeader}>
              <h3 style={styles.reportTitle}>{section.title}</h3>

              {status === "High" && <span style={styles.highBadge}>High</span>}
              {status === "Low" && <span style={styles.lowBadge}>Low</span>}
            </div>

            <div style={styles.reportBody}>
              <p style={styles.reportText}>{section.content}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default MultilingualPanel;

const styles = {
  container: {
    marginTop: "20px",
    padding: "18px",
    border: "1px solid #dbeafe",
    borderRadius: "14px",
    background: "#f8fbff",
    boxShadow: "0 6px 18px rgba(15, 23, 42, 0.08)",
  },
  title: {
    marginBottom: "14px",
    fontSize: "20px",
    fontWeight: "700",
    color: "#1e3a8a",
  },
  controls: {
    display: "flex",
    flexWrap: "wrap",
    gap: "12px",
    alignItems: "center",
    marginBottom: "12px",
  },
  row: {
    display: "flex",
    gap: "8px",
    alignItems: "center",
  },
  label: {
    fontWeight: "600",
    color: "#374151",
  },
  select: {
    padding: "8px 10px",
    borderRadius: "8px",
    border: "1px solid #cbd5e1",
    background: "#fff",
  },
  checkboxLabel: {
    display: "flex",
    gap: "8px",
    alignItems: "center",
    color: "#374151",
    fontWeight: "500",
  },
  button: {
    padding: "9px 18px",
    background: "#2563eb",
    color: "#fff",
    border: "none",
    borderRadius: "9px",
    fontWeight: "600",
  },
  error: {
    marginTop: "10px",
    padding: "10px",
    borderRadius: "8px",
    background: "#fee2e2",
    color: "#991b1b",
  },
  output: {
    marginTop: "18px",
  },
  note: {
    padding: "10px",
    marginBottom: "12px",
    background: "#fff7ed",
    color: "#9a3412",
    borderRadius: "10px",
    border: "1px solid #fed7aa",
  },
  confidenceBox: {
    padding: "14px",
    background: "#eef2ff",
    borderRadius: "12px",
    border: "1px solid #c7d2fe",
    marginBottom: "14px",
  },
  confidenceHeader: {
    display: "flex",
    justifyContent: "space-between",
    color: "#3730a3",
    marginBottom: "8px",
  },
  progressOuter: {
    width: "100%",
    height: "10px",
    background: "#e5e7eb",
    borderRadius: "999px",
    overflow: "hidden",
  },
  progressInner: {
    height: "100%",
    background: "#4f46e5",
    borderRadius: "999px",
  },
  card: {
    padding: "14px",
    marginTop: "12px",
    background: "#ffffff",
    borderRadius: "12px",
    border: "1px solid #e5e7eb",
  },
  cardTitle: {
    marginBottom: "12px",
    color: "#111827",
    fontWeight: "700",
    fontSize: "18px",
  },
  reportCard: {
    marginTop: "16px",
    background: "#f9fafb",
    borderRadius: "20px",
    overflow: "hidden",
    border: "1px solid #e5e7eb",
  },
  reportHeader: {
    padding: "20px 24px",
    background: "#ffffff",
    borderBottom: "1px solid #e5e7eb",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
  },
  reportTitle: {
    fontSize: "24px",
    fontWeight: "800",
    color: "#111827",
    margin: 0,
  },
  highBadge: {
    padding: "8px 18px",
    borderRadius: "999px",
    background: "#fee2e2",
    color: "#dc2626",
    fontWeight: "700",
  },
  lowBadge: {
    padding: "8px 18px",
    borderRadius: "999px",
    background: "#dbeafe",
    color: "#2563eb",
    fontWeight: "700",
  },
  reportBody: {
    padding: "22px 24px",
  },
  reportText: {
    whiteSpace: "pre-wrap",
    lineHeight: "1.7",
    color: "#374151",
    margin: 0,
    fontSize: "15px",
  },
  text: {
    whiteSpace: "pre-wrap",
    lineHeight: "1.6",
    color: "#374151",
    margin: 0,
  },
  aiPanel: {
    padding: "14px",
    marginTop: "12px",
    background: "#faf5ff",
    borderRadius: "12px",
    border: "1px solid #e9d5ff",
  },
  aiTitle: {
    color: "#7e22ce",
    fontWeight: "700",
    marginBottom: "8px",
  },
  list: {
    paddingLeft: "20px",
    margin: 0,
  },
  listItem: {
    marginBottom: "6px",
    color: "#374151",
    lineHeight: "1.5",
  },
  muted: {
    color: "#6b7280",
    margin: 0,
  },
};
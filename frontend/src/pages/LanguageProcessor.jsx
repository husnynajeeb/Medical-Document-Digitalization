import { useState } from "react";
import { processMedicalImage } from "../api/translationApi";

function toBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
  });
}

export default function LanguageProcessor() {
  const [file, setFile] = useState(null);
  const [lang, setLang] = useState("en");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    setFile(e.target.files[0]);
  };

  const handleProcess = async () => {
    if (!file) return;

    setLoading(true);

    try {
      const base64 = await toBase64(file);

      const res = await processMedicalImage(base64, lang);

      setResult(res);
    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Medical Language Processor</h2>

      {/* Upload */}
      <input type="file" accept="image/*" onChange={handleUpload} />

      {/* Language Selector */}
      <select value={lang} onChange={(e) => setLang(e.target.value)}>
        <option value="en">English</option>
        <option value="si">Sinhala</option>
        <option value="ta">Tamil</option>
      </select>

      <button onClick={handleProcess} disabled={loading}>
        {loading ? "Processing..." : "Process Image"}
      </button>

      {/* OUTPUT */}
      {result && (
        <div style={{ marginTop: "20px" }}>
          <h3>Raw OCR Text</h3>
          <p>{result.raw_text}</p>

          <h3>Full Translation</h3>
          <p>{result.full_translation}</p>

          <h3>Medical Summary</h3>
          <p>{result.medical_summary}</p>

          <h3>Patient Friendly</h3>
          <p>{result.patient_summary}</p>
        </div>
      )}
    </div>
  );
}
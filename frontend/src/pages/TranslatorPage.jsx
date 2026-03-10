import React, { useState } from "react";
import TextInput from "../components/TextInput";
import OutputCard from "../components/OutputCard";
import GenerateButton from "../components/GenerateButton";
import ModeToggle from "../components/ModeToggle";
import LanguageSelector from "../components/LanguageSelector";
import { translateText } from "../services/api";
import "../styles/app.css";

function TranslatorPage() {

  const [text, setText] = useState("");
  const [output, setOutput] = useState(null);
  const [summarize, setSummarize] = useState(false);
  const [summaryType, setSummaryType] = useState("patient");
  const [lang, setLang] = useState("si");
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {

    if (!text.trim()) return;

    setLoading(true);

    try {

      const data = {
        text: text,
        target_lang: lang,
        summarize: summarize,
        summary_type: summaryType,
      };

      const result = await translateText(data);

      setOutput(result.translated_output);

    } catch (err) {
      console.error(err);
      alert("Translation failed");
    }

    setLoading(false);
  };

  return (

    <div className="container">

      <h1 className="title">
        Translation & Summarization
      </h1>

      <div className="controls">

        <LanguageSelector lang={lang} setLang={setLang} />

        <ModeToggle summarize={summarize} setSummarize={setSummarize} />

        {summarize && (
          <select
            className="dropdown"
            value={summaryType}
            onChange={(e) => setSummaryType(e.target.value)}
          >
            <option value="patient">Patient Summary</option>
            <option value="medical">Medical Summary</option>
          </select>
        )}

      </div>

      <div className="input-section">
        <TextInput text={text} setText={setText} />
      </div>

      <GenerateButton
        onClick={handleGenerate}
        loading={loading}
      />

      <div className="output-section">
        <OutputCard
          output={output}
          lang={lang}
        />
      </div>

    </div>
  );
}

export default TranslatorPage;
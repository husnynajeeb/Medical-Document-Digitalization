import React from "react";

function LanguageSelector({ lang, setLang }) {
  return (
    <select value={lang} onChange={(e) => setLang(e.target.value)}>
      <option value="si">Sinhala</option>
      <option value="ta">Tamil</option>
    </select>
  );
}

export default LanguageSelector;
import React from "react";

function LanguageSelector({ lang, setLang }) {
  return (
    <select value={lang} onChange={(e) => setLang(e.target.value)} className="dropdown">
      <option value="si" className="dropdown_opn">Sinhala</option>
      <option value="ta" className="dropdown_opn">Tamil</option>
    </select>
  );
}

export default LanguageSelector;
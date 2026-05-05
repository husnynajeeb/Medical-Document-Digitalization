import { useLanguage } from "../../services/useLanguage";

function LanguageSwitcher() {
  const { lang, setLang } = useLanguage();

  return (
    <select
      value={lang}
      onChange={(e) => setLang(e.target.value)}
      style={{
        padding: "6px 10px",
        borderRadius: "8px",
        border: "1px solid #ccc",
        background: "white",
        cursor: "pointer",
      }}
    >
      <option value="en">English</option>
      <option value="si">Sinhala</option>
      <option value="ta">Tamil</option>
    </select>
  );
}

export default LanguageSwitcher;
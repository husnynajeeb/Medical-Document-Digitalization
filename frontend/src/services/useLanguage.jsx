import { createContext, useContext, useState } from "react";
import { translations } from "../i18n";

// =============================
// CONTEXT
// =============================
const LanguageContext = createContext();

// =============================
// PROVIDER
// =============================
export const LanguageProvider = ({ children }) => {
  const [lang, setLang] = useState("en");

  const t = (key) => {
    return translations?.[lang]?.[key] || key;
  };

  return (
    <LanguageContext.Provider value={{ lang, setLang, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

// =============================
// HOOK
// =============================
export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error("useLanguage must be used inside LanguageProvider");
  }
  return context;
};
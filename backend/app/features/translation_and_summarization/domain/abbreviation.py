import re
from typing import Dict

ABBREVIATIONS = {
    "BP": {"en": "Blood Pressure", "si": "රුධිර පීඩනය", "ta": "இரத்த அழுத்தம்"},
    "HbA1c": {"en": "Glycated Hemoglobin", "si": "ග්ලයිකේටඩ් හෙමෝග්ලොබින්", "ta": "கிளைக்கேட்டட் ஹீமோகுளோபின்"},
    "LDL": {"en": "Low-Density Lipoprotein", "si": "අඩු ඝණත්ව ලිපොප්‍රෝටීන්", "ta": "குறைந்த அடர்த்தி லிப்போப்புரோட்டீன்"},
    "HDL": {"en": "High-Density Lipoprotein", "si": "ඉහළ ඝණත්ව ලිපොප්‍රෝටීන්", "ta": "உயர் அடர்த்தி லிப்போப்புரோட்டீன்"},
    "ECG": {"en": "Electrocardiogram", "si": "ඉලෙක්ට්‍රොකාර්ඩියොග්‍රෑම්", "ta": "எலெக்ட்ரோகார்டியோகிராம்"},
    "eGFR": {"en": "Estimated Glomerular Filtration Rate", "si": "ඇස්තමේන්තුගත ග්ලොමෙරුලර් පෙරීමේ වේගය", "ta": "மதிப்பிடப்பட்ட குளோமெருலர் வடிகட்டும் விகிதம்"}
}


def expand_abbreviations(text: str, lang: str = "en") -> Dict[str, str]:
    found = {}
    for abbr, translations in ABBREVIATIONS.items():
        if re.search(rf"\b{abbr}\b", text, re.IGNORECASE):
            found[abbr] = translations.get(lang, translations["en"])
    return found


def inject_abbreviations(text: str, lang: str = "en") -> str:
    for abbr, translations in ABBREVIATIONS.items():
        if re.search(rf"\b{abbr}\s*\(", text):
            continue

        full = translations.get(lang, translations["en"])

        text = re.sub(
            rf"\b{abbr}\b",
            f"{abbr} ({full})",
            text,
            flags=re.IGNORECASE
        )

    return text
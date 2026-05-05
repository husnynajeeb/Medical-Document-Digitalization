import re
from typing import Dict

MEDICAL_EXPLANATIONS = {
    "HbA1c": {
        "en": "Average blood sugar over 3 months",
        "si": "පසුගිය මාස 3 තුළ සාමාන්‍ය රුධිර සීනි මට්ටම",
        "ta": "கடந்த 3 மாதங்களில் சராசரி இரத்த சர்க்கரை"
    },
    "LDL": {
        "en": "Bad cholesterol",
        "si": "අහිතකර කොලෙස්ටරෝල්",
        "ta": "கெட்ட கொழுப்பு"
    },
    "HDL": {
        "en": "Good cholesterol",
        "si": "හොඳ කොලෙස්ටරෝල්",
        "ta": "நல்ல கொழுப்பு"
    },
    "BP": {
        "en": "Blood pressure level",
        "si": "රුධිර පීඩනය",
        "ta": "இரத்த அழுத்தம்"
    },
    "ECG": {
        "en": "Heart test",
        "si": "හෘද පරීක්ෂාව",
        "ta": "இதய பரிசோதனை"
    }
}


def get_explanations(abbreviations: Dict[str, str], lang: str = "en") -> Dict[str, str]:
    return {
        abbr: MEDICAL_EXPLANATIONS[abbr].get(lang, MEDICAL_EXPLANATIONS[abbr]["en"])
        for abbr in abbreviations if abbr in MEDICAL_EXPLANATIONS
    }


def add_explanations(text: str, lang: str = "en") -> str:

    for term, translations in MEDICAL_EXPLANATIONS.items():

        if re.search(rf"\b{term}\s*\(", text):
            continue

        explanation = translations.get(lang, translations["en"])

        text = re.sub(
            rf"\b{term}\b",
            f"{term} ({explanation})",
            text,
            flags=re.IGNORECASE
        )

    return text
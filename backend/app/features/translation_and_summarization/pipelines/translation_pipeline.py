import os
import re
import torch
from transformers import MarianMTModel, MarianTokenizer

from app.features.translation_and_summarization.config import (
    DEVICE,
    SI_MODEL_PATH,
    TA_MODEL_PATH,
)


# ===================================================
# MODEL HOLDERS
# ===================================================
si_tokenizer, si_model = None, None
ta_tokenizer, ta_model = None, None


# ===================================================
# LOAD MODELS
# ===================================================
def load_models():
    global si_tokenizer, si_model, ta_tokenizer, ta_model

    if si_model is None and os.path.isdir(SI_MODEL_PATH):
        print("✅ Loading Sinhala model...")
        si_tokenizer = MarianTokenizer.from_pretrained(SI_MODEL_PATH)
        si_model = MarianMTModel.from_pretrained(SI_MODEL_PATH).to(DEVICE)
        si_model.eval()

    if ta_model is None and os.path.isdir(TA_MODEL_PATH):
        print("✅ Loading Tamil model...")
        ta_tokenizer = MarianTokenizer.from_pretrained(TA_MODEL_PATH)
        ta_model = MarianMTModel.from_pretrained(TA_MODEL_PATH).to(DEVICE)
        ta_model.eval()


def get_model(lang: str):
    load_models()

    if lang == "si":
        return si_tokenizer, si_model

    if lang == "ta":
        return ta_tokenizer, ta_model

    return None, None


# ===================================================
# CLEAN TEXT
# ===================================================
def clean_text(text: str) -> str:
    if not text:
        return ""

    text = re.sub(r"\s+", " ", text)

    # Safe decimal cleanup only where dot exists
    text = re.sub(r"(\d)\s*\.\s*(\d)", r"\1.\2", text)

    # BP format cleanup
    text = re.sub(r"(\d{2,3})\s*/\s*(\d{2,3})", r"\1/\2", text)

    return text.strip()


# ===================================================
# MEDICAL TOKEN PROTECTION
# ===================================================
def protect(text: str) -> str:
    replacements = {
        "HbA1c": "HBA1C_TOKEN",
        "LDL": "LDL_TOKEN",
        "HDL": "HDL_TOKEN",
        "ECG": "ECG_TOKEN",
        "mg/dL": "MGDL_TOKEN",
        "mg/dl": "MGDL_TOKEN",
        "mmHg": "MMHG_TOKEN",
    }

    for original, token in replacements.items():
        text = re.sub(rf"\b{re.escape(original)}\b", token, text)

    return text


def restore(text: str) -> str:
    replacements = {
        "HBA1C_TOKEN": "HbA1c",
        "LDL_TOKEN": "LDL",
        "HDL_TOKEN": "HDL",
        "ECG_TOKEN": "ECG",
        "MGDL_TOKEN": "mg/dL",
        "MMHG_TOKEN": "mmHg",
    }

    for token, original in replacements.items():
        text = text.replace(token, original)

    return text


# ===================================================
# FINAL MEDICAL CLEANUP
# ===================================================
def final_medical_cleanup(text: str) -> str:
    if not text:
        return ""

    # Remove leaked or partially translated placeholder tokens
    token_fixes = {
        "MGGLTOken": "mg/dL",
        "MGDLTOken": "mg/dL",
        "MGDLTOKEN": "mg/dL",
        "MGDL_TOKEN": "mg/dL",
        "MGDLடோகென்": "mg/dL",
        "LDLடோகென்": "LDL",
        "HDLடோகென்": "HDL",
        "HBA1Cடோகென்": "HbA1c",
        "MMHGடோகென்": "mmHg",
        "LDLTOKEN": "LDL",
        "HDLTOKEN": "HDL",
        "HBA1CTOKEN": "HbA1c",
    }

    for wrong, correct in token_fixes.items():
        text = text.replace(wrong, correct)

    # Remove leftover token-like fragments
    text = re.sub(r"\b[A-Z]+TOken\b", "", text)
    text = re.sub(r"\b[A-Z]+TOKEN\b", "", text)

    # Common range corrections caused by model output
    text = text.replace("125.0-20.0", "125.0-200.0")
    text = text.replace("0.150.0", "0.0-150.0")
    text = text.replace("45.0-60.0", "45.0-60.0")

    # Unit normalization
    text = text.replace("mg/dl", "mg/dL")
    text = text.replace("மி.கி./டி.எல்.", "mg/dL")
    text = text.replace("மி.கி/டி.எல்", "mg/dL")

    # Duplicate units
    text = re.sub(r"mg/dL\s*mg/dL", "mg/dL", text)

    # Fix accidental spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ===================================================
# TAMIL GRAMMAR IMPROVER
# ===================================================
def improve_tamil(text: str) -> str:
    if not text:
        return ""

    text = text.replace("_", "")

    replacements = {
        "நிலை உயர்": "உயர் நிலையில் உள்ளது",
        "நிலை குறைந்தது": "குறைந்த நிலையில் உள்ளது",
        "சாதாரணம்:": "குறிப்பு:",
        "முக்கிய கண்டறியல்": "முக்கிய கண்டறிவுகள்",
        "கண்டறியல்": "கண்டறிவுகள்",
        "உயர் மதிப்புகள் கண்டறியப்பட்டது": "அதிகமான அளவுகள் கண்டறியப்பட்டுள்ளன",
        "குறைந்த மதிப்பீடு கண்டறிவிக்கப்பட்டது": "குறைந்த அளவுகள் கண்டறியப்பட்டுள்ளன",
        "சுகாதார குழந்தைகளுடன்": "ஆரோக்கியமான கொழுப்புகளுடன்",
        "சுகாதார குழாய்களுடன்": "ஆரோக்கியமான கொழுப்புகளுடன்",
        "சுதந்திர எடை": "ஆரோக்கியமான எடை",
        "வாழ்க்கை முறை ஊசிகள்": "வாழ்க்கை முறை மாற்றங்கள்",
        "மருத்துவரை பரிசோதனை": "மருத்துவரை அணுகவும்",
        "மருத்துவ மதிப்பீடு பயன்படுத்தவும்": "மருத்துவ மதிப்பீடு பெறவும்",
    }

    for wrong, correct in replacements.items():
        text = text.replace(wrong, correct)

    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ===================================================
# MEDICAL WORDING IMPROVER
# ===================================================
def medical_rewriter(text: str, lang: str) -> str:
    if not text:
        return ""

    if lang == "ta":
        replacements = {
            "High values detected": "அதிகமான அளவுகள் கண்டறியப்பட்டுள்ளன",
            "Low values detected": "குறைந்த அளவுகள் கண்டறியப்பட்டுள்ளன",
            "Key Findings": "முக்கிய கண்டறிவுகள்",
            "Abnormalities": "அசாதாரண முடிவுகள்",
        }

    elif lang == "si":
        replacements = {
            "High values detected": "ඉහළ අගයන් හඳුනාගෙන ඇත",
            "Low values detected": "අඩු අගයන් හඳුනාගෙන ඇත",
            "Key Findings": "ප්‍රධාන සොයාගැනීම්",
            "Abnormalities": "අසාමාන්‍ය ප්‍රතිඵල",
        }

    else:
        replacements = {}

    for wrong, correct in replacements.items():
        text = text.replace(wrong, correct)

    return text


# ===================================================
# TRANSLATE SINGLE SENTENCE
# ===================================================
def translate_sentence(text: str, lang: str) -> str:
    if not text:
        return ""

    if lang == "en":
        return text

    tokenizer, model = get_model(lang)

    if not tokenizer or not model:
        return text

    try:
        protected_text = protect(text)

        inputs = tokenizer(
            protected_text,
            return_tensors="pt",
            truncation=True,
            max_length=256,
        ).to(DEVICE)

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_length=256,
                num_beams=5,
                repetition_penalty=1.2,
                no_repeat_ngram_size=3,
            )

        translated = tokenizer.decode(outputs[0], skip_special_tokens=True)
        translated = restore(translated)
        translated = final_medical_cleanup(translated)

        return clean_text(translated)

    except Exception as e:
        print("❌ Translation sentence error:", str(e))
        return text


# ===================================================
# MAIN TRANSLATION FUNCTION
# ===================================================
def translate_text(text: str, lang: str) -> str:
    if not text:
        return ""

    if lang == "en":
        return text

    text = clean_text(text)

    sentences = re.split(r"(?<=[.!?])\s+", text)
    results = []

    for sentence in sentences:
        sentence = sentence.strip()

        if len(sentence) < 3:
            continue

        translated = translate_sentence(sentence, lang)

        if not translated:
            translated = sentence

        results.append(translated)

    final = " ".join(results)

    final = medical_rewriter(final, lang)

    if lang == "ta":
        final = improve_tamil(final)

    final = final_medical_cleanup(final)
    final = clean_text(final)

    return final


# ===================================================
# EXPORTS
# ===================================================
__all__ = ["translate_text"]
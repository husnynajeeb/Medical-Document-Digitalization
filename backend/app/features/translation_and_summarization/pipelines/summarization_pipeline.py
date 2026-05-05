import re
import torch
from transformers import AutoTokenizer, T5ForConditionalGeneration

from app.features.translation_and_summarization.config import DEVICE, T5_MODEL_PATH


# ===================================================
# MODEL HOLDERS
# ===================================================
t5_tokenizer = None
t5_model = None


# ===================================================
# MODEL LOADING
# ===================================================
def load_t5_model():
    global t5_tokenizer, t5_model

    if t5_tokenizer is None or t5_model is None:
        try:
            print("✅ Loading Clinical T5 model...")
            t5_tokenizer = AutoTokenizer.from_pretrained(T5_MODEL_PATH)
            t5_model = T5ForConditionalGeneration.from_pretrained(T5_MODEL_PATH).to(DEVICE)
            t5_model.eval()
        except Exception as e:
            print("❌ T5 model load failed:", str(e))
            t5_tokenizer = None
            t5_model = None

    return t5_tokenizer, t5_model


# ===================================================
# CLINICAL DATA EXTRACTION
# ===================================================
LAB_PATTERNS = {
    "HbA1c": r"HbA1c[:\s]*([\d.]+)\s*%",
    "LDL": r"LDL[:\s]*([\d.]+)\s*mg/dL",
    "HDL": r"HDL[:\s]*([\d.]+)\s*mg/dL",
    "BP": r"BP[:\s]*([\d]{2,3}/[\d]{2,3})(?:\s*mmHg)?",
    "eGFR": r"eGFR[:\s]*([\d.]+)",
    "Total Cholesterol": r"TOTAL\s+CHOLESTEROL[:\s]*([\d.]+)\s*mg/dl",
    "Triglycerides": r"TRIGLYCERIDES[:\s]*([\d.]+)\s*mg/dl",
}


def extract_clinical_data(text: str) -> dict:
    labs = {}

    for key, pattern in LAB_PATTERNS.items():
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            value = match.group(1)

            if key == "BP":
                labs[key] = f"{value} mmHg"
            elif key == "HbA1c":
                labs[key] = f"{value}%"
            elif key in ["LDL", "HDL", "Total Cholesterol", "Triglycerides"]:
                labs[key] = f"{value} mg/dL"
            else:
                labs[key] = value

    return labs


# ===================================================
# ABNORMALITY DETECTION
# ===================================================
def detect_abnormalities(text: str):
    abnormalities = []

    if re.search(r"\bhigh\b|\belevated\b", text, re.IGNORECASE):
        abnormalities.append("High values detected")

    if re.search(r"\blow\b|\breduced\b", text, re.IGNORECASE):
        abnormalities.append("Low values detected")

    return abnormalities


# ===================================================
# FALLBACK SUMMARY
# ===================================================
def fallback_summary(text: str, summary_type: str = "patient") -> str:
    labs = extract_clinical_data(text)
    abnormalities = detect_abnormalities(text)

    parts = []

    if labs:
        lab_text = ", ".join([f"{k}: {v}" for k, v in labs.items()])
        parts.append(f"Key findings: {lab_text}")

    if abnormalities:
        parts.append("Clinical note: " + ", ".join(abnormalities))

    if "cholesterol" in text.lower():
        parts.append("This report includes cholesterol-related results.")

    if "triglycerides" in text.lower():
        parts.append("Triglyceride level is included in the report.")

    if "blood sugar" in text.lower() or "glucose" in text.lower():
        parts.append("Blood sugar-related information is included.")

    if parts:
        return ". ".join(parts) + "."

    return text[:350].strip()


# ===================================================
# CLEAN INPUT PROMPT
# ===================================================
def build_clean_input(text: str, summary_type: str) -> str:
    text = re.sub(r"(\w+):\s*([^\.\n]+)", r"\1 is \2.", text)

    if summary_type == "patient":
        return f"""
Summarize this medical information for a patient in simple language.
Keep the original medical values accurate.
Do not add new advice that is not present in the text.

{text}
"""

    if summary_type == "medical":
        return f"""
Write a concise clinical summary.
Preserve key medical values, units, and abnormal findings.
Do not invent new diagnosis.

{text}
"""

    return text


# ===================================================
# OUTPUT CLEANER
# ===================================================
def clean_output(text: str) -> str:
    if not text:
        return ""

    text = re.sub(
        r"(Summarize.*|Write.*|Preserve.*|Do not.*|Keep.*)",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(r"[-•]\s*", "", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ===================================================
# STRUCTURED EXTRACTION
# ===================================================
def extract_sections(text: str):
    symptoms = []
    meds = []

    symptom_keywords = ["fatigue", "pain", "fever", "urination", "dizziness", "weakness"]

    for word in symptom_keywords:
        if word in text.lower():
            symptoms.append(word)

    meds.extend(re.findall(r"(Metformin\s*\d+mg)", text, re.IGNORECASE))

    return symptoms, meds


# ===================================================
# SAFE MEDICAL SUMMARY BUILDER
# ===================================================
def build_safe_medical_summary(model_summary: str, labs: dict, text: str) -> str:
    symptoms, meds = extract_sections(text)
    abnormalities = detect_abnormalities(text)

    ordered_keys = [
        "HbA1c",
        "LDL",
        "HDL",
        "Total Cholesterol",
        "Triglycerides",
        "BP",
        "eGFR",
    ]

    lab_parts = [f"{k}: {labs[k]}" for k in ordered_keys if k in labs]

    parts = []

    if lab_parts:
        parts.append("Key Findings: " + ", ".join(lab_parts))

    if abnormalities:
        parts.append("Abnormalities: " + ", ".join(abnormalities))

    if symptoms:
        parts.append("Symptoms: " + ", ".join(symptoms))

    if meds:
        parts.append("Medications: " + ", ".join(meds))

    if parts:
        return ". ".join(parts) + "."

    return model_summary if model_summary else fallback_summary(text, "medical")


# ===================================================
# CORE PIPELINE
# ===================================================
def summarize_section_aware(text: str, summary_type: str) -> str:
    if not text or len(text.split()) < 5:
        return text or ""

    tokenizer, model = load_t5_model()

    if tokenizer is None or model is None:
        return fallback_summary(text, summary_type)

    try:
        labs = extract_clinical_data(text)
        clean_input = build_clean_input(text, summary_type)

        inputs = tokenizer(
            clean_input,
            return_tensors="pt",
            truncation=True,
            max_length=512,
        ).to(DEVICE)

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_length=140,
                num_beams=4,
                repetition_penalty=1.2,
                no_repeat_ngram_size=3,
                early_stopping=True,
            )

        summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
        summary = clean_output(summary)

        if not summary or len(summary.split()) < 5:
            return fallback_summary(text, summary_type)

        if summary_type == "patient":
            return summary

        if summary_type == "medical":
            return build_safe_medical_summary(summary, labs, text)

        return summary

    except Exception as e:
        print("❌ Summarization error:", str(e))
        return fallback_summary(text, summary_type)


# ===================================================
# PUBLIC API
# ===================================================
def summarize_text(text: str, summary_type: str = "patient") -> str:
    if summary_type not in ["patient", "medical"]:
        return text
    return summarize_section_aware(text, summary_type)


def summarize_patient_friendly(text: str) -> str:
    return summarize_section_aware(text, "patient")


def summarize_medical(text: str) -> str:
    return summarize_section_aware(text, "medical")


summarize = summarize_text


__all__ = [
    "summarize_text",
    "summarize_patient_friendly",
    "summarize_medical",
    "summarize",
]
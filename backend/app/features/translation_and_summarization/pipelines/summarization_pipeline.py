import os
import torch
from typing import Dict, List
from transformers import AutoTokenizer, T5ForConditionalGeneration
from app.features.translation_and_summarization.config import DEVICE, T5_MODEL_PATH

t5_tokenizer = None
t5_model = None


def load_t5_model():
    """Lazy-load tokenizer and model so app import doesn't crash immediately."""
    global t5_tokenizer, t5_model

    if t5_tokenizer is None or t5_model is None:
        print("Loading Clinical T5 Model...")
        print("T5_MODEL_PATH:", repr(T5_MODEL_PATH))
        print("Path exists:", os.path.exists(T5_MODEL_PATH))
        print("Is directory:", os.path.isdir(T5_MODEL_PATH))

        if os.path.isdir(T5_MODEL_PATH):
            print("Files in model folder:", os.listdir(T5_MODEL_PATH))

        try:
            t5_tokenizer = AutoTokenizer.from_pretrained(T5_MODEL_PATH, use_fast=True)
            t5_model = T5ForConditionalGeneration.from_pretrained(T5_MODEL_PATH).to(DEVICE)
            t5_model.eval()
            print("✅ Clinical T5 loaded for specialized summaries")
        except Exception as e:
            print("❌ Failed to load Clinical T5 model/tokenizer")
            raise RuntimeError(
                f"Could not load T5 model from {T5_MODEL_PATH}. "
                f"The folder may be missing tokenizer files or may be incomplete. "
                f"Original error: {e}"
            ) from e

    return t5_tokenizer, t5_model


# ---------------------------------------------------
# SPECIALIZED PROMPTS - YOUR EXACT REQUIREMENT
# ---------------------------------------------------
def build_specialized_prompt(text: str, summary_type: str) -> str:
    """Patient: status/meds/plan | Medical: labs/conditions"""

    if summary_type == "patient":
        return """Patient-friendly summary: Focus ONLY on:
1. Current health status
2. Current medications (with doses)
3. Treatment plan/next steps

Use simple language. Keep ALL drug names, doses, numbers EXACTLY as written.

{text}""".format(text=text)

    if summary_type == "medical":
        return """Medical summary: Focus ONLY on:
1. Lab test values (HbA1c, eGFR, creatinine, etc.)
2. Diagnoses/conditions
3. Objective clinical data

Keep ALL lab values, numbers, medical terms EXACTLY as written.

{text}""".format(text=text)

    raise ValueError("summary_type must be 'patient' or 'medical'")


# ---------------------------------------------------
# SECTION-AWARE SUMMARIZATION
# ---------------------------------------------------
def extract_clinical_sections(text: str) -> Dict[str, List[str]]:
    """Extract relevant sections for targeted summaries"""
    sections = {
        "status": [],
        "medications": [],
        "labs": [],
        "conditions": [],
        "plan": []
    }

    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue

        lower = line.lower()

        # Status/conditions
        if any(word in lower for word in ['presents', 'history', 'reports', 'complains']):
            sections["status"].append(line)

        # Medications
        if any(drug in line for drug in ['mg ', 'BID', 'daily', 'nightly', 'Metformin', 'Amlodipine']):
            sections["medications"].append(line)

        # Labs
        if any(lab in line for lab in ['HbA1c', 'eGFR', 'creatinine', 'mg/dL', 'mmHg']):
            sections["labs"].append(line)

        # Plan
        if any(word in lower for word in ['plan', 'increase', 'add', 'continue', 'monitor', 'refer']):
            sections["plan"].append(line)

    return sections


# ---------------------------------------------------
# TARGETED SUMMARY GENERATION
# ---------------------------------------------------
def summarize_section_aware(text: str, summary_type: str) -> str:
    """Generate specialized summaries based on clinical focus"""

    if len(text.split()) < 30:
        return text

    tokenizer, model = load_t5_model()
    sections = extract_clinical_sections(text)

    if summary_type == "patient":
        patient_content = (
            '\n'.join(sections["status"]) + '\n' +
            '\n'.join(sections["medications"]) + '\n' +
            '\n'.join(sections["plan"])
        )
        if patient_content.strip():
            prompt = build_specialized_prompt(patient_content.strip(), "patient")
        else:
            prompt = build_specialized_prompt(text, "patient")

    else:  # medical
        medical_content = (
            '\n'.join(sections["labs"]) + '\n' +
            '\n'.join(sections["status"])
        )
        if medical_content.strip():
            prompt = build_specialized_prompt(medical_content.strip(), "medical")
        else:
            prompt = build_specialized_prompt(text, "medical")

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    ).to(DEVICE)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=200,
            num_beams=4,
            early_stopping=True,
            length_penalty=0.9,
            do_sample=False
        )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)


# ---------------------------------------------------
# MAIN API FUNCTIONS
# ---------------------------------------------------
def summarize_text(text: str, summary_type: str = "patient") -> str:
    """Main function - YOUR ORIGINAL SIGNATURE"""
    if summary_type not in ["patient", "medical"]:
        return text

    if len(text.split()) < 40:
        return text

    return summarize_section_aware(text, summary_type)


def summarize_patient_friendly(text: str) -> str:
    """Patient-focused: status, medications, plan"""
    return summarize_section_aware(text, "patient")


def summarize_medical(text: str) -> str:
    """Medical-focused: labs, conditions"""
    return summarize_section_aware(text, "medical")


# ---------------------------------------------------
# BACKWARD COMPATIBILITY
# ---------------------------------------------------
summarize = summarize_text


# ✅ EXPORTS FOR YOUR ROUTES
__all__ = [
    'summarize_text',
    'summarize_patient_friendly',
    'summarize_medical',
    'summarize'
]
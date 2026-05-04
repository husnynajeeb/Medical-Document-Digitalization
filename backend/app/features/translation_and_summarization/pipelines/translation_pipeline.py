import os
import re
from typing import Dict, List

import torch
from transformers import MarianMTModel, MarianTokenizer

from app.features.translation_and_summarization.config import DEVICE, SI_MODEL_PATH, TA_MODEL_PATH

try:
    from huggingface_hub import snapshot_download

    HF_HUB_AVAILABLE = True
except ImportError:
    HF_HUB_AVAILABLE = False

si_tokenizer = None
si_model = None
ta_tokenizer = None
ta_model = None


def _resolve_model_dir(model_path: str, repo_env: str, subdir_env: str) -> str:
    if os.path.isdir(model_path):
        return model_path

    if not HF_HUB_AVAILABLE:
        print("Translation model not found locally and huggingface_hub is missing")
        return model_path

    repo_id = os.getenv(repo_env)
    subdir = os.getenv(subdir_env)
    if not repo_id:
        print(f"Translation model not found locally. Set {repo_env} to download.")
        return model_path

    cache_dir = os.getenv("HF_CACHE_DIR")
    allow_patterns = None
    if subdir:
        allow_patterns = f"{subdir}/*"

    snapshot_path = snapshot_download(
        repo_id=repo_id,
        cache_dir=cache_dir,
        allow_patterns=allow_patterns,
    )

    if subdir:
        return os.path.join(snapshot_path, subdir)
    return snapshot_path


def _ensure_translation_models_loaded() -> None:
    global si_tokenizer, si_model, ta_tokenizer, ta_model

    if si_tokenizer is None or si_model is None:
        print("Loading Sinhala Translation Model...")
        si_dir = _resolve_model_dir(
            SI_MODEL_PATH, "HF_SI_MODEL_REPO", "HF_SI_MODEL_SUBDIR"
        )
        if os.path.isdir(si_dir):
            si_tokenizer = MarianTokenizer.from_pretrained(si_dir)
            si_model = MarianMTModel.from_pretrained(si_dir).to(DEVICE)
            si_model.eval()
        else:
            print("Sinhala translation model not available")

    if ta_tokenizer is None or ta_model is None:
        print("Loading Tamil Translation Model...")
        ta_dir = _resolve_model_dir(
            TA_MODEL_PATH, "HF_TA_MODEL_REPO", "HF_TA_MODEL_SUBDIR"
        )
        if os.path.isdir(ta_dir):
            ta_tokenizer = MarianTokenizer.from_pretrained(ta_dir)
            ta_model = MarianMTModel.from_pretrained(ta_dir).to(DEVICE)
            ta_model.eval()
        else:
            print("Tamil translation model not available")

# ---------------------------------------------------
# YOUR EXACT WORKING UTILITY FUNCTIONS
# ---------------------------------------------------
def split_sentences(text: str) -> List[str]:
    """Your reliable sentence splitter"""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

def get_translation_model(target_lang: str):
    """Your exact model getter"""
    _ensure_translation_models_loaded()
    if target_lang == "si":
        if si_tokenizer is None or si_model is None:
            raise ValueError("Sinhala translation model is not available")
        return si_tokenizer, si_model
    if target_lang == "ta":
        if ta_tokenizer is None or ta_model is None:
            raise ValueError("Tamil translation model is not available")
        return ta_tokenizer, ta_model
    raise ValueError(f"Unsupported language: {target_lang}")

# ---------------------------------------------------
# MEDICAL TERM PRESERVATION (SIMPLE REGEX)
# ---------------------------------------------------
def preserve_medical_terms(text: str) -> str:
    """Preserve critical clinical terms BEFORE translation"""
    # Preserve abbreviations
    text = re.sub(r'\b(HbA1c|eGFR|EF|CKD|LDL|HDL|ECG)\b', r'[\1]', text)
    
    # Preserve units  
    text = re.sub(r'\b(mg|mg/dL|mmHg|mL/min/1\.73m²?|%|units)\b', r'[\1]', text)
    
    # Preserve drug names
    drugs = ['Metformin', 'Amlodipine', 'Lisinopril', 'Atorvastatin', 'Aspirin', 
             'insulin glargine']
    for drug in drugs:
        text = re.sub(rf'\b{re.escape(drug)}\b', f'[{drug}]', text, flags=re.IGNORECASE)
    
    return text

def restore_medical_terms(text: str) -> str:
    """Simple bracket restoration"""
    # Restore abbreviations
    text = re.sub(r'\[(HbA1c|eGFR|EF|CKD|LDL|HDL|ECG)\]', r'\1', text)
    
    # Restore units
    text = re.sub(r'\[(mg|mg/dL|mmHg|mL/min/1\.73m²?|%|units)\]', r'\1', text)
    
    # Restore drugs
    drugs = ['Metformin', 'Amlodipine', 'Lisinopril', 'Atorvastatin', 'Aspirin', 
             'insulin glargine']
    for drug in drugs:
        text = re.sub(rf'\[' + re.escape(drug) + r'\]', drug, text, flags=re.IGNORECASE)
    
    return text

# ---------------------------------------------------
# POST-PROCESSING FIXES (Your translation artifacts)
# ---------------------------------------------------
def post_process_medical(text: str, lang: str) -> str:
    """Fix common Tamil/Sinhala translation errors"""
    if lang == "ta":
        fixes = {
            "மெலிட்டஸ்": "நீரிழிவு நோய்",
            "நீரிழிவு சிறுநீரக": "நிலையான சிறுநீரக நோய்", 
            "தோல் கட்டுப்பாடு": "இரத்த அழுத்த கட்டுப்பாடு",
            "அட்டோர்வாஸ்டடின்": "அட்ரோவாஸ்டாடின்",
            "கிரியாடினின்": "கிரியேட்டினின்",
        }
    elif lang == "si":
        fixes = {
            "මැලිතස්": "මධුමේහ රෝගය",
            "ඊශ්‍රායෙල් හෘද": "ඉස්කීමියා හෘද රෝගය",
            "රුටින් අනුගමනය": "රුටින් පරීක්ෂණය",
            "ලෙබ්‍රෑම්": "පරීක්ෂණ",
            "අධික රේඛාව": "සාමාන්‍ය මට්ටම",
        }
    else:
        return text
    
    for wrong, correct in fixes.items():
        text = re.sub(re.escape(wrong), correct, text, flags=re.IGNORECASE)
    return text

# ---------------------------------------------------
# YOUR CORE TRANSLATION FUNCTIONS
# ---------------------------------------------------
def translate_sentence(sentence: str, target_lang: str) -> str:
    """Single sentence translation - YOUR EXACT LOGIC + preservation"""
    # 1. Preserve medical terms
    preserved = preserve_medical_terms(sentence)
    
    # 2. Translate (YOUR WORKING CODE)
    tokenizer, model = get_translation_model(target_lang)
    inputs = tokenizer(preserved, return_tensors="pt", truncation=True, max_length=256).to(DEVICE)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            num_beams=5,
            max_length=256,
            early_stopping=True
        )
    
    translated = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # 3. Restore + post-process
    cleaned = restore_medical_terms(translated)
    final = post_process_medical(cleaned, target_lang)
    
    return final

def translate_text(text: str, target_lang: str) -> str:
    """Full text translation - YOUR PROVEN METHOD"""
    sentences = split_sentences(text)
    translated_sentences = [translate_sentence(sentence, target_lang) for sentence in sentences]
    return " ".join(translated_sentences)

# ---------------------------------------------------
# YOUR PERFECT SECTION STRUCTURE (KILLER FEATURE!)
# ---------------------------------------------------
def structure_text(text: str) -> Dict[str, List[str]]:
    """Clinical section detection - YOUR BRILLIANT LOGIC"""
    structured = {
        "General": [],
        "Recent Labs": [],
        "Current Medications": [],
        "Assessment": [],
        "Plan": []
    }
    
    current_section = "General"
    
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
            
        lower = line.lower()
        
        if "recent lab" in lower:
            current_section = "Recent Labs"
            continue
        if "current medication" in lower or "current medications" in lower:
            current_section = "Current Medications"
            continue
        if "assessment" in lower:
            current_section = "Assessment"
            continue
        if "plan" in lower:
            current_section = "Plan"
            continue
            
        structured[current_section].append(line)
    
    return structured

def translate_structured(text: str, target_lang: str) -> Dict[str, str]:
    """Section-structured translation - YOUR SIGNATURE FEATURE"""
    structured = structure_text(text)
    translated_sections = {}
    
    for section, content in structured.items():
        joined_text = "\n".join(content).strip()
        if not joined_text:
            translated_sections[section] = ""
            continue
        translated_sections[section] = translate_text(joined_text, target_lang)
    
    return translated_sections

# ---------------------------------------------------
# EXPORTS FOR YOUR ROUTES (EXACT MATCH)
# ---------------------------------------------------
__all__ = [
    'translate_text',           # Main function your routes need
    'translate_structured',     # Section translation  
    'split_sentences',         # Utility
    'get_translation_model',   # Internal
    'structure_text',          # Section detection
]

# Global instances for direct access
translation_pipeline = type('Pipeline', (), {
    'translate_text': translate_text,
    'translate_structured': translate_structured,
    'structure_text': structure_text
})()

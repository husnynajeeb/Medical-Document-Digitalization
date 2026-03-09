from transformers import MarianMTModel, MarianTokenizer
import torch
import re

from app.features.translation_and_summarization.config import DEVICE, SI_MODEL_PATH, TA_MODEL_PATH
from app.features.translation_and_summarization.utils.sentence_splitter import split_sentences
from app.features.translation_and_summarization.dictionaries.medical_dictionary import MEDICAL_TERM_MAP


# ---------------------------------------------------
# Load Models
# ---------------------------------------------------
print("Loading Sinhala Translation Model...")
si_tokenizer = MarianTokenizer.from_pretrained(SI_MODEL_PATH, local_files_only=True)
si_model = MarianMTModel.from_pretrained(SI_MODEL_PATH, local_files_only=True).to(DEVICE)
si_model.eval()

print("Loading Tamil Translation Model...")
ta_tokenizer = MarianTokenizer.from_pretrained(TA_MODEL_PATH, local_files_only=True)
ta_model = MarianMTModel.from_pretrained(TA_MODEL_PATH, local_files_only=True).to(DEVICE)
ta_model.eval()


def get_translation_model(target_lang):

    if target_lang == "si":
        return si_tokenizer, si_model

    if target_lang == "ta":
        return ta_tokenizer, ta_model

    raise ValueError("Unsupported language")


# ---------------------------------------------------
# Common clinical tokens to protect
# ---------------------------------------------------
MEDICAL_ABBREVIATIONS = [
    "HbA1c",
    "LDL",
    "HDL",
    "ECG",
    "EF",
    "eGFR",
    "CKD",
]

UNITS = [
    "mg",
    "mg/dL",
    "mmHg",
    "mL",
    "mL/min",
    "units",
    "%",
]


DRUG_NAMES = [
    "Metformin",
    "Amlodipine",
    "Lisinopril",
    "Atorvastatin",
    "Aspirin",
    "Insulin",
]


# ---------------------------------------------------
# Generic protection function
# ---------------------------------------------------
def protect_terms(text, terms, prefix):

    protected = {}
    modified_text = text
    index = 0

    for term in sorted(terms, key=len, reverse=True):

        pattern = re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)

        if pattern.search(modified_text):

            placeholder = f"{prefix}_{index}"

            modified_text = pattern.sub(placeholder, modified_text)

            protected[placeholder] = term

            index += 1

    return modified_text, protected


# ---------------------------------------------------
# Protect dictionary medical terms
# ---------------------------------------------------
def protect_medical_dictionary(text):

    protected = {}
    modified_text = text
    index = 0

    sorted_terms = sorted(MEDICAL_TERM_MAP.keys(), key=len, reverse=True)

    for term in sorted_terms:

        pattern = re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)

        if pattern.search(modified_text):

            placeholder = f"MEDTERM_{index}"

            modified_text = pattern.sub(placeholder, modified_text)

            protected[placeholder] = term

            index += 1

    return modified_text, protected


# ---------------------------------------------------
# Restore protected terms
# ---------------------------------------------------
def restore_terms(text, protected_terms):

    for placeholder in sorted(protected_terms.keys(), key=len, reverse=True):
        text = text.replace(placeholder, protected_terms[placeholder])

    return text


# ---------------------------------------------------
# Restore medical dictionary translations
# ---------------------------------------------------
def restore_medical_dictionary(text, protected_terms, target_lang):

    for placeholder, original_term in protected_terms.items():

        if original_term in MEDICAL_TERM_MAP:

            correct_translation = MEDICAL_TERM_MAP[original_term][target_lang]

            text = text.replace(placeholder, correct_translation)

    return text


# ---------------------------------------------------
# Translate a single sentence
# ---------------------------------------------------
def translate_sentence(sentence, target_lang):

    tokenizer, model = get_translation_model(target_lang)

    # Protect medical dictionary terms
    sentence, med_terms = protect_medical_dictionary(sentence)

    # Protect drug names
    sentence, drug_terms = protect_terms(sentence, DRUG_NAMES, "DRUG")

    # Protect abbreviations
    sentence, abbr_terms = protect_terms(sentence, MEDICAL_ABBREVIATIONS, "ABBR")

    # Protect units
    sentence, unit_terms = protect_terms(sentence, UNITS, "UNIT")

    inputs = tokenizer(
        sentence,
        return_tensors="pt",
        truncation=True,
        max_length=256
    ).to(DEVICE)

    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            num_beams=6,
            length_penalty=1.1,
            max_length=256,
            early_stopping=True
        )

    translated = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Restore terms
    translated = restore_terms(translated, drug_terms)
    translated = restore_terms(translated, abbr_terms)
    translated = restore_terms(translated, unit_terms)

    # Restore medical dictionary translations
    translated = restore_medical_dictionary(translated, med_terms, target_lang)

    return translated


# ---------------------------------------------------
# Translate full clinical text
# ---------------------------------------------------
def translate_text(text, target_lang):

    sentences = split_sentences(text)

    translated_sentences = []

    for sentence in sentences:

        translated = translate_sentence(sentence, target_lang)

        translated_sentences.append(translated)

    return " ".join(translated_sentences)
from app.features.translation_and_summarization.pipelines.summarization_pipeline import (
    summarize_medical,
    summarize_patient_friendly
)

from app.features.translation_and_summarization.pipelines.translation_pipeline import translate_text
from app.features.translation_and_summarization.services.ocr_service import extract_text_from_image
from app.features.translation_and_summarization.preprocessing.text_normalizer import normalize_text
from app.features.translation_and_summarization.domain.abbreviation import expand_abbreviations
from app.features.translation_and_summarization.postprocessing.explanation import get_explanations


# ===================================================
# OCR QUALITY CHECK
# ===================================================
def is_bad_ocr(text: str) -> bool:
    if not text or len(text.strip()) < 30:
        return True

    medical_keywords = [
        "HbA1c",
        "Blood Pressure",
        "Fasting Blood Sugar",
        "Cholesterol",
        "Triglycerides",
        "HDL",
        "LDL",
        "mg/dL",
        "mg/dl",
        "mmHg",
        "Blood Sugar",
        "Glucose",
        "Result",
        "Reference Range",
        "Patient",
    ]

    found_count = sum(
        1 for keyword in medical_keywords
        if keyword.lower() in text.lower()
    )

    if found_count < 2:
        return True

    words = text.split()
    if len(words) > 20:
        short_noise_count = sum(1 for word in words if len(word) <= 2)
        if short_noise_count / len(words) > 0.45:
            return True

    return False


# ===================================================
# CONFIDENCE SCORE
# ===================================================
def calculate_confidence(text: str, input_type: str, low_ocr: bool = False) -> float:
    if not text:
        return 0.0

    if low_ocr:
        return 0.25

    word_count = len(text.split())

    if "No text detected" in text or "No meaningful" in text:
        return 0.3

    if input_type == "image":
        return round(min(0.95, max(0.55, word_count / 120)), 2)

    if input_type == "text":
        return round(min(0.98, max(0.6, word_count / 100)), 2)

    if input_type == "prediction":
        return round(min(0.95, max(0.65, word_count / 80)), 2)

    return 0.5


# ===================================================
# SAFETY RESPONSE FOR BAD OCR
# ===================================================
def build_low_ocr_response(result: dict, raw_ocr_text: str, target_lang: str):
    safety_message = (
        "Low OCR quality detected. The system avoided translating unreliable OCR output. "
        "Please upload a clearer medical report image or use the interpreted text input."
    )

    result["raw_text"] = raw_ocr_text or ""
    result["processing_note"] = safety_message
    result["confidence"] = 0.25
    result["medical_summary"] = ""
    result["patient_summary"] = ""

    try:
        result["full_translation"] = translate_text(safety_message, target_lang)
    except Exception:
        result["full_translation"] = safety_message

    return result


# ===================================================
# MAIN ORCHESTRATION FUNCTION
# ===================================================
def process_input(
    input_type: str,
    text: str = None,
    image_base64: str = None,
    target_lang: str = "en",
    summarize: bool = True
):
    result = {
        "input_type": input_type,
        "raw_text": "",
        "full_translation": "",
        "medical_summary": "",
        "patient_summary": "",
        "abbreviations": {},
        "explanations": {},
        "prediction_output": None,
        "confidence": 0.0,
        "processing_note": ""
    }

    low_ocr_detected = False

    # ================= IMAGE INPUT =================
    if input_type == "image":
        try:
            extracted_text = extract_text_from_image(image_base64 or "")
        except Exception as e:
            print("❌ OCR error:", str(e))
            extracted_text = ""

        if is_bad_ocr(extracted_text):
            return build_low_ocr_response(
                result=result,
                raw_ocr_text=extracted_text,
                target_lang=target_lang
            )

        text = extracted_text
        result["raw_text"] = extracted_text

    # ================= TEXT INPUT =================
    elif input_type == "text":
        if not text or not text.strip():
            text = "No input text provided."
            result["processing_note"] = "No text input was provided."

        result["raw_text"] = text

    # ================= PREDICTION INPUT =================
    elif input_type == "prediction":
        normalized_prediction = normalize_text(text or "")

        if not normalized_prediction.strip():
            normalized_prediction = "No prediction output provided."
            result["processing_note"] = "No prediction text was provided."

        result["prediction_output"] = normalized_prediction
        result["raw_text"] = normalized_prediction

        try:
            result["full_translation"] = translate_text(normalized_prediction, target_lang)
        except Exception:
            result["full_translation"] = normalized_prediction

        result["confidence"] = calculate_confidence(normalized_prediction, input_type)
        return result

    else:
        raise ValueError("Invalid input_type. Use image, text, or prediction.")

    # ================= NORMALIZATION =================
    text = normalize_text(text or "")

    if not text.strip():
        text = "No meaningful medical content found."
        result["processing_note"] = "Input did not contain meaningful medical text."

    # ================= ABBREVIATIONS + EXPLANATIONS =================
    try:
        abbreviations = expand_abbreviations(text, lang=target_lang)
        explanations = get_explanations(abbreviations, lang=target_lang)

        result["abbreviations"] = abbreviations or {}
        result["explanations"] = explanations or {}

    except Exception as e:
        print("❌ Abbreviation/explanation error:", str(e))
        result["abbreviations"] = {}
        result["explanations"] = {}

    # ================= SUMMARIZATION =================
    if summarize:
        try:
            medical_summary_en = summarize_medical(text)
            patient_summary_en = summarize_patient_friendly(text)

            if not medical_summary_en or len(medical_summary_en.strip()) < 5:
                medical_summary_en = text

            if not patient_summary_en or len(patient_summary_en.strip()) < 5:
                patient_summary_en = text

            result["medical_summary"] = translate_text(medical_summary_en, target_lang)
            result["patient_summary"] = translate_text(patient_summary_en, target_lang)

        except Exception as e:
            print("❌ Summarization error:", str(e))
            result["medical_summary"] = translate_text(text, target_lang)
            result["patient_summary"] = translate_text(text, target_lang)

    else:
        result["medical_summary"] = ""
        result["patient_summary"] = ""

    # ================= FULL TRANSLATION =================
    try:
        translated_text = translate_text(text, target_lang)

        if not translated_text or len(translated_text.strip()) < 2:
            translated_text = text

        result["full_translation"] = translated_text

    except Exception as e:
        print("❌ Translation error:", str(e))
        result["full_translation"] = text

    # ================= CONFIDENCE =================
    result["confidence"] = calculate_confidence(
        text,
        input_type,
        low_ocr=low_ocr_detected
    )

    return result
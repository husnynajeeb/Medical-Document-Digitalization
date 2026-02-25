import re
from pathlib import Path
from PIL import Image
import pytesseract
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from .config import MODEL_PATH, TEST_KNOWLEDGE, TEST_ALIASES

# Configure Tesseract OCR path (Windows example)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ----------------- NER Model -----------------
def load_ner_model():
    global ner_pipeline

    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
    model = AutoModelForTokenClassification.from_pretrained(MODEL_PATH, local_files_only=True)

    ner_pipeline = pipeline(
        "ner",
        model=model,
        tokenizer=tokenizer,
        aggregation_strategy="simple"  # combine split tokens
    )

    print(f"NER model loaded from {MODEL_PATH}")

# ----------------- OCR Helpers -----------------
def normalize(text):
    text = text.upper()
    text = re.sub(r"[^A-Z0-9.%<>/\- ]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def ocr_lines(image_path):
    img = Image.open(image_path)
    raw = pytesseract.image_to_string(img)
    return [normalize(l) for l in raw.split("\n") if len(l.strip()) > 2]

def normalize_for_match(text):
    return re.sub(r"[^A-Z0-9]", "", text.upper())

# ----------------- Regex -----------------
RANGE_RE = re.compile(r"\d+\.?\d*\s*[-–]\s*\d+\.?\d*")
NUMBER_RE = re.compile(r"\b\d+\.\d+|\b\d+\b")

# ----------------- Test Matching -----------------
def match_test(line):
    line_norm = normalize_for_match(line)
    for test, aliases in TEST_ALIASES.items():
        for alias in aliases:
            alias_norm = normalize_for_match(alias)
            if line_norm.startswith(alias_norm) or line_norm[:15].startswith(alias_norm):
                return test
    return None

# ----------------- Value & Range Extraction -----------------
def extract_value_from_line(line):
    cleaned = RANGE_RE.sub("", line)
    decimal_match = re.search(r"\b\d+\.\d+\b", cleaned)
    if decimal_match:
        value = float(decimal_match.group())
    else:
        integer_match = re.search(r"\b\d+\b", cleaned)
        if not integer_match:
            return None
        value = float(integer_match.group())
    if value > 1000:
        return None
    return value

def extract_range_from_line(line):
    match = RANGE_RE.search(line)
    if match:
        return match.group(0).replace(" ", "")
    return None

# ----------------- Test Extraction -----------------
def extract_tests(lines):
    extracted = []
    seen = set()
    for line in lines:
        test = match_test(line)
        if not test or test in seen:
            continue
        value = extract_value_from_line(line)
        if value is None:
            continue
        report_range = extract_range_from_line(line)
        extracted.append({
            "test": test,
            "value": value,
            "range": report_range
        })
        seen.add(test)
    return extracted

def extract_tests_with_model(lines):
    if "ner_pipeline" not in globals():
        raise RuntimeError("NER model not loaded! Call load_ner_model() first.")

    extracted = []
    seen = set()

    for line in lines:
        entities = ner_pipeline(line)

        # ⭐⭐⭐ ADD DEBUG HERE ⭐⭐⭐
        print("\n========= OCR LINE =========")
        print(line)
        print("========= NER OUTPUT =======")
        print(entities)
        print("============================\n")

        for ent in entities:
            if ent['entity_group'] == "TEST" and float(ent['score']) > 0.80:
                test_name = ent['word']
                test_name = match_test(test_name) or test_name.upper()
                if test_name in seen:
                    continue

                value = extract_value_from_line(line)
                if value is None:
                    continue

                report_range = extract_range_from_line(line)

                extracted.append({
                    "test": test_name,
                    "value": value,
                    "range": report_range
                })
                seen.add(test_name)

    return extracted

# ----------------- Interpretation -----------------
def interpret_tests(extracted_list):
    merged = {}
    for report in extracted_list:
        for item in report:
            merged[item["test"]] = item

    output = []
    for test, data in merged.items():
        val = data["value"]
        info = TEST_KNOWLEDGE.get(test)
        if not info:
            continue
        unit = info["unit"]
        meaning = info["meaning"]
        low, high = None, None
        report_range = data.get("range")
        if report_range:
            nums = list(map(float, re.findall(r"\d+\.\d+|\d+", report_range)))
            if len(nums) == 2 and nums[0] <= nums[1]:
                low, high = nums
        if low is None or high is None:
            try:
                low, high = map(float, info["range"].split("-"))
            except:
                low, high = 0, val
        if val < low:
            status = "Low"
            advice_text = info.get("advice_low", "")
        elif val > high:
            status = "High"
            advice_text = info.get("advice_high", "")
        else:
            status = "Normal"
            advice_text = "Maintain a healthy lifestyle and routine monitoring."
        output.append({
            "test": test,
            "value": val,
            "unit": unit,
            "range": f"{low}-{high}",
            "status": status,
            "meaning": meaning,
            "advice": (
                f"Your {test} is {val} {unit}, which is {status.lower()} "
                f"compared to the normal range of {low}-{high}. {advice_text}"
            )
        })
    return output

# ----------------- Combined Interpretation -----------------
from .ocr_interpret_combined import generate_full_combined_interpretation


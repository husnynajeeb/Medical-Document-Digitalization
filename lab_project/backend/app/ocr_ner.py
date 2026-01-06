# app/ocr_ner.py
import re
import json
from PIL import Image
import pytesseract
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

from .config import MODEL_PATH, TEST_KNOWLEDGE, TEST_ALIASES

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# Ensure Windows path works
MODEL_ROOT = MODEL_PATH.replace("\\", "/")

# Load tokenizer and model locally
tokenizer = AutoTokenizer.from_pretrained(MODEL_ROOT, local_files_only=True)
model = AutoModelForTokenClassification.from_pretrained(MODEL_ROOT, local_files_only=True)

# Create NER pipeline
ner_pipeline = pipeline(
    "ner",
    model=model,
    tokenizer=tokenizer,
    aggregation_strategy="simple"
)

def normalize(text):
    """Normalize OCR text"""
    text = text.upper()
    # Escape '-' to avoid regex range errors
    text = re.sub(r"[^A-Z0-9.%<>/\- ]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def ocr_lines(image_path):
    img = Image.open(image_path)
    raw = pytesseract.image_to_string(img)
    return [normalize(l) for l in raw.split("\n") if len(l.strip()) > 2]

def normalize_for_match(text):
    """Remove non-alphanumeric for matching"""
    return re.sub(r"[^A-Z0-9]", "", text.upper())


VALUE_RE = re.compile(r"(?<![-–])\b\d+(\.\d+)?\b")
RANGE_RE = re.compile(r"\d+\.?\d*\s*[-–]\s*\d+\.?\d*")

def extract_value_from_lines(lines, idx, lookahead=3):
    # 1️⃣ Prefer value on SAME line
    same_line_nums = re.findall(r"\d+\.\d+|\d+", lines[idx])
    if same_line_nums:
        return float(same_line_nums[0])

    # 2️⃣ Otherwise look ahead
    for offset in range(1, lookahead + 1):
        if idx + offset < len(lines):
            nums = re.findall(r"\d+\.\d+|\d+", lines[idx + offset])
            if nums:
                return float(nums[0])

    return None

def extract_range_from_lines(lines, idx):
    """Extract range from current or next line"""
    for offset in [0, 1]:
        if idx + offset < len(lines):
            m = RANGE_RE.search(lines[idx + offset])
            if m:
                return m.group(0).replace(" ", "")
    return None

def match_test(line):
    line_norm = normalize_for_match(line)
    matched = None
    longest_len = 0

    for test, aliases in TEST_ALIASES.items():
        for alias in aliases:
            alias_norm = normalize_for_match(alias)
            if alias_norm in line_norm:
                if len(alias_norm) > longest_len:
                    matched = test
                    longest_len = len(alias_norm)

    return matched


def extract_tests(lines):
    extracted = []
    seen = set()

    for i, line in enumerate(lines):
        test = match_test(line)
        if not test or test in seen:
            continue

        value = extract_value_from_lines(lines, i)
        if value is None:
            continue

        report_range = extract_range_from_lines(lines, i)

        extracted.append({
            "test": test,
            "value": value,
            "range": report_range
        })

        seen.add(test)

    return extracted

import re

def interpret_tests(extracted):
    output = []

    for t in extracted:
        test = t["test"]
        val = t["value"]
        info = TEST_KNOWLEDGE[test]

        unit = info["unit"]
        meaning = info["meaning"]

        # 1️⃣ Prefer OCR range if it looks valid (skip ratio tests)
        rng = t.get("range")
        low, high = None, None
        if rng and "RATIO" not in test and "/" not in test:
            nums = list(map(float, re.findall(r"\d+\.\d+|\d+", rng)))
            if len(nums) == 2 and nums[0] <= nums[1]:
                low, high = nums

        # 2️⃣ Fallback to knowledge range if OCR range is invalid
        if low is None or high is None:
            try:
                low, high = map(float, info["range"].split("-"))
            except Exception:
                low, high = 0, val  # ultimate fallback

        # Status determination
        if val < low:
            status = "Low"
            advice = info.get("advice_low", "")
        elif val > high:
            status = "High"
            advice = info.get("advice_high", "")
        else:
            status = "Normal"
            advice = "Maintain a healthy lifestyle and routine monitoring."

        output.append({
            "test": test,
            "value": val,
            "unit": unit,
            "range": f"{low}-{high}",
            "status": status,
            "meaning": meaning,
            "advice": (
                f"Your {test} is {val} {unit}, which is {status.lower()} "
                f"compared to the normal range of {low}-{high}. {advice}"
            )
        })

    return output





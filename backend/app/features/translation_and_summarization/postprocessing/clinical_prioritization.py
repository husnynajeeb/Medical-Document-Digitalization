import re
from typing import List, Dict

# Reference ranges (expandable)
REFERENCE_RANGES = {
    "HbA1c": (4.0, 5.6),
    "LDL": (0, 100),
    "HDL": (40, 60),
    "Glucose": (70, 99)
}


def classify_value(param: str, value: float):
    if param not in REFERENCE_RANGES:
        return "unknown", "low"

    low, high = REFERENCE_RANGES[param]

    if value > high:
        if param == "HbA1c" and value >= 7:
            return "high", "critical"
        return "high", "abnormal"

    if value < low:
        return "low", "abnormal"

    return "normal", "low"


def detect_abnormalities(text: str) -> List[Dict]:
    findings = []

    patterns = {
        "HbA1c": r'HbA1c\s*[:\-]?\s*(\d+\.?\d*)',
        "LDL": r'LDL\s*[:\-]?\s*(\d+\.?\d*)',
        "HDL": r'HDL\s*[:\-]?\s*(\d+\.?\d*)',
        "Glucose": r'glucose\s*[:\-]?\s*(\d+\.?\d*)'
    }

    for param, pattern in patterns.items():
        matches = re.findall(pattern, text, re.IGNORECASE)

        for m in matches:
            value = float(m)

            status, priority = classify_value(param, value)

            findings.append({
                "parameter": param,
                "value": value,
                "status": status,
                "priority": priority
            })

    return findings
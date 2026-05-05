import re

SECTION_PATTERNS = {
    "Recent Labs": [r"lab results?", r"investigations?", r"blood test"],
    "Current Medications": [r"medications?", r"drugs?", r"rx"],
    "Assessment": [r"assessment", r"diagnosis", r"impression"],
    "Plan": [r"plan", r"recommendation", r"advice", r"treatment"]
}

def detect_section(line: str):
    lower = line.lower()

    for section, patterns in SECTION_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, lower):
                return section

    return None


def structure_text(text: str):

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

        detected = detect_section(line)

        if detected:
            current_section = detected
            continue

        structured[current_section].append(line)

    return structured
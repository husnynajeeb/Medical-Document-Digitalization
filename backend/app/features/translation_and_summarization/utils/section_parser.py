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

        lower = line.lower()

        if "recent lab" in lower:
            current_section = "Recent Labs"
            continue

        if "current medication" in lower:
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
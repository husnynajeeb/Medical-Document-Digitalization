import re

def normalize_text(text: str) -> str:

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)

    # Fix spacing around units
    text = re.sub(r'(\d)(mg/dL|mmHg|%)', r'\1 \2', text)

    # Standardize common terms
    text = re.sub(r'\bBP\b', 'Blood Pressure', text)
    text = re.sub(r'\bHR\b', 'Heart Rate', text)

    # Remove unwanted symbols
    text = re.sub(r'[^\w\s\.\,\%\-/]', '', text)

    return text.strip()
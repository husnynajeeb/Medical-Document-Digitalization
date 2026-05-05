import re

ABBREVIATIONS = ["Dr.", "Mr.", "Mrs.", "mg/dL", "mmHg", "HbA1c"]

def split_sentences(text: str):

    for abbr in ABBREVIATIONS:
        text = text.replace(abbr, abbr.replace(".", "<DOT>"))

    sentences = re.split(r'(?<=[.!?])\s+', text)

    sentences = [s.replace("<DOT>", ".").strip() for s in sentences if s.strip()]

    return sentences
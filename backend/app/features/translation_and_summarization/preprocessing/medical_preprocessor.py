from app.features.translation_and_summarization.preprocessing.text_normalizer import normalize_text
from app.features.translation_and_summarization.preprocessing.sentence_splitter import split_sentences
from app.features.translation_and_summarization.preprocessing.section_parser import structure_text

def preprocess_medical_text(text: str):

    # Step 1: Normalize
    normalized = normalize_text(text)

    # Step 2: Structure
    structured = structure_text(normalized)

    # Step 3: Sentence split each section
    processed = {}

    for section, content in structured.items():
        joined = " ".join(content)
        processed[section] = split_sentences(joined)

    return processed
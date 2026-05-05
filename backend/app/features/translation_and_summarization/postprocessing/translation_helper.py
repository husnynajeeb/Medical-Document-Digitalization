from typing import Dict
from app.features.translation_and_summarization.pipelines.translation_pipeline import translate_text

def translate_dict(data: Dict[str, str], target_lang: str) -> Dict[str, str]:
    """
    Translate dictionary values while keeping keys unchanged.
    """
    translated = {}

    for key, value in data.items():
        translated[key] = translate_text(value, target_lang)

    return translated
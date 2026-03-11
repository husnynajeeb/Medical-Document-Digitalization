from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.features.translation_and_summarization.schemas.request_schema import (
    TranslateRequest,
    TTSRequest
)

from app.features.translation_and_summarization.pipelines.translation_pipeline import translate_text
from app.features.translation_and_summarization.pipelines.summarization_pipeline import summarize_text
from app.features.translation_and_summarization.pipelines.tts_pipeline import generate_tts

from app.features.translation_and_summarization.utils.section_parser import structure_text
from app.features.translation_and_summarization.utils.text_normalizer import normalize_text


router = APIRouter()


@router.post("/translate")
def translate_endpoint(req: TranslateRequest):

    text = normalize_text(req.text)

    if req.summarize:

        summarized = summarize_text(text, req.summary_type)

        translated = translate_text(
            summarized,
            req.target_lang
        )

        return {"translated_output": translated}

    structured = structure_text(text)

    translated_sections = {}

    for section, content in structured.items():

        joined = "\n".join(content).strip()

        if not joined:
            translated_sections[section] = ""
            continue

        translated_sections[section] = translate_text(
            joined,
            req.target_lang
        )

    return {"translated_output": translated_sections}


@router.post("/tts")
def text_to_speech(req: TTSRequest):

    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Empty text")

    audio = generate_tts(req.text, req.target_lang)

    return StreamingResponse(
        audio,
        media_type="audio/mpeg"
    )
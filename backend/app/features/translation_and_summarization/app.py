from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from schemas.request_schema import TranslateRequest, TTSRequest

from pipelines.translation_pipeline import translate_text
from pipelines.summarization_pipeline import summarize_text
from pipelines.tts_pipeline import generate_tts

from utils.section_parser import structure_text
from utils.text_normalizer import normalize_text

app = FastAPI(title="Medical Translation & Clinical Summarization API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "Medical Translation API running"}


@app.post("/translate")
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


@app.post("/tts")
def text_to_speech(req: TTSRequest):

    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Empty text")

    audio = generate_tts(req.text, req.target_lang)

    return StreamingResponse(
        audio,
        media_type="audio/mpeg"
    )

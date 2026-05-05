from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.features.translation_and_summarization.schemas.request_schema import (
    TranslateRequest,
    TTSRequest
)

from app.features.translation_and_summarization.pipelines.tts_pipeline import generate_tts
from app.features.translation_and_summarization.core.unified_processor import process_input


router = APIRouter()


# ===================================================
# 🧠 UNIFIED PROCESS ENDPOINT
# ===================================================
@router.post("/process")
def process_endpoint(req: TranslateRequest):

    # ===================================================
    # VALIDATION
    # ===================================================
    allowed_types = ["text", "image", "prediction"]

    if not req.input_type or req.input_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid input_type. Allowed: {allowed_types}"
        )

    if req.input_type == "text" and not req.text:
        raise HTTPException(status_code=400, detail="Text input missing")

    if req.input_type == "image" and not req.image_base64:
        raise HTTPException(status_code=400, detail="Image input missing")

    try:
        # ===================================================
        # CORE PROCESSING
        # ===================================================
        result = process_input(
            input_type=req.input_type,
            text=req.text,
            image_base64=req.image_base64,
            target_lang=req.target_lang,
            summarize=req.summarize
        )

        # ===================================================
        # STANDARD RESPONSE FORMAT
        # ===================================================
        return {
            "status": "success",
            "data": result
        }

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error during processing"
        )


# ===================================================
# 🔊 TEXT TO SPEECH
# ===================================================
@router.post("/tts")
def text_to_speech(req: TTSRequest):

    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="Empty text")

    try:
        audio = generate_tts(req.text, req.target_lang)

        return StreamingResponse(
            audio,
            media_type="audio/mpeg"
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="TTS generation failed"
        )
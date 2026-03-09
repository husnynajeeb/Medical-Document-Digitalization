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



# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import StreamingResponse
# from pydantic import BaseModel
# from transformers import (
#     MarianMTModel,
#     MarianTokenizer,
#     T5Tokenizer,
#     T5ForConditionalGeneration
# )
# from typing import Optional
# import torch
# import re
# import io
# import os
# from gtts import gTTS

# # =========================================================
# # FastAPI Initialization
# # =========================================================

# app = FastAPI(title="Medical Translation & Clinical Summarization API")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# print("Using device:", DEVICE)

# # =========================================================
# # Model Paths
# # =========================================================

# SI_MODEL_PATH = os.path.join(BASE_DIR, "./models/en_si_finetuned_new")
# TA_MODEL_PATH = os.path.join(BASE_DIR, "./models/en_ta_finetuned_new")
# T5_MODEL_PATH = os.path.join(BASE_DIR, "./models/clinical_t5_finetuned")

# # =========================================================
# # Load Translation Models
# # =========================================================

# print("Loading Sinhala Translation Model...")
# si_tokenizer = MarianTokenizer.from_pretrained(SI_MODEL_PATH)
# si_model = MarianMTModel.from_pretrained(SI_MODEL_PATH).to(DEVICE)
# si_model.eval()

# print("Loading Tamil Translation Model...")
# ta_tokenizer = MarianTokenizer.from_pretrained(TA_MODEL_PATH)
# ta_model = MarianMTModel.from_pretrained(TA_MODEL_PATH).to(DEVICE)
# ta_model.eval()

# # =========================================================
# # Load Clinical Summarization Model
# # =========================================================

# print("Loading Clinical T5 Model...")
# t5_tokenizer = T5Tokenizer.from_pretrained(T5_MODEL_PATH)
# t5_model = T5ForConditionalGeneration.from_pretrained(T5_MODEL_PATH).to(DEVICE)
# t5_model.eval()

# print("All models loaded successfully")

# # =========================================================
# # Request Schemas
# # =========================================================

# class TranslateRequest(BaseModel):
#     text: str
#     target_lang: str
#     summarize: Optional[bool] = False
#     summary_type: Optional[str] = "patient"


# class TTSRequest(BaseModel):
#     text: str
#     target_lang: str


# # =========================================================
# # Utility Functions
# # =========================================================

# def normalize_text(text: str) -> str:
#     return text.strip()


# def split_sentences(text: str):
#     """
#     Split text safely into sentences
#     """
#     sentences = re.split(r'(?<=[.!?])\s+', text)
#     return [s.strip() for s in sentences if s.strip()]


# # =========================================================
# # Section Structuring
# # =========================================================

# def structure_text(text: str):

#     structured = {
#         "General": [],
#         "Recent Labs": [],
#         "Current Medications": [],
#         "Assessment": [],
#         "Plan": []
#     }

#     current_section = "General"

#     for line in text.split("\n"):

#         line = line.strip()
#         if not line:
#             continue

#         lower = line.lower()

#         if "recent lab" in lower:
#             current_section = "Recent Labs"
#             continue

#         if "current medication" in lower:
#             current_section = "Current Medications"
#             continue

#         if "assessment" in lower:
#             current_section = "Assessment"
#             continue

#         if "plan" in lower:
#             current_section = "Plan"
#             continue

#         structured[current_section].append(line)

#     return structured


# # =========================================================
# # Translation Logic
# # =========================================================

# def get_translation_model(target_lang: str):

#     if target_lang == "si":
#         return si_tokenizer, si_model

#     if target_lang == "ta":
#         return ta_tokenizer, ta_model

#     raise HTTPException(
#         status_code=400,
#         detail="Unsupported language"
#     )


# def translate_sentence(sentence: str, target_lang: str):

#     tokenizer, model = get_translation_model(target_lang)

#     inputs = tokenizer(
#         sentence,
#         return_tensors="pt",
#         truncation=True,
#         max_length=256
#     ).to(DEVICE)

#     with torch.no_grad():

#         outputs = model.generate(
#             **inputs,
#             num_beams=5,
#             max_length=256,
#             early_stopping=True
#         )

#     return tokenizer.decode(outputs[0], skip_special_tokens=True)


# def translate_text(text: str, target_lang: str):

#     sentences = split_sentences(text)

#     translated = [
#         translate_sentence(sentence, target_lang)
#         for sentence in sentences
#     ]

#     return " ".join(translated)


# # =========================================================
# # Summarization Logic
# # =========================================================

# def summarize_text(text: str, summary_type: str):

#     if summary_type not in ["patient", "medical"]:
#         raise HTTPException(
#             status_code=400,
#             detail="summary_type must be 'patient' or 'medical'"
#         )

#     if len(text.split()) < 40:
#         return text

#     prompt = f"{summary_type}: {text}"

#     inputs = t5_tokenizer(
#         prompt,
#         return_tensors="pt",
#         truncation=True,
#         max_length=512
#     ).to(DEVICE)

#     with torch.no_grad():

#         outputs = t5_model.generate(
#             **inputs,
#             max_length=180,
#             num_beams=4,
#             early_stopping=True
#         )

#     return t5_tokenizer.decode(outputs[0], skip_special_tokens=True)


# # =========================================================
# # API Routes
# # =========================================================

# @app.get("/")
# def root():
#     return {"status": "Medical Translation API running"}


# # =========================================================
# # Translation Endpoint
# # =========================================================

# @app.post("/translate")
# def translate_endpoint(req: TranslateRequest):

#     text = normalize_text(req.text)

#     # ------------------------------
#     # Case 1 : Summarization Enabled
#     # ------------------------------

#     if req.summarize:

#         summarized = summarize_text(
#             text,
#             req.summary_type
#         )

#         translated = translate_text(
#             summarized,
#             req.target_lang
#         )

#         return {"translated_output": translated}

#     # ------------------------------
#     # Case 2 : Structured Translation
#     # ------------------------------

#     structured = structure_text(text)

#     translated_sections = {}

#     for section, content in structured.items():

#         joined_text = "\n".join(content).strip()

#         if not joined_text:
#             translated_sections[section] = ""
#             continue

#         translated_sections[section] = translate_text(
#             joined_text,
#             req.target_lang
#         )

#     return {"translated_output": translated_sections}


# # =========================================================
# # Text-to-Speech Endpoint
# # =========================================================

# @app.post("/tts")
# def text_to_speech(req: TTSRequest):

#     if not req.text.strip():
#         raise HTTPException(
#             status_code=400,
#             detail="Empty text"
#         )

#     if req.target_lang not in ["si", "ta"]:
#         raise HTTPException(
#             status_code=400,
#             detail="Unsupported language"
#         )

#     try:

#         mp3_buffer = io.BytesIO()

#         tts = gTTS(
#             text=req.text,
#             lang=req.target_lang
#         )

#         tts.write_to_fp(mp3_buffer)
#         mp3_buffer.seek(0)

#         return StreamingResponse(
#             mp3_buffer,
#             media_type="audio/mpeg"
#         )

#     except Exception as e:

#         raise HTTPException(
#             status_code=500,
#             detail=str(e)
#         )
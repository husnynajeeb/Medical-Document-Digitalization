from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from transformers import MarianMTModel, MarianTokenizer, pipeline
from typing import Optional
import torch
import re
import io
from gtts import gTTS

# -------------------------
# App Initialization
# -------------------------
app = FastAPI(title="Medical Translation & Summarization API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# -------------------------
# Load Translation Models (FINETUNED)
# -------------------------
print("Loading translation models...")

si_model_path = "./en_si_finetuned"
ta_model_path = "./en_ta_finetuned"

si_tokenizer = MarianTokenizer.from_pretrained(si_model_path)
si_model = MarianMTModel.from_pretrained(si_model_path).to(DEVICE)

ta_tokenizer = MarianTokenizer.from_pretrained(ta_model_path)
ta_model = MarianMTModel.from_pretrained(ta_model_path).to(DEVICE)

print("Translation models loaded.")

# -------------------------
# Load Summarization Models (ENGLISH ONLY)
# -------------------------
print("Loading summarization models...")

try:
    distilbart_pipeline = pipeline(
        "summarization",
        model="sshleifer/distilbart-cnn-12-6",
        device=0 if DEVICE == "cuda" else -1
    )
    print("DistilBART loaded.")
except Exception as e:
    distilbart_pipeline = None
    print("DistilBART unavailable:", e)

try:
    pegasus_pipeline = pipeline(
        "summarization",
        model="google/pegasus-pubmed",
        device=0 if DEVICE == "cuda" else -1
    )
    print("PEGASUS-PubMed loaded.")
except Exception as e:
    pegasus_pipeline = None
    print("PEGASUS-PubMed unavailable:", e)

# -------------------------
# Request Schemas
# -------------------------
class TranslateRequest(BaseModel):
    text: str
    target_lang: str            # "si" or "ta"
    summarize: Optional[bool] = False
    summary_type: Optional[str] = "patient"  # patient / medical

class TTSRequest(BaseModel):
    text: str
    target_lang: str            # "si" or "ta"

# -------------------------
# Utility Functions
# -------------------------
def normalize_text(text: str) -> str:
    text = text.strip()
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text

def split_sentences(text: str):
    return re.split(r'(?<=[.!?])\s+', text)

# -------------------------
# Translation Logic
# -------------------------
def translate_sentence(sentence: str, target_lang: str) -> str:
    if target_lang == "si":
        tokenizer = si_tokenizer
        model = si_model
    elif target_lang == "ta":
        tokenizer = ta_tokenizer
        model = ta_model
    else:
        raise HTTPException(status_code=400, detail="Unsupported language")

    inputs = tokenizer(
        sentence,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=128
    ).to(DEVICE)

    outputs = model.generate(
        **inputs,
        num_beams=5,
        max_length=128,
        early_stopping=True
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def translate_text(text: str, target_lang: str) -> str:
    sentences = split_sentences(text)
    translated = [
        translate_sentence(s, target_lang)
        for s in sentences if s.strip()
    ]
    return " ".join(translated)

# -------------------------
# Summarization Logic (ENGLISH ONLY)
# -------------------------
def summarize_text(text: str, summary_type: str) -> str:
    if len(text.split()) < 40:
        return text  # too short → skip

    try:
        if summary_type == "medical" and pegasus_pipeline:
            result = pegasus_pipeline(
                text,
                max_length=150,
                min_length=50,
                do_sample=False
            )
            return result[0]["summary_text"]

        if summary_type == "patient" and distilbart_pipeline:
            result = distilbart_pipeline(
                text,
                max_length=130,
                min_length=40,
                do_sample=False
            )
            return result[0]["summary_text"]

        return text

    except Exception as e:
        print("Summarization error:", e)
        return text

# -------------------------
# API Routes
# -------------------------
@app.get("/")
def root():
    return {
        "status": "running",
        "message": "Medical Translator API",
        "endpoints": ["/translate", "/tts", "/docs"]
    }

@app.post("/translate")
def translate_endpoint(req: TranslateRequest):
    text = normalize_text(req.text)
    if req.summarize:
        text = summarize_text(text, req.summary_type)
    translated = translate_text(text, req.target_lang)
    return {"translated_text": translated}

# -------------------------
# Text To Speech (Sinhala / Tamil) using gTTS
# -------------------------
@app.post("/tts")
def text_to_speech(req: TTSRequest):
    text = req.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Empty text")
    if req.target_lang not in ["si", "ta"]:
        raise HTTPException(status_code=400, detail="Unsupported language")

    # Create mp3 in memory
    mp3_fp = io.BytesIO()
    tts = gTTS(text=text, lang=req.target_lang)
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    return StreamingResponse(
        mp3_fp,
        media_type="audio/mpeg",
        headers={"Content-Disposition": "inline; filename=tts.mp3"}
    )

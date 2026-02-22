from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
import shutil
import os
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.features.extraction_interpretation import ocr_ner
from app.features.extraction_interpretation.ocr_ner import (
    ocr_lines,
    extract_tests,
    interpret_tests,
    generate_full_combined_interpretation,
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# Load NER model on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    ocr_ner.load_ner_model()
    yield


app = FastAPI(
    title="Lab Report OCR + Interpretation API",
    lifespan=lifespan
)

# Allow frontend to access backend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload")
async def upload_reports(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")

    all_extracted = []
    saved_files = []

    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        saved_files.append(file.filename)

        lines = ocr_lines(file_path)
        extracted = extract_tests(lines)
        all_extracted.append(extracted)

    interpreted = interpret_tests(all_extracted)

    combined_json = generate_full_combined_interpretation(
        interpreted,
        saved_files
    )

    return combined_json


@app.get("/")
def home():
    return {"message": "API running"}

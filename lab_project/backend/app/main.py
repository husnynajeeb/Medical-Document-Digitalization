# backend/app/main.py
from fastapi import FastAPI, UploadFile, File
import shutil
import os
import json

from .ocr_ner import ocr_lines, extract_tests, interpret_tests

app = FastAPI(title="Lab Report OCR + Interpretation API")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload_report/")
async def upload_report(file: UploadFile = File(...)):
    # Save uploaded file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Process OCR & extract
    lines = ocr_lines(file_path)
    extracted = extract_tests(lines)
    interpreted = interpret_tests(extracted)

    return {"filename": file.filename, "results": interpreted}

@app.get("/")
def home():
    return {"message": "Welcome to the Lab Report OCR API. Use /upload_report/ to upload a report."}

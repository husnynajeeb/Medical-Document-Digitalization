from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import shutil, os

from .ocr_ner import (
    extract_tests_with_model,
    ocr_lines,
    extract_tests,
    interpret_tests,
    generate_full_combined_interpretation
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()

@router.post("/upload")
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

        # 1️⃣ NER extraction
        try:
            extracted_ner = extract_tests_with_model(lines)
        except RuntimeError:
            extracted_ner = []

        # 2️⃣ Strict alias extraction
        extracted_strict = extract_tests(lines)

        # Merge without duplicates
        seen_tests = set()
        combined_extracted = []
        for e in extracted_ner + extracted_strict:
            if e['test'] not in seen_tests:
                combined_extracted.append(e)
                seen_tests.add(e['test'])

        all_extracted.append(combined_extracted)

    interpreted = interpret_tests(all_extracted)
    combined_json = generate_full_combined_interpretation(interpreted, saved_files)

    return combined_json
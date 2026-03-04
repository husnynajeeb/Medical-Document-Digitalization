from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
import shutil
import os
from datetime import datetime

from utils.dependencies import get_current_user
from database import reports_collection

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
async def upload_reports(
    files: List[UploadFile] = File(...),
    current_user: dict = Depends(get_current_user)
):
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

        try:
            extracted_ner = extract_tests_with_model(lines)
        except RuntimeError:
            extracted_ner = []

        extracted_strict = extract_tests(lines)

        seen = set()
        combined = []

        for e in extracted_ner + extracted_strict:
            if e["test"] not in seen:
                combined.append(e)
                seen.add(e["test"])

        all_extracted.append(combined)

    interpreted = interpret_tests(all_extracted)
    combined_json = generate_full_combined_interpretation(interpreted, saved_files)

    await reports_collection.insert_one({
        "user_id": current_user["_id"],
        "filenames": saved_files,
        "results": interpreted,
        "combined_interpretation": combined_json.get("combined_interpretation", []),
        "created_at": datetime.utcnow()
    })

    return combined_json


@router.get("/my-reports")
async def get_my_reports(current_user: dict = Depends(get_current_user)):
    cursor = reports_collection.find({"user_id": current_user["_id"]}).sort("created_at", -1)
    reports = []
    async for r in cursor:
        r["_id"] = str(r["_id"])
        r["user_id"] = str(r["user_id"])  # Convert user_id to string
        reports.append(r)
    return reports
import base64
import io
import re

import cv2
import numpy as np
from PIL import Image
import pytesseract


# ===================================================
# TESSERACT PATH - WINDOWS
# ===================================================
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# ===================================================
# IMAGE PREPROCESSING FOR OCR
# ===================================================
def preprocess_image(image: Image.Image):
    img = np.array(image.convert("RGB"))

    # RGB to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Upscale small text
    gray = cv2.resize(
        gray,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    # Denoise
    denoised = cv2.fastNlMeansDenoising(gray, h=30)

    # Sharpen
    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])

    sharpened = cv2.filter2D(denoised, -1, kernel)

    # Adaptive threshold
    thresholded = cv2.adaptiveThreshold(
        sharpened,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11
    )

    return thresholded


# ===================================================
# CLEAN OCR TEXT
# ===================================================
def clean_ocr_text(text: str) -> str:
    if not text:
        return ""

    # Remove strange characters but keep medical symbols
    text = re.sub(r"[^A-Za-z0-9\s:/%.\-()]", " ", text)

    # Fix common unit spacing
    text = text.replace("mg / dL", "mg/dL")
    text = text.replace("mg/ dL", "mg/dL")
    text = text.replace("mg /dl", "mg/dL")
    text = text.replace("mg/dl", "mg/dL")
    text = text.replace("MG/DL", "mg/dL")

    # Fix BP format
    text = re.sub(r"(\d{2,3})\s*/\s*(\d{2,3})", r"\1/\2", text)

    # Fix decimal spaces only around dot
    text = re.sub(r"(\d)\s*\.\s*(\d)", r"\1.\2", text)

    # Normalize spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ===================================================
# OCR FUNCTION
# ===================================================
def extract_text_from_image(image_base64: str) -> str:
    try:
        if not image_base64:
            return ""

        # Remove base64 header if exists
        image_base64 = re.sub(r"^data:image/.+;base64,", "", image_base64)

        image_data = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_data))

        processed_image = preprocess_image(image)

        custom_config = r"--oem 3 --psm 6"

        raw_text = pytesseract.image_to_string(
            processed_image,
            lang="eng",
            config=custom_config
        )

        print("🧪 RAW OCR OUTPUT:", raw_text)

        cleaned_text = clean_ocr_text(raw_text)

        return cleaned_text

    except Exception as e:
        print("❌ OCR SERVICE ERROR:", str(e))
        return ""
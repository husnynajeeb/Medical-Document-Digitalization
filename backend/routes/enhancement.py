"""
Image Enhancement routes — IT22348098
======================================
All /api/enhance* endpoints for the U-Net-based medical report
deblurring and denoising feature.

Teammates: add your own route files alongside this one in routes/.
"""

import time
from pathlib import Path
from typing import List

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.features.medical_report_enhancement import ModelEnhancer
from utils.image_utils import image_to_base64, read_image_from_bytes

print("✅ enhancement router file loaded")

router = APIRouter(prefix="/api", tags=["enhancement"])

# Resolve model path: backend/routes/ → backend/models/medical_report_enhancement/
_MODEL_PATH = (
    Path(__file__).parent.parent
    / "models"
    / "medical_report_enhancement"
    / "best_model.keras"
)

# Lazy-loaded model instance.  `load_enhancer()` is called once during
# application startup (registered in app/main.py), so importing this module
# does NOT trigger model loading (helpful for testing or when disabled).
enhancer: "ModelEnhancer | None" = None

def load_enhancer() -> None:
    global enhancer
    print("🚀 load_enhancer called")
    print("MODEL PATH:", _MODEL_PATH)
    enhancer = ModelEnhancer(str(_MODEL_PATH))



def _get_enhancer() -> ModelEnhancer:
    if enhancer is None:
        raise HTTPException(503, "Enhancement model is not loaded yet")
    return enhancer


@router.get("/health")
async def health():
    """Return backend status and model-load information."""
    active = enhancer
    return {
        "status": "ok",
        "model_loaded": active.is_loaded if active is not None else False,
        "model_params": active.param_count if active is not None else 0,
    }


@router.post("/enhance")
async def enhance_single(file: UploadFile = File(...)):
    """Enhance a single document image and return base64-encoded result."""
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(400, "File must be an image")

        contents = await file.read()
        img = read_image_from_bytes(contents)

        start = time.time()
        enhanced, psnr_val, ssim_val = _get_enhancer().enhance(img)
        elapsed = time.time() - start

        return {
            "filename": file.filename,
            "original_image": image_to_base64(img),
            "enhanced_image": image_to_base64(enhanced),
            "psnr": round(psnr_val, 2) if psnr_val is not None else None,
            "ssim": round(ssim_val, 4) if ssim_val is not None else None,
            "processing_time": round(elapsed, 2),
            "original_size": list(img.shape[:2]),
            "status": "success",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Enhancement failed: {str(e)}")


@router.post("/enhance/batch")
async def enhance_batch(files: List[UploadFile] = File(...)):
    """Enhance multiple document images in one request."""
    results = []
    for file in files:
        try:
            contents = await file.read()
            img = read_image_from_bytes(contents)

            start = time.time()
            enhanced, psnr_val, ssim_val = _get_enhancer().enhance(img)
            elapsed = time.time() - start

            results.append(
                {
                    "filename": file.filename,
                    "original_image": image_to_base64(img),
                    "enhanced_image": image_to_base64(enhanced),
                    "psnr": round(psnr_val, 2) if psnr_val is not None else None,
                    "ssim": round(ssim_val, 4) if ssim_val is not None else None,
                    "processing_time": round(elapsed, 2),
                    "status": "success",
                }
            )
        except HTTPException:
            raise
        except Exception as e:
            results.append(
                {
                    "filename": file.filename,
                    "status": "error",
                    "error": str(e),
                }
            )

    return {"results": results, "total": len(results)}

"""
Medical Document Processing Backend - Main Application
File: backend/app.py
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from datetime import datetime
import numpy as np
import cv2
import torch


from models import UNet, load_model
from utils import (
    enhance_image, perform_ocr, correct_medical_text, 
    create_corrected_image, enhance_medical_terms
)
from config import config
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Medical Document Processor API",
    description="AI-Powered Document Enhancement, OCR & Language Correction",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model storage
model = None
grammar_corrector = None
tokenizer = None

# ============================================================================
# CONFIGURATION - Toggle features here
# ============================================================================
USE_IMAGE_ENHANCEMENT = True   # Set to False to disable U-Net enhancement
USE_OCR_PROCESSING = False     # Set to False to disable OCR until enhancement is better

# ============================================================================
# RESPONSE MODELS
# ============================================================================

class ProcessResponse(BaseModel):
    success: bool
    message: str
    original_text: Optional[str] = None
    corrected_text: Optional[str] = None
    enhanced_image_path: Optional[str] = None
    corrected_image_path: Optional[str] = None
    ocr_confidence: Optional[float] = None
    processing_time: Optional[float] = None

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    grammar_model_loaded: bool
    device: str
    enhancement_enabled: bool
    ocr_enabled: bool

# ============================================================================
# STARTUP EVENT
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Load models on startup"""
    global model, grammar_corrector, tokenizer
    
    print("🚀 Starting Medical Document Processor...")
    
    # Create necessary directories
    config.UPLOAD_DIR.mkdir(exist_ok=True)
    config.ENHANCED_DIR.mkdir(exist_ok=True)
    config.CORRECTED_DIR.mkdir(exist_ok=True)
    
    # Load U-Net model only if enhancement is enabled
    if USE_IMAGE_ENHANCEMENT:
        try:
            model = load_model(config.MODEL_PATH, config.DEVICE)
            print("✓ U-Net model loaded successfully")
        except Exception as e:
            print(f"⚠ Warning: Could not load U-Net model: {e}")
            model = None
    else:
        print("ℹ Image enhancement disabled - skipping U-Net model")
        model = None
    
    # Load grammar correction model only if OCR is enabled
    if USE_OCR_PROCESSING:
        try:
            from transformers import pipeline
            grammar_corrector = pipeline(
                "text2text-generation",
                model="prithivida/grammar_error_correcter_v1"
            )
            tokenizer = None  # Not needed with pipeline
            print("✓ Grammar correction model loaded successfully")
        except Exception as e:
            print(f"⚠ Warning: Could not load grammar model: {e}")
            grammar_corrector = None
            tokenizer = None
    else:
        print("ℹ OCR processing disabled - skipping grammar model")
        grammar_corrector = None
        tokenizer = None
    
    print("✨ Server ready!")

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/", tags=["General"])
async def root():
    """Root endpoint"""
    return {
        "message": "Medical Document Processing API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health_check():
    """Check API health and model status"""
    return HealthResponse(
        status="healthy",
        model_loaded=model is not None,
        grammar_model_loaded=grammar_corrector is not None,
        device=str(config.DEVICE),
        enhancement_enabled=USE_IMAGE_ENHANCEMENT,
        ocr_enabled=USE_OCR_PROCESSING
    )

@app.post("/process", response_model=ProcessResponse, tags=["Processing"])
async def process_document(file: UploadFile = File(...)):
    """
    Process medical document through complete pipeline:
    1. Image Enhancement (U-Net) - OPTIONAL
    2. OCR (Tesseract) - OPTIONAL
    3. Language Correction (T5) - OPTIONAL
    4. Generate Corrected Image - OPTIONAL
    
    Returns: Enhanced image only when OCR is disabled
    """
    start_time = datetime.now()
    
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read uploaded file
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"doc_{timestamp}"
        
        # Step 1: Enhance image (or skip if disabled)
        print(f"📄 Processing: {file.filename}")
        
        if USE_IMAGE_ENHANCEMENT and model is not None:
            print("  ➤ Enhancing image...")
            enhanced_img = enhance_image(img, model, config.DEVICE, config.IMG_SIZE)
        else:
            print("  ➤ Using original image (enhancement disabled)...")
            enhanced_img = img.copy()
        
        enhanced_path = config.ENHANCED_DIR / f"{base_name}_enhanced.png"
        cv2.imwrite(str(enhanced_path), cv2.cvtColor(enhanced_img, cv2.COLOR_RGB2BGR))
        
        # If OCR is disabled, return just the enhanced image
        if not USE_OCR_PROCESSING:
            processing_time = (datetime.now() - start_time).total_seconds()
            print(f"  ✓ Enhancement complete! OCR skipped. ({processing_time:.2f}s)")
            
            return ProcessResponse(
                success=True,
                message="Image enhanced successfully (OCR disabled)",
                original_text=None,
                corrected_text=None,
                enhanced_image_path=f"enhanced/{enhanced_path.name}",
                corrected_image_path=None,
                ocr_confidence=None,
                processing_time=processing_time
            )
        
        # Step 2: Perform OCR (only if enabled)
        print("  ➤ Performing OCR...")
        ocr_data = perform_ocr(enhanced_img)
        original_text = ocr_data['full_text']
        
        # Calculate average confidence
        avg_confidence = np.mean([
            block['confidence'] for block in ocr_data['text_blocks']
        ]) if ocr_data['text_blocks'] else 0
        
        # Step 3: Correct language
        print("  ➤ Correcting text...")
        corrected_text = correct_medical_text(
            original_text, grammar_corrector, tokenizer
        )
        corrected_text = enhance_medical_terms(corrected_text)
        
        # Step 4: Create corrected image
        print("  ➤ Creating corrected image...")
        corrected_img = create_corrected_image(enhanced_img, ocr_data, corrected_text)
        corrected_path = config.CORRECTED_DIR / f"{base_name}_corrected.png"
        cv2.imwrite(str(corrected_path), cv2.cvtColor(corrected_img, cv2.COLOR_RGB2BGR))
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        
        print(f"  ✓ Complete! ({processing_time:.2f}s)")
        
        return ProcessResponse(
            success=True,
            message="Document processed successfully",
            original_text=original_text,
            corrected_text=corrected_text,
            enhanced_image_path=f"enhanced/{enhanced_path.name}",
            corrected_image_path=f"corrected/{corrected_path.name}",
            ocr_confidence=float(avg_confidence),
            processing_time=processing_time
        )
        
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@app.get("/download/{file_type}/{filename}", tags=["Download"])
async def download_file(file_type: str, filename: str):
    """
    Download processed files
    
    Args:
        file_type: 'enhanced' or 'corrected'
        filename: Name of the file to download
    """
    if file_type == "enhanced":
        file_path = config.ENHANCED_DIR / filename
    elif file_type == "corrected":
        file_path = config.CORRECTED_DIR / filename
    else:
        raise HTTPException(status_code=400, detail="Invalid file type. Use 'enhanced' or 'corrected'")
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        file_path,
        media_type='image/png',
        filename=filename
    )

@app.delete("/cleanup", tags=["Maintenance"])
async def cleanup_files():
    """Clean up old processed files (optional maintenance endpoint)"""
    try:
        import shutil
        for directory in [config.UPLOAD_DIR, config.ENHANCED_DIR, config.CORRECTED_DIR]:
            if directory.exists():
                for file in directory.glob('*'):
                    file.unlink()
        return {"message": "Cleanup completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cleanup error: {str(e)}")

# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=config.HOST,
        port=config.PORT,
        log_level="info"
    )
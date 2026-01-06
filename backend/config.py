"""
Configuration Settings
File: backend/config.py
"""

import torch
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application Configuration"""
    
    # Server Settings
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    
    # Model Settings
    MODEL_PATH = Path(os.getenv("MODEL_PATH", "trained_models/unet_document_enhancer.pth"))
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    IMG_SIZE = int(os.getenv("IMG_SIZE", 512))
    
    # Directory Settings
    BASE_DIR = Path(__file__).parent
    UPLOAD_DIR = BASE_DIR / "uploads"
    ENHANCED_DIR = BASE_DIR / "enhanced"
    CORRECTED_DIR = BASE_DIR / "corrected"
    TRAINED_MODELS_DIR = BASE_DIR / "trained_models"
    
    # OCR Settings
    TESSERACT_CMD = os.getenv("TESSERACT_CMD", None)  # Set if tesseract not in PATH
    OCR_CONFIDENCE_THRESHOLD = float(os.getenv("OCR_CONFIDENCE_THRESHOLD", 30))
    
    # Processing Settings
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 10 * 1024 * 1024))  # 10MB default
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff'}
    
    # Grammar Correction Model
    GRAMMAR_MODEL = os.getenv("GRAMMAR_MODEL", "flexudy/t5-small-wav2vec2-grammar-fixer")
    
    # CORS Settings
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = BASE_DIR / "app.log"
    
    # Performance
    USE_GPU = torch.cuda.is_available()
    NUM_WORKERS = int(os.getenv("NUM_WORKERS", 2))
    
    @classmethod
    def display_config(cls):
        """Display current configuration"""
        print("\n" + "="*60)
        print("CONFIGURATION")
        print("="*60)
        print(f"Host: {cls.HOST}:{cls.PORT}")
        print(f"Device: {cls.DEVICE}")
        print(f"Model Path: {cls.MODEL_PATH}")
        print(f"Image Size: {cls.IMG_SIZE}")
        print(f"GPU Available: {cls.USE_GPU}")
        print(f"Upload Dir: {cls.UPLOAD_DIR}")
        print(f"Enhanced Dir: {cls.ENHANCED_DIR}")
        print(f"Corrected Dir: {cls.CORRECTED_DIR}")
        print("="*60 + "\n")

# Create global config instance
config = Config()

# Set tesseract path if specified
if config.TESSERACT_CMD:
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_CMD
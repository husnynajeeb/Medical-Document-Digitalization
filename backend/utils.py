"""
Utility Functions for Document Processing
File: backend/utils.py
"""

import cv2
import numpy as np
import torch
import pytesseract
from PIL import Image, ImageDraw, ImageFont
import re

# ============================================================================
# IMAGE PROCESSING
# ============================================================================

def preprocess_image(image_array, size=512):
    """
    Preprocess image for model input
    
    Args:
        image_array: RGB image as numpy array
        size: Target size for model
    
    Returns:
        Preprocessed tensor
    """
    img = cv2.resize(image_array, (size, size))
    img = img.astype(np.float32) / 255.0
    
    # Normalize using ImageNet stats
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    img = (img - mean) / std
    
    # Convert to tensor (C, H, W)
    img = torch.from_numpy(img.transpose(2, 0, 1)).float()
    return img.unsqueeze(0)

def postprocess_image(tensor, original_size):
    """
    Convert model output back to image
    
    Args:
        tensor: Model output tensor
        original_size: Tuple of (height, width) for resizing
    
    Returns:
        RGB image as numpy array
    """
    # Denormalize
    mean = torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1)
    std = torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1)
    
    img = tensor * std + mean
    img = torch.clamp(img, 0, 1)
    
    # Convert to numpy
    img = img.squeeze(0).cpu().numpy()
    img = np.transpose(img, (1, 2, 0))
    img = (img * 255).astype(np.uint8)
    
    # Resize back to original
    img = cv2.resize(img, (original_size[1], original_size[0]))
    return img

def enhance_image(image_array, model, device, img_size=512):
    """
    Enhance image using U-Net model
    
    Args:
        image_array: Input image as numpy array
        model: Loaded U-Net model
        device: torch device
        img_size: Size for model processing
    
    Returns:
        Enhanced image as numpy array
    """
    if model is None:
        return image_array  # Return original if model not loaded
    
    original_size = image_array.shape[:2]
    
    # Preprocess
    input_tensor = preprocess_image(image_array, img_size).to(device)
    
    # Predict
    with torch.no_grad():
        output = model(input_tensor)
    
    # Postprocess
    enhanced = postprocess_image(output, original_size)
    return enhanced

# ============================================================================
# OCR FUNCTIONS
# ============================================================================

def perform_ocr(image_array):
    """
    Extract text from image using Tesseract OCR
    
    Args:
        image_array: RGB image as numpy array
    
    Returns:
        Dictionary with full_text and text_blocks
    """
    # Convert to grayscale for better OCR
    gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
    
    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    
    # OCR with detailed data
    data = pytesseract.image_to_data(thresh, output_type=pytesseract.Output.DICT)
    
    # Extract text and bounding boxes
    text_blocks = []
    full_text = []
    
    n_boxes = len(data['text'])
    for i in range(n_boxes):
        if int(data['conf'][i]) > 30:  # Confidence threshold
            text = data['text'][i].strip()
            if text:
                text_blocks.append({
                    'text': text,
                    'confidence': float(data['conf'][i]),
                    'bbox': {
                        'x': int(data['left'][i]),
                        'y': int(data['top'][i]),
                        'width': int(data['width'][i]),
                        'height': int(data['height'][i])
                    }
                })
                full_text.append(text)
    
    return {
        'full_text': ' '.join(full_text),
        'text_blocks': text_blocks
    }

# ============================================================================
# LANGUAGE CORRECTION
# ============================================================================

def correct_medical_text(text, grammar_corrector, tokenizer=None):
    """
    Correct grammar and spelling in medical text
    
    Args:
        text: Input text to correct
        grammar_corrector: Grammar correction pipeline
        tokenizer: Not used with pipeline
    
    Returns:
        Corrected text
    """
    if not text or grammar_corrector is None:
        return text
    
    # Split into sentences for better processing
    sentences = re.split(r'(?<=[.!?])\s+', text)
    corrected_sentences = []
    
    for sentence in sentences:
        if len(sentence.strip()) < 3:
            corrected_sentences.append(sentence)
            continue
        
        try:
            # Use pipeline for correction
            result = grammar_corrector(sentence, max_length=512)
            corrected = result[0]['generated_text']
            corrected_sentences.append(corrected)
        except Exception as e:
            print(f"Warning: Could not correct sentence: {e}")
            corrected_sentences.append(sentence)
    
    return ' '.join(corrected_sentences)

def enhance_medical_terms(text):
    """
    Fix common medical term OCR errors
    
    Args:
        text: Input text
    
    Returns:
        Text with corrected medical terms
    """
    # Common OCR mistakes in medical documents
    corrections = {
        r'\bpatient\b': 'patient',
        r'\bdiagnosis\b': 'diagnosis',
        r'\bprescription\b': 'prescription',
        r'\bmedicine\b': 'medicine',
        r'\bmedication\b': 'medication',
        r'\btreatment\b': 'treatment',
        r'\bdosage\b': 'dosage',
        r'\bsymptoms\b': 'symptoms',
        r'\bdoctor\b': 'doctor',
        r'\bhospital\b': 'hospital',
        r'\btherapy\b': 'therapy',
        r'\bexamination\b': 'examination',
        r'\ballergy\b': 'allergy',
        r'\bblood pressure\b': 'blood pressure',
        r'\btemperature\b': 'temperature',
        # Add more medical terms as needed
    }
    
    corrected = text
    for pattern, replacement in corrections.items():
        corrected = re.sub(pattern, replacement, corrected, flags=re.IGNORECASE)
    
    return corrected

# ============================================================================
# IMAGE GENERATION
# ============================================================================

def create_corrected_image(original_image, ocr_data, corrected_text):
    """
    Create new image with corrected text overlaid
    
    Args:
        original_image: Original RGB image as numpy array
        ocr_data: OCR data with bounding boxes
        corrected_text: Corrected text string
    
    Returns:
        New image with corrected text as numpy array
    """
    # Convert to PIL Image
    img = Image.fromarray(original_image)
    draw = ImageDraw.Draw(img)
    
    # Try to load a font
    try:
        # Try different font paths
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "C:\\Windows\\Fonts\\arial.ttf"
        ]
        font = None
        for font_path in font_paths:
            try:
                font = ImageFont.truetype(font_path, 20)
                break
            except:
                continue
        if font is None:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # Split corrected text into words
    corrected_words = corrected_text.split()
    text_blocks = ocr_data['text_blocks']
    
    # Overlay corrected words at their original positions
    for i, block in enumerate(text_blocks):
        if i < len(corrected_words):
            bbox = block['bbox']
            
            # White out original text
            draw.rectangle(
                [bbox['x'], bbox['y'], 
                 bbox['x'] + bbox['width'], 
                 bbox['y'] + bbox['height']],
                fill='white'
            )
            
            # Draw corrected text
            draw.text(
                (bbox['x'], bbox['y']),
                corrected_words[i],
                fill='black',
                font=font
            )
    
    return np.array(img)

# ============================================================================
# VALIDATION
# ============================================================================

def validate_image(image_array):
    """
    Validate image array
    
    Args:
        image_array: Image as numpy array
    
    Returns:
        Boolean indicating if image is valid
    """
    if image_array is None:
        return False
    if len(image_array.shape) != 3:
        return False
    if image_array.shape[2] != 3:
        return False
    return True
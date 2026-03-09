"""Shared utility helpers for the DocEnhance AI backend."""

import base64

import cv2
import numpy as np


SUPPORTED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/tiff",
    "image/bmp",
    "image/webp",
}

MAX_IMAGE_BYTES = 50 * 1024 * 1024  # 50 MB


def validate_image_content_type(content_type: str) -> bool:
    """Return True if *content_type* is a supported image MIME type."""
    return content_type in SUPPORTED_CONTENT_TYPES or content_type.startswith("image/")


def read_image_from_bytes(image_bytes: bytes) -> np.ndarray:
    """Decode raw bytes into a grayscale NumPy array."""
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Could not decode image")
    return img


def image_to_base64(img: np.ndarray) -> str:
    """Encode a NumPy image array as a base64 PNG string."""
    _, buffer = cv2.imencode(".png", img)
    return base64.b64encode(buffer).decode("utf-8")


def resize_if_too_large(img: np.ndarray, max_side: int = 4096) -> np.ndarray:
    """Downscale *img* so that its longest side is at most *max_side* pixels."""
    h, w = img.shape[:2]
    longest = max(h, w)
    if longest <= max_side:
        return img
    scale = max_side / longest
    new_w = int(w * scale)
    new_h = int(h * scale)
    return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)


def normalize(img: np.ndarray) -> np.ndarray:
    """Normalise a uint8 image to float32 in [0, 1]."""
    return img.astype(np.float32) / 255.0


def denormalize(img: np.ndarray) -> np.ndarray:
    """Convert a float32 image in [0, 1] back to uint8."""
    return np.clip(img * 255, 0, 255).astype(np.uint8)

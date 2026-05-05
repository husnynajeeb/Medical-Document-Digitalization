from pydantic import BaseModel, Field, validator
from typing import Optional, Literal


class TranslateRequest(BaseModel):
    """
    Unified request schema for multilingual processing.
    Supports:
    - image input (OCR)
    - text input
    - prediction input
    """

    # ----------------------------
    # INPUT TYPE
    # ----------------------------
    input_type: Literal["image", "text", "prediction"]

    # ----------------------------
    # INPUT DATA
    # ----------------------------
    text: Optional[str] = Field(default=None, description="Medical text input")

    image_base64: Optional[str] = Field(
        default=None,
        description="Base64 encoded image"
    )

    # ----------------------------
    # OUTPUT SETTINGS
    # ----------------------------
    target_lang: Literal["en", "si", "ta"] = "en"

    summarize: bool = True

    # ----------------------------
    # VALIDATION LOGIC
    # ----------------------------
    @validator("text", always=True)
    def validate_text(cls, v, values):
        if values.get("input_type") == "text" and not v:
            raise ValueError("Text input is required for input_type='text'")
        return v

    @validator("image_base64", always=True)
    def validate_image(cls, v, values):
        if values.get("input_type") == "image" and not v:
            raise ValueError("Image input is required for input_type='image'")
        return v


class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1)
    target_lang: Literal["en", "si", "ta"] = "en"
from pydantic import BaseModel
from typing import Optional

class TranslateRequest(BaseModel):
    text: str
    target_lang: str
    summarize: Optional[bool] = False
    summary_type: Optional[str] = "patient"


class TTSRequest(BaseModel):
    text: str
    target_lang: str
    
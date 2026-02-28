from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.features.extraction_interpretation import ocr_ner
from app.features.extraction_interpretation.router import router as ei_router

# Load NER model on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        ocr_ner.load_ner_model()
    except Exception as e:
        print(f"Warning: NER model could not be loaded: {e}")
    yield

app = FastAPI(title="Lab Report API", lifespan=lifespan)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://127.0.0.1:5173"
    ],  # your frontend dev URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your router with prefix
app.include_router(ei_router, prefix="/extraction-interpretation")

@app.get("/")
def home():
    return {"message": "API running"}
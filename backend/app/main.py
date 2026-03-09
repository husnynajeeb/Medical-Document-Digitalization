from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.features.extraction_interpretation import ocr_ner
from routes.auth_routes import router as auth_router
from app.features.extraction_interpretation.router import router as ei_router
from app.features.diabetes_risk_recommendation.router import router as dr_router  # NEW
from app.features.translation_and_summarization.translate_routes import router as translation_router
# Load NER model on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        ocr_ner.load_ner_model()
        print("NER model loaded successfully")
    except Exception as e:
        print(f"NER load warning: {e}")
    yield


app = FastAPI(title="Lab Report API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(ei_router, prefix="/extraction-interpretation")
app.include_router(dr_router, prefix="/diabetes")  # NEW
app.include_router(translation_router, prefix="/translation")


@app.get("/")
def home():
    return {"message": "API running"}
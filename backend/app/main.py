from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Feature imports
from app.features.extraction_interpretation import ocr_ner
from app.features.extraction_interpretation.router import router as ei_router
from app.features.diabetes_risk_recommendation.router import router as dr_router
from app.features.translation_and_summarization.api.multilingual_routes import router as translation_router

# External routes (keep if required)
from routes.auth_routes import router as auth_router
from routes.enhancement import router as im_router
from routes.enhancement import load_enhancer as load_enhancer_model


# ===================================================
# 🚀 STARTUP INITIALIZATION
# ===================================================
@asynccontextmanager
async def lifespan(app: FastAPI):

    # Load NER model
    try:
        ocr_ner.load_ner_model()
    except Exception:
        pass  # safe fallback

    # Load enhancement model
    try:
        load_enhancer_model()
    except Exception:
        pass

    yield


# ===================================================
# 🌐 FASTAPI APP INIT
# ===================================================
app = FastAPI(
    title="AI Medical Processing API",
    description="Multilingual Medical Document Digitization System",
    version="1.0.0",
    lifespan=lifespan
)


# ===================================================
# 🌍 CORS CONFIG
# ===================================================
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


# ===================================================
# 🔗 ROUTES
# ===================================================
app.include_router(auth_router)
app.include_router(ei_router, prefix="/extraction-interpretation")
app.include_router(dr_router, prefix="/diabetes")  # NEW app.include_router(translation_router, prefix="/translation")
app.include_router(dr_router, prefix="/diabetes")
app.include_router(im_router, prefix="/enhancement")  # NEW

app.include_router(
    ei_router,
    prefix="/extraction-interpretation",
    tags=["Extraction & Interpretation"]
)

app.include_router(
    dr_router,
    prefix="/diabetes",
    tags=["Risk Prediction"]
)

app.include_router(
    translation_router,
    prefix="/multilingual",
    tags=["Multilingual Processing"]
)

app.include_router(
    im_router,
    prefix="/enhancement",
    tags=["Image Enhancement"]
)


# ===================================================
# 🏠 ROOT
# ===================================================
@app.get("/")
def home():
    return {
        "status": "running",
        "message": "AI Medical API is active"
    }
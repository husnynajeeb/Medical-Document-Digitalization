from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from datetime import datetime
import time
from pathlib import Path

from utils.dependencies import get_current_user  # same as extraction router

from .utils import (
    get_risk_assessment,
    generate_personalized_recommendations,
    prepare_features_for_model,
    align_features_with_model,
)
from .model_loader import safe_load_xgboost_model

router = APIRouter(tags=["Diabetes Risk (XGBoost)"])

# Load model once (module import time)
ROOT = Path(__file__).resolve().parents[3]  # backend/
MODEL_PATH = ROOT / "models" / "xgboost" / "best_model.pkl"
model = safe_load_xgboost_model(str(MODEL_PATH)) if MODEL_PATH.exists() else None

EXPECTED_FEATURES = [
    'age', 'hypertension', 'heart_disease', 'bmi', 'HbA1c_level',
    'blood_glucose_level', 'glucose_risk', 'bmi_risk',
    'gender_Male', 'gender_Other', 'smoking_history_current',
    'smoking_history_ever', 'smoking_history_former',
    'smoking_history_never', 'smoking_history_not current',
    'hypoglycemia_risk_score', 'hyperglycemia_risk_score',
    'prediabetes_risk_score', 'cardiovascular_risk_score',
    'kidney_risk_score', 'eye_risk_score', 'neuropathy_risk_score',
    'stroke_risk_score', 'oral_risk_score', 'glycemic_risk_score',
    'total_risk_score'
]

class PatientData(BaseModel):
    age: float = Field(..., gt=0, lt=120)
    gender: str = Field("Male")
    bmi: float = Field(..., gt=10, lt=70)
    HbA1c_level: float = Field(..., gt=3, lt=15)
    blood_glucose_level: float = Field(..., gt=50, lt=400)
    hypertension: int = Field(0, ge=0, le=1)
    heart_disease: int = Field(0, ge=0, le=1)
    smoking_history: str = Field("never")

@router.get("/health")
def health(current_user: dict = Depends(get_current_user)):
    # If user is not logged in, get_current_user should raise HTTPException (401)
    return {
        "status": "healthy" if model is not None else "degraded",
        "timestamp": datetime.now(),
        "model_loaded": model is not None,
        "model_features": len(EXPECTED_FEATURES),
        "user_id": str(current_user.get("_id", "")),
    }

@router.post("/predict")
def predict(
    data: PatientData,
    current_user: dict = Depends(get_current_user),
):
    start = time.time()
    patient_dict = data.model_dump()

    risk_assessment_result = get_risk_assessment(patient_dict)

    probability = 0.5
    prediction = "Unknown"

    if model is not None:
        try:
            features_df = prepare_features_for_model(patient_dict)
            actual_features = getattr(model, "feature_names_in_", EXPECTED_FEATURES)
            features_df = align_features_with_model(features_df, actual_features)

            probabilities = model.predict_proba(features_df)
            probability = float(probabilities[0][1]) if probabilities.shape[1] == 2 else float(probabilities[0][0])
            prediction = "Diabetic" if probability >= 0.5 else "Non-Diabetic"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

    recommendations = generate_personalized_recommendations(
        risk_assessment_result,
        age=data.age,
        bmi=data.bmi,
        gender=data.gender,
        smoking_history=data.smoking_history,
        hypertension=data.hypertension,
        heart_disease=data.heart_disease,
        HbA1c_level=data.HbA1c_level,
        blood_glucose_level=data.blood_glucose_level,
        diabetes_prediction=prediction,
    )[:40]

    return {
        "user_id": str(current_user.get("_id", "")),
        "diabetes_probability": round(probability, 4),
        "diabetes_prediction": prediction,
        "risk_assessment": {
            "overall_risk": risk_assessment_result["overall_risk"],
            "overall_score": risk_assessment_result["overall_score"],
            "risk_counts": risk_assessment_result["risk_counts"],
            "urgency": risk_assessment_result["urgency"],
            "timestamp": risk_assessment_result["timestamp"],
        },
        "risk_breakdown": risk_assessment_result["risk_breakdown"],
        "recommendations": recommendations,
        "processing_time": round(time.time() - start, 3),
    }
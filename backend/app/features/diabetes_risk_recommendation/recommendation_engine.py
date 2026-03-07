"""
AI-assisted recommendation engine:
- Generate many candidate recommendations
- Score + rank them (impact, urgency, feasibility)
- Return top-N personalized recommendations
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import numpy as np


@dataclass
class Recommendation:
    id: str
    title: str
    actions: List[str]
    tags: List[str]               # e.g. ["glycemic", "weight", "cardio"]
    difficulty: int               # 1(easy) - 5(hard)
    time_to_start_days: int       # 0/1/7 etc.
    medical_priority: int         # 1(low) - 5(high)
    applies_if: Dict[str, Tuple[float, float]]  # feature -> (min,max) ranges (simple gating)


# ---- 1) A small library of structured recommendations ----
# You can keep expanding this list over time.
REC_LIBRARY: List[Recommendation] = [
    Recommendation(
        id="check_hba1c_doctor",
        title="Review blood sugar control with a doctor",
        actions=[
            "Book a doctor appointment within 1–2 weeks.",
            "Discuss medication review / dose adjustment.",
            "Repeat HbA1c in ~3 months (or as advised).",
        ],
        tags=["glycemic"],
        difficulty=2,
        time_to_start_days=1,
        medical_priority=5,
        applies_if={"HbA1c_level": (7.0, 20.0)},
    ),
    Recommendation(
        id="daily_glucose_monitoring",
        title="Start a simple glucose monitoring routine",
        actions=[
            "Measure fasting glucose daily for 1 week.",
            "If available, add 2-hour post-meal readings 3 days/week.",
            "Record readings + meals (simple notes).",
        ],
        tags=["glycemic"],
        difficulty=2,
        time_to_start_days=0,
        medical_priority=4,
        applies_if={"blood_glucose_level": (140.0, 500.0)},
    ),
    Recommendation(
        id="weight_loss_plan",
        title="Weight reduction plan (small, sustainable)",
        actions=[
            "Aim for 5–10% weight loss over 3–6 months.",
            "Replace sugary drinks with water.",
            "Use plate method: 1/2 vegetables, 1/4 protein, 1/4 carbs.",
        ],
        tags=["weight", "glycemic"],
        difficulty=3,
        time_to_start_days=0,
        medical_priority=4,
        applies_if={"bmi": (27.0, 100.0)},
    ),
    Recommendation(
        id="bp_control",
        title="Blood pressure control and monitoring",
        actions=[
            "Check BP at least weekly (home or pharmacy).",
            "Reduce salt and processed foods.",
            "Discuss BP targets and medications with your doctor.",
        ],
        tags=["cardio"],
        difficulty=2,
        time_to_start_days=0,
        medical_priority=4,
        applies_if={"hypertension": (1, 1)},
    ),
    Recommendation(
        id="foot_care",
        title="Foot care to reduce nerve/ulcer risk",
        actions=[
            "Daily foot inspection (cuts, blisters, numbness).",
            "Use comfortable footwear; avoid walking barefoot.",
            "Request a foot exam during your next clinic visit.",
        ],
        tags=["neuropathy"],
        difficulty=1,
        time_to_start_days=0,
        medical_priority=3,
        applies_if={"neuropathy_risk_score": (2, 3)},
    ),
    Recommendation(
        id="eye_exam",
        title="Eye screening (retinopathy prevention)",
        actions=[
            "Schedule a dilated eye exam within 1–3 months.",
            "If vision changes occur, seek earlier review.",
        ],
        tags=["eye"],
        difficulty=2,
        time_to_start_days=7,
        medical_priority=4,
        applies_if={"eye_risk_score": (2, 3)},
    ),
    Recommendation(
        id="kidney_screen",
        title="Kidney screening (early detection)",
        actions=[
            "Ask for urine ACR (albumin/creatinine ratio).",
            "Check serum creatinine/eGFR as advised.",
        ],
        tags=["kidney"],
        difficulty=2,
        time_to_start_days=7,
        medical_priority=4,
        applies_if={"kidney_risk_score": (2, 3)},
    ),
    Recommendation(
        id="physical_activity",
        title="Physical activity plan (starter)",
        actions=[
            "Start with 20–30 minutes brisk walking, 5 days/week.",
            "Add light strength training 2 days/week if safe.",
        ],
        tags=["activity", "glycemic", "weight"],
        difficulty=3,
        time_to_start_days=0,
        medical_priority=3,
        applies_if={"age": (18, 120)},
    ),
]


def _passes_gating(rec: Recommendation, features: Dict[str, float]) -> bool:
    for k, (mn, mx) in rec.applies_if.items():
        if k not in features:
            continue
        v = features[k]
        if v < mn or v > mx:
            return False
    return True


def _estimate_impact(rec: Recommendation, risk_assessment: dict) -> float:
    """
    Data-driven-ish heuristic: if the patient has high/medium risks in rec.tags,
    impact score increases. (Later you can replace with SHAP-driven attribution.)
    """
    tag_to_riskkey = {
        "glycemic": ["glycemic_risk_score", "hyperglycemia_risk_score", "prediabetes_risk_score"],
        "weight": ["bmi_risk"],
        "cardio": ["cardiovascular_risk_score", "stroke_risk_score"],
        "kidney": ["kidney_risk_score"],
        "eye": ["eye_risk_score"],
        "neuropathy": ["neuropathy_risk_score"],
    }

    scores = risk_assessment.get("raw_scores", {})  # we'll pass this in
    impact = 0.0
    for t in rec.tags:
        keys = tag_to_riskkey.get(t, [])
        for k in keys:
            impact += float(scores.get(k, 0))

    # normalize a bit
    return impact / 6.0


def rank_recommendations(
    features: Dict[str, float],
    risk_assessment: dict,
    top_n: int = 7,
) -> List[dict]:
    """
    Returns a ranked list of recommendation dicts suitable for API response.
    """
    candidates: List[Tuple[float, Recommendation]] = []

    # add raw scores into risk_assessment so impact estimator can use it
    # (your utils.py already computes these inside calculate_risk_scores;
    # you can pass them here)
    if "raw_scores" not in risk_assessment:
        risk_assessment["raw_scores"] = {}

    for rec in REC_LIBRARY:
        if not _passes_gating(rec, features):
            continue

        impact = _estimate_impact(rec, risk_assessment)
        urgency = rec.medical_priority / 5.0
        feasibility = 1.0 - ((rec.difficulty - 1) / 4.0)  # easy => 1.0

        # final score (tune weights)
        score = (0.55 * impact) + (0.30 * urgency) + (0.15 * feasibility)
        candidates.append((score, rec))

    candidates.sort(key=lambda x: x[0], reverse=True)
    selected = candidates[:top_n]

    return [
        {
            "id": rec.id,
            "title": rec.title,
            "actions": rec.actions,
            "tags": rec.tags,
            "difficulty": rec.difficulty,
            "start_in_days": rec.time_to_start_days,
            "score": round(score, 3),
        }
        for score, rec in selected
    ]
"""
Utility functions for diabetes risk assessment (PERSONALIZED + PRIORITIZED)

Works with ONLY your existing input fields:
- age, gender, bmi, HbA1c_level, blood_glucose_level, hypertension, heart_disease, smoking_history

Key features:
- Same risk scoring + breakdown you already use
- Personalized recommendations that clearly say what to do first:
  ✅ DO FIRST (Urgent) / 📅 DO NEXT (Soon) / 🌱 CONTINUE (Routine) / 💡 OPTIONAL
- BMI obesity classes so BMI 32 vs 42 produces different recommendations
- Stage-correct wording: avoids "Diabetes Prevention" when model says Diabetic
"""

from datetime import datetime
import pandas as pd

# ======================================================================
# RISK CALCULATION
# ======================================================================

def calculate_risk_scores(data):
    scores = {}

    # Hypoglycemia
    if data['blood_glucose_level'] < 50:
        scores['hypoglycemia_risk_score'] = 3
    elif data['blood_glucose_level'] < 60:
        scores['hypoglycemia_risk_score'] = 2
    elif data['blood_glucose_level'] < 70:
        scores['hypoglycemia_risk_score'] = 1
    else:
        scores['hypoglycemia_risk_score'] = 0

    # Hyperglycemia
    if data['blood_glucose_level'] > 250:
        scores['hyperglycemia_risk_score'] = 3
    elif data['blood_glucose_level'] > 180:
        scores['hyperglycemia_risk_score'] = 2
    elif data['blood_glucose_level'] > 140:
        scores['hyperglycemia_risk_score'] = 1
    else:
        scores['hyperglycemia_risk_score'] = 0

    # Prediabetes progression
    if data['blood_glucose_level'] >= 126 or data['HbA1c_level'] > 6.4:
        scores['prediabetes_risk_score'] = 3
    elif (111 <= data['blood_glucose_level'] <= 125) or (5.7 <= data['HbA1c_level'] <= 6.0):
        scores['prediabetes_risk_score'] = 2
    elif 100 <= data['blood_glucose_level'] <= 110:
        scores['prediabetes_risk_score'] = 1
    else:
        scores['prediabetes_risk_score'] = 0

    # Cardiovascular risk
    cardio_score = 0
    if data['age'] > 60:
        cardio_score += 2
    elif data['age'] > 45:
        cardio_score += 1
    if data['hypertension'] == 1:
        cardio_score += 2
    if data['heart_disease'] == 1:
        cardio_score += 3
    if data['HbA1c_level'] > 8:
        cardio_score += 3
    elif data['HbA1c_level'] > 7:
        cardio_score += 2
    elif data['HbA1c_level'] > 6:
        cardio_score += 1

    if cardio_score >= 5:
        scores['cardiovascular_risk_score'] = 3
    elif cardio_score >= 3:
        scores['cardiovascular_risk_score'] = 2
    else:
        scores['cardiovascular_risk_score'] = 1

    # Kidney risk
    kidney_score = 0
    if data['HbA1c_level'] > 8:
        kidney_score += 3
    elif data['HbA1c_level'] > 7:
        kidney_score += 2
    if data['hypertension'] == 1:
        kidney_score += 2
    if data['blood_glucose_level'] > 180:
        kidney_score += 1
    if data['age'] > 60:
        kidney_score += 1

    if kidney_score >= 5:
        scores['kidney_risk_score'] = 3
    elif kidney_score >= 3:
        scores['kidney_risk_score'] = 2
    else:
        scores['kidney_risk_score'] = 1

    # Eye risk
    eye_score = 0
    if data['HbA1c_level'] > 8:
        eye_score += 3
    elif data['HbA1c_level'] > 7:
        eye_score += 2
    elif data['HbA1c_level'] > 6:
        eye_score += 1
    if data['blood_glucose_level'] > 200:
        eye_score += 2
    if data['hypertension'] == 1:
        eye_score += 2

    if eye_score >= 5:
        scores['eye_risk_score'] = 3
    elif eye_score >= 3:
        scores['eye_risk_score'] = 2
    else:
        scores['eye_risk_score'] = 1

    # Neuropathy risk
    nerve_score = 0
    if data['HbA1c_level'] > 8:
        nerve_score += 3
    elif data['HbA1c_level'] > 7:
        nerve_score += 2
    if data['blood_glucose_level'] > 200:
        nerve_score += 2
    if data['bmi'] > 30:
        nerve_score += 1

    if nerve_score >= 5:
        scores['neuropathy_risk_score'] = 3
    elif nerve_score >= 3:
        scores['neuropathy_risk_score'] = 2
    else:
        scores['neuropathy_risk_score'] = 1

    # Stroke risk
    stroke_score = 0
    if data['age'] > 65:
        stroke_score += 3
    elif data['age'] > 50:
        stroke_score += 2
    elif data['age'] > 40:
        stroke_score += 1
    if data['hypertension'] == 1:
        stroke_score += 2
    if data['heart_disease'] == 1:
        stroke_score += 2
    if data['HbA1c_level'] > 8:
        stroke_score += 3
    elif data['HbA1c_level'] > 7:
        stroke_score += 1

    if stroke_score >= 7:
        scores['stroke_risk_score'] = 3
    elif stroke_score >= 4:
        scores['stroke_risk_score'] = 2
    else:
        scores['stroke_risk_score'] = 1

    # Oral infection risk
    oral_score = 0
    if data['HbA1c_level'] > 8:
        oral_score += 3
    elif data['HbA1c_level'] > 7:
        oral_score += 2
    if data['blood_glucose_level'] > 180:
        oral_score += 1
    if data['age'] > 60:
        oral_score += 1

    if oral_score >= 5:
        scores['oral_risk_score'] = 3
    elif oral_score >= 3:
        scores['oral_risk_score'] = 2
    else:
        scores['oral_risk_score'] = 1

    # Glycemic control risk
    if data['HbA1c_level'] > 8:
        scores['glycemic_risk_score'] = 3
    elif data['HbA1c_level'] > 7:
        scores['glycemic_risk_score'] = 2
    elif data['HbA1c_level'] > 6.5:
        scores['glycemic_risk_score'] = 1
    else:
        scores['glycemic_risk_score'] = 0

    # Glucose risk (simple)
    if data['blood_glucose_level'] < 100:
        scores['glucose_risk'] = 0
    elif data['blood_glucose_level'] < 126:
        scores['glucose_risk'] = 1
    else:
        scores['glucose_risk'] = 2

    # BMI risk (simple)
    if data['bmi'] < 18.5:
        scores['bmi_risk'] = 0
    elif data['bmi'] < 25:
        scores['bmi_risk'] = 1
    elif data['bmi'] < 30:
        scores['bmi_risk'] = 2
    else:
        scores['bmi_risk'] = 3

    # Total risk score
    scores['total_risk_score'] = sum([
        scores['hypoglycemia_risk_score'],
        scores['hyperglycemia_risk_score'],
        scores['prediabetes_risk_score'],
        scores['cardiovascular_risk_score'],
        scores['kidney_risk_score'],
        scores['eye_risk_score'],
        scores['neuropathy_risk_score'],
        scores['stroke_risk_score'],
        scores['oral_risk_score'],
        scores['glycemic_risk_score'],
    ])

    return scores

# ======================================================================
# FEATURES FOR MODEL
# ======================================================================

def prepare_features_for_model(data):
    risk_scores = calculate_risk_scores(data)

    features = {
        'age': [float(data['age'])],
        'hypertension': [int(data['hypertension'])],
        'heart_disease': [int(data['heart_disease'])],
        'bmi': [float(data['bmi'])],
        'HbA1c_level': [float(data['HbA1c_level'])],
        'blood_glucose_level': [int(data['blood_glucose_level'])],
    }
    features.update(risk_scores)
    df = pd.DataFrame(features)

    df['gender_Male'] = 1 if str(data['gender']).lower() == 'male' else 0
    df['gender_Other'] = 1 if str(data['gender']).lower() not in ['male', 'female'] else 0

    smoking_cols = [
        'smoking_history_current',
        'smoking_history_ever',
        'smoking_history_former',
        'smoking_history_never',
        'smoking_history_not current'
    ]
    for c in smoking_cols:
        df[c] = 0

    smoking_map = {
        'never': 'smoking_history_never',
        'current': 'smoking_history_current',
        'former': 'smoking_history_former',
        'ever': 'smoking_history_ever',
        'not current': 'smoking_history_not current',
        'no info': 'smoking_history_never'
    }
    key = str(data['smoking_history']).lower()
    df[smoking_map.get(key, 'smoking_history_never')] = 1

    return df

def align_features_with_model(features_df, expected_features):
    aligned = pd.DataFrame(columns=expected_features)
    for f in expected_features:
        aligned[f] = features_df[f] if f in features_df.columns else 0
    return aligned

# ======================================================================
# RISK ASSESSMENT
# ======================================================================

def get_risk_assessment(data):
    risk_scores = calculate_risk_scores(data)

    mapping = {
        'hypoglycemia_risk_score': 'Hypoglycemia',
        'hyperglycemia_risk_score': 'Hyperglycemia',
        'prediabetes_risk_score': 'Prediabetes Progression',
        'cardiovascular_risk_score': 'Cardiovascular Disease',
        'kidney_risk_score': 'Kidney Disease',
        'eye_risk_score': 'Eye Disease',
        'neuropathy_risk_score': 'Nerve Damage',
        'stroke_risk_score': 'Stroke Risk',
        'oral_risk_score': 'Oral Infections',
        'glycemic_risk_score': 'Glycemic Control'
    }

    breakdown = []
    for k, name in mapping.items():
        s = risk_scores.get(k, 0)
        if s >= 3:
            level = "High"
        elif s >= 2:
            level = "Medium"
        elif s >= 1:
            level = "Low"
        else:
            level = "None"
        breakdown.append({"type": name, "level": level, "score": int(s)})

    total = int(risk_scores.get('total_risk_score', 0))
    risk_counts = {
        "High": sum(1 for r in breakdown if r["level"] == "High"),
        "Medium": sum(1 for r in breakdown if r["level"] == "Medium"),
        "Low": sum(1 for r in breakdown if r["level"] == "Low"),
        "None": sum(1 for r in breakdown if r["level"] == "None"),
    }

    if risk_counts["High"] >= 3 or total >= 20:
        overall_risk = "High"
        urgency = "Immediate attention required"
    elif risk_counts["Medium"] >= 3 or total >= 15:
        overall_risk = "Medium"
        urgency = "Monitor closely"
    elif risk_counts["Low"] >= 5 or total >= 10:
        overall_risk = "Low to Moderate"
        urgency = "Regular monitoring"
    else:
        overall_risk = "Low"
        urgency = "Maintain current management"

    return {
        "overall_risk": overall_risk,
        "overall_score": total,
        "risk_breakdown": breakdown,
        "risk_counts": risk_counts,
        "urgency": urgency,
        "timestamp": datetime.now(),
    }

# ======================================================================
# RECOMMENDATIONS
# ======================================================================

def _priority_key(p: str) -> int:
    return {"P0": 0, "P1": 1, "P2": 2, "P3": 3}.get(p, 99)

def _priority_header(p: str) -> str:
    if p == "P0":
        return "✅ DO FIRST (Urgent)"
    if p == "P1":
        return "📅 DO NEXT (Soon)"
    if p == "P2":
        return "🌱 CONTINUE (Routine)"
    return "💡 OPTIONAL"

def _bmi_class(bmi: float) -> str:
    if bmi < 18.5:
        return "underweight"
    if bmi < 25:
        return "healthy"
    if bmi < 30:
        return "overweight"
    if bmi < 35:
        return "obesity_1"
    if bmi < 40:
        return "obesity_2"
    return "obesity_3"

def _likely_diabetes(hba1c: float, glucose: float, diabetes_prediction: str | None) -> bool:
    if diabetes_prediction:
        return str(diabetes_prediction).lower().startswith("diab")
    return (hba1c is not None and hba1c >= 6.5) or (glucose is not None and glucose >= 126)

def generate_personalized_recommendations(
    risk_assessment,
    age=None,
    bmi=None,
    gender=None,
    smoking_history=None,
    hypertension=None,
    heart_disease=None,
    HbA1c_level=None,
    blood_glucose_level=None,
    diabetes_prediction: str | None = None,
):
    overall = risk_assessment.get("overall_risk", "Unknown")
    breakdown = risk_assessment.get("risk_breakdown", [])

    age = float(age) if age is not None else 40.0
    bmi = float(bmi) if bmi is not None else 24.0
    bmi_group = _bmi_class(bmi)

    diabetic_stage = _likely_diabetes(HbA1c_level, blood_glucose_level, diabetes_prediction)

    items = []  # {"p": "P0", "lines":[...]}

    # Overall urgency
    if overall == "High":
        items.append({"p": "P0", "lines": [
            "🚨 Overall risk is HIGH.",
            "• See a doctor/clinic within 24–48 hours.",
            "• Emergency signs: chest pain, severe weakness, confusion, fainting, breathing trouble."
        ]})
    elif overall == "Medium":
        items.append({"p": "P1", "lines": [
            "🟠 Overall risk is MEDIUM.",
            "• Book a medical review within 2–4 weeks."
        ]})
    else:
        items.append({"p": "P2", "lines": [
            "🟢 Overall risk is LOW.",
            "• Maintain healthy habits and routine screening."
        ]})

    # Stage-correct wording
    if diabetic_stage:
        items.append({"p": "P1", "lines": [
            "🩺 Sugars are in diabetes range (HbA1c/glucose).",
            "• Focus on diabetes management (diet + activity + clinician plan)."
        ]})
    else:
        items.append({"p": "P2", "lines": [
            "🧭 Prevention focus.",
            "• Lifestyle changes can reduce progression risk."
        ]})

    # BMI personalization (BMI 32 vs 42 differs)
    if bmi_group == "overweight":
        items.append({"p": "P1", "lines": [
            "⚖️ Weight: Overweight.",
            "• Target 5–10% weight loss over 3–6 months."
        ]})
    elif bmi_group == "obesity_1":
        items.append({"p": "P1", "lines": [
            "⚖️ Weight: Obesity Class I (30–34.9).",
            "• Target ~7–10% weight loss over 3–6 months."
        ]})
    elif bmi_group == "obesity_2":
        items.append({"p": "P1", "lines": [
            "⚖️ Weight: Obesity Class II (35–39.9).",
            "• Target ~10–15% weight loss over 6 months with a structured plan."
        ]})
    elif bmi_group == "obesity_3":
        items.append({"p": "P0" if overall == "High" else "P1", "lines": [
            "⚖️ Weight: Severe obesity (Class III, BMI ≥ 40).",
            "• Strongly consider clinician-supervised weight management.",
            "• Target ~15%+ reduction over 6–12 months (safe, supervised)."
        ]})

    # Hypertension / heart disease
    if hypertension == 1:
        items.append({"p": "P1", "lines": [
            "🩸 Hypertension present.",
            "• Low-salt diet + follow BP plan to protect kidneys/heart/brain."
        ]})
    if heart_disease == 1:
        items.append({"p": "P0", "lines": [
            "❤️ Heart disease history.",
            "• Prioritize clinician/cardiology follow-up."
        ]})

    # High risk areas
    high = [r for r in breakdown if r.get("level") == "High"]
    if high:
        lines = ["🔴 High risk areas (focus first):"]
        for r in high:
            t = r.get("type", "")
            if t == "Eye Disease":
                lines.append("• Eyes: Dilated eye exam within 1 month.")
            elif t == "Kidney Disease":
                lines.append("• Kidneys: Ask for urine ACR + eGFR/creatinine tests.")
            elif t == "Nerve Damage":
                lines.append("• Feet: Daily foot checks; comprehensive foot exam.")
            elif t == "Cardiovascular Disease":
                lines.append("• Heart: ECG/lipid profile discussion; strict BP control.")
            elif t == "Stroke Risk":
                lines.append("• Stroke: Learn FAST signs; focus BP/sugar control.")
            elif t == "Glycemic Control":
                lines.append("• HbA1c: Review plan; reduce refined carbs; consistent meals.")
            elif t == "Prediabetes Progression":
                lines.append("• Diabetes management: intensive lifestyle + clinician review."
                             if diabetic_stage else
                             "• Prediabetes prevention: intensive lifestyle intervention.")
        items.append({"p": "P0", "lines": lines})

    # Medium risk areas
    med = [r for r in breakdown if r.get("level") == "Medium"]
    if med:
        lines = ["🟡 Moderate risk areas (do next):"]
        for r in med:
            t = r.get("type", "")
            if t == "Hyperglycemia":
                lines.append("• Glucose: Adjust diet + walk after meals to reduce spikes.")
            elif t == "Oral Infections":
                lines.append("• Oral: Dental cleaning every 6 months; treat gum disease early.")
            elif t == "Stroke Risk":
                lines.append("• Stroke: BP control + activity; know warning signs.")
        items.append({"p": "P1", "lines": lines})

    # Optional tips
    items.append({"p": "P3", "lines": [
        "🍽️ Optional food swaps:",
        "• Prefer red/brown rice more often; reduce white rice portion size.",
        "• Add leafy greens and legumes regularly."
    ]})

    # Sort and group with headers
    items.sort(key=lambda x: _priority_key(x["p"]))

    out = []
    last = None
    for it in items:
        if it["p"] != last:
            out.append(_priority_header(it["p"]))
            last = it["p"]
        out.extend(it["lines"])

    # Deduplicate
    seen = set()
    final = []
    for line in out:
        if line not in seen:
            final.append(line)
            seen.add(line)
    return final
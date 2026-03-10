# Production medical dictionary for Sinhala/Tamil clinical translation
MEDICAL_TERM_MAP = {
    # Core clinical conditions
    "type 2 diabetes mellitus": {
        "si": "2 වර්ගයේ මධුමේහ රෝගය",
        "ta": "வகை 2 நீரிழிவு நோய்"
    },
    "hypertension": {"si": "රුධිර පීඩන රෝගය", "ta": "இரத்த அழுத்த நோய்"},
    "chronic kidney disease stage 3": {
        "si": "ක්‍රෝනික් කිඩ්නි රෝගය අදියර 3", 
        "ta": "நிலையான சிறுநீரக நோய் 3ஆம் கட்டம்"
    },
    "ischemic heart disease": {
        "si": "ඉස්කීමියා හෘද රෝගය", 
        "ta": "இஸ்கீமிக் இதய நோய்"
    },
    "Poor glycemic control": {"si": "මධුමේහ පාලනය දුර්වල", "ta": "மோசமான சர்க்கரை கட்டுப்பாடு"},
    "Suboptimal blood pressure control": {
        "si": "රුධිර පීඩන පාලනය අඩුපාඩු", 
        "ta": "இரத்த அழுத்த கட்டுப்பாடு மோசமானது"
    },
    
    # Preserve abbreviations
    "HbA1c": {"si": "HbA1c", "ta": "HbA1c"},
    "eGFR": {"si": "eGFR", "ta": "eGFR"},
    "EF": {"si": "EF", "ta": "EF"},
    "CKD": {"si": "CKD", "ta": "CKD"},
    "LDL": {"si": "LDL", "ta": "LDL"},
    
    # Grammar fixes for translation artifacts (CRITICAL)
    "grammar_fixes": {
        # Sinhala artifacts
        "මග්‍රෑම්": {"si": "මධුමේහ"},
        "මීඩියා": {"si": "මධ්‍යම"},
        "MEDterM": {"si": "", "ta": ""},  # Remove bad placeholders
        "MEDERM": {"si": "", "ta": ""},
        "රුටින්": {"si": "රුටින්"},
        "ලක්ෂණ": {"si": "පරීක්ෂණ"},
        
        # Tamil artifacts  
        "METTERM": {"ta": ""},
        "MEDLM": {"ta": ""},
        "மெடெரம்": {"ta": ""},
        "தோல்": {"ta": "இரத்த அழுத்தம்"},  # BP mistranslation
        "மோச": {"ta": "மோசமான"},
        "1.1": {"ta": "1."},  # Number formatting
    }
}
MEDICAL_TERM_MAP.update({
    # MISSING TERMS FROM YOUR NOTE
    "chronic kidney disease stage 3": {"si": "ක්‍රෝනික් කිඩ්නි රෝග අදියර 3", "ta": "நிலையான சிறுநீரக நோய் 3ஆம் கட்டம்"},
    "Poor glycemic control": {"si": "මධුමේහ පාලනය දුර්වල", "ta": "மோசமான சர்க்கரை கட்டுப்பாடு"},
    "Suboptimal blood pressure control": {"si": "රුධිර පීඩන පාලනය අඩුපාඩු", "ta": "இரத்த அழுத்த கட்டுப்பாடு மோசமானது"},
    
    # EMERGENCY ARTIFACT FIXES
    "grammar_fixes": {
        "මග්‍රෑම්": {"si": "මධුමේහ"},
        "MEDterM": {"si": "", "ta": ""},
        "METTERM": {"ta": ""},
        "MEDLM": {"ta": ""},
        "MEDERM": {"si": ""},
        "මීඩියා": {"si": "මධ්‍යම"},
        "තோல்": {"ta": "இரத்த அழுத்தம்"},
        "மோச": {"ta": "மோசமான"},
    }
})

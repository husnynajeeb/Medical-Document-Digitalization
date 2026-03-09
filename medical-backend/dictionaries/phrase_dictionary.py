import re

# ---------------------------------------------------
# Medical Phrase Dictionary
# ---------------------------------------------------

phrase_dictionary = {

    # Cardiovascular
    "high blood pressure": {
        "ta": "உயர் இரத்த அழுத்தம்",
        "si": "අධි රුධිර පීඩනය"
    },

    "blood pressure": {
        "ta": "இரத்த அழுத்தம்",
        "si": "රුධිර පීඩනය"
    },

    "low blood pressure": {
        "ta": "குறைந்த இரத்த அழுத்தம்",
        "si": "අඩු රුධිර පීඩනය"
    },

    "heart rate": {
        "ta": "இதய துடிப்பு",
        "si": "හෘද ස්පන්දනය"
    },

    "heart disease": {
        "ta": "இதய நோய்",
        "si": "හෘද රෝගය"
    },

    "ischemic heart disease": {
        "ta": "இஸ்கீமிக் இதய நோய்",
        "si": "ඉස්කීමික් හෘද රෝගය"
    },

    "chest pain": {
        "ta": "மார்பு வலி",
        "si": "වක්ෂ වේදනාව"
    },

    "shortness of breath": {
        "ta": "மூச்சுத்திணறல்",
        "si": "හුස්ම ගැනීමේ අපහසුතාව"
    },

    "left ventricular hypertrophy": {
        "ta": "இடது வெண்ட்ரிக்கிள் தடிப்பு",
        "si": "වම වෙන්ට්‍රිකල් ඝනතාව"
    },

    # Diabetes
    "diabetes mellitus": {
        "ta": "நீரிழிவு மெலிட்டஸ்",
        "si": "දියවැඩියාව මැලිතස්"
    },

    "type 2 diabetes mellitus": {
        "ta": "வகை 2 நீரிழிவு மெலிட்டஸ்",
        "si": "දෙවන වර්ගයේ දියවැඩියාව"
    },

    "high blood sugar": {
        "ta": "உயர் இரத்த சர்க்கரை",
        "si": "අධි රුධිර සීනි"
    },

    "low blood sugar": {
        "ta": "குறைந்த இரத்த சர்க்கரை",
        "si": "අඩු රුධිර සීනි"
    },

    "blood sugar level": {
        "ta": "இரத்த சர்க்கரை அளவு",
        "si": "රුධිර සීනි මට්ටම"
    },

    "blood glucose": {
        "ta": "இரத்த குளுக்கோஸ்",
        "si": "රුධිර ග්ලුකෝස්"
    },

    "glycemic control": {
        "ta": "சர்க்கரை கட்டுப்பாடு",
        "si": "රුධිර සීනි පාලනය"
    },

    "poor glycemic control": {
        "ta": "சர்க்கரை கட்டுப்பாடு குறைவு",
        "si": "රුධිර සීනි පාලනය දුර්වලයි"
    },

    # Kidney
    "chronic kidney disease": {
        "ta": "நீடித்த சிறுநீரக நோய்",
        "si": "ක්‍රෝනික වකුගඩු රෝගය"
    },

    "renal function": {
        "ta": "சிறுநீரக செயல்பாடு",
        "si": "වකුගඩු ක්‍රියාකාරීත්වය"
    },

    "kidney function": {
        "ta": "சிறுநீரக செயல்பாடு",
        "si": "වකුගඩු ක්‍රියාකාරීත්වය"
    },

    # Clinical workflow
    "routine follow up": {
        "ta": "வழக்கமான பின்தொடர்பு",
        "si": "සාමාන්‍ය අනුගමනය"
    },

    "follow up": {
        "ta": "பின்தொடர்பு",
        "si": "අනුගමනය"
    },

    "clinical report": {
        "ta": "மருத்துவ அறிக்கை",
        "si": "වෛද්‍ය වාර්තාව"
    },

    "treatment plan": {
        "ta": "சிகிச்சை திட்டம்",
        "si": "ප්‍රතිකාර සැලැස්ම"
    },

    "lifestyle modification": {
        "ta": "வாழ்க்கை முறை மாற்றம்",
        "si": "ජීවන රටාව වෙනස් කිරීම"
    },

    "diet control": {
        "ta": "உணவு கட்டுப்பாடு",
        "si": "ආහාර පාලනය"
    },

    # Patient phrases
    "patient presents with": {
        "ta": "நோயாளர் வருகிறார்",
        "si": "රෝගියා පැමිණෙයි"
    },

    "patient reports": {
        "ta": "நோயாளர் தெரிவிக்கிறார்",
        "si": "රෝගියා වාර්තා කරයි"
    },

    "patient complains of": {
        "ta": "நோயாளர் புகார் தெரிவிக்கிறார்",
        "si": "රෝගියා පැමිණිලි කරයි"
    },

    # Lab
    "laboratory results": {
        "ta": "ஆய்வக முடிவுகள்",
        "si": "පරීක්ෂාගාර ප්‍රතිඵල"
    },

    "test results": {
        "ta": "பரிசோதனை முடிவுகள்",
        "si": "පරීක්ෂණ ප්‍රතිඵල"
    },

    "blood test": {
        "ta": "இரத்த பரிசோதனை",
        "si": "රුධිර පරීක්ෂාව"
    },

    "urine test": {
        "ta": "சிறுநீர் பரிசோதனை",
        "si": "මූත්‍රා පරීක්ෂාව"
    }
}


# ---------------------------------------------------
# Apply Phrase Dictionary
# ---------------------------------------------------

def apply_phrase_dictionary(text, target_lang):

    # Sort phrases by length to avoid partial replacement
    phrases = sorted(phrase_dictionary.keys(), key=len, reverse=True)

    for phrase in phrases:

        translations = phrase_dictionary[phrase]

        translation = translations.get(target_lang)

        if translation:

            pattern = re.compile(r"\b" + re.escape(phrase) + r"\b", re.IGNORECASE)

            text = pattern.sub(translation, text)

    return text
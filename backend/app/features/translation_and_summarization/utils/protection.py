# import re
# from dictionaries.medical_dictionary import MEDICAL_TERM_MAP

# # -----------------------------------------------------------
# # Improvement 1: Drug name protection
# # Many translation models distort drug names.
# # We protect them before translation so they remain unchanged.
# # -----------------------------------------------------------

# DRUG_NAMES = [
#     "Metformin",
#     "Amlodipine",
#     "Lisinopril",
#     "Atorvastatin",
#     "Aspirin",
#     "Insulin",
# ]


# # -----------------------------------------------------------
# # Improvement 2: Lab value protection
# # Clinical values like "132 mg/dL" or "148/92 mmHg"
# # must never be altered during translation.
# # Regex detects common lab patterns.
# # -----------------------------------------------------------

# LAB_PATTERN = r'\d+(\.\d+)?\s?(mg/dL|mmHg|mL/min|%)'


# def protect_lab_values(text):

#     protected = {}
#     index = 0

#     def replacer(match):
#         nonlocal index

#         placeholder = f"LABVAL_{index}"

#         protected[placeholder] = match.group(0)

#         index += 1

#         return placeholder

#     modified = re.sub(LAB_PATTERN, replacer, text)

#     return modified, protected


# # -----------------------------------------------------------
# # Improvement 3: Medical term protection
# # Prevents incorrect translation of important medical terms
# # such as "hypertension" or "salt".
# # -----------------------------------------------------------

# def protect_medical_terms(text):

#     protected = {}

#     modified = text

#     index = 0

#     for term in MEDICAL_TERM_MAP.keys():

#         if term.lower() in modified.lower():

#             placeholder = f"MEDTERM_{index}"

#             modified = re.sub(
#                 term,
#                 placeholder,
#                 modified,
#                 flags=re.IGNORECASE
#             )

#             protected[placeholder] = term

#             index += 1

#     return modified, protected


# # -----------------------------------------------------------
# # Improvement 4: Drug protection
# # Drug names remain exactly the same in the output.
# # -----------------------------------------------------------

# def protect_drug_names(text):

#     protected = {}

#     modified = text

#     index = 0

#     for drug in DRUG_NAMES:

#         if drug in modified:

#             placeholder = f"DRUG_{index}"

#             modified = modified.replace(drug, placeholder)

#             protected[placeholder] = drug

#             index += 1

#     return modified, protected


# # -----------------------------------------------------------
# # Improvement 5: Bullet structure protection
# # Prevents bullet lists collapsing into a single line.
# # -----------------------------------------------------------

# def protect_bullets(text):

#     modified = text.replace("- ", "BULLET_ITEM ")

#     return modified


# def restore_bullets(text):

#     return text.replace("BULLET_ITEM ", "- ")


# # -----------------------------------------------------------
# # Restore placeholders after translation
# # -----------------------------------------------------------

# def restore_terms(text, protected_dict):

#     for placeholder, original in protected_dict.items():

#         text = text.replace(placeholder, original)

#     return text
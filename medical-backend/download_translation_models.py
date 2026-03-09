# # download_translation_models.py

# from transformers import MarianMTModel, MarianTokenizer
# import os

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# print("Loading translation models...")

# # Sinhala model
# si_path = os.path.join(BASE_DIR, "./en_si_medical_final")

# si_tokenizer = MarianTokenizer.from_pretrained(si_path)
# si_model = MarianMTModel.from_pretrained(si_path)

# print("Sinhala translation model loaded")

# # Tamil model
# ta_path = os.path.join(BASE_DIR, "./en_ta_medical_final")

# ta_tokenizer = MarianTokenizer.from_pretrained(ta_path)
# ta_model = MarianMTModel.from_pretrained(ta_path)

# print("Tamil translation model loaded")

# print("All translation models loaded successfully")
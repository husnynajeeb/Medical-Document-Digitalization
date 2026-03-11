import os
import torch

# go up to backend folder
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

SI_MODEL_PATH = os.path.join(BASE_DIR, "models", "MarianMt", "en_si_finetuned_new")
TA_MODEL_PATH = os.path.join(BASE_DIR, "models", "MarianMt", "en_ta_finetuned_new")
T5_MODEL_PATH = os.path.join(BASE_DIR, "models", "clinicalT5", "clinical_t5_finetuned")

print("SI_MODEL_PATH:", SI_MODEL_PATH)
print("TA_MODEL_PATH:", TA_MODEL_PATH)
print("T5_MODEL_PATH:", T5_MODEL_PATH)
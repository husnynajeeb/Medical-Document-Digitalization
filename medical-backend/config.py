import os
import torch

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

SI_MODEL_PATH = os.path.join(BASE_DIR, "models/en_si_finetuned_new")
TA_MODEL_PATH = os.path.join(BASE_DIR, "models/en_ta_finetuned_new")
T5_MODEL_PATH = os.path.join(BASE_DIR, "models/clinical_t5_finetuned")
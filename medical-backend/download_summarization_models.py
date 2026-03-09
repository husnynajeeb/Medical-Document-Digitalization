# # download_summarization_models.py

# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# import torch
# import os

# MODEL_PATH = os.path.join(os.path.dirname(__file__), "./clinical_t5_finetuned")

# print("Loading Fine-Tuned Clinical T5 Model...")

# tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
# model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH)

# device = "cuda" if torch.cuda.is_available() else "cpu"
# model.to(device)
# model.eval()

# print(f"Clinical T5 loaded successfully on {device}")
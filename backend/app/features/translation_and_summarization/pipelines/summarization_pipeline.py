from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
from app.features.translation_and_summarization.config import DEVICE, T5_MODEL_PATH

print("Loading T5 Model...")
t5_tokenizer = T5Tokenizer.from_pretrained(T5_MODEL_PATH, local_files_only=True)
t5_model = T5ForConditionalGeneration.from_pretrained(T5_MODEL_PATH, local_files_only=True).to(DEVICE)
t5_model.eval()


def build_prompt(text: str, summary_type: str) -> str:
    """
    Create task-specific prompts for the T5 model
    """

    if summary_type == "patient":
        return (
            "Summarize the following clinical note in simple language "
            "that a patient can easily understand:\n\n"
            f"{text}"
        )

    if summary_type == "medical":
        return (
            "Generate a concise professional medical summary of the "
            "following clinical note:\n\n"
            f"{text}"
        )

    raise ValueError("summary_type must be 'patient' or 'medical'")


def summarize_text(text: str, summary_type: str):

    # Skip summarization for very short text
    if len(text.split()) < 40:
        return text

    prompt = build_prompt(text, summary_type)

    inputs = t5_tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    ).to(DEVICE)

    with torch.no_grad():

        outputs = t5_model.generate(
            **inputs,
            max_length=200,
            min_length=40,
            num_beams=4,
            length_penalty=1.2,
            early_stopping=True
        )

    summary = t5_tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return summary
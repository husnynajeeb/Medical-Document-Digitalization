🩺 Medical Language Processing Backend
📌 Project Overview

This project is a Medical Language Processing Backend designed to support medical translation, medical text summarization, and text-to-speech output.
It is mainly focused on healthcare-related content, where accuracy, terminology awareness, and language support are critical.

The system is developed as a backend-only service, which can be integrated with any frontend or mobile application.

🎯 Objectives

Translate medical text accurately between English, Sinhala, and Tamil

Generate concise medical summaries from long clinical text

Convert generated text into speech output

Provide a reliable alternative for domain-specific medical language processing

🧠 System Architecture

The backend follows a modular AI pipeline:

Input Processing – Receives medical text

Translation Module – Converts text between supported languages

Summarization Module – Produces concise medical summaries

🔹 Text-to-Speech (TTS)

Converts translated or summarized medical text into audio

Useful for accessibility and voice-based medical assistance

🧠 Use of Large Language Models (LLMs)

LLMs are used to:

Improve contextual understanding of medical text

Preserve semantic meaning during summarization

Support future enhancements such as medical Q&A and decision support

The system is designed to combine task-specific models with LLM capabilities, instead of relying entirely on a single large model.

❌ Models Experimented but Rejected

Generic Google Translate / API-based translation

Poor handling of medical terminology

No control over domain customization

Very large LLM-only approaches

High computational cost

Not suitable for offline or private deployment

Slower response times

Text-to-Speech Module – Converts final text into audio

API Layer – Exposes endpoints for integration

🤖 Models Used
🔹 Translation Models

Fine-tuned MarianMT / Transformer-based models

Language pairs:

English → Sinhala

English → Tamil

Why these models?

Lightweight compared to large LLMs

Can be fine-tuned with domain-specific (medical) data

Faster inference for real-time applications

⚠️ Fine-tuned model files are not included in the repository due to size limitations.

🔹 Summarization Model

BART-based summarization model

Used for abstractive summarization of medical reports

Why BART?

Performs well on long structured text

Generates fluent, human-readable summaries

Suitable for future medical-specific fine-tuning

⭐ Why This System Is Needed (Even with ChatGPT & Google Translate)

One solid reason:

This system is domain-specific, controllable, and deployable in restricted medical environments where public AI tools cannot be used.

Medical data privacy is critical

Hospitals cannot rely on public APIs

General translators are not trained on medical terminology

This system can be fine-tuned, audited, and deployed locally

🔮 Future Improvements

Fine-tune summarization using BioBART

Improve translation accuracy using larger medical parallel datasets

Add medical entity recognition

Introduce speech-to-speech translation

Support more regional languages

Improve evaluation using BLEU and ROUGE metrics

🧪 Planned Model Upgrade – BioBART

Why BioBART?

Pretrained on biomedical and clinical datasets

Better understanding of medical terminology

Produces more accurate medical summaries than general BART

Reduces hallucinations in clinical summarization

🛠 Technologies Used

Python

FastAPI / Flask

HuggingFace Transformers

PyTorch

Text-to-Speech libraries

Git & GitHub

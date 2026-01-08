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

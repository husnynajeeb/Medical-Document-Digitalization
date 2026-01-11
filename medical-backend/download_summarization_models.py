from transformers import pipeline

# Pre-download DistilBART
pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Pre-download PEGASUS-PubMed
pipeline("summarization", model="google/pegasus-pubmed")

from transformers import MarianMTModel, MarianTokenizer, pipeline

# Translation models
MarianMTModel.from_pretrained("./en_si_finetuned")
MarianTokenizer.from_pretrained("./en_si_finetuned")
MarianMTModel.from_pretrained("./en_ta_finetuned")
MarianTokenizer.from_pretrained("./en_ta_finetuned")

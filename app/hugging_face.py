from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)

import torch
MODEL_NAME = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)
model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME
)
model.eval()
prompt="Generate a realistic patient complaint."
inputs = tokenizer(
    prompt,
    return_tensors="pt"
)
outputs = model.generate(
    **inputs,
    max_new_tokens=32
)
response = tokenizer.decode(
    outputs[0],
    skip_special_tokens=True
)
print(response)
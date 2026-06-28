from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)

import torch
MODEL_NAME = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)
model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME
)
model.eval()
prompt =  "Generate a realistic patient complaint for orthopedic pain in knees"
print(MODEL_NAME)
print(prompt)

inputs = tokenizer(
    prompt,
    return_tensors="pt"
)
outputs = model.generate(
    **inputs,
    max_new_tokens=16,
    num_beams=4,
    do_sample=False,
    early_stopping=True
)
response = tokenizer.decode(
    outputs[0],
    skip_special_tokens=True
)
print(response)
print(outputs)
print(tokenizer.decode(outputs[0], skip_special_tokens=False))
print(model.config.architectures)
print(model.config.model_type)
print(tokenizer.__class__)
print(model.__class__)
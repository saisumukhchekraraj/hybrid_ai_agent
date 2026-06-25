from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM

import torch
MODEL_NAME = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
def generate_sentence(prompt):
    inputs = tokenizer(
    prompt,
    return_tensors="pt"
)
    output = model.generate(
    **inputs,
    max_new_tokens=30,
    do_sample=True,
    temperature=0.8,
    top_p=0.95
)
    sentence = tokenizer.decode(
    output[0],
    skip_special_tokens=True
)
    return sentence
if __name__ == "__main__":

    prompt = "Generate a patient complaint for booking an appointment with a doctor"

    print(generate_sentence(prompt))
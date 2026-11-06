import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "Applied-Innovation-Center/Karnak-6B-v1.0"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
)

# Prepare Input
prompt = "اشرح لي نظرية النسبية بشكل مبسط."
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt},
]

# Apply chat template
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
)
model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

# Generate
generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=512,
    temperature=0.7,
    top_p=0.9,
)

# Decode output (removing the prompt tokens)
generated_ids = generated_ids[:, model_inputs.input_ids.shape[1]:]
response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
print(response)

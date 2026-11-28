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
prompt = """
كيف يضمن الدستور استقلال القضاء؟

[دستور 2014 (معدل 2019) | مادة 51]
 "(1) تقوم كل جهة او هيئة قضائية علي شئونها، ويؤخذ رايها في مشروعات القوانين المنظمة لشئونها، ويكون لكل منها موازنة مستقلة. ويعين رئيس الجمهورية رؤساء الجهات والهيئات القضائية من بين اقدم سبعة من نوابهم، وذلك لمدة اربع سنوات، او للمدة الباقية حتي بلوغه سن التقاعد، ايهما اقرب، ولمرة واحدة طوال مدة عمله، وذلك علي النحو الذي ينظمه القانون. ويقوم علي شئونها المشتركة مجلس اعلي للجهات والهيئات القضائية، يراسه رئيس الجمهورية، وبعضوية رئيس المحكمة الدستورية العليا، ورؤساء الجهات والهيئات القضائية، ورئيس محكمة استئناف (1) مستبدلة بموجب الاستفتاء علي تعديل الدستور الذي اجري بالخارج ايام: 19، 20، 21، وبالداخل ايام: 20، 21، 22 من ابريل سنة 2019. القاهرة، والنائب العام. ويكون للمجلس امين عام، يصدر بتعيينه قرار من رئيس الجمهورية للمدة التي يحددها القانون وبالتناوب بين الجهات اعضاء المجلس. ويحل محل رئيس الجمهورية عند غيابه من يفوضه من رؤساء الجهات والهيئات القضائية. ويختص المجلس بالنظر في شروط تعيين اعضاء الجهات والهيئات القضائية وترقيتهم وتاديبهم، ويؤخذ رايه في مشروعات القوانين المنظمة لشئون هذه الجهات والهيئات، وتصدر قراراته بموافقة اغلبية اعضائه علي ان يكون من بينهم رئيس المجلس.",
"""
messages = [
    {"role": "system", "content": "اجب طبقا للمعلومات بين القوسين"},
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
import json
import pymupdf
import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForImageTextToText

model_name = "NAMAA-Space/Qari-OCR-0.4.0-VL-4B-Instruct"
processor = AutoProcessor.from_pretrained(model_name)
model = AutoModelForImageTextToText.from_pretrained(
    model_name, torch_dtype=torch.float16, device_map="auto"
)

def extract(src_path, target_path, source_version):
    doc = pymupdf.open(src_path)

    with open(target_path, "w", encoding="utf-8") as f:
        for i, page in enumerate(doc, start=1):
            pix = page.get_pixmap(dpi=200)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img.thumbnail((2300, 2300))

            messages = [{"role": "user", "content": [
                {"type": "image", "image": img},
                {"type": "text", "text": "Free OCR."},
            ]}]
            inputs = processor.apply_chat_template(
                messages, tokenize=True, add_generation_prompt=True,
                return_dict=True, return_tensors="pt",
            ).to(model.device)

            with torch.no_grad():
                out = model.generate(**inputs, max_new_tokens=2048)
            text = processor.batch_decode(
                [o[len(i_):] for i_, o in zip(inputs.input_ids, out)],
                skip_special_tokens=True,
            )[0].strip()

            f.write(json.dumps({"page": i, "text": text, "source_version": source_version}, ensure_ascii=False) + "\n")
            f.flush()
            print(f"page {i}/{len(doc)} done")

extract("data/raw/constitution_2014_original.pdf",
        "data/interim/constitution_2014_original.jsonl",
        "constitution_2014_original")

extract("data/raw/constitution_2014_amended_2019.pdf", 
        "data/interim/constitution_2014_amended_2019.jsonl",
        "constitution_2014_amended_2019")
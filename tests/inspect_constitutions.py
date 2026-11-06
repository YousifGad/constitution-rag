import json

doc_1 = "data/interim/constitution_2014_original.jsonl"
doc_2 = "data/interim/constitution_2014_amended_2019.jsonl"

with open(doc_1, encoding="utf-8") as f:
    pages_1 = [json.loads(line) for line in f]

with open(doc_2, encoding="utf-8") as f:
    pages_2 = [json.loads(line) for line in f]

print("دستور ٢٠١٤")
for page in pages_1[:15]:
    print(f"--- صفحة {page["page"]} ---")
    print(page["text"])
    print("\n")

print("دستور ٢٠١٤ المعدل ٢٠١٩")
for page in pages_2[:15]:
    print(f"--- صفحة {page["page"]} ---")
    print(page["text"])
    print("\n")
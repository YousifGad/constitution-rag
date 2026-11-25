import json

def read_jsonl_records(path: str) -> list[dict]:
    with open(path, mode="r", encoding="utf-8") as f:
        articles = [json.loads(line) for line in f]
    return articles

def write_jsonl_records(records: list[dict], path: str) -> None:
    with open(path, mode="w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

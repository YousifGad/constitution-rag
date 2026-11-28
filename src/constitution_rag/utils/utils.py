import re
import json
from constitution_rag.ingest.normalize import normalize_arabic

EXACT_QUERY_RE = re.compile(
    r"(?:ال)?ماد[ةه]\s*\(?\s*([0-9٠-٩۰-۹]+)\s*\)?(?:\s*[-–]?\s*(مكرر[ةه]?|bis))?"
)

ORIGINAL_CONSTITUTION_RE = re.compile(
    r"(?:الدستور\s+(?:الاصلي|الأصلي|الاساسي|الأساسي)|النسخة\s+(?:الاصلية|الأصلية)|دستور\s+2014(?:\s+(?:الاصلي|الأصلي))?(?!\s*(?:\(|معدل|المعدل|تعديلات)))"
)

def read_jsonl_records(path: str) -> list[dict]:
    with open(path, mode="r", encoding="utf-8") as f:
        articles = [json.loads(line) for line in f]
    return articles

def write_jsonl_records(records: list[dict], path: str) -> None:
    with open(path, mode="w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

def parse_query(query: str, version: str = "2014-amended-2019") -> dict | None:
    match = EXACT_QUERY_RE.search(query)
    constitution_flag = ORIGINAL_CONSTITUTION_RE.search(query)

    if not match:
        return None
    if constitution_flag:
        version = "2014-original"
    number = int(normalize_arabic(match.group(1)))
    suffix = "مكرراً" if match.group(2) else None
    return {
        "version": version,
        "number": number,
        "suffix": suffix
    }
import re
import json
from constitution_rag.ingest.normalize import normalize_arabic
from constitution_rag.utils.utils import read_jsonl_records, write_jsonl_records

SINGLE_ARTICLE_RE = re.compile(
    r"(?:وفق[اًا]\s+ل)?(?:ال)?ماد[ةه]\s*(?:\(\s*)?([0-9٠-٩۰-۹]+)(?:\s*\))?"
)
RANGE_ARTICLES_RE = re.compile(
    r"(?:ال)?مواد\s+(?:من\s+)?(?:\(\s*)?([0-9٠-٩۰-۹]+)(?:\s*\))?\s+(?:الى|إلى)\s+(?:\(\s*)?([0-9٠-٩۰-۹]+)(?:\s*\))?"
)

def extract_referenced_numbers(text: str) -> list[int]:
    text = normalize_arabic(text)
    numbers = []

    for match in RANGE_ARTICLES_RE.finditer(text):
        start = int(match.group(1))
        end = int(match.group(2))
        if 0 < start <= end and (end - start) <= 200:
            numbers.extend(range(start, end+1))

    for match in SINGLE_ARTICLE_RE.finditer(text):
        numbers.append(int(match.group(1)))

    return numbers

def build_cross_references(
    articles: list[dict],
) -> tuple[dict, list]:
    
    # Index articles by (version, number) -> article_id
    version_num_to_id = {}
    for article in articles:
        version_num_to_id[(article["article_id"].strip(":")[0], article["number"])] = article["article_id"]

    adjacency = {}
    unresolved = []

    for article in sorted(articles, key=lambda a: a["article_id"]):
        src_id = article["article_id"]
        version = article["article_id"].strip(":")[0]
        seen_targets = []

        for ref_num in extract_referenced_numbers(article["text_ar"]):
            target_id = version_num_to_id.get((version, ref_num))
            if target_id and target_id != src_id:
                if target_id not in seen_targets:
                    seen_targets.append(target_id)
            elif not target_id:
                unresolved.append(
                    {
                        "source_article_id": src_id,
                        "version": version,
                        "referenced_number": ref_num,
                        "reason": "target_not_found_in_version",
                    }
                )

        adjacency[src_id] = seen_targets

    return adjacency, unresolved

if __name__ == "__main__":
    original_articles = read_jsonl_records("data/processed/constitution_2014_original_articles.jsonl")
    amended_articles = read_jsonl_records("data/processed/constitution_2014_amended_2019_articles.jsonl")

    adjacency_original, unresolved_original = build_cross_references(original_articles)
    adjacency_amended, unresolved_amended = build_cross_references(amended_articles)

    references = []
    for article, refs in adjacency_original.items():
        if refs:
            references.append({article: refs})

    for article, refs in adjacency_amended.items():
        if refs:
            references.append({article: refs})

    write_jsonl_records(references, "data/processed/references.jsonl")
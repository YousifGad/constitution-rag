import difflib
from constitution_rag.utils.utils import read_jsonl_records, write_jsonl_records
from constitution_rag.ingest.normalize import normalize_arabic

def similarity_score(a: str, b: str) -> float:
    a_norm = normalize_arabic(a)
    b_norm = normalize_arabic(b)

    if not a_norm and not b_norm:
        return 1.0
    elif not a_norm or not b_norm:
        return 0.0
    return difflib.SequenceMatcher(a=a_norm, b=b_norm).ratio()

def build_candidate_records(
    original_articles: list[dict],
    amended_articles: list[dict],
    similarity_threshold: float = 0.9
) -> list[dict]:
    original_map = {(a["number"], a["suffix"]): a for a in original_articles}
    amended_map = {(a["number"], a["suffix"]): a for a in amended_articles}
    all_keys = sorted(set(original_map) | set(amended_map), key=lambda k: (k[0], k[1] or ""))

    records = []
    for number, suffix in all_keys:
        original = original_map.get((number, suffix))
        amended = amended_map.get((number, suffix))
        base_id = f"article-{number:04d}" + ("-mukarrar" if suffix else "")

        if original and amended: # unchanged or amended 
            score = similarity_score(original["text_ar"], amended["text_ar"])
            change_type = "unchanged" if score >= similarity_threshold else "amended"
            records.append(
                {
                    "lineage_id": base_id,
                    "number": number,
                    "suffix": suffix,
                    "original_article_id": original["article_id"],
                    "amended_article_id": amended["article_id"],
                    "change_type": change_type,
                    "_similarity": round(score, 4),
                    "_needs_review": change_type == "amended"
                }
            )

        elif original and not amended: # repealed
            records.append(
                {
                    "lineage_id": base_id,
                    "number": number,
                    "suffix": suffix,
                    "original_article_id": original["article_id"],
                    "amended_article_id": None,
                    "change_type": "repealed",
                    "_similarity": 0.0,
                    "_needs_review": True
                }
            )

        elif not original and amended: # added
            records.append(
                {
                    "lineage_id": base_id,
                    "number": number,
                    "suffix": suffix,
                    "original_article_id": None,
                    "amended_article_id": amended["article_id"],
                    "change_type": "added",
                    "_similarity": 0.0,
                    "_needs_review": True
                }
            )
            
    return records

def build_article_to_lineage_map(records: list[dict]) -> dict:
    lookup = {}

    for record in records:
        lineage_id = record["lineage_id"]

        for field, role in [
            ("original_article_id", "original"),
            ("amended_article_id", "amended"),
        ]:
            article_id = record.get(field)
            if not article_id:
                continue
            if article_id in lookup and lookup[article_id]["lineage_id"] != lineage_id:
                raise ValueError(
                    f"Conflicting lineage_id for {article_id}: "
                    f"{lookup[article_id]['lineage_id']} vs {lineage_id}"
                )
            lookup[article_id] = {
                "lineage_id": lineage_id
            }

    return lookup

def attach_lineage_to_dicts(
    articles: list[dict],
    records: list[dict],
) -> list[dict]:
    lookup = build_article_to_lineage_map(records)
    updated: list[dict] = []

    for article in articles:
        article_id = article["article_id"]
        meta = lookup.get(article_id)
        if meta is None:
            raise KeyError(f"No lineage record found for article id: {article_id}")

        updated.append(
            {
                **article,
                "lineage_id": meta["lineage_id"],
            }
        )

    return updated

if __name__ == "__main__":
    original_articles = read_jsonl_records("data/processed/constitution_2014_original_articles.jsonl")
    amended_articles = read_jsonl_records("data/processed/constitution_2014_amended_2019_articles.jsonl")
    records = build_candidate_records(original_articles, amended_articles)
    write_jsonl_records(records, "data/processed/changes.jsonl")
    original_articles_updated = attach_lineage_to_dicts(original_articles, records)
    amended_articles_updated = attach_lineage_to_dicts(amended_articles, records)
    write_jsonl_records(original_articles_updated, "data/processed/constitution_2014_original_articles.jsonl")
    write_jsonl_records(amended_articles_updated, "data/processed/constitution_2014_amended_2019_articles.jsonl")

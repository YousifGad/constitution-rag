from constitution_rag.utils.utils import read_jsonl_records, write_jsonl_records

VERSION_LABELS = {
    "2014-original": "دستور 2014",
    "2014-amended-2019": "دستور 2014 (معدل 2019)"
}

def build_context_header(version: str, number: int, suffix: str | None = None) -> str:
    version_label = VERSION_LABELS.get(version)
    article_label = f"مادة {number} " + (suffix if suffix else "")
    return f"[{version_label} | {article_label}]"

def build_chunks(
    original_articles: list[dict],
    amended_articles: list[dict],
) -> list[dict]:
    articles = original_articles + amended_articles
    chunks = []

    for id, article in enumerate(articles, start=1):
        context_header = build_context_header(article["version"], article["number"], article["suffix"])
        chunks.append({
            "chunk_id": f"chunk-{id:04d}",
            "article_id": article["article_id"],
            "lineage_id": article["lineage_id"],
            "version": article["version"],
            "number": article["number"],
            "suffix": article["suffix"],
            "text_ar": article["text_ar"],
            "text_ar_search": context_header + "\n" + article["text_ar_search"]
        })
    return chunks

if __name__ == "__main__":
    original_articles = read_jsonl_records("data/processed/constitution_2014_original_articles.jsonl")
    amended_articles = read_jsonl_records("data/processed/constitution_2014_amended_2019_articles.jsonl")
    chunks = build_chunks(original_articles, amended_articles)
    write_jsonl_records(chunks, "data/processed/chunks.jsonl")
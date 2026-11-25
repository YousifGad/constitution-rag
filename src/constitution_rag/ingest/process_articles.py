import json
from constitution_rag.ingest.normalize import normalize_arabic
from constitution_rag.utils.utils import read_jsonl_records

articles_1 = read_jsonl_records("data/interim/constitution_2014_original_articles.jsonl")
articles_2 = read_jsonl_records("data/interim/constitution_2014_amended_2019_articles.jsonl")

with open("data/processed/constitution_2014_original_articles.jsonl",
           mode="w", encoding="utf-8") as f:
    for article in articles_1:
        suffix = "-mukarrar" if article["suffix"] else ""
        f.write(json.dumps({
            "article_id": f"2014-original:article-{article["article_number"]:04d}{suffix}",
            "lineage_id": None,
            "version": "2014-original",
            "number": article["article_number"],
            "suffix": article["suffix"],
            "text_ar": article["text"],
            "text_ar_search": normalize_arabic(article["text"]),
            "start_page": article["start_page"],
            "end_page": article["end_page"],
            "refs": [],
        }) + "\n")


with open("data/processed/constitution_2014_amended_2019_articles.jsonl",
           mode="w", encoding="utf-8") as f:
    for article in articles_2:
        suffix = "-mukarrar" if article["suffix"] else ""
        f.write(json.dumps({
            "article_id": f"2014-amended-2019:article-{article["article_number"]:04d}{suffix}",
            "lineage_id": None,
            "version": "2014-amended-2019",
            "number": article["article_number"],
            "suffix": article["suffix"],
            "text_ar": article["text"],
            "text_ar_search": normalize_arabic(article["text"]),
            "start_page": article["start_page"],
            "end_page": article["end_page"],
            "refs": []
        }) + "\n")
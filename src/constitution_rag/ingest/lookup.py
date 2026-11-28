from constitution_rag.utils.utils import read_jsonl_records, parse_query
from constitution_rag.ingest.normalize import normalize_arabic

class ExactArticleLookup:
    def __init__(self, articles: list[dict]):
        # (version, number, suffix) -> article
        self.index: dict[tuple, dict] = {}
        for article in articles:
            key = (article["version"], article["number"], article.get("suffix"))
            self.index[key] = article

    def lookup(self, version: str, number: int | str, suffix: str | None) -> dict:
        if isinstance(number, str):
            number = int(normalize_arabic(number))
        return self.index.get((version, number, suffix))

    def lookup_query(self, query: str, version: str = "2014-amended-2019") -> dict | None:
        parsed = parse_query(query, version)
        if not parsed:
            return None
        return self.lookup(**parsed)
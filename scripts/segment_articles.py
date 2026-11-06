import re
import json

ARTICLE_PATTERN = re.compile(
    r"مادة\s*\(([0-9٠-٩]+)(?:\s+(مكرر(?:اً)?))?\)"
)

DIGITS = str.maketrans(
    '٠١٢٣٤٥٦٧٨٩',
    '0123456789'
)

doc_1 = "data/interim/constitution_2014_original.jsonl"
doc_2 = "data/interim/constitution_2014_amended_2019.jsonl"

with open(doc_1, mode="r", encoding="utf-8") as f:
    pages_1 = [json.loads(line) for line in f]

with open(doc_2, mode="r", encoding="utf-8") as f:
    pages_2 = [json.loads(line) for line in f]

def split_articles(pages: list[dict]):
    articles = []
    current = None
    expected = 1

    def close(end_page):
        current["text"] = current["text"].strip()
        current["end_page"] = end_page
        articles.append(current)

    # the last two pages are the footer
    for page in pages[:-2]:
        for line in page["text"].split("\n"):
            line = line.strip()
            if not line:
                continue

            # pass 1: pick the matches that are real article starts
            accepted = []
            matches = re.finditer(ARTICLE_PATTERN, line)
            for m in matches:
                number = int(m.group(1).translate(DIGITS))
                if number == expected-1 and m.group(2) is not None:
                    accepted.append(m)  # suffixed article
                elif number == expected:
                    accepted.append(m)
                    expected += 1

            # no article starts: the line continues the current article
            if not accepted:
                if current:
                    current["text"] += " " + line
                    current["end_page"] = page["page"]
                continue

            # text before the first accepted match belongs to the previous article
            prefix = line[:accepted[0].start()].strip()
            if current:
                current["text"] += " " + prefix
                close(page["page"])

            # pass 2: start a new article at each accepted match
            for i, m in enumerate(accepted):
                end = accepted[i+1].start() if i+1 < len(accepted) else len(line)
                new = {
                    "article_number": int(m.group(1).translate(DIGITS)),
                    "suffix": m.group(2),
                    "source_version": page["source_version"],
                    "start_page": page["page"],
                    "end_page": page["page"],
                    "text": line[m.end():end].strip(),
                }
                if i+1 < len(accepted):  # article fully contained in this line
                    articles.append(new)
                else:
                    current = new

    if current:
        current["text"] = current["text"].strip()
        articles.append(current)

    return articles

results_1 = split_articles(pages_1)
results_2 = split_articles(pages_2)

with open("data/processed/constitution_2014_original_articles.jsonl", mode="w", encoding="utf-8") as f:
    for article in results_1:
        f.write(json.dumps(article, ensure_ascii=False) + "\n")

with open("data/processed/constitution_2014_amended_2019_articles.jsonl", mode="w", encoding="utf-8") as f:
    for article in results_2:
        f.write(json.dumps(article, ensure_ascii=False) + "\n")
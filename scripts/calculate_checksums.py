from pathlib import Path
import hashlib

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


for path in Path("data/raw").glob("*.pdf"):
    print(path.name, sha256_file(path))

for path in Path("data/interim").glob("*.jsonl"):
    print(path.name, sha256_file(path))
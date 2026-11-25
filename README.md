## Text Extraction and Quality Assurance

The Arabic text of both constitutional versions was extracted using the OCR model [`NAMAA-Space/Qari-OCR-0.4.0-VL-4B-Instruct`](https://huggingface.co/NAMAA-Space/Qari-OCR-0.4.0-VL-4B-Instruct), followed by manual review and correction.

### Extraction Process

- **2014 Original Constitution:** The original PDF did not contain a text layer, so OCR was necessary to extract its Arabic content.
- **2019 Amended Constitution:** Initial text extraction using PyMuPDF (`get_text()`) produced messy and unreliable output. Consequently, OCR was used instead.

### Manual Review

After OCR extraction, I manually reviewed both extracted texts against their respective source documents and corrected minor OCR errors and formatting issues.

### Data Integrity

- Original source PDFs are preserved unchanged.
- Extracted text is stored in JSONL format.
- Each JSONL record includes its page number and constitutional version.
- Manual corrections were made to the extracted text without modifying the original source documents.
- OCR output was reviewed manually; perfect transcription accuracy is not assumed.


### Article-Level Segmentation

Implemented an article segmentation pipeline to transform page-level OCR output into individual constitutional articles.

The segmentation process handles:

- Arabic article numbering.
- Articles spanning multiple pages.
- Multiple articles appearing on the same page or line.
- Suffixed articles, such as `مادة (٢٤٤ مكرر)`.
- In-text references to other articles, which must not be mistaken for article headings.
- OCR reading-order inconsistencies in article headings.

The resulting article records retain their source page information and original Arabic text.

### Arabic Text Normalization

Implemented Arabic text normalization for retrieval while preserving the original extracted text.

The intended normalization operations include:

- Removing Arabic diacritics.
- Removing tatweel characters.
- Normalizing Alef variants.
- Normalizing Yeh variants.
- Standardizing whitespace.

Original text and normalized search text are stored separately to avoid losing the source wording.

### Article Data Schema and Validation

Defined a Pydantic model to validate the article records and maintain a consistent data structure across both constitutional versions.

The schema includes:

| Field | Description |
|---|---|
| `article_id` | Unique identifier for an article within a version |
| `lineage_id` | Identifier connecting corresponding articles across versions |
| `version` | Original or amended version |
| `number` | Article number |
| `suffix` | Article suffix, when present |
| `text_ar` | Original Arabic article text |
| `text_ar_search` | Normalized Arabic text for retrieval |
| `start_page` | First source page |
| `end_page` | Last source page |
| `status` | Article status |
| `refs` | References to other articles |

### Article Lineage Matching

Implemented article lineage matching between the original 2014 Constitution and its 2019 amended version.

The purpose of lineage tracking is to connect corresponding articles across versions, allowing the system to identify and trace constitutional changes.

The `lineage_id` field provides a stable identifier for connecting related article records across versions.

---

## Current Project Structure

```text
data/
├── raw/
│   ├── constitution_2014_original.pdf
│   ├── constitution_2014_amended_2019.pdf
│   └── SOURCES.md
│
├── interim/
│   ├── constitution_2014_original.jsonl
│   ├── constitution_2014_original_articles.jsonl
│   ├── constitution_2014_amended_2019.jsonl
│   └── constitution_2014_amended_2019_articles.jsonl
│
└── processed/
    ├── constitution_2014_original_articles.jsonl
    ├── constitution_2014_amended_2019_articles.jsonl
    └── changes.jsonl
```

## Next Development Milestones

- [ ] Cross-reference extraction and validation.
- [ ] Article-level chunking and metadata enrichment.
- [ ] Exact article lookup.
- [ ] BM25 lexical retrieval baseline.
- [ ] Initial retrieval evaluation dataset.
- [ ] Dense and hybrid retrieval.
- [ ] Citation-grounded answer generation and abstention.
- [ ] API development and evaluation.
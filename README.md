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
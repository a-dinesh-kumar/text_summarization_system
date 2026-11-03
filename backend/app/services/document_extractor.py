from io import BytesIO
from pathlib import Path

import pymupdf
from docx import Document


class DocumentExtractionError(Exception):
    """Raised when an uploaded document cannot be converted to readable text."""


def extract_text(filename: str, content: bytes) -> str:
    suffix = Path(filename).suffix.lower()

    try:
        if suffix == ".pdf":
            with pymupdf.open(stream=content, filetype="pdf") as pdf:
                text = "\\n".join(page.get_text("text") for page in pdf)
        elif suffix == ".docx":
            document = Document(BytesIO(content))
            paragraphs = [p.text for p in document.paragraphs if p.text.strip()]
            table_text = [
                " ".join(
                    cell.text.strip()
                    for row in table.rows
                    for cell in row.cells
                    if cell.text.strip()
                )
                for table in document.tables
            ]
            text = "\\n".join(paragraphs + table_text)
        elif suffix == ".txt":
            try:
                text = content.decode("utf-8-sig")
            except UnicodeDecodeError:
                text = content.decode("latin-1")
        else:
            raise DocumentExtractionError(
                "Unsupported file type. Upload a PDF, DOCX, or TXT file."
            )
    except DocumentExtractionError:
        raise
    except Exception as exc:
        raise DocumentExtractionError(
            f"Could not read the uploaded {suffix or 'document'} file."
        ) from exc

    text = text.strip()
    if not text:
        if suffix == ".pdf":
            raise DocumentExtractionError(
                "No selectable text was found in this PDF. Scanned/image-only PDF "
                "OCR is not supported in this version."
            )
        raise DocumentExtractionError(
            "The uploaded document contains no readable text."
        )

    return text

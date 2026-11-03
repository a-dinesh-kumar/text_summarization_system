from io import BytesIO

import pymupdf
import pytest
from docx import Document

from app.services.document_extractor import (
    DocumentExtractionError,
    extract_text,
)


def make_pdf(text):
    pdf = pymupdf.open()
    page = pdf.new_page()
    page.insert_text((72, 72), text)
    content = pdf.tobytes()
    pdf.close()
    return content


def make_docx(text):
    document = Document()
    document.add_paragraph(text)
    buffer = BytesIO()
    document.save(buffer)
    return buffer.getvalue()


def test_extracts_utf8_txt():
    result = extract_text("notes.txt", "Hello summarization".encode("utf-8"))
    assert result == "Hello summarization"


def test_extracts_utf8_bom_txt():
    result = extract_text("notes.txt", bytes([0xEF, 0xBB, 0xBF]) + b"Hello")
    assert result == "Hello"


def test_extracts_docx():
    result = extract_text("notes.docx", make_docx("A Word document paragraph."))
    assert "A Word document paragraph." in result


def test_extracts_pdf():
    result = extract_text("paper.pdf", make_pdf("Attention is all you need."))
    assert "Attention is all you need." in result


def test_rejects_unsupported_extension():
    with pytest.raises(DocumentExtractionError, match="Unsupported file type"):
        extract_text("notes.xlsx", b"some content")


def test_rejects_empty_or_scanned_pdf():
    empty_pdf = pymupdf.open()
    empty_pdf.new_page()
    content = empty_pdf.tobytes()
    empty_pdf.close()

    with pytest.raises(DocumentExtractionError, match="No selectable text"):
        extract_text("scanned.pdf", content)


def test_rejects_corrupt_pdf():
    with pytest.raises(DocumentExtractionError, match="Could not read"):
        extract_text("broken.pdf", b"not a PDF")

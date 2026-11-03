from io import BytesIO

import pymupdf
from docx import Document
import pytest
from fastapi.testclient import TestClient

import app.main as main
from app.core.config import Settings
from tests.conftest import FakeSummarizer


@pytest.fixture
def client(monkeypatch, settings):
    fake_model = FakeSummarizer()
    monkeypatch.setattr(main, "get_settings", lambda: settings)
    monkeypatch.setattr(main, "create_summarizer", lambda _settings: fake_model)

    with TestClient(main.app) as test_client:
        yield test_client


def test_health_reports_model_loaded(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ready", "model_loaded": True}


def test_root_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["docs"] == "/docs"


def test_summarize_text_success(client):
    response = client.post(
        "/api/v1/summarize",
        data={"text": "This is a short test document."},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["summary"] == "brief summary"
    assert body["source_type"] == "text"
    assert body["source_name"] is None
    assert body["source_characters"] == len("This is a short test document.")
    assert body["model_key"] == "fake"


def test_summarize_txt_upload_success(client):
    response = client.post(
        "/api/v1/summarize",
        files={"file": ("notes.txt", BytesIO(b"Text from an uploaded file."), "text/plain")},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["source_type"] == "document"
    assert body["source_name"] == "notes.txt"
    assert body["source_characters"] == len("Text from an uploaded file.")


def test_rejects_request_without_input(client):
    response = client.post("/api/v1/summarize")

    assert response.status_code == 400
    assert "exactly one input" in response.json()["detail"]


def test_rejects_text_and_file_together(client):
    response = client.post(
        "/api/v1/summarize",
        data={"text": "Some text"},
        files={"file": ("notes.txt", b"Some file text", "text/plain")},
    )

    assert response.status_code == 400
    assert "exactly one input" in response.json()["detail"]


def test_rejects_unsupported_upload(client):
    response = client.post(
        "/api/v1/summarize",
        files={"file": ("notes.xlsx", b"spreadsheet", "application/octet-stream")},
    )

    assert response.status_code == 422
    assert "Unsupported file type" in response.json()["detail"]


def test_rejects_empty_text(client):
    response = client.post("/api/v1/summarize", data={"text": "   "})

    assert response.status_code == 400


def test_rejects_upload_over_size_limit(monkeypatch, client):
    # The fixture's settings object is attached to the running app.
    client.app.state.settings.max_upload_size_mb = 0
    response = client.post(
        "/api/v1/summarize",
        files={"file": ("notes.txt", b"more than zero bytes", "text/plain")},
    )

    assert response.status_code == 413
    assert "upload limit" in response.json()["detail"]


def test_rejects_text_over_character_limit(client):
    client.app.state.settings.max_document_characters = 5
    response = client.post(
        "/api/v1/summarize",
        data={"text": "sixsix"},
    )

    assert response.status_code == 413
    assert "Maximum supported size" in response.json()["detail"]


def test_summarize_pdf_upload_success(client):
    pdf = pymupdf.open()
    page = pdf.new_page()
    page.insert_text((72, 72), "PDF content for API testing.")
    content = pdf.tobytes()
    pdf.close()

    response = client.post(
        "/api/v1/summarize",
        files={"file": ("sample.pdf", content, "application/pdf")},
    )

    assert response.status_code == 200
    assert response.json()["source_name"] == "sample.pdf"
    assert response.json()["source_type"] == "document"


def test_summarize_docx_upload_success(client):
    document = Document()
    document.add_paragraph("DOCX content for API testing.")
    buffer = BytesIO()
    document.save(buffer)

    response = client.post(
        "/api/v1/summarize",
        files={
            "file": (
                "sample.docx",
                buffer.getvalue(),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
    )

    assert response.status_code == 200
    assert response.json()["source_name"] == "sample.docx"
    assert response.json()["source_type"] == "document"

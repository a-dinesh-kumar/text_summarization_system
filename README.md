# Text Summarization System

A Docker-first FastAPI backend for summarizing pasted text and uploaded PDF, DOCX, and TXT documents. The backend supports interchangeable Hugging Face summarization models.

## Features

- Text input or PDF / DOCX / TXT upload
- BART-large-CNN and FLAN-T5-small selected through `SUMMARIZATION_MODEL`
- Sentence-aware chunking and map/reduce summarization
- Model loaded once during application startup
- FastAPI Swagger documentation
- Docker Compose development workflow with hot reload
- Persistent Hugging Face model cache
- Automated unit, API, and integration tests using pytest and a lightweight fake model

Scanned/image-only PDF OCR is not included. Such PDFs return a clear extraction error.

## Prerequisites

- Docker Desktop with Docker Compose
- Git

The Docker image provides Python 3.13.15 and CPU-only PyTorch. A host Python virtual environment is not required for the Docker workflow.

## Configure

From the repository root:

```powershell
Copy-Item backend/.env.example backend/.env
```

Set `SUMMARIZATION_MODEL=bart` or `SUMMARIZATION_MODEL=flan_t5` in `backend/.env`.

Do not commit `backend/.env`. It is ignored by Git. Commit `.env.example` instead.

## Build and run locally

```powershell
docker compose build
docker compose up -d
docker compose ps
docker compose logs -f backend
```

Open:

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Health: http://localhost:8000/health

Development mode mounts the backend source code into the container and enables Uvicorn hot reload.

Stop:

```powershell
docker compose down
```

The named Hugging Face cache volume remains. To delete it as well:

```powershell
docker compose down -v
```

## Run automated backend tests

The development image contains pytest and HTTPX. Run the suite inside Docker:

```powershell
docker compose run --rm backend pytest -v
```

For a concise summary:

```powershell
docker compose run --rm backend pytest -q
```

The tests use a fake summarizer. They do not download or load BART/T5, so routine test runs should be much faster than real inference.

Test coverage includes:

- Text extraction from TXT, PDF, and DOCX
- Empty, corrupt, and unsupported documents
- Sentence splitting and chunking
- Model factory selection and invalid model configuration
- Map/reduce summarization service
- API text and TXT upload success paths
- Missing, conflicting, oversized, and unsupported API inputs
- Health endpoint and end-to-end service flow

## Switch models

Change `SUMMARIZATION_MODEL` in `backend/.env`, then recreate the container:

```powershell
docker compose up -d --force-recreate
```

The model cache is persisted in a named volume.

## Production image

The Dockerfile has separate build targets:

- `development`: includes pytest and runs Uvicorn with `--reload`
- `production`: excludes test dependencies and runs Uvicorn without `--reload`

The current `docker-compose.yml` intentionally selects the development target. `docker-compose.prod.yml` selects the production target, does not mount source code from the host, and does not enable hot reload.

Example production image build:

```powershell
docker compose -f docker-compose.prod.yml build\ndocker compose -f docker-compose.prod.yml up -d
```

Before deployment, configure environment variables and persistent model storage appropriate to the hosting platform. Measure memory and inference time; Docker does not reduce model RAM requirements.

## API

`POST /api/v1/summarize`

Send exactly one multipart form field:

- `text`: pasted text
- `file`: a `.pdf`, `.docx`, or `.txt` file

The response contains the generated summary, source metadata, selected model, token/chunk counts, reduction levels, and processing time.

## Current limitations

- OCR for scanned PDFs is not implemented.
- Sentence splitting is a lightweight rule-based baseline and may need improvement for complex layouts and abbreviations.
- CPU inference may be slow for large documents.
- Before public deployment, add authentication, rate limiting, stronger file validation, structured logging, and model-specific quality evaluation.

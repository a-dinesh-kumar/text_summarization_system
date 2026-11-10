# Text Summarization System

An AI-powered text summarization application that converts lengthy text and documents into concise, meaningful summaries using transformer-based language models.

The application supports direct text input and document uploads, with a React frontend, FastAPI backend, and Docker-based development environment.

## Live Demo


---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Key Features](#2-key-features)
3. [Application Architecture](#3-application-architecture)
4. [Technology Stack](#4-technology-stack)
5. [Supported Summarization Models](#5-supported-summarization-models)
6. [Project Structure](#6-project-structure)
7. [Application Workflow](#7-application-workflow)
8. [Getting Started](#8-getting-started)
9. [Environment Configuration](#9-environment-configuration)
10. [Running with Docker](#10-running-with-docker)
11. [API Documentation](#11-api-documentation)
12. [Input Validation](#12-input-validation)
13. [Document Processing](#13-document-processing)
14. [Testing](#14-testing)
15. [Model Configuration and Switching](#15-model-configuration-and-switching)
16. [Troubleshooting](#16-troubleshooting)
17. [Future Enhancements](#17-future-enhancements)
18. [Author](#18-author)

---

## 1. Project Overview

Reading lengthy documents, research materials, technical articles, and other content can be time-consuming.

The Text Summarization System addresses this problem by using transformer-based NLP models to generate concise summaries while retaining the important information from the original content.

Users can:

- Enter text directly into the application.
- Upload PDF, DOCX, or TXT documents.
- Generate summaries using configured transformer models.
- View processing information, including the selected model and processing time.
- Copy or download the generated summary.

The application is designed with a modular architecture so that different summarization models can be evaluated and configured without changing the overall application workflow.

## 2. Key Features

### Text Summarization
- Summarize content entered directly into the application.
- Process lengthy text using chunk-based summarization.
- Generate concise summaries using transformer-based models.

### Document Upload
- Upload PDF documents.
- Upload Microsoft Word documents (DOCX).
- Upload plain text files (TXT).
- Extract document text before summarization.

### Multiple Model Support
- BART-large-CNN.
- FLAN-T5-small.
- Configurable model selection.

### Input Validation
- Reject empty and whitespace-only inputs.
- Reject punctuation-only inputs.
- Require at least 50 meaningful characters.
- Validate both directly entered text and extracted document content.
- Enforce document size and text length limits.

### Processing Information
The application provides useful processing metadata, including:

- Selected summarization model.
- Source type and document name.
- Source character count.
- Source token count.
- Initial chunk count.
- Total generation chunks.
- Reduction levels.
- Processing time.

### User Interface
- React-based responsive interface.
- Text input and document upload modes.
- Input validation and error handling.
- Loading indicators.
- Copy summary functionality.
- Download summary functionality.
- GitHub and LinkedIn profile links.

### Development and Testing
- Docker-based backend environment.
- Automated backend test suite.
- Mock-based testing for API and application logic.
- Separate application and test dependencies.

## 3. Application Architecture

The application follows a frontend-backend architecture.

```text
                 USER
                   |
                   v
          REACT FRONTEND
           (React + Vite)
                   |
          Text Input / Upload
                   |
                   v
             FASTAPI
              BACKEND
                   |
          Input Validation
                   |
                   v
          TEXT EXTRACTION
           PDF / DOCX / TXT
                   |
                   v
          TEXT PREPROCESSING
                   |
                   v
          CHUNKING PIPELINE
                   |
                   v
        SUMMARIZATION SERVICE
                   |
             +-----+-----+
             |           |
             v           v
       BART-LARGE-CNN  FLAN-T5-SMALL
             |           |
             +-----+-----+
                   |
                   v
          SUMMARY GENERATION
                   |
                   v
           API RESPONSE
                   |
                   v
            REACT FRONTEND
                   |
                   v
          DISPLAY SUMMARY
```

### Architectural Components

| Component | Responsibility |
|---|---|
| React + Vite | User interface and user interactions |
| FastAPI | REST API and request handling |
| Input Validation | Validates input before model inference |
| Document Extraction | Extracts text from uploaded documents |
| Text Processing | Prepares text for summarization |
| Chunking Pipeline | Splits lengthy content into manageable sections |
| Summarization Service | Coordinates model inference |
| BART / FLAN-T5 | Generates summaries |
| Docker | Provides a consistent backend development environment |
| Pytest | Automated backend testing |

## 4. Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Frontend | React, JavaScript, Vite |
| Backend | FastAPI |
| Machine Learning | Hugging Face Transformers |
| NLP Models | BART-large-CNN, FLAN-T5-small |
| Deep Learning | PyTorch |
| Document Processing | PyMuPDF, python-docx |
| API Testing | Postman, FastAPI Swagger UI |
| Automated Testing | Pytest, HTTPX |
| Containerization | Docker, Docker Compose |
| Version Control | Git, GitHub |

## 5. Supported Summarization Models

The application supports two transformer-based summarization models.

### BART-large-CNN

BART is a sequence-to-sequence transformer model based on a denoising autoencoder architecture.

It is particularly useful for abstractive summarization tasks.

**Characteristics:**
- Designed for text generation and summarization.
- Produces more detailed and contextually relevant summaries in the project's evaluation.
- Requires comparatively more computational resources.
- Takes longer to process lengthy documents.

### FLAN-T5-small

FLAN-T5 is an instruction-tuned version of the T5 transformer architecture.

It uses a text-to-text approach, where both inputs and outputs are represented as text.

**Characteristics:**
- Smaller and comparatively lightweight.
- Faster inference in the project's evaluation.
- Supports instruction-based text generation.
- Produced lower summarization quality than BART in the project's initial evaluation.

### Model Comparison

| Evaluation Metric | BART-large-CNN | FLAN-T5-small |
|---|---:|---:|
| ROUGE-1 | 0.4575 | 0.1998 |
| ROUGE-2 | 0.1762 | 0.0409 |
| ROUGE-L | 0.3419 | 0.1638 |
| Inference Time (Full Document) | 427.79 sec | 83.39 sec |
| Initial Chunks | 11 | 23 |
| Reduction Levels | 1 | 2 |

**Evaluation note:** These measurements come from the project's earlier model evaluation using the same full-document input. They are experimental results, not guaranteed performance benchmarks. Actual processing time depends on hardware, document size, and runtime conditions.

BART demonstrated stronger summarization quality in this evaluation, while FLAN-T5-small offered faster processing.

The application supports configurable model selection so that the models can be tested and compared.

## 6. Project Structure

```text
text_summarization_system/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       └── summarize.py
│   │   │
│   │   ├── core/
│   │   │   └── config.py
│   │   │
│   │   ├── services/
│   │   │   ├── input_validation.py
│   │   │   └── ...
│   │   │
│   │   ├── models/
│   │   ├── schemas/
│   │   └── main.py
│   │
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── ...
│   │
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── requirements-test.txt
│   ├── pytest.ini
│   ├── .env
│   └── .env.example
│
├── frontend/
│   ├── public/
│   │   └── icons/
│   │       ├── github.png
│   │       └── linkedin.png
│   │
│   ├── src/
│   │   ├── App.jsx
│   │   ├── api.js
│   │   ├── main.jsx
│   │   └── styles.css
│   │
│   ├── package.json
│   └── vite.config.js
│
├── .dockerignore
├── .gitignore
├── docker-compose.yml
└── README.md
```

The structure above highlights the main application components. Additional files and service modules may exist as the implementation evolves.

## 7. Application Workflow

### Text Input Workflow

1. User selects text input mode.
2. User enters the content.
3. Frontend checks the meaningful character count.
4. User submits the request.
5. FastAPI performs server-side validation.
6. The summarization service processes the content.
7. The selected transformer model generates the summary.
8. FastAPI returns the summary and processing metadata.
9. Frontend displays the result.

### Document Upload Workflow

1. User selects document upload mode.
2. User uploads a PDF, DOCX, or TXT file.
3. Backend validates the uploaded file.
4. The appropriate document extraction component extracts text.
5. Extracted content undergoes meaningful character validation.
6. Valid content enters the summarization pipeline.
7. The model generates the summary.
8. The application displays the generated summary and metadata.

### Long Document Processing

Transformer models have input token limits. Therefore, lengthy documents cannot always be passed to a model in a single request.

The application uses a chunk-based processing approach:

1. Tokenize the source content.
2. Divide the content into manageable chunks.
3. Generate summaries for individual chunks.
4. Combine intermediate summaries when necessary.
5. Apply additional reduction levels when required.
6. Produce the final summary.

This approach enables the application to handle content that exceeds the model's individual input token limit.

## 8. Getting Started

### Prerequisites

Install the following tools:

- Git
- Docker Desktop
- Docker Compose (included with current Docker Desktop installations)
- Node.js and npm (for frontend development outside Docker)
- VS Code or another code editor

For local development, Docker Desktop should be running before executing Docker commands.

### Clone the Repository

```bash
git clone https://github.com/a-dinesh-kumar/text_summarization_system
cd text_summarization_system
```

### Backend Setup

The backend runs inside Docker.

Create your local environment configuration:

```bash
copy backend\.env.example backend\.env
```

Update the required configuration values in `backend/.env`.

### Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
```

Start the frontend development server:

```bash
npm run dev
```

The frontend should be available at:

```text
http://localhost:5173
```

### Start the Backend

From the project root:

```bash
docker compose up --build
```

The backend API should be available at:

```text
http://localhost:8000
```

Health endpoint:

```text
http://localhost:8000/health
```

Swagger API documentation:

```text
http://localhost:8000/docs
```

## 9. Environment Configuration

Backend configuration is maintained in:

```text
backend/.env
```

Use `backend/.env.example` as the template.

Example configuration:

```env
SUMMARIZATION_MODEL=bart
HF_HOME=/app/.cache/huggingface
```

The application supports:

| Variable | Purpose |
|---|---|
| `SUMMARIZATION_MODEL` | Selects the summarization model |
| `HF_HOME` | Configures the Hugging Face model cache |
| `CORS_ORIGINS` | Configures permitted frontend origins |

Frontend configuration is maintained using Vite environment variables.

Example:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_MAX_UPLOAD_SIZE_MB=15
VITE_GITHUB_URL=https://github.com/your-username
VITE_LINKEDIN_URL=https://www.linkedin.com/in/your-profile/
```

Update the profile URLs with your actual public profile links.

**Important:**
- Never commit `.env` files containing local or sensitive configuration.
- Commit `.env.example` files so other developers can understand the required configuration.
- Restart the relevant development process after changing environment variables.

## 10. Running with Docker

Docker provides a consistent backend runtime environment.

### Start Containers

```bash
docker compose up --build
```

### Run in Detached Mode

```bash
docker compose up -d --build
```

### View Running Containers

```bash
docker compose ps
```

### View Backend Logs

```bash
docker compose logs -f backend
```

### Stop Containers

```bash
docker compose down
```

### Run Backend Tests

```bash
docker compose exec backend pytest
```

### Model Cache

The Docker Compose configuration uses a named volume for the Hugging Face model cache.

This prevents model files from needing to be downloaded again every time the backend container is recreated.

## 11. API Documentation

The backend exposes REST APIs through FastAPI.

### Health Check

**Endpoint**

```http
GET /health
```

Used to verify backend availability.

### Generate Summary

**Endpoint**

```http
POST /api/v1/summarize
```

The API supports two input modes:

- Direct text input.
- Document upload.

Provide exactly one input type per request.

### Text Input Example

```bash
curl -X POST "http://localhost:8000/api/v1/summarize" \
  -F "text=Your meaningful text content goes here..."
```

### Document Upload Example

```bash
curl -X POST "http://localhost:8000/api/v1/summarize" \
  -F "file=@document.pdf"
```

### Example Response

```json
{
  "summary": "The generated summary appears here.",
  "source_type": "text",
  "source_name": null,
  "source_characters": 1200,
  "model": "BART-large-CNN",
  "model_key": "bart",
  "source_tokens": 260,
  "initial_chunk_count": 1,
  "total_generation_chunks": 1,
  "reduction_levels": 0,
  "processing_time_seconds": 22.424
}
```

The values above illustrate the response structure; actual values depend on the input and model execution.

### Interactive API Testing

FastAPI provides Swagger UI for exploring and testing the endpoints:

```text
http://localhost:8000/docs
```

You can use Swagger UI to:

- Inspect API request and response schemas.
- Submit text input.
- Upload supported documents.
- Verify validation errors.
- Test backend functionality independently of the frontend.

## 12. Input Validation

The application performs validation at both frontend and backend levels.

### Meaningful Character Validation

A minimum of 50 meaningful characters is required.

Meaningful characters include:

- Alphabetic characters.
- Numeric characters.
- Unicode letters and numbers.

Whitespace and punctuation do not contribute to the meaningful character count.

Examples:

| Input | Expected Result |
|---|---|
| Empty input | Rejected |
| Whitespace only | Rejected |
| Punctuation only | Rejected |
| Fewer than 50 meaningful characters | Rejected |
| Exactly 50 meaningful characters | Accepted |
| More than 50 meaningful characters | Accepted |

### Why Both Frontend and Backend Validation?

Frontend validation provides immediate feedback and improves user experience.

Backend validation ensures that invalid requests are rejected even when someone bypasses the frontend and calls the API directly.

This creates a consistent validation mechanism across both input methods.

### Other Limits

- Maximum upload size: 15 MB.
- Maximum extracted/input text length: 500,000 characters.
- Supported document formats: PDF, DOCX, TXT.

## 13. Document Processing

The application supports text extraction from common document formats.

| Format | Processing Approach |
|---|---|
| PDF | PyMuPDF |
| DOCX | python-docx |
| TXT | Standard text file processing |

After extraction, the content passes through the same validation and summarization pipeline used for direct text input.

**Current limitation:** Image-only or scanned PDFs may not contain an extractable text layer. OCR support can be introduced as a future enhancement.

## 14. Testing

Backend testing is implemented using Pytest and HTTPX.

The test suite covers application and API behaviour, including:

- Meaningful character counting.
- Empty and whitespace-only input validation.
- Punctuation-only input validation.
- Minimum character requirements.
- Valid text input.
- Text upload.
- PDF extraction and upload.
- DOCX extraction and upload.
- API validation and error handling.
- Summarization request handling.

### Execute the Test Suite

Make sure the backend container is running:

```bash
docker compose up -d
```

Execute:

```bash
docker compose exec backend pytest
```

### Latest Test Status

**37 tests passed**, as reported during the project's development validation.

The test suite uses mocked model behaviour where appropriate, so automated test success validates application logic and API workflows rather than proving the quality of actual model-generated summaries.

Actual model inference should also be verified separately using meaningful input.

## 15. Model Configuration and Switching

The summarization model can be configured through the backend environment file.

Open:

```text
backend/.env
```

For BART:

```env
SUMMARIZATION_MODEL=bart
```

For FLAN-T5:

```env
SUMMARIZATION_MODEL=flan_t5
```

After changing the model, recreate the backend container so that the updated configuration is loaded:

```bash
docker compose up -d --force-recreate backend
```

The model is loaded during backend startup and reused for subsequent requests.

This avoids loading the model separately for every summarization request.

## 16. Troubleshooting

### Docker Is Not Running

**Problem:** Docker commands fail because the Docker daemon is unavailable.

**Solution:**
1. Start Docker Desktop.
2. Verify that the Docker engine is running.
3. Retry the Docker Compose command.

### Backend Is Not Accessible

**Problem:** Frontend requests fail to connect to the backend.

**Solution:**

Check the running containers:

```bash
docker compose ps
```

Check backend logs:

```bash
docker compose logs -f backend
```

Verify:

```text
http://localhost:8000/health
```

### Model Download Takes Time

**Problem:** The first application startup takes longer than expected.

**Reason:** Hugging Face needs to download the configured model and its dependencies.

**Solution:** Allow the initial model download to complete. Subsequent startups can reuse the persistent model cache.

### Input Validation Error

**Problem:** The application rejects the submitted content.

**Reason:** The content may contain fewer than 50 meaningful characters or exceed the configured input limits.

**Solution:** Provide sufficient meaningful content and retry.

### Frontend Cannot Reach Backend

**Problem:** The frontend cannot communicate with FastAPI.

**Solution:**
- Verify that the backend is running.
- Check `VITE_API_BASE_URL`.
- Confirm that the configured CORS origins permit the frontend origin.
- Restart the relevant development processes after configuration changes.

## 17. Future Enhancements

Potential improvements include:

- OCR support for scanned and image-based PDFs.
- Additional transformer-based summarization models.
- Summary length and output-style controls.
- Improved evaluation using ROUGE and other summarization metrics.
- Production-ready frontend and backend container orchestration.
- Cloud deployment and monitoring.
- Performance optimization for lengthy documents.
- More comprehensive end-to-end testing.
- Support for additional document formats.

## 18. Author

**Dinesh Kumar Alagarsamy**

*Software Quality Engineer / SDET*

- **GitHub:** [https://github.com/a-dinesh-kumar](https://github.com/a-dinesh-kumar)
- **LinkedIn:** [https://www.linkedin.com/in/dinesh-kumar-alagarsamy](https://www.linkedin.com/in/dinesh-kumar-alagarsamy)

### Areas of Interest

- Quality Engineering
- Test Automation
- API Testing
- Artificial Intelligence
- Machine Learning
- AI-powered Testing
- Software Architecture
- Generative AI and Agentic AI

---

*Built as part of my learning journey in NLP, transformer models, FastAPI, React, Docker, and AI application development.*
# Text Summarization System

An AI-powered application that transforms lengthy text and documents into concise, meaningful summaries using the **Gemini Developer API**.

The application supports direct text input and document uploads through a React frontend and FastAPI backend. It uses a chunk-based summarization pipeline to process longer content and is containerized with Docker for consistent backend development and deployment.

## Live Demo

**Application:** https://text-summarization-system-ieit.onrender.com/

**Backend API:** https://text-summarization-api-ordi.onrender.com

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Key Features](#2-key-features)
3. [Application Architecture](#3-application-architecture)
4. [Technology Stack](#4-technology-stack)
5. [Summarization Approach](#5-summarization-approach)
6. [Project Structure](#6-project-structure)
7. [Application Workflow](#7-application-workflow)
8. [Getting Started](#8-getting-started)
9. [Environment Configuration](#9-environment-configuration)
10. [Running with Docker](#10-running-with-docker)
11. [API Documentation](#11-api-documentation)
12. [Input Validation](#12-input-validation)
13. [Document Processing](#13-document-processing)
14. [Testing](#14-testing)
15. [Deployment Architecture](#15-deployment-architecture)
16. [Troubleshooting](#16-troubleshooting)
17. [Future Enhancements](#17-future-enhancements)
18. [Author](#18-author)

---

## 1. Project Overview

Reading lengthy documents, research materials, technical articles, and other content can be time-consuming.

The Text Summarization System addresses this problem by using a generative AI model to produce concise summaries while retaining important information from the original content.

Users can:

- Enter text directly into the application.
- Upload PDF, DOCX, or TXT documents.
- Generate summaries using the Gemini Developer API.
- Process longer content through a chunk-based summarization pipeline.
- View processing information, including the model used and processing time.
- Copy or download the generated summary.

The application separates the user interface, API layer, document processing, and summarization logic to keep the implementation modular and maintainable.

## 2. Key Features

### Text Summarization

- Summarize content entered directly into the application.
- Process lengthy text using chunk-based summarization.
- Generate summaries through the Gemini Developer API.
- Return processing metadata along with the generated summary.

### Document Upload

- Upload PDF documents.
- Upload Microsoft Word documents (DOCX).
- Upload plain text files (TXT).
- Extract document content before summarization.
- Process extracted content through the same summarization pipeline as direct text input.

### AI-Powered Summarization

- Integrates with Google's Gemini Developer API.
- Uses the Google GenAI Python SDK.
- Keeps model configuration outside the application code.
- Uses chunking and reduction stages to handle longer documents.
- Avoids downloading and hosting large transformer model weights in the backend container.

### Input Validation

- Reject empty and whitespace-only inputs.
- Reject punctuation-only inputs.
- Require at least 50 meaningful characters.
- Validate both direct text and extracted document content.
- Enforce upload size and maximum input text limits.
- Validate requests on the backend even when frontend validation is bypassed.

### Processing Information

The application returns processing metadata, including:

- Selected model.
- Source type and document name.
- Source character count.
- Source token count.
- Initial chunk count.
- Total generation chunks.
- Reduction levels.
- Processing time.

### User Interface

- Responsive React-based interface.
- Text input and document upload modes.
- Loading indicators and error handling.
- Copy summary functionality.
- Download summary functionality.
- GitHub and LinkedIn profile links.

### Development and Testing

- Docker-based backend environment.
- Docker Compose for local development.
- Automated backend tests using Pytest and HTTPX.
- Mock-based tests for summarization and API logic.
- Environment-based configuration for local and production deployments.

## 3. Application Architecture

The application follows a decoupled frontend-backend architecture. The frontend is responsible for user interactions, while the backend handles validation, document extraction, text processing, and communication with the Gemini API.

### High-Level Architecture

```text
                         USER
                           |
                           v
                  REACT FRONTEND
                    React + Vite
                           |
                 Text Input / File Upload
                           |
                           v
                    FASTAPI BACKEND
                           |
                    INPUT VALIDATION
                           |
              +------------+------------+
              |                         |
              v                         v
        DIRECT TEXT INPUT        DOCUMENT EXTRACTION
                                  PDF / DOCX / TXT
              |                         |
              +------------+------------+
                           |
                           v
                    TEXT PROCESSING
                           |
                           v
                    CHUNKING PIPELINE
                           |
                           v
                  SUMMARIZATION SERVICE
                           |
                           v
                 GEMINI DEVELOPER API
                   Google GenAI SDK
                           |
                           v
                 SUMMARY GENERATION
                  Chunk / Reduction
                           |
                           v
                     API RESPONSE
                           |
                           v
                    REACT FRONTEND
                           |
                           v
                  DISPLAY GENERATED SUMMARY
```

### Deployment Architecture

```text
                    USER'S BROWSER
                           |
                           v
                  RENDER STATIC SITE
                    React + Vite
                           |
                     HTTPS API Call
                           |
                           v
                  RENDER WEB SERVICE
                   Docker + FastAPI
                           |
                     Google GenAI SDK
                           |
                           v
                 GEMINI DEVELOPER API
```

The frontend and backend are deployed as separate Render services:

| Service | Responsibility |
|---|---|
| Render Static Site | Hosts the built React frontend |
| Render Web Service | Runs the Dockerized FastAPI backend |
| Gemini Developer API | Performs AI-powered summary generation |

The frontend communicates with the backend through the configured API base URL. The backend communicates with Gemini using a server-side API key.

### Architectural Components

| Component | Responsibility |
|---|---|
| React + Vite | User interface and interactions |
| FastAPI | REST API and request handling |
| Input Validation | Validates text and uploaded content |
| Document Extraction | Extracts content from PDF, DOCX, and TXT |
| Text Processing | Prepares source content for summarization |
| Chunking Pipeline | Divides long content into manageable sections |
| Summarization Service | Coordinates summary generation |
| Google GenAI SDK | Connects the backend to Gemini |
| Gemini Developer API | Generates summaries |
| Docker | Provides a consistent backend runtime |
| Docker Compose | Simplifies local backend execution |
| Pytest + HTTPX | Automated backend testing |

## 4. Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python, JavaScript |
| Frontend | React, Vite |
| Backend | FastAPI |
| Generative AI | Google Gemini Developer API |
| AI Integration | Google GenAI Python SDK |
| Document Processing | PyMuPDF, python-docx |
| API Testing | FastAPI Swagger UI, Postman |
| Automated Testing | Pytest, HTTPX |
| Containerization | Docker, Docker Compose |
| Deployment | Render |
| Version Control | Git, GitHub |

## 5. Summarization Approach

### Gemini Developer API

The application uses the Gemini Developer API for AI-powered text summarization.

The backend integrates with Gemini through Google's GenAI Python SDK.

**Why use an external AI API?**

During development, local transformer models such as BART-large-CNN and FLAN-T5-small were evaluated for summarization quality and performance.

Although BART produced stronger results in the initial evaluation, running large transformer models required significant memory and processing resources. This became a limitation when targeting Render's free deployment resources.

The application was therefore migrated to the Gemini Developer API.

This approach:

- Avoids loading large model weights into the backend container.
- Reduces backend memory requirements.
- Simplifies model integration and configuration.
- Makes deployment on resource-constrained hosting more practical.
- Allows the backend to focus on document processing and application logic.

The Gemini model is configured through backend environment variables rather than being hardcoded into the application.

### Earlier Transformer Model Evaluation

BART-large-CNN and FLAN-T5-small were evaluated during the earlier development phase.

The following measurements were recorded using the same full-document input:

| Evaluation Metric | BART-large-CNN | FLAN-T5-small |
|---|---:|---:|
| ROUGE-1 | 0.4575 | 0.1998 |
| ROUGE-2 | 0.1762 | 0.0409 |
| ROUGE-L | 0.3419 | 0.1638 |
| Inference Time | 427.79 sec | 83.39 sec |
| Initial Chunks | 11 | 23 |
| Reduction Levels | 1 | 2 |

**Evaluation note:** These are historical experimental results from the local transformer-model evaluation. They are not benchmarks for the current Gemini-powered implementation. Actual Gemini response time and output quality depend on the configured model, input size, API conditions, and generation settings.

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
│   │   │   ├── document_extraction.py
│   │   │   ├── gemini_summarizer.py
│   │   │   └── ...
│   │   │
│   │   ├── schemas/
│   │   ├── models/
│   │   └── main.py
│   │
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── ...
│   │
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── .env
│   └── .env.example
│
├── frontend/
│   ├── public/
│   │   └── icons/
│   │
│   ├── src/
│   │   ├── App.jsx
│   │   ├── api.js
│   │   ├── main.jsx
│   │   └── styles.css
│   │
│   ├── .env.example
│   ├── package.json
│   └── vite.config.js
│
├── .dockerignore
├── .gitignore
├── docker-compose.yml
└── README.md
```

The structure above highlights the main application components. Additional modules and configuration files may exist as the implementation evolves.

## 7. Application Workflow

### Text Input Workflow

1. User selects text input mode.
2. User enters the content.
3. Frontend performs initial input validation.
4. User submits the request.
5. FastAPI validates the incoming content.
6. The summarization service prepares the content.
7. Long content is divided into manageable chunks.
8. The backend sends summarization requests to Gemini.
9. Intermediate summaries are combined and reduced when necessary.
10. FastAPI returns the final summary and processing metadata.
11. Frontend displays the result.

### Document Upload Workflow

1. User selects document upload mode.
2. User uploads a PDF, DOCX, or TXT file.
3. Backend validates the uploaded file.
4. The corresponding extraction component extracts the document text.
5. Extracted content undergoes meaningful-character and length validation.
6. Valid content enters the summarization pipeline.
7. The backend processes the content through Gemini.
8. The application displays the generated summary and metadata.

### Long Document Processing

Long documents may exceed the input limits of a single model request. The application therefore uses a chunk-based processing approach.

The general workflow is:

1. Prepare and tokenize the source content.
2. Divide the content into manageable chunks.
3. Generate intermediate summaries for the chunks.
4. Combine intermediate summaries when necessary.
5. Apply reduction stages when the combined content is still too large.
6. Generate the final summary.

This approach allows the application to process longer content without sending the entire document in one model request.

## 8. Getting Started

### Prerequisites

Install the following tools:

- Git
- Docker Desktop
- Docker Compose (included with current Docker Desktop installations)
- Node.js and npm
- VS Code or another code editor
- A Gemini Developer API key from Google AI Studio

Docker Desktop should be running before executing Docker commands.

### Clone the Repository

```bash
git clone https://github.com/a-dinesh-kumar/text_summarization_system.git
cd text_summarization_system
```

### Backend Setup

Create the local backend environment file:

```powershell
Copy-Item backend/.env.example backend/.env
```

Open `backend/.env` and configure the Gemini API key and model settings.

**Important:** Obtain your API key through Google AI Studio. Never commit the actual key to GitHub.

### Frontend Setup

Open another terminal:

```powershell
cd frontend
npm install
npm run dev
```

The frontend development server should be available at:

```text
http://localhost:5173
```

### Start the Backend

From the project root:

```powershell
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

The application uses environment variables to separate application configuration from source code.

### Backend Configuration

Backend configuration is maintained in:

```text
backend/.env
```

Use `backend/.env.example` as the template.

The backend configuration includes:

| Configuration | Purpose |
|---|---|
| Gemini API key | Authenticates backend requests to the Gemini Developer API |
| Gemini model | Selects the Gemini model used for summarization |
| CORS origins | Defines which frontend origins can access the backend |

Keep the API key on the backend only. Do not expose it through frontend variables or browser code.

### Frontend Configuration

Frontend configuration is maintained through Vite environment variables.

Example:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_MAX_UPLOAD_SIZE_MB=15
VITE_GITHUB_URL=https://github.com/your-username/
VITE_LINKEDIN_URL=https://www.linkedin.com/in/your-profile/
```

Replace the profile URLs with your actual public profile links.

**Important:**

- Never commit `.env` files containing API keys or sensitive configuration.
- Commit `.env.example` files with placeholder values.
- Vite environment variables prefixed with `VITE_` are embedded into the frontend build and are visible to browser users.
- Never place the Gemini API key in a `VITE_` variable.
- After changing frontend environment variables, rebuild or redeploy the frontend.
- After changing backend environment variables, restart or redeploy the backend service.

## 10. Running with Docker

Docker provides a consistent backend runtime environment across local development and deployment.

### Start Containers

```powershell
docker compose up --build
```

### Run in Detached Mode

```powershell
docker compose up -d --build
```

### View Running Containers

```powershell
docker compose ps
```

### View Backend Logs

```powershell
docker compose logs -f backend
```

### Rebuild the Backend

```powershell
docker compose build --no-cache backend
docker compose up -d --force-recreate backend
```

### Stop Containers

```powershell
docker compose down
```

### Run Backend Tests

```powershell
docker compose exec backend pytest
```

Unlike the earlier local transformer implementation, the current Gemini-based backend does not need to download and cache large Hugging Face model weights at startup. It communicates with the configured Gemini API instead.

## 11. API Documentation

The backend exposes REST APIs through FastAPI.

### Health Check

**Endpoint**

```http
GET /health
```

Used to verify backend availability and report application readiness.

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
  "model": "Configured Gemini model",
  "model_key": "gemini",
  "source_tokens": 260,
  "initial_chunk_count": 1,
  "total_generation_chunks": 1,
  "reduction_levels": 0,
  "processing_time_seconds": 12.5
}
```

The values above illustrate the response structure. Actual values depend on the input and model execution.

### Interactive API Testing

FastAPI provides Swagger UI for exploring and testing the endpoints:

```text
http://localhost:8000/docs
```

Swagger UI can be used to:

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

| Input | Expected Result |
|---|---|
| Empty input | Rejected |
| Whitespace only | Rejected |
| Punctuation only | Rejected |
| Fewer than 50 meaningful characters | Rejected |
| Exactly 50 meaningful characters | Accepted |
| More than 50 meaningful characters | Accepted |

### Why Validate at Both Levels?

Frontend validation provides immediate feedback and improves user experience.

Backend validation ensures invalid requests are rejected even when someone bypasses the frontend and calls the API directly.

### Other Limits

- Maximum upload size: 15 MB.
- Maximum extracted/input text length: 500,000 characters.
- Supported document formats: PDF, DOCX, TXT.

The backend remains the authoritative validation layer.

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
- Text summarization request handling.
- Document upload handling.
- PDF extraction and upload.
- DOCX extraction and upload.
- API validation and error handling.
- Summarization pipeline and chunk-processing logic.

### Execute the Test Suite

Make sure the backend container is running:

```powershell
docker compose up -d
```

Execute:

```powershell
docker compose exec backend pytest
```

### Latest Test Status

**40 tests passed, 0 failed** during the latest local backend validation.

The automated suite uses mocked summarization behaviour where appropriate. Therefore, passing tests validates application logic, API workflows, and integration boundaries; it does not independently measure the quality of summaries generated by Gemini.

Real API functionality was also verified separately through the backend Swagger interface using both direct text input and document uploads.

## 15. Deployment Architecture

The application is designed to use two separate Render services.

### Frontend — Render Static Site

The React application is built using Vite and deployed as a Render Static Site.

Typical configuration:

| Setting | Value |
|---|---|
| Root Directory | `frontend` |
| Build Command | `npm install && npm run build` |
| Publish Directory | `dist` |

Configure the frontend environment variables in the Static Site service:

```env
VITE_API_BASE_URL=https://your-backend-service.onrender.com
VITE_MAX_UPLOAD_SIZE_MB=15
VITE_GITHUB_URL=https://github.com/your-username/
VITE_LINKEDIN_URL=https://www.linkedin.com/in/your-profile/
```

These values are read during the Vite build. Changes require a new frontend build and deployment.

### Backend — Render Web Service

The FastAPI backend is deployed separately using its Dockerfile.

Configure the backend environment variables in the Web Service:

- Gemini API key.
- Gemini model configuration.
- CORS origins containing the deployed frontend URL.

The Gemini API key must remain in the backend environment and must never be exposed to the frontend.

### Cross-Origin Resource Sharing (CORS)

Since the frontend and backend use different service URLs, the backend must allow requests from the deployed frontend origin.

Configure the backend CORS setting with the actual Render Static Site URL.

### Deployment Considerations

- Keep frontend and backend environment variables in their respective Render services.
- Do not configure the Gemini API key on the frontend.
- Rebuild the frontend after changing `VITE_` variables.
- Verify the backend health endpoint after deployment.
- Test text summarization and document upload against the deployed services.
- Check backend logs if requests fail or the service restarts.

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

```powershell
docker compose ps
docker compose logs -f backend
```

Verify the health endpoint:

```text
http://localhost:8000/health
```

### Gemini API Request Fails

**Problem:** Summary generation fails when the backend communicates with Gemini.

**Check:**

- The Gemini API key is configured correctly in the backend environment.
- The configured model is available to the API key.
- The API key has not been revoked or restricted.
- API quota and rate limits have not been exceeded.
- The backend has network access to the Gemini API.

Never expose the API key in frontend code, logs, screenshots, or public repositories.

### Input Validation Error

**Problem:** The application rejects submitted content.

**Reason:** The content may contain fewer than 50 meaningful characters or exceed the configured input limits.

**Solution:** Provide sufficient meaningful content and retry.

### Frontend Cannot Reach Backend

**Problem:** The frontend cannot communicate with FastAPI.

**Check:**

- Verify that the backend service is running.
- Check `VITE_API_BASE_URL`.
- Confirm that backend CORS configuration allows the frontend origin.
- Rebuild the frontend after changing Vite environment variables.
- Inspect the browser developer console and backend logs.

### GitHub and LinkedIn Links Are Not Clickable in Production

**Problem:** Social profile links work locally but not after deployment.

**Reason:** The frontend profile URLs are Vite build-time environment variables.

**Solution:**

1. Open the Render Static Site service.
2. Verify `VITE_GITHUB_URL` and `VITE_LINKEDIN_URL`.
3. Save the environment variables.
4. Trigger a new frontend deployment.
5. Verify both links in the deployed application.

## 17. Future Enhancements

Potential improvements include:

- OCR support for scanned and image-based PDFs.
- Additional Gemini model evaluation.
- Summary length and output-style controls.
- Improved summarization evaluation using ROUGE and other metrics.
- More comprehensive frontend and end-to-end testing.
- Improved error handling for API quotas and rate limits.
- Performance optimization for lengthy documents.
- Application monitoring and usage analytics.
- Support for additional document formats.

## 18. Author

**Dinesh Kumar Alagarsamy**

Software Quality Engineer / SDET

- **GitHub:** https://github.com/a-dinesh-kumar
- **LinkedIn:** https://www.linkedin.com/in/dinesh-kumar-alagarsamy

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

*Built as part of my learning journey in NLP, generative AI, FastAPI, React, Docker, and AI application development.*
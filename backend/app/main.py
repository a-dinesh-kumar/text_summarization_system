from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.summarize import router as summarize_router
from app.core.config import get_settings
from app.models.factory import create_summarizer
from app.services.summarization_service import SummarizationService


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.state.settings = settings

    # Load the selected model once per application process.
    summarizer = create_summarizer(settings)
    summarizer.load()
    app.state.summarizer = summarizer
    app.state.summarization_service = SummarizationService(summarizer, settings)

    yield


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Model-switchable text and document summarization API.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Text Summarization System API is running.",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    ready = hasattr(app.state, "summarization_service")
    return {
        "status": "ready" if ready else "starting",
        "model_loaded": ready,
    }


app.include_router(summarize_router, prefix="/api/v1", tags=["Summarization"])

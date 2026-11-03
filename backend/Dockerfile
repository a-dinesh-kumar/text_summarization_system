FROM python:3.13.15-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/app/.cache/huggingface \ 
    HF_HUB_DISABLE_TELEMETRY=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd --create-home appuser \
    && mkdir -p /app/.cache/huggingface \
    && chown -R appuser:appuser /app

EXPOSE 8000


# Local development image: includes test tools and Uvicorn hot reload.
FROM base AS development

COPY requirements-test.txt .
RUN pip install --no-cache-dir -r requirements-test.txt

COPY app ./app
COPY tests ./tests
COPY pytest.ini ./pytest.ini

RUN chown -R appuser:appuser /app
USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


# Production image: no pytest dependencies, no source bind mount, no hot reload.
FROM base AS production

COPY app ./app
RUN chown -R appuser:appuser /app
USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

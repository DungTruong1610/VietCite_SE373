# VietCite backend API (FastAPI + agents). Build context: backend/
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app/.venv

RUN pip install --no-cache-dir uv==0.13.5 \
    && useradd --create-home --uid 1000 app

WORKDIR /app

# Dependencies first (cached layer), then the code.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY geo ./geo
COPY app ./app
COPY cli.py ./
RUN uv sync --frozen --no-dev && mkdir -p /app/.data && chown -R app:app /app

USER app
EXPOSE 8000
CMD ["/app/.venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

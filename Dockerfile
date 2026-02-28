# FastAPI-based LARP rules chatbot backend
# Exposes REST API endpoints for rules question answering

FROM python:3.14 AS build

COPY --from=ghcr.io/astral-sh/uv:0.8.21 /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

COPY uv.lock pyproject.toml ./

RUN uv sync --no-install-project --no-dev

COPY . .

RUN uv sync --frozen --no-dev

FROM python:3.14 AS runtime

ENV PATH="/app/.venv/bin:$PATH"

RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup -m -d /app -s /bin/false appuser

WORKDIR /app

COPY --from=build --chown=appuser:appgroup /app .

USER appuser

# Expose FastAPI port (default 8000, configurable via PORT env var)
EXPOSE 8000

# Run the FastAPI application
# To run: docker run --env-file .env -v "$(pwd)/rules:/app/rules" -p 8000:8000 --name boffer-bot -it boffer-bot
ENTRYPOINT ["python", "main.py"]
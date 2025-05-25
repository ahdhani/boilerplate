FROM python:3.10-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1 \
    UV_LINK_MODE=copy \
    UV_CACHE_DIR="/tmp/.uv-cache"

# Install OS dependencies (only what's needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Copy uv binary from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
COPY --from=ghcr.io/astral-sh/uv:latest /uvx /bin/uvx

# Set working directory
WORKDIR /app

# Copy project files early to leverage Docker layer caching
COPY pyproject.toml poetry.lock* ./

# Install Python dependencies
RUN uv pip install --system --no-cache .

# Copy the rest of the application
COPY . .

# Set entrypoint (optional if using uvicorn or a CLI)
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


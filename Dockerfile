# Author: Chris Ward <chris@calmrat.com.>
# Description: Dockerfile for Qrypto
# License: MIT

# Use official Python image
FROM python:3.13-slim-bookworm

# Update and makes sure we have curl and ca-certificates
RUN apt-get update && apt-get install -y curl ca-certificates

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Add uv to PATH explicitly (for current layer and future ones)
ENV PATH="/root/.local/bin:$PATH"

# Make sure we have Python 3.13 installed.
RUN uv python install 3.13

# Set working directory
WORKDIR /app

# Install system dependencies
RUN uv venv .venv
ENV VIRTUAL_ENV="/app/.venv"
# Add .venv/bin to PATH
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy the rest of the project files
COPY README.md .
COPY start.sh .
COPY staticserve .
COPY localcache .
COPY qrypt.db .

# Copy Build Files
#COPY uv.lock .
#COPY .python-version .
#COPY requirements.txt .
COPY pyproject.toml .

# Copy app .env config
COPY .env .

# Copy project files
COPY src/qrypt .

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

RUN uv pip install -r pyproject.toml

# Install this project
RUN uv pip install -e .

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

# Expose webhook port
EXPOSE 8000 8501

# Start services
CMD ["/bin/bash", "./start.sh"]
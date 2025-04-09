# Author: Chris Ward <chris@calmrat.com.>
# Description: Dockerfile for Qrypto
# License: MIT

# Use official Python image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY src/qrypt .

# Install UV (make sure curl & tar are available)
RUN apt-get update && apt-get install -y curl ca-certificates
RUN curl -LsSf https://astral.sh/uv/install.sh | bash

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Add uv to PATH explicitly (for current layer and future ones)
ENV PATH="/root/.cargo/bin:/root/.local/bin:$PATH"

# Install build dependencies
COPY README.md .
COPY requirements.txt .
COPY pyproject.toml .
COPY .python-version .
COPY start.sh .
COPY .env .
COPY staticserve .
COPY localcache .

RUN uv pip install --system -r requirements.txt
#RUN uv pip install --system -e .

# Expose webhook port
EXPOSE 8000 8501

# Start services
CMD ["/bin/bash", "./start.sh"]
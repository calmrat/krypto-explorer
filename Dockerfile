# Author: Chris Ward <chris@calmrat.com.>
# Description: Dockerfile for Krypto Explorer
# License: MIT

# Use official Python image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install UV package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Install dependencies
RUN uv pip install --system

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose webhook port
EXPOSE 5000

# Start services
# FastAPI entrypoint
CMD ["python", "krypto-explorer/main.py"]

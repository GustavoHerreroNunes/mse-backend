# Use slim image instead of full python image (much smaller)
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata/ \
    TESSERACT_CMD=tesseract

WORKDIR /app

# Install system dependencies needed for psycopg2, Tesseract, and Poppler
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    tesseract-ocr \
    tesseract-ocr-por \
    tesseract-ocr-eng \
    poppler-utils \
    libpoppler-cpp-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Pre-compile Python bytecode for faster startup
RUN python -m compileall .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Use exec form and optimize gunicorn settings for Cloud Run (increased timeout for PDF processing)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app", \
     "--workers=1", "--threads=8", "--timeout=120", \
     "--keep-alive=2", "--max-requests=1000", "--max-requests-jitter=50", \
     "--preload"]
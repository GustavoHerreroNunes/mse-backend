FROM python:3.11-slim

WORKDIR /generate_pdf

# Install build dependencies for pycairo and other packages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libcairo2-dev \
    pkg-config \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . /generate_pdf

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "generate_pdf_with_reportlab.py"]
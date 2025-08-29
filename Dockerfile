# syntax=docker/dockerfile:1

FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr tesseract-ocr-eng tesseract-ocr-vie libtesseract-dev \
 && rm -rf /var/lib/apt/lists/*
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata

# 1) System deps (nếu cần build wheels)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# 2) App workspace
WORKDIR /app

# 3) Cài deps
#   - Nếu repo có requirements.txt: dùng block này
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

#   - Nếu repo dùng pyproject.toml/poetry, thay bằng:
# COPY pyproject.toml poetry.lock* /app/
# RUN pip install --no-cache-dir poetry && \
#     poetry config virtualenvs.create false && \
#     poetry install --no-interaction --no-ansi

# 4) Copy code vào image
COPY . /app

# 5) Biến môi trường & cổng
ENV PORT=8000
EXPOSE 8000

# 6) Lệnh chạy app
#    SỬA "app.main:app" theo module thật sự của bạn
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

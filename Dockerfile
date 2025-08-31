# syntax=docker/dockerfile:1
FROM python:3.11-slim

# --- OCR (nếu app cần Tesseract) ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr tesseract-ocr-eng tesseract-ocr-vie libtesseract-dev \
 && rm -rf /var/lib/apt/lists/*
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata \
    TESSERACT_CMD=/usr/bin/tesseract

# --- Dụng cụ build nhẹ (tuỳ dự án) ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# --- Chromium + Chromedriver từ apt (đồng bộ phiên bản) ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium chromium-driver \
    fonts-liberation xdg-utils \
    libnss3 libxss1 libgbm1 libasound2 \
 && rm -rf /var/lib/apt/lists/*
ENV CHROME_BIN=/usr/bin/chromium \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver

# --- App ---
WORKDIR /app

# 1) Cài Python deps (rất quan trọng)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 2) Copy toàn bộ code
COPY . /app

# 3) Expose + Run
EXPOSE 8000
CMD ["python","-m","uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]

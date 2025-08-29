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

# Install Chrome and Chromedriver dependencies
RUN apt-get update && apt-get install -y \
    gnupg \
    wget \
    unzip \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libexpat1 \
    libfontconfig1 \
    libgbm1 \
    libgdk-pixbuf-xlib-2.0-0 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    lsb-release \
    xdg-utils \
    --no-install-recommends \
 && rm -rf /var/lib/apt/lists/*

# Install Google Chrome (latest stable version)
RUN wget -O /tmp/google-chrome-keyring.gpg https://dl.google.com/linux/linux_signing_key.pub \
 && mkdir -p /etc/apt/keyrings/ \
 && mv /tmp/google-chrome-keyring.gpg /etc/apt/keyrings/google-chrome.gpg \
 && echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
 && apt-get update && apt-get install -y google-chrome-stable \
 && rm -rf /var/lib/apt/lists/*

# Install Chromedriver (using a known stable version, 114.0.5735.90)
RUN wget -q --continue -P /tmp "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip" \
 && unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin \
 && rm /tmp/chromedriver_linux64.zip \
 && chmod +x /usr/local/bin/chromedriver

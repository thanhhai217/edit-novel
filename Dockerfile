# ---------- Stage 1: builder (tạo wheels, cache nhanh) ----------
FROM python:3.12-slim AS builder
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PIP_NO_CACHE_DIR=1
WORKDIR /app

# Cài tool build tối thiểu (chỉ ở builder)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy trước requirements để tối ưu cache layer
COPY requirements.txt .
RUN python -m pip install --upgrade pip wheel && \
    pip wheel --no-deps -r requirements.txt -w /wheels

# Copy toàn bộ mã nguồn (để nếu có bước build asset thì đặt ở đây)
COPY . .

# ---------- Stage 2: runtime (nhẹ, bảo mật hơn) ----------
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

# Tạo user non-root
RUN adduser --disabled-password --gecos "" appuser

# Cài deps đã build ở stage trước
COPY --from=builder /wheels /wheels
RUN python -m pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir /wheels/* && \
    rm -rf /wheels

# Copy code (chỉ phần cần thiết)
COPY . /app

# Static: nếu anh phục vụ tĩnh trực tiếp qua FastAPI, không cần step bổ sung.
# Nếu có build front-end, thêm bước build tại stage builder và COPY vào /app/static ở đây.

# Expose cổng app
EXPOSE 8000

# Healthcheck: FastAPI nên có /health trả 200
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD \
  python - <<'PY' || exit 1
import urllib.request, sys
try:
    urllib.request.urlopen("http://127.0.0.1:8000/health", timeout=2).read()
except Exception:
    sys.exit(1)
PY

# Chạy bằng gunicorn + uvicorn worker
USER appuser
ENV WORKERS=2 LOG_LEVEL=info HOST=0.0.0.0 PORT=8000
CMD ["sh","-lc","gunicorn app.main:app -k uvicorn.workers.UvicornWorker -b ${HOST}:${PORT} --workers ${WORKERS} --log-level ${LOG_LEVEL} --access-logfile - --error-logfile -"]

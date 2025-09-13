# ---------- base python (builder) ----------
FROM python:3.12-slim-bookworm AS py-build

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Build deps for wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential libpq-dev libjpeg62-turbo-dev zlib1g-dev curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Leverage cache: copy lockfiles first
COPY requirements.txt ./
# Build a venv and install deps into it
RUN python -m venv /opt/venv \
 && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project (respect .dockerignore)
COPY . .

# ---------- node builder for Tailwind ----------
FROM node:20-bookworm AS node-build
WORKDIR /web
COPY package.json package-lock.json ./
RUN npm ci
COPY ./static ./static

# If you can, prefer a production-only build
# RUN npm ci --omit=dev
RUN npm run build:css || echo "No build:css script; skipping"

# ---------- final runtime ----------
FROM python:3.12-slim-bookworm AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src \
    PATH="/opt/venv/bin:$PATH" \
    PORT=8000

# Only runtime libs
RUN apt-get update && apt-get install -y --no-install-recommends \
      libpq5 libjpeg62-turbo zlib1g \
    && rm -rf /var/lib/apt/lists/*

# Non-root user
RUN useradd -m appuser
WORKDIR /app

# Copy venv and app
COPY --from=py-build /opt/venv /opt/venv
COPY --from=py-build /app /app
# Built static assets
COPY --from=node-build /web/static/dist /app/static/dist

# Ensure entrypoint is executable
RUN chmod u+x docker-entrypoint.sh && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD curl -fsS http://127.0.0.1:${PORT}/health || exit 1
CMD ["./docker-entrypoint.sh"]

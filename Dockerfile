# Multi-stage Dockerfile for EduQuery AI

# Stage 1: Build Frontend App (React 19 + Vite)
FROM node:20-alpine AS frontend-builder
WORKDIR /app/apps/web
COPY apps/web/package*.json ./
RUN npm ci
COPY apps/web/ ./
RUN npm run build

# Stage 2: Python Backend Environment
FROM python:3.12-slim AS backend
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager
RUN pip install --no-cache-dir uv

# Copy dependency specifications
COPY pyproject.toml package.json ./
COPY packages/contracts/ ./packages/contracts/

# Install Python dependencies
RUN uv pip install --system -e .

# Copy application source code & assets
COPY services/ ./services/
COPY data/ ./data/
COPY docs/09-rag-data-md/ ./docs/09-rag-data-md/
COPY ml/ ./ml/

# Copy built frontend assets from Stage 1 into apps/web/dist
COPY --from=frontend-builder /app/apps/web/dist ./apps/web/dist

# Expose port
EXPOSE 8000

# Set default environment variables for Safe Demo Mode
ENV APP_ENV=production
ENV FORCE_DEMO_FALLBACK=true
ENV PORT=8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/healthz || exit 1

# Launch FastAPI Uvicorn Server
CMD ["uvicorn", "services.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

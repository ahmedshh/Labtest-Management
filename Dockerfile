# Multi-stage Dockerfile for Laboratory Information System
# Stage 1: Build React frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy package files
COPY frontend/package.json frontend/package-lock.json* ./

# Install frontend dependencies
# Remove package-lock.json to ensure Alpine Linux (musl) optional dependencies are installed
# The lock file from Windows/Linux glibc doesn't include musl-specific optional deps
RUN rm -f package-lock.json && npm install

# Copy frontend source code
COPY frontend/ .

# Build React app for production
RUN npm run build

# Stage 2: Python backend with frontend static files
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/ .

# Copy built frontend from previous stage
COPY --from=frontend-builder /app/frontend/dist /app/static

# Create directory for SQLite database
RUN mkdir -p /app/data

# Expose Flask port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV DATABASE_URL=sqlite:////app/data/lab_tests.db
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

# Run Flask application
CMD ["python", "app.py"]

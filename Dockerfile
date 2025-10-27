FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/storage /app/data

# Expose port 80 (matching compose.yml)
EXPOSE 80

# Health check with proper startup time
HEALTHCHECK --interval=30s --timeout=15s --start-period=120s --retries=3 \
  CMD curl -f http://localhost:80/health || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "1"]
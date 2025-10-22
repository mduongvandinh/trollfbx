# ==============================================================================
# TrollFB Backend Dockerfile
# Python FastAPI application with Ollama integration
# ==============================================================================

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p uploads/images uploads/memes

# Expose port
EXPOSE 8000

# Environment variables (can be overridden by docker-compose)
ENV PYTHONUNBUFFERED=1
ENV DATABASE_URL=sqlite:///./football_meme.db
ENV OLLAMA_URL=http://ollama:11434

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Run the application
CMD ["python", "main.py"]

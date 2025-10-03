# Use a slim Python 3.11 image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install OS-level dependencies and uv
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files
COPY pyproject.toml .
COPY .python-version .

# Install dependencies using uv (no virtual env needed in Docker)
RUN uv pip install --system -r pyproject.toml

# Download needed NLTK data
RUN python -m nltk.downloader punkt punkt_tab stopwords wordnet averaged_perceptron_tagger

# Copy the rest of the backend code into /app
COPY . ./

# Expose the port that FastAPI (via Uvicorn) will listen on
EXPOSE 8000

# Start FastAPI with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Use a slim Python 3.11 image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install OS-level dependencies
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copy requirements to /app
COPY requirements.txt .

# Create a virtual environment and activate it
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Download needed NLTK data
# Adjust the list (punkt, stopwords, wordnet, averaged_perceptron_tagger, etc.)
# If you specifically need 'punkt_tab', include it as well:
RUN python -m nltk.downloader punkt punkt_tab stopwords wordnet averaged_perceptron_tagger

# Copy the rest of the backend code into /app
COPY . ./

# Expose the port that FastAPI (via Uvicorn) will listen on
EXPOSE 8000

# Start FastAPI with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

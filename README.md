Below is a re-written version of your `README.md` that reflects your latest changes and highlights hybrid search as a primary feature:

---

# NotStuck: AI-Powered Document Assistant

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)  
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)  
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.0-green.svg)](https://fastapi.tiangolo.com/)  
[![Next.js](https://img.shields.io/badge/Next.js-15.1.6-blue.svg)](https://nextjs.org/)  
[![MongoDB](https://img.shields.io/badge/MongoDB-6.0-green.svg)](https://www.mongodb.com/)  
[![Pinecone](https://img.shields.io/badge/Pinecone-Vector%20DB-orange.svg)](https://www.pinecone.io/)  
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT-9cf.svg)](https://openai.com/)  
[![Docker](https://img.shields.io/badge/Docker-20.10.17-blue.svg)](https://www.docker.com/)  
[![CI/CD](https://github.com/praneethravuri/notstuck/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/praneethravuri/notstuck/actions)  
[![Fly.io Deployment](https://github.com/praneethravuri/notstuck/actions/workflows/fly.yml/badge.svg)](https://github.com/praneethravuri/notstuck/actions)

---

## Overview

**NotStuck** is an AI-powered knowledge base assistant designed to help you get "unstuck" by providing intelligent, context-aware answers derived from your own documents. Whether you're researching, studying, or managing projects, NotStuck makes it easy to upload documents, ask questions, and receive responses backed by both dense and sparse semantic search.

> **Hybrid Search at Its Core:**  
> NotStuck's standout feature is its **hybrid search** capability. By combining **dense embeddings** (generated with OpenAI models) and **sparse vectors** (powered by a BM25 encoder), the system delivers highly accurate, context-aware results from your document data.

---

## Key Features

- **Hybrid Search:**  
  Seamlessly combines dense (neural) and sparse (BM25-based) embeddings to deliver precise retrieval of document chunks, ensuring relevant context for every query.

- **Document Upload & Processing:**  
  Easily upload PDFs through a user-friendly interface. Documents are automatically chunked, cleaned, and embedded.

- **Vector Database Integration:**  
  Store and query document embeddings using [Pinecone](https://www.pinecone.io/), enabling lightning-fast similarity searches.

- **Conversational Chat Interface:**  
  Engage in interactive sessions where you can ask questions and receive answers that reference your uploaded documents. All chat sessions are stored in MongoDB for future reference.

- **Context-Aware Answer Generation:**  
  Leverages OpenAI's GPT models to generate responses that are informed by both the document context and prior conversation history.

- **Robust Logging & Configurable Storage:**  
  BM25 encoder states and application logs are saved in designated directories for easy management and debugging.

---

## Tech Stack

1. **Backend**
   - **[FastAPI](https://fastapi.tiangolo.com/)** for building high-performance APIs.
   - **[MongoDB](https://www.mongodb.com/)** to store chat sessions and metadata.
   - **[Pinecone](https://www.pinecone.io/)** as the vector database for storing document embeddings.
   - **[OpenAI](https://openai.com/)** for embeddings and GPT-based response generation.
   - **[LangChain](https://github.com/hwchase17/langchain)** for document chunking and retrieval-augmented generation.

2. **Frontend**
   - **[Next.js](https://nextjs.org/)** for the interactive web interface.
   - **[Tailwind CSS](https://tailwindcss.com/)** for rapid and responsive UI design.

3. **Deployment & DevOps**
   - **[Docker](https://www.docker.com/)** for containerizing backend and frontend services.
   - **[GitHub Actions](https://docs.github.com/en/actions)** for CI/CD pipelines.
   - **[Fly.io](https://fly.io/)** for scalable deployment of containerized applications.

---

## Architecture

NotStuck's architecture is designed for speed, accuracy, and scalability:

1. **Frontend (Next.js):**
   - **Upload Documents:** Users upload PDFs via an intuitive interface.
   - **Chat Interface:** Users interact via chat to ask questions and receive context-aware responses.

2. **Backend (FastAPI):**
   - **Document Processing Pipeline:**
     - **Chunking & Cleaning:** PDFs are split into manageable chunks.
     - **Hybrid Embedding Generation:** Dense embeddings from OpenAI and sparse BM25 embeddings are generated.
     - **Vector Upsertion:** Embeddings are stored in Pinecone for efficient retrieval.
   - **Retrieval-Augmented Generation (RAG):**
     - For each query, the system retrieves the most relevant document chunks using hybrid search.
     - A dynamic prompt is constructed and sent to a GPT model for answer generation.
   - **Chat Session Management:** User interactions are logged in MongoDB for persistent chat sessions.

3. **Vector Database (Pinecone):**
   - Provides high-performance, scalable storage and similarity search for document embeddings.

4. **Hybrid Search:**
   - The innovative blend of **dense neural embeddings** and **sparse BM25 vectors** ensures that NotStuck retrieves the most contextually relevant document chunks, even in large datasets.

---

## Installation and Setup

### 1. Prerequisites

- **Python 3.10+**
- **Node.js 20+**
- **Docker & Docker Compose**
- **MongoDB** (local or remote)
- **Pinecone API Key**
- **OpenAI API Key**

### 2. Clone the Repository

```bash
git clone https://github.com/praneethravuri/notstuck.git
cd notstuck
```

### 3. Environment Variables


| Variable             | Description                                                        | Location  |
|----------------------|--------------------------------------------------------------------|-----------|
| `OPENAI_API_KEY`     | API Key from [OpenAI](https://platform.openai.com/account/api-keys) | Backend   |
| `PINECONE_API_KEY`   | API Key from [Pinecone](https://docs.pinecone.io/guides/get-started/quickstart)                                                   | Backend   |
| `PINECONE_ENV`       | Pinecone environment (e.g., `us-west1-gcp`)                        | Backend   |
| `PINECONE_INDEX_NAME`| Name of the Pinecone index                                         | Backend   |
| `MONGODB_URI`        | MongoDB connection URI (e.g., `mongodb://...`)                     | Backend   |
| `NEXT_PUBLIC_BACKEND_URL` | URL where the FastAPI backend can be reached (e.g. `http://localhost:8000`) | Frontend |

> **Note**: For local development, create a `.env` file in `backend/` and `frontend/` respectively. See `.env.example` patterns or references in the existing `.gitignore`.

### 4. Local Development

#### A. Using Docker Compose (Recommended)

From the root of the repository:

```bash
docker-compose up --build
```

- **MongoDB** will be accessible on `localhost:27017`.
- **FastAPI backend** will be available on `localhost:8000`.
- **Next.js frontend** will run on `localhost:3000`.

#### B. Manual Setup

1. **Backend (FastAPI):**

   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate   # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

2. **Frontend (Next.js):**

   ```bash
   cd ../frontend
   npm install
   npm run dev
   ```

Visit `http://localhost:3000` in your browser.

---

## Usage

1. **Upload Documents:**
   - Use the “Upload Documents” feature to send PDFs to the backend.
   - The system processes files, splits them into chunks, generates embeddings using hybrid search (dense + sparse), and stores them in Pinecone.

2. **Ask Questions:**
   - Use the chat interface to ask questions.
   - The backend retrieves relevant document chunks via hybrid search, constructs a dynamic prompt, and calls GPT to generate context-aware responses.
   - All interactions are stored in MongoDB for session persistence.

3. **View Chat Sessions & PDFs:**
   - Access chat histories and view the processed documents directly via the provided routes.

---

## Production Deployment

### Docker Images

- **Backend:**

  ```bash
  docker run -d --pull always -p 8000:8000 --env-file=backend/.env praneeth2510/notstuck-backend:latest
  ```

- **Frontend:**

  ```bash
  docker run -d --pull always -p 3000:3000 -e NEXT_PUBLIC_BACKEND_URL=http://backend:8000 praneeth2510/notstuck-frontend:latest
  ```

### CI/CD and Fly.io Deployment

- **GitHub Actions:**  
  Automated CI/CD pipelines build and push Docker images.
- **Fly.io:**  
  Deployment workflows (via `fly.toml` files) deploy the backend and frontend containers.

---

## Contributing

1. **Fork** the repository.
2. Create a new **feature branch**.
3. **Commit** your changes.
4. Open a **pull request** against `main`.

We welcome contributions on any aspect of the project—from improving hybrid search performance to enhancing the user interface.

---

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute this project under the license terms.

---

## Contact & Support

- **Author:** [@praneethravuri](https://github.com/praneethravuri)
- If you encounter issues or have feature requests, please open a [GitHub Issue](https://github.com/praneethravuri/notstuck/issues).

Thank you for using **NotStuck**! If this project helps you, please consider giving it a star on GitHub.
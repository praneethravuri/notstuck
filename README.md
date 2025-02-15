# NotStuck: AI-Powered Knowledge Base Assistant

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

## Overview

**NotStuck** is an AI-powered knowledge base assistant that allows you to **upload documents**, **ask questions**, and receive **intelligent, context-aware** answers. It leverages advanced NLP techniques, including **document chunking**, **embeddings**, and **retrieval-augmented generation (RAG)**. The goal is to provide accurate, relevant responses from your own documents—helping you get “unstuck” with your research, study, or project needs.

## Key Features

- **Document Upload and Processing**  
  Upload PDFs (and potentially other document formats) via an intuitive web interface. Documents are chunked and embedded using [OpenAI embeddings](https://platform.openai.com/docs/guides/embeddings).

- **Vector Database with Pinecone**  
  Store and query your document chunks in a high-performance vector database (Pinecone) for lightning-fast semantic retrieval.

- **Chat Interface**  
  Interact with a chat-like UI built with Next.js. Ask questions and get answers grounded in the context of your documents.

- **Contextual Answering with GPT**  
  Utilize GPT-based models (configurable—e.g., GPT-4, GPT-3.5, or custom “GPT-4o”) for generating answers that reference your document data.

- **MongoDB Integration**  
  Persist chat histories, user queries, and metadata in MongoDB for session-based interactions and retrieval of past conversation context.

- **Configurable Model Settings**  
  Control similarity thresholds, results returned, temperature, max tokens, and response style (concise, detailed, technical, or casual) all from the UI.

- **Production-Ready**  
  Includes Docker configurations, GitHub Actions CI/CD, and Fly.io deployment workflow.

---

## Tech Stack

1. **Backend**
   - **[FastAPI](https://fastapi.tiangolo.com/)**: High-performance Python web framework for building APIs.
   - **[MongoDB](https://www.mongodb.com/)**: Document-oriented NoSQL database for storing chats and metadata.
   - **[Pinecone](https://www.pinecone.io/)**: Vector database to store embedded document chunks and perform semantic similarity searches.
   - **[OpenAI Embeddings / GPT](https://openai.com/)**: Generate embeddings for chunked documents and produce final answers.
   - **[LangChain](https://github.com/hwchase17/langchain)**: Manages chunking logic, LLM calls, and retrieval-augmented generation pipeline.

2. **Frontend**
   - **[Next.js](https://nextjs.org/)**: React-based framework for server-rendered or statically exported websites.
   - **[Tailwind CSS](https://tailwindcss.com/)**: Utility-first CSS framework for rapid UI development.
   - **[shadcn/UI + Radix](https://ui.shadcn.com/)**: Beautiful, accessible React components built with Radix UI and Tailwind CSS.

3. **Deployment and DevOps**
   - **[Docker](https://www.docker.com/)**: Containerization of both backend (FastAPI) and frontend (Next.js).
   - **[GitHub Actions](https://docs.github.com/en/actions)**: CI/CD pipeline for build-and-push of Docker images and Fly.io deployment.
   - **[Fly.io](https://fly.io/)**: Hosting platform to deploy both backend and frontend containers.

---

## Architecture

Below is a high-level overview of how NotStuck’s components interact:

1. **Frontend (Next.js)**
   - **Upload PDFs**: Sends uploaded PDF files to the `/api/upload` endpoint.  
   - **Ask Questions**: Sends chat queries to the `/api/ask` endpoint for RAG-based answers.  
   - **Chats & Sessions**: Retrieves chat history and maintains state for multiple sessions.  

2. **Backend (FastAPI)**  
   - **Routes**:
     - `/upload`: Receives and stores raw PDFs, processes them into chunks, generates embeddings, and upserts them into Pinecone.
     - `/ask`: Accepts user questions, retrieves relevant chunks from Pinecone, and calls GPT to generate the final answer.
     - `/chats`: Stores and retrieves chat sessions from MongoDB.
     - `/get-pdfs`: Returns a list of processed PDFs or serves individual PDF files.
   - **RAG Pipeline**:
     1. **Document Chunking**: Splits PDFs into text chunks.
     2. **Embeddings**: Uses OpenAI embedding models to vectorize chunks.
     3. **Vector Store (Pinecone)**: Persists vectors for semantic similarity queries.
     4. **Query**: For each new question, embed the query and find top-k chunks in Pinecone.
     5. **Prompt Construction**: Build a GPT prompt with retrieved chunks + chat context.
     6. **OpenAI Completion**: GPT returns a final answer, which is stored in the chat history.
   - **MongoDB**: Stores user messages (both questions and answers), enabling persistent chat sessions.  

3. **Vector Database (Pinecone)**  
   - Receives chunk embeddings from the backend.
   - Provides fast vector similarity searches for each incoming query.

4. **OpenAI Services**  
   - **Embeddings API**: Generates vector embeddings for each chunk and for user queries.
   - **GPT Chat/Completion**: Produces the final answer text from the retrieved context.

**Control Flow** (typical usage scenario):
1. **User Uploads Document**  
   - Frontend sends PDF to `/upload`.  
   - The backend stores it, splits into chunks, embeds them, and upserts embeddings into Pinecone.  

2. **User Asks a Question**  
   - Frontend calls `/ask` with the question and optional chat session ID.  
   - The backend:
     1. Embeds the question (OpenAI Embeddings).
     2. Searches Pinecone for top-k similar chunks.
     3. Builds a GPT prompt with those chunks + prior chat summary (if a session).
     4. Calls GPT (OpenAI) to generate an answer.
     5. Stores user question & GPT response in MongoDB.
     6. Returns the response, relevant chunk metadata, and source info to the frontend.  

3. **User Views Answer**  
   - Frontend updates the chat interface with the new GPT response.  
   - Relevant sources are displayed for transparency.  

---

## Installation and Setup

### 1. Prerequisites

- **Python** 3.10 or higher  
- **Node.js** 20 or higher  
- **Docker** & **Docker Compose**  
- **MongoDB** (local or remote)  
- **Pinecone API Key** + configured environment (for vector DB)  
- **OpenAI API Key** (for embeddings and GPT)

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

From the **root** of the repository:

```bash
docker-compose up --build
```

- **MongoDB** will be exposed on `localhost:27017`.
- **FastAPI backend** will be on `localhost:8000`.
- **Next.js frontend** will be on `localhost:3000`.

Wait until all containers are up and running. Then open `http://localhost:3000` in your browser to access the NotStuck interface.

#### B. Manual Setup (Without Docker)

1. **Backend** (FastAPI)
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate   # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   # Set environment variables (OPENAI_API_KEY, PINECONE_API_KEY, etc.)
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

2. **Frontend** (Next.js)
   ```bash
   cd ../frontend
   npm install
   # Set NEXT_PUBLIC_BACKEND_URL to point to your local backend (e.g., http://localhost:8000)
   npm run dev
   ```
3. Visit `http://localhost:3000`.

---

## Usage

1. **Upload Documents**  
   - In the sidebar, under “Upload Documents”, drag and drop or click to select PDF files.  
   - The backend automatically splits these files into chunks, embeds them, and stores them in Pinecone.

2. **Chat and Ask Questions**  
   - Navigate to “Chat” (or directly open `http://localhost:3000/chat`).  
   - Type your question in the chat input. The system will use retrieval-augmented generation to find relevant chunks in Pinecone and generate an AI answer with references.

3. **View Active Sources**  
   - The “Active Sources” panel shows you the exact chunks from your documents that informed the AI’s response, along with the filenames.

4. **Configure Model Settings**  
   - Adjust parameters like **Similarity Threshold**, **Temperature**, **Max Tokens**, **Response Style**, or **Model** from the sidebar.  
   - The system picks up these updated parameters on each subsequent query.

5. **Start a New Chat**  
   - Use “New Chat” to spin up a fresh session.  
   - Each chat session is stored separately in MongoDB, so you can revisit it later.

---

## Production Deployment

### 1. Building Docker Images Manually

**Backend** (from `./backend`):

```bash
docker run -d --pull always -p 8000:8000 --en-file=backend.env praneeth2510/notstuck-backend:latest
```

**Frontend** (from `./frontend`):

```bash
docker run -d --pull always -p 3000:3000 -e NEXT_PUBLIC_BACKEND_URL=http://backend:8000 praneeth2510/notstuck-frontend:latest
```

### 2. GitHub Actions CI/CD

This repository includes:
- **`.github/workflows/ci-cd.yml`**: Builds the Docker images for **frontend** and **backend** and pushes them to Docker Hub (or another registry).
- **`.github/workflows/fly.yml`**: Deploys the images to Fly.io when the CI/CD pipeline completes successfully.

### 3. Fly.io Deployment

- The backend has a `fly.toml` in `backend/`; the frontend has a `fly.toml` in `frontend/`.
- The GitHub Action `fly.yml` automatically invokes `flyctl deploy` for each service (assuming you have the correct secrets set in your GitHub repository: `FLY_API_TOKEN_BACKEND` and `FLY_API_TOKEN_FRONTEND`).

### 4. Environment Variables in Production

Make sure to configure environment variables in your production environment (e.g., Fly.io secrets, or your hosting provider’s config) for `OPENAI_API_KEY`, `PINECONE_API_KEY`, `MONGODB_URI`, etc.

---

## Detailed RAG Flow

1. **PDF Ingestion**  
   - Documents are uploaded to the backend, stored in `RAW_DATA_PATH`, and chunked with [LangChain text splitter](https://python.langchain.com/docs/modules/data_connection/document_transformers/text_splitters).  
   - The system cleans the text (removing special characters, etc.) and calls **OpenAI embeddings** to get vectors.

2. **Upserting Vectors**  
   - Each chunk is upserted into Pinecone with metadata like `{ "source_file": "filename.pdf", "subjects": "some-subject" }`.  
   - Similar chunks are deduplicated or updated to avoid storing exact duplicates.

3. **Query Handling**  
   - A user’s question is similarly embedded and used for similarity lookup in Pinecone.  
   - Top-k matches are returned, filtered by a similarity threshold if set.

4. **Prompt Construction**  
   - The retrieved chunks are appended to a system + user prompt for GPT.  
   - The system prompt can specify style, tone, or chain-of-thought instructions.  
   - The user prompt includes the question and relevant chunk texts.

5. **Answer Generation**  
   - GPT returns an answer that references the context.  
   - This answer is logged in the user’s chat history, along with relevant chunk references and sources.

---

## Contributing

1. **Fork** the repository.  
2. Create a new **feature branch**.  
3. **Commit** your changes.  
4. Open a **pull request** against `main`.  

We welcome contributions, especially around expanding document format support, improving chunking strategies, or adding new retrieval features.

---

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute this project as permitted under the license.

---

## Contact & Support

- **Author**: [@praneethravuri](https://github.com/praneethravuri)  
- If you encounter issues or have feature requests, please open a [GitHub Issue](https://github.com/praneethravuri/notstuck/issues).  

Thank you for using **NotStuck**! If this project helps you, consider giving it a star on GitHub. We hope NotStuck helps you stay productive and never get stuck again.
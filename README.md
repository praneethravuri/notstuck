# NotStuck: AI-Powered Document Assistant

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT) [![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/) [![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)](https://fastapi.tiangolo.com/) [![Next.js](https://img.shields.io/badge/Next.js-15.1.6-blue.svg)](https://nextjs.org/) [![Pinecone](https://img.shields.io/badge/Pinecone-Vector%20DB-orange.svg)](https://www.pinecone.io/) [![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-purple.svg)](https://www.crewai.com/) [![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

---

## Overview

**NotStuck** is a production-ready, AI-powered RAG (Retrieval-Augmented Generation) system that helps you extract insights from your documents using cutting-edge AI models. Upload documents (PDF, DOCX, TXT), ask questions, and receive intelligent answers powered by **CrewAI agents**, **vector search**, and your choice of 10+ LLM models through OpenRouter.

> **Intelligent Multi-Agent RAG System:**
> NotStuck combines **CrewAI-powered intelligent routing**, **Pinecone vector search**, **streaming responses**, and **multi-model LLM support** (GPT-4, Claude, Gemini, Llama, and more) to deliver highly accurate, context-aware answers. Agents automatically decide whether to use the knowledge base, search the web, or answer directly from their knowledge.

## Quick Start with Docker 🐳

```bash
# 1. Clone the repository
git clone https://github.com/praneethravuri/notstuck.git
cd notstuck

# 2. Create backend/.env with your API keys
cat > backend/.env << EOF
OPENROUTER_API_KEY=your_openrouter_key
OPENAI_API_KEY=your_openai_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX_NAME=notstuck-index
PINECONE_ENV=us-east-1
EMBEDDING_DIMENSION=1024
EOF

# 3. Start with Docker Compose
docker-compose up --build

# 4. Open http://localhost:3000
```

That's it! 🎉 Upload documents and start asking questions.

---

## Key Features

### 🚀 **Multi-Model LLM Support**
- Choose from **10+ AI models** via OpenRouter: GPT-4o, Claude 3.5, Gemini Pro, Llama 3.1, Mistral, and more
- Dynamic model selection in the UI
- Model-specific optimizations for different use cases

### 🤖 **Intelligent AI Agents**
- **CrewAI-powered** multi-agent system
- Agents decide when to use knowledge base vs. web search
- General knowledge questions answered directly
- Document-specific queries use RAG pipeline
- Current information retrieved via web search with source URLs

### 📄 **Smart Document Processing**
- **Semantic-aware chunking** with configurable overlap (1000 chars, 200 overlap)
- **Automatic text cleaning** removes unicode, escape characters, and artifacts
- **Original filename preservation** in metadata
- **Temporary file processing** - no local storage required
- **Batch embedding generation** for efficiency

### 🔍 **Advanced Search & Retrieval**
- **Dense embeddings** (OpenAI text-embedding-3-large, 1024 dimensions)
- **Pinecone vector database** with dotproduct metric
- **Context optimization** with deduplication
- **Web search integration** with DuckDuckGo (includes source URLs)

### ⚡ **Production-Ready Features**
- **Docker & Docker Compose** support for easy deployment
- **Streaming responses** for real-time answer generation
- **Health checks** and automatic restarts
- **Full Pydantic validation** for all API endpoints
- **Auto database reset** on startup
- **Type-safe** throughout the entire pipeline

### 💎 **Developer Experience**
- **Interactive API docs** at `/docs`
- **Clean, modular architecture**
- **uv** for fast dependency management
- **Hot reload** for rapid development
- **Windows console UTF-8** support for emoji logs

---

## Tech Stack

### **Backend**
- **[FastAPI](https://fastapi.tiangolo.com/)** - High-performance async API framework
- **[CrewAI](https://www.crewai.com/)** - Multi-agent AI framework
- **[Pydantic](https://pydantic.dev/)** - Data validation and settings management
- **[Pinecone](https://www.pinecone.io/)** - Vector database with cosine similarity
- **[OpenRouter](https://openrouter.ai/)** - Unified API for 10+ LLM providers
- **[OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)** - text-embedding-3-large (1024 dimensions)
- **[PyPDF](https://pypdf.readthedocs.io/)** - PDF text extraction
- **[BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)** - HTML parsing for web search
- **[uv](https://github.com/astral-sh/uv)** - Ultra-fast Python package manager

### **Frontend**
- **[Next.js 15](https://nextjs.org/)** - React framework with Turbopack
- **[TypeScript](https://www.typescriptlang.org/)** - Type-safe JavaScript
- **[Tailwind CSS](https://tailwindcss.com/)** - Utility-first CSS framework
- **[Shadcn/ui](https://ui.shadcn.com/)** - Re-usable component library
- **[Axios](https://axios-http.com/)** - HTTP client for API calls

### **Development Tools**
- **[Concurrently](https://www.npmjs.com/package/concurrently)** - Run multiple dev servers
- **[Pytest](https://pytest.org/)** - Python testing framework
- **[NLTK](https://www.nltk.org/)** - Natural language processing

---

## Architecture

### **Complete System Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    1. DOCUMENT UPLOAD                        │
│  User uploads file → Frontend → Backend API → Temp storage  │
│  Supported: PDF, DOCX, TXT                                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                 2. DOCUMENT PROCESSING                       │
│  ├─ Text extraction (PyPDF, python-docx)                   │
│  ├─ Unicode & escape character cleaning                    │
│  ├─ Semantic chunking (1000 chars, 200 overlap)           │
│  └─ Original filename preservation in metadata             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   3. EMBEDDING GENERATION                    │
│  ├─ OpenAI text-embedding-3-large (1024 dims)              │
│  ├─ Batch processing (100 vectors per batch)               │
│  └─ Metadata: text, source_file, chunk_index               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  4. PINECONE VECTOR STORAGE                  │
│  ├─ Upsert vectors with metadata                           │
│  ├─ Dotproduct metric                                       │
│  ├─ 1024-dimensional vectors                                │
│  └─ Auto file cleanup after processing                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      5. USER QUERY                           │
│  User asks question → Model selection → CrewAI Agent        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  6. CREWAI AGENT ROUTING                     │
│  Agent analyzes question and decides:                       │
│  ├─ General knowledge? → Direct answer                     │
│  ├─ Document-related? → Pinecone Search Tool               │
│  └─ Current info needed? → Web Search Tool                 │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│           7A. PINECONE SEARCH (if document query)            │
│  ├─ Generate query embedding (1024 dims)                   │
│  ├─ Search Pinecone (top_k=5)                               │
│  ├─ Return context with source metadata                    │
│  └─ Agent constructs answer with citations                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│           7B. WEB SEARCH (if current info needed)            │
│  ├─ DuckDuckGo search via BeautifulSoup                    │
│  ├─ Extract: Title, URL, Snippet                            │
│  ├─ Return formatted results with URLs                     │
│  └─ Agent constructs answer with web sources               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   8. LLM GENERATION                          │
│  ├─ CrewAI calls OpenRouter with selected model            │
│  ├─ Model: GPT-4o, Claude 3.5, Gemini, Llama, etc.        │
│  ├─ Context: Knowledge base or web search results          │
│  └─ Generate comprehensive answer                          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│               9. STREAMING RESPONSE (SSE)                    │
│  ├─ Send sources first (document or web)                   │
│  ├─ Stream answer in chunks (50 chars each)               │
│  ├─ Real-time display in frontend                          │
│  └─ Send completion signal when done                       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   10. FRONTEND DISPLAY                       │
│  ├─ Render streaming answer in real-time                   │
│  ├─ Display sources (documents or web URLs)                │
│  └─ User sees complete answer with citations               │
└─────────────────────────────────────────────────────────────┘
```


---

## Installation and Setup

### 1. Prerequisites

#### **Option A: Docker (Recommended)**
- **Docker** and **Docker Compose** installed
- **Pinecone API Key** - [Sign up](https://www.pinecone.io/) and create an index (1024 dimensions, dotproduct metric)
- **OpenRouter API Key** - [Sign up](https://openrouter.ai/) and add credits
- **OpenAI API Key** - For embeddings

#### **Option B: Local Development**
- **Python 3.11+**
- **Node.js 20+**
- **Pinecone API Key** - [Sign up](https://www.pinecone.io/) and create an index (1024 dimensions, dotproduct metric)
- **OpenRouter API Key** - [Sign up](https://openrouter.ai/) and add credits
- **OpenAI API Key** - For embeddings

### 2. Clone the Repository

```bash
git clone https://github.com/praneethravuri/notstuck.git
cd notstuck
```

### 3. Environment Configuration

Create a `backend/.env` file with your API keys:

```bash
# OpenRouter Configuration (for LLM models)
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# OpenAI Configuration (for embeddings)
OPENAI_API_KEY=your_openai_api_key_here

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENV=us-east-1
PINECONE_INDEX_NAME=notstuck-index

# Model Configuration (optional - can be changed in UI)
DEFAULT_LLM_MODEL=openai/gpt-4o
DEFAULT_EMBEDDING_MODEL=text-embedding-3-large
EMBEDDING_DIMENSION=1024
```

Create a `frontend/.env.local` file:

```bash
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

> **Note**: A `.env.example` file is provided at the root for reference. Never commit your `.env` files.

### 4. Installation & Running

#### **🐳 Option A: Docker (Recommended)**

The easiest way to run NotStuck is using Docker Compose:

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**What happens:**
- ✅ Backend starts on `http://localhost:8000`
- ✅ Frontend starts on `http://localhost:3000`
- ✅ Automatic health checks and restart policies
- ✅ Isolated network for service communication
- ✅ Pinecone database is reset on backend startup

Visit `http://localhost:3000` to start using NotStuck!

**Docker Commands:**
```bash
# Rebuild specific service
docker-compose build backend
docker-compose build frontend

# View service logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Restart services
docker-compose restart

# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes
docker-compose down -v
```

#### **💻 Option B: Local Development (Without Docker)**

For local development with hot reload:

```bash
# Install root dependencies (concurrently)
npm install

# Install frontend dependencies
cd frontend && npm install && cd ..

# Install backend dependencies (using uv - ultra fast!)
cd backend && uv sync && cd ..

# Run both backend and frontend
npm run dev
```

This will:
- Start **backend first** on `http://localhost:8000`
- Then start **frontend** on `http://localhost:3000`
- Auto-reload both on file changes

**Individual Services:**

- **Backend only:**
  ```bash
  npm run dev:backend
  # or manually: cd backend && uv run uvicorn backend.api.main:app --reload
  ```

- **Frontend only:**
  ```bash
  npm run dev:frontend
  # or manually: cd frontend && npm run dev
  ```

#### **First Time Setup**

When you first run the backend (both Docker and local):
- ✅ Pinecone database is **automatically reset** on startup
- ✅ Required directories are created
- ✅ API connections are validated
- ✅ Health check endpoint available at `/health`

Visit `http://localhost:3000` in your browser to start using NotStuck!

---

## Usage

### **1. Select Your AI Model**
- Click the model selector in the header
- Choose from 10+ models (GPT-4o, Claude 3.5, Gemini Pro, Llama 3.1, etc.)
- Model selection affects all subsequent queries

### **2. Upload Documents**
- Click the paperclip icon or drag & drop files
- Supported formats: **PDF**, **DOCX**, **TXT**
- Files are processed with:
  - ✅ Text extraction (PyPDF, python-docx)
  - ✅ **Unicode and escape character cleaning**
  - ✅ **Original filename preservation**
  - ✅ Semantic chunking (1000 chars, 200 overlap)
  - ✅ Embedding generation (1024 dimensions)
  - ✅ Pinecone vector storage
- **No files saved locally** - uses temporary storage only
- **Automatic deletion** after processing

### **3. Ask Questions**
- Type your question in the chat input
- Press Enter or click Send
- **Streaming response** displays answer in real-time

**How the agent decides:**
- **General knowledge** (e.g., "What is photosynthesis?") → Direct answer from agent
- **Document questions** (e.g., "What does my resume say?") → Searches Pinecone knowledge base
- **Current info** (e.g., "Latest AI news?") → Web search with DuckDuckGo

Backend processing:
  - ✅ Intelligent routing (knowledge base / web / general)
  - ✅ Vector search with Pinecone (if document-related)
  - ✅ Web search with URLs (if current info needed)
  - ✅ Context optimization
  - ✅ LLM generation with streaming

### **4. View Sources**
- **Document sources**: Filename, chunk index, and extracted text
- **Web sources**: Title, URL, and snippet from search results
- Sources appear in the response for transparency

---

## API Documentation

Interactive API documentation is available when running the backend:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

### **Key Endpoints**

```
GET    /                        - Root endpoint with API info
GET    /health                  - Health check endpoint
GET    /docs                    - Interactive Swagger UI
GET    /redoc                   - ReDoc API documentation

GET    /api/models              - List available AI models
POST   /api/ask                 - Ask a question (streaming SSE)
POST   /api/upload              - Upload documents (PDF, DOCX, TXT)
```

**Example: Ask a Question**

```bash
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is machine learning?",
    "modelName": "openai/gpt-4o"
  }'
```

Response: Server-Sent Events (SSE) stream with:
- `sources` - Document or web sources
- `content` - Streaming answer chunks
- `done` - Completion signal

## Configuration

### **Environment Variables**

Key configuration options in `backend/.env`:

```bash
# Embedding Configuration
EMBEDDING_DIMENSION=1024                    # Must match Pinecone index
DEFAULT_EMBEDDING_MODEL=text-embedding-3-large

# LLM Configuration
DEFAULT_LLM_MODEL=openai/gpt-4o            # Can be changed in UI

# Pinecone Configuration
PINECONE_INDEX_NAME=notstuck-index
PINECONE_ENV=us-east-1                     # Your Pinecone region
```

### **Document Processing**

Configured in `backend/src/backend/tools/document_processor.py`:

```python
# Chunking
chunk_size = 1000           # Characters per chunk
chunk_overlap = 200         # Overlap for continuity
batch_size = 100            # Vectors per batch upsert
```

### **Agent Configuration**

Agents and tasks configured via YAML in `backend/src/backend/config/`:
- `agents.yaml` - Agent roles, goals, and backstory
- `tasks.yaml` - Task descriptions and expected outputs

---

## Project Structure

```
notstuck/
├── backend/
│   ├── src/
│   │   └── backend/
│   │       ├── api/              # FastAPI application
│   │       │   ├── routes/       # API endpoints (ask, upload, models)
│   │       │   └── main.py       # FastAPI app entry point
│   │       ├── clients/          # External API clients (Pinecone, OpenAI)
│   │       ├── config/           # Agent and task configurations (YAML)
│   │       ├── tools/            # CrewAI tools (document processor, web search, Pinecone search)
│   │       └── crew.py           # CrewAI agent definitions
│   ├── Dockerfile                # Backend Docker image
│   ├── .dockerignore             # Docker ignore patterns
│   ├── pyproject.toml            # Dependencies (uv)
│   ├── .env                      # Environment variables (not in git)
│   └── README.md                 # Backend docs
├── frontend/
│   ├── app/                      # Next.js app router
│   │   ├── api/                  # API routes (proxy to backend)
│   │   └── page.tsx              # Main page
│   ├── components/               # React components
│   │   └── common/               # Shared components (ChatMessages, ChatInput, etc.)
│   ├── hooks/                    # Custom hooks (useChatLogic, useBackendHealth)
│   ├── Dockerfile                # Frontend Docker image
│   ├── .dockerignore             # Docker ignore patterns
│   └── package.json              # Dependencies
├── docker-compose.yml            # Docker Compose configuration
├── .env.example                  # Example environment variables
├── package.json                  # Root dev scripts
└── README.md                     # This file
```

## Performance Optimizations

- ✅ **Batch embedding generation** - Process multiple chunks at once
- ✅ **Concurrent PDF processing** - ThreadPoolExecutor for parallel processing
- ✅ **Optimized chunking** - Semantic-aware separators
- ✅ **Adaptive filtering** - Statistical thresholds reduce noise
- ✅ **Context deduplication** - Jaccard similarity removes redundancy
- ✅ **Token-aware truncation** - Respects model context limits
- ✅ **Pinecone batch upsert** - 100 vectors per batch
- ✅ **Cosine similarity** - More accurate than dot product
- ✅ **Manual HTTP requests** - Avoids OpenAI SDK parsing overhead

## Troubleshooting

### Docker Issues

#### **Services won't start**
```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

#### **Backend health check failing**
- Ensure `.env` file exists in `backend/` directory
- Check Pinecone API key and index configuration
- Verify OpenAI API key for embeddings
- Wait 40 seconds for initial startup

#### **Frontend can't connect to backend**
- Check `NEXT_PUBLIC_BACKEND_URL` in docker-compose.yml
- Ensure backend service is healthy: `docker-compose ps`
- Check network: `docker network inspect notstuck_notstuck-network`

### Local Development Issues

#### **Backend won't start**
- Check `backend/.env` file has all required variables
- Verify Pinecone API key and index name (1024 dimensions)
- Ensure OpenAI API key is valid (for embeddings)
- Check Python version (3.11+)
- Run `cd backend && uv sync` to install dependencies

#### **Embeddings fail**
- OpenAI API key must be valid (for text-embedding-3-large)
- Check `EMBEDDING_DIMENSION=1024` in .env
- Verify Pinecone index dimension matches (1024)

#### **Upload fails**
- Check file is PDF, DOCX, or TXT format
- Verify Pinecone index exists with correct dimensions (1024)
- Check backend logs for detailed error messages
- Ensure temporary directory has write permissions

#### **Model selection doesn't work**
- Ensure backend is running first
- Check network tab for `/api/models` call
- Verify OpenRouter API key has access to models
- Check for CORS issues in browser console

#### **Streaming not working**
- Clear browser cache
- Check browser console for errors
- Verify `/api/ask` endpoint returns `text/event-stream`
- Ensure frontend is on latest version

#### **Unicode/emoji errors in console (Windows)**
- Fixed automatically in code via UTF-8 reconfiguration
- If issues persist, run: `chcp 65001` in terminal

## Contributing

Contributions are welcome! Please:

1. **Fork** the repository
2. Create a **feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit** changes (`git commit -m 'Add amazing feature'`)
4. **Push** to branch (`git push origin feature/amazing-feature`)
5. Open a **Pull Request**

### Areas for Contribution
- Additional LLM providers
- Advanced reranking algorithms
- UI/UX improvements
- Performance optimizations
- Test coverage
- Documentation

---

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute this project under the license terms.

---

## Roadmap

- [x] **Streaming responses** for real-time answer generation ✅
- [x] **Docker support** with Docker Compose ✅
- [x] **Web search integration** with source URLs ✅
- [x] **Intelligent agent routing** (knowledge base vs. web vs. general) ✅
- [ ] **Multi-document conversations** with context management
- [ ] **Advanced reranking** with cross-encoders
- [ ] **Document management** UI (view, delete, organize)
- [ ] **User authentication** and multi-user support
- [ ] **Custom model configuration** per query
- [ ] **Export conversations** as PDF/Markdown
- [ ] **Vector database alternatives** (Qdrant, Weaviate)
- [ ] **Image/OCR support** for scanned documents
- [ ] **Citation linking** to original document locations
- [ ] **Kubernetes deployment** manifests

## Acknowledgments

Built with:
- [CrewAI](https://www.crewai.com/) for intelligent multi-agent systems
- [FastAPI](https://fastapi.tiangolo.com/) by Sebastián Ramírez
- [Next.js](https://nextjs.org/) by Vercel
- [OpenRouter](https://openrouter.ai/) for multi-model API access
- [Pinecone](https://www.pinecone.io/) for vector database
- [uv](https://github.com/astral-sh/uv) by Astral for fast dependency management

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute.

## Contact & Support

- **Author:** [@praneethravuri](https://github.com/praneethravuri)
- **Issues:** [GitHub Issues](https://github.com/praneethravuri/notstuck/issues)
- **Discussions:** [GitHub Discussions](https://github.com/praneethravuri/notstuck/discussions)

---

**⭐ If this project helps you, please give it a star on GitHub!**

Thank you for using **NotStuck** - Your AI-powered document assistant!

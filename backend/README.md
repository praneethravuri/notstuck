# NotStuck Backend

RAG (Retrieval-Augmented Generation) backend API with multi-model LLM support via OpenRouter.

## Features

- **Multi-Model Support**: Choose from 10+ OpenRouter models dynamically (GPT-4, Claude, Gemini, Llama, etc.)
- **Hybrid Search**: Advanced retrieval combining semantic (dense) and keyword (sparse/BM25) search
- **Smart Chunking**: Semantic-aware text splitting with configurable overlap
- **Advanced Filtering**: Adaptive threshold using statistical analysis
- **Context Optimization**: Intelligent deduplication and truncation
- **Type Safety**: Full Pydantic validation for all API endpoints
- **PDF Processing**: Extract, chunk, clean, and index PDF documents
- **Production Ready**: Comprehensive error handling, logging, and monitoring

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

Or using `uv` (recommended):

```bash
cd backend
uv sync
```

### 2. Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
# OpenRouter Configuration (OpenAI-compatible API)
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENV=your_pinecone_environment_here
PINECONE_INDEX_NAME=your_pinecone_index_name_here

# Optional: Specific models to use (can be overridden at runtime)
# See https://openrouter.ai/models for available models
DEFAULT_LLM_MODEL=openai/gpt-4-turbo-preview
DEFAULT_EMBEDDING_MODEL=openai/text-embedding-3-large
```

### 3. Get API Keys

#### OpenRouter API Key
1. Sign up at [OpenRouter](https://openrouter.ai/)
2. Go to [API Keys](https://openrouter.ai/keys)
3. Create a new API key
4. Add credits to your account

#### Pinecone API Key
1. Sign up at [Pinecone](https://www.pinecone.io/)
2. Create a new index (dimension: 3072 for text-embedding-3-large)
3. Copy your API key from the dashboard

### 4. Run the Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

## Project Structure

```
backend/
├── app/
│   ├── clients/           # External API clients
│   │   ├── openai_client.py      # LLM client (OpenRouter/OpenAI)
│   │   ├── openai_embeddings.py  # Embedding client
│   │   └── pinecone_client.py    # Vector database client
│   ├── core/              # Core business logic
│   │   ├── query_llm.py          # LLM query functions
│   │   └── rag.py                # RAG pipeline
│   ├── helpers/           # Utility functions
│   │   ├── subjects_classifier.py # Text classification
│   │   └── ...
│   ├── routes/            # API endpoints
│   │   ├── ask.py                # Question answering
│   │   ├── upload.py             # Document upload
│   │   └── ...
│   ├── config.py          # Configuration management
│   ├── main.py            # FastAPI application
│   └── logging_config.py  # Logging setup
├── data/                  # Data storage
├── tests/                 # Unit and integration tests
├── .env                   # Environment variables (create this)
├── pyproject.toml         # Python dependencies
└── README.md              # This file
```

## Architecture

### LLM Integration (OpenRouter)

The backend uses OpenRouter for LLM access, which provides:
- **Unified API**: OpenAI-compatible API for 100+ models
- **Model Flexibility**: Switch between providers without code changes
- **Cost Optimization**: Choose the best model for each task
- **Fallback Support**: Automatic fallback to alternative models

### Key Modules

#### 1. LLM Client (`app/clients/openai_client.py`)
- OpenAI-compatible client configured for OpenRouter
- Supports any model available on OpenRouter
- Automatic error handling and logging

#### 2. Embeddings (`app/clients/openai_embeddings.py`)
- Vector embeddings for semantic search
- Compatible with OpenRouter's embedding models
- LangChain integration

#### 3. Query LLM (`app/core/query_llm.py`)
- High-level interface for LLM queries
- Type-safe function signatures
- Comprehensive error handling
- Simple and advanced query methods

#### 4. Subject Classifier (`app/helpers/subjects_classifier.py`)
- LLM-based text classification
- Subject detection for smart routing
- Category classification

## API Endpoints

### Models
- `GET /api/models` - List available OpenRouter models
- `GET /api/models/default` - Get default model configuration

### RAG (Question Answering)
```
POST /api/ask
Body: {
  "question": "Your question here",
  "modelName": "openai/gpt-4o",
  "subject": "optional-subject-filter"
}
```

### Documents
- `POST /api/upload` - Upload PDF documents
- `GET /api/get-pdfs` - List processed PDFs
- `GET /api/get-pdfs?filename=<name>` - Download specific PDF

### Database
- `DELETE /api/reset-pinecone-db` - Reset Pinecone database

### Health
- `GET /api/health-check` - Check backend status

### API Documentation
- Interactive docs at `http://localhost:8000/docs` when running

## Available Models

Some popular models available via OpenRouter:

### OpenAI
- `openai/gpt-4-turbo-preview`
- `openai/gpt-4o`
- `openai/gpt-3.5-turbo`

### Anthropic
- `anthropic/claude-3-opus`
- `anthropic/claude-3-sonnet`
- `anthropic/claude-3-haiku`

### Google
- `google/gemini-pro`
- `google/gemini-pro-vision`

### Meta
- `meta-llama/llama-3-70b-instruct`

### Others
- `mistralai/mistral-large`
- `cohere/command-r-plus`

See [OpenRouter Models](https://openrouter.ai/models) for the complete list.

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENROUTER_API_KEY` | OpenRouter API key | Yes | - |
| `OPENROUTER_BASE_URL` | OpenRouter base URL | No | `https://openrouter.ai/api/v1` |
| `PINECONE_API_KEY` | Pinecone API key | Yes | - |
| `PINECONE_ENV` | Pinecone environment | Yes | - |
| `PINECONE_INDEX_NAME` | Pinecone index name | Yes | - |
| `DEFAULT_LLM_MODEL` | Default LLM model | No | `openai/gpt-4-turbo-preview` |
| `DEFAULT_EMBEDDING_MODEL` | Default embedding model | No | `openai/text-embedding-3-large` |

## Development

### Running Tests
```bash
pytest tests/
```

### Code Style
```bash
black app/
flake8 app/
```

### Type Checking
```bash
mypy app/
```

## Troubleshooting

### LLM Client Not Initialized
- Check that `OPENROUTER_API_KEY` is set in `.env`
- Verify the API key is valid
- Check OpenRouter account has credits

### Pinecone Connection Error
- Verify `PINECONE_API_KEY` is correct
- Check `PINECONE_INDEX_NAME` matches your index
- Ensure index dimension is 3072

### Model Not Found
- Check model name format: `provider/model-name`
- Verify model is available on OpenRouter
- Check account has access to the model

## Migration from OpenAI

If migrating from direct OpenAI integration:

1. Old code will continue to work (backward compatible)
2. `OPENAI_API_KEY` now maps to `OPENROUTER_API_KEY`
3. Model names now use OpenRouter format: `openai/gpt-4` instead of `gpt-4`
4. Update model names in your code or use `DEFAULT_LLM_MODEL`

## 🔄 Complete RAG Pipeline

See [PIPELINE_FLOW.md](./PIPELINE_FLOW.md) for detailed documentation of the entire pipeline.

**Quick Overview:**
1. **Upload** → PDF validation → Text extraction → Semantic chunking → Subject detection → Embedding (dense + sparse) → Pinecone upsert
2. **Query** → Question embedding → Hybrid search → Adaptive filtering → Deduplication → Context building → Prompt construction → LLM generation

## 📊 Key Improvements

### Chunking Strategy
- ✅ Increased chunk size to 1000 chars with 200 overlap
- ✅ Semantic-aware separators (paragraphs, sentences)
- ✅ Minimum chunk size filtering (100 chars)

### Retrieval
- ✅ Changed metric from dotproduct to **cosine** for better similarity
- ✅ Increased TOP_K from 20 to **30** for better recall
- ✅ Adaptive thresholding using statistical analysis

### Context Building
- ✅ Jaccard similarity-based deduplication (85% threshold)
- ✅ Token-aware truncation (8000 max tokens)
- ✅ Preserves highest relevance chunks

### Prompts
- ✅ Enhanced system prompt with clear responsibilities
- ✅ Structured user prompt with context/question format
- ✅ Fallback handling when no context found

## Best Practices

1. **Model Selection**: Choose appropriate models for each task
   - Fast models (GPT-4o-mini, GPT-3.5) for simple questions
   - Powerful models (GPT-4o, Claude 3.5) for complex reasoning
   - Long context models (Gemini Pro 1.5) for large documents

2. **Error Handling**: System handles errors gracefully
   - Per-document error handling (continue on failure)
   - Comprehensive validation with Pydantic
   - Detailed logging for debugging

3. **Logging**: Structured logging at all stages
   - Request/response logging
   - Processing metrics (chunks, scores, tokens)
   - Performance monitoring
   - Error tracking with stack traces

4. **Security**: Built-in security features
   - File type validation (.pdf only)
   - File size limits (50MB max)
   - Input sanitization
   - Error message sanitization
   - Never commit `.env` file

## License

See the main project LICENSE file.

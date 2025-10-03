# Migration Guide: OpenAI to OpenRouter

This guide explains the changes made to migrate from OpenAI-only support to OpenRouter multi-model support.

## What Changed?

### 1. Environment Variables

**Before:**
```bash
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=...
PINECONE_ENV=...
PINECONE_INDEX_NAME=...
```

**After:**
```bash
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
PINECONE_API_KEY=...
PINECONE_ENV=...
PINECONE_INDEX_NAME=...
DEFAULT_LLM_MODEL=openai/gpt-4-turbo-preview
DEFAULT_EMBEDDING_MODEL=openai/text-embedding-3-large
```

### 2. Configuration (`app/config.py`)

**Added:**
- `OPENROUTER_API_KEY`: API key for OpenRouter
- `OPENROUTER_BASE_URL`: Base URL for OpenRouter API
- `DEFAULT_LLM_MODEL`: Default model to use
- `DEFAULT_EMBEDDING_MODEL`: Default embedding model

**Maintained:**
- `OPENAI_API_KEY`: Now maps to `OPENROUTER_API_KEY` for backward compatibility
- All Pinecone configuration remains the same

### 3. LLM Client (`app/clients/openai_client.py`)

**Before:**
```python
from openai import OpenAI

openai_client = OpenAI(api_key=OPENAI_API_KEY)
```

**After:**
```python
from openai import OpenAI
from app.config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL

def get_llm_client() -> OpenAI:
    client = OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url=OPENROUTER_BASE_URL
    )
    return client

openai_client = get_llm_client()
```

**Benefits:**
- Works with any OpenAI-compatible API
- Easy to switch between providers
- Better error handling
- Comprehensive documentation

### 4. Embeddings Client (`app/clients/openai_embeddings.py`)

**Before:**
```python
embedding_function = OpenAIEmbeddings(
    openai_api_key=OPENAI_API_KEY,
    model=EMBEDDING_MODEL
)
```

**After:**
```python
embedding_function = OpenAIEmbeddings(
    openai_api_key=OPENROUTER_API_KEY,
    openai_api_base=OPENROUTER_BASE_URL,
    model=EMBEDDING_MODEL
)
```

**Benefits:**
- Supports OpenRouter's embedding endpoint
- Configurable embedding models
- Better error handling

### 5. Query LLM (`app/core/query_llm.py`)

**Added:**
- Type hints for better IDE support
- Comprehensive docstrings
- `query_llm_simple()` function for simple queries
- Better error messages

**Before:**
```python
def query_llm(model_name: str, messages: list, temperature: float, max_tokens: int) -> str:
    response = openai_client.chat.completions.create(...)
    return response.choices[0].message.content.strip()
```

**After:**
```python
def query_llm(
    model_name: str,
    messages: List[Dict[str, str]],
    temperature: float,
    max_tokens: int
) -> str:
    """Comprehensive docstring with examples..."""
    if not openai_client:
        raise RuntimeError("LLM client is not initialized")
    # ... rest of implementation

def query_llm_simple(
    prompt: str,
    model_name: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 500
) -> str:
    """Simplified interface for single prompts..."""
```

### 6. Subject Classifier (`app/helpers/subjects_classifier.py`)

**Added:**
- Type hints
- `classify_text()` function for category classification
- Better documentation
- Configurable parameters

**Model Name Change:**
```python
# Before
model="gpt-4o"

# After
model="openai/gpt-4o"  # OpenRouter format
```

### 7. Main Application (`app/main.py`)

**Enhanced:**
- Better startup logging with checkmarks (✓/✗)
- FastAPI metadata (title, description, version)
- More descriptive error messages
- Validates OpenRouter configuration

## Model Name Format

OpenRouter uses a `provider/model` format:

| Provider | Before | After |
|----------|---------|--------|
| OpenAI | `gpt-4-turbo-preview` | `openai/gpt-4-turbo-preview` |
| OpenAI | `gpt-4o` | `openai/gpt-4o` |
| OpenAI | `gpt-3.5-turbo` | `openai/gpt-3.5-turbo` |
| Anthropic | N/A | `anthropic/claude-3-opus` |
| Google | N/A | `google/gemini-pro` |
| Meta | N/A | `meta-llama/llama-3-70b-instruct` |

## Breaking Changes

### ⚠️ Model Names Must Be Updated

If you have hardcoded model names in your code, update them:

```python
# Before
model_name = "gpt-4-turbo-preview"

# After
model_name = "openai/gpt-4-turbo-preview"
# OR use the default from config
from app.config import DEFAULT_LLM_MODEL
model_name = DEFAULT_LLM_MODEL
```

### ⚠️ Environment Variables

You must update your `.env` file to use `OPENROUTER_API_KEY` instead of `OPENAI_API_KEY`.

## Non-Breaking Changes

### ✅ API Compatibility

The OpenAI client interface remains the same:
```python
# This still works!
openai_client.chat.completions.create(
    model="openai/gpt-4-turbo-preview",
    messages=[...],
    temperature=0.7
)
```

### ✅ Existing Code

Most existing code will work without changes because:
- The client interface is identical
- `OPENAI_API_KEY` maps to `OPENROUTER_API_KEY`
- All function signatures are backward compatible

## New Features

### 1. Multi-Model Support

```python
# Use OpenAI models
query_llm("openai/gpt-4-turbo-preview", messages, 0.7, 500)

# Use Anthropic Claude
query_llm("anthropic/claude-3-opus", messages, 0.7, 500)

# Use Google Gemini
query_llm("google/gemini-pro", messages, 0.7, 500)
```

### 2. Simple Query Interface

```python
from app.core.query_llm import query_llm_simple

# Quick one-liner queries
answer = query_llm_simple("Explain Python in one sentence")

# With custom model
answer = query_llm_simple(
    "Explain RAG systems",
    model_name="anthropic/claude-3-sonnet"
)
```

### 3. Better Error Handling

All modules now have:
- Proper exception handling
- Descriptive error messages
- Validation of required configuration
- Graceful fallbacks

### 4. Improved Documentation

All functions now have:
- Type hints
- Comprehensive docstrings
- Usage examples
- Parameter descriptions

## Migration Steps

### Step 1: Update Environment Variables

1. Copy `backend/.env.example` to `backend/.env`
2. Fill in your OpenRouter API key
3. Fill in your Pinecone credentials
4. Optionally set default models

### Step 2: Update Model Names (if hardcoded)

Search your codebase for hardcoded model names:
```bash
cd backend
grep -r "gpt-4" app/
grep -r "gpt-3.5" app/
```

Update them to OpenRouter format:
```python
"gpt-4" → "openai/gpt-4"
"gpt-4o" → "openai/gpt-4o"
```

### Step 3: Test Your Application

```bash
# Run tests
pytest tests/

# Start the server
uvicorn app.main:app --reload

# Check health
curl http://localhost:8000/api/health-check
```

### Step 4: Verify Logs

Check the startup logs for:
```
✓ Pinecone index initialized successfully
✓ LLM client initialized successfully
  Base URL: https://openrouter.ai/api/v1
Application startup complete!
```

## Rollback Plan

If you need to rollback:

1. **Revert environment variables:**
   ```bash
   OPENAI_API_KEY=sk-...  # Your OpenAI key
   ```

2. **Revert config.py:**
   ```python
   OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
   ```

3. **Revert client:**
   ```python
   openai_client = OpenAI(api_key=OPENAI_API_KEY)
   ```

4. **Update model names back:**
   ```python
   "openai/gpt-4" → "gpt-4"
   ```

## Benefits of OpenRouter

### 1. Cost Optimization
- Compare prices across providers
- Use cheaper models for simple tasks
- Use powerful models only when needed

### 2. Flexibility
- Switch models without code changes
- Test different providers easily
- Avoid vendor lock-in

### 3. Reliability
- Automatic fallback to alternative models
- Multiple provider support
- Better uptime

### 4. Access to More Models
- 100+ models from 20+ providers
- Latest models available quickly
- Specialized models for specific tasks

## Support

For issues or questions:
- Check the [OpenRouter Documentation](https://openrouter.ai/docs)
- See the [Backend README](README.md)
- Review code comments and docstrings

## Summary

The migration to OpenRouter provides:
- ✅ Multi-model support (OpenAI, Anthropic, Google, Meta, etc.)
- ✅ Better error handling and validation
- ✅ Comprehensive documentation
- ✅ Backward compatibility with minimal changes
- ✅ Modular, maintainable code structure
- ✅ Type hints and better IDE support
- ✅ Simplified query interfaces

All while maintaining the same OpenAI-compatible API interface!

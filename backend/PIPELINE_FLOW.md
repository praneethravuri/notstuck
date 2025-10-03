# NotStuck RAG Pipeline - Complete Flow Documentation

## Architecture Overview

```
┌─────────────┐
│  Frontend   │
│  (Next.js)  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│            Frontend API Routes (Next.js)                │
│  /api/models  |  /api/upload  |  /api/ask              │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              Backend (FastAPI)                          │
│  Routes → Services → Core → Clients                     │
└──────────────────────┬──────────────────────────────────┘
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
    ┌──────────┐            ┌──────────────┐
    │ Pinecone │            │  OpenRouter  │
    │ (Vectors)│            │    (LLM)     │
    └──────────┘            └──────────────┘
```

---

## 1. Model Selection Flow

### Step-by-Step Process

```
1. Frontend Initialization (page.tsx)
   └─> ModelSelector component mounts
       └─> useEffect fetches /api/models

2. Frontend API (/api/models/route.ts)
   └─> Forwards to backend: GET ${BACKEND_URL}/api/models

3. Backend (routes/models.py)
   └─> Returns curated list of OpenRouter models
       └─> Includes: GPT-4o, Claude, Gemini, Llama, etc.

4. Frontend (ModelSelector.tsx)
   └─> Renders dropdown with available models
   └─> Sets default model (openai/gpt-4o)
   └─> User selects model → Updates state in useChatLogic
```

### Data Flow

**Request:**
```
GET /api/models
```

**Response:**
```json
{
  "models": [
    {
      "id": "openai/gpt-4o",
      "name": "GPT-4o",
      "description": "OpenAI's most advanced model",
      "context_length": 128000,
      "provider": "openai"
    },
    // ... more models
  ],
  "count": 10
}
```

**Validation:** Pydantic model `ModelsListResponse`

---

## 2. Document Upload Flow

### Step-by-Step Process

```
1. User Action (Frontend)
   └─> User selects PDF file(s) via ChatInput
       └─> File button or drag-and-drop

2. Frontend (useChatLogic.ts - handleFileUpload)
   └─> Creates FormData with files
   └─> POST to /api/upload
   └─> Shows upload progress indicator

3. Frontend API (app/api/upload/route.ts)
   └─> Validates FormData
   └─> Forwards to backend: POST ${BACKEND_URL}/api/upload

4. Backend Route (routes/upload.py)
   ├─> Validates files:
   │   ├─> Check file count (max 20)
   │   ├─> Check extensions (.pdf only)
   │   └─> Check file size (max 50MB)
   └─> Calls save_files() and process_and_upsert()

5. Backend Service (services/upload_services.py)
   ├─> save_files()
   │   └─> Saves files to RAW_DATA_PATH
   └─> process_and_upsert()
       └─> Calls document processing

6. Document Processing (services/document_services.py)
   ├─> process_pdf_files()
   │   └─> Concurrent processing (ThreadPoolExecutor)
   └─> For each PDF:
       ├─> PyPDFLoader loads pages
       ├─> RecursiveCharacterTextSplitter chunks text
       │   ├─> Chunk size: 1000 chars
       │   ├─> Overlap: 200 chars
       │   └─> Semantic separators (paragraphs, sentences)
       ├─> clean_pdf_text() cleans each chunk
       ├─> detect_subjects() tags with LLM
       └─> Returns structured chunks

7. Embedding & Upserting (vector_db/pinecone_db.py)
   ├─> Fit BM25 encoder on all chunks (sparse)
   ├─> Save BM25 state to JSON
   ├─> Get OpenAI embedding function (dense)
   └─> For each document:
       ├─> Generate dense embeddings (batch)
       ├─> Generate sparse embeddings (BM25)
       ├─> Create vectors with metadata:
       │   ├─> Dense values (3072 dimensions)
       │   ├─> Sparse values (BM25)
       │   └─> Metadata (text, source_file, page, subjects)
       ├─> Upsert to Pinecone (batch size: 100)
       └─> Move file to PROCESSED_DATA_PATH

8. Response to Frontend
   └─> Success message with file count
```

### Data Flow

**Request:**
```
POST /api/upload
Content-Type: multipart/form-data

FormData {
  files: [File, File, ...]
}
```

**Response:**
```json
{
  "message": "Files uploaded and processed successfully",
  "files": ["document1.pdf", "document2.pdf"],
  "count": 2
}
```

**Validation:** File validation in `routes/upload.py`

---

## 3. Query/Ask Flow (RAG Pipeline)

### Step-by-Step Process

```
1. User Question (Frontend)
   └─> User types question in ChatInput
       └─> Hits Enter or clicks Send

2. Frontend (useChatLogic.ts - handleSendMessage)
   ├─> Adds user message to chat
   ├─> Creates request with:
   │   ├─> question: string
   │   └─> modelName: string (from ModelSelector)
   └─> POST to /api/ask

3. Frontend API (app/api/ask/route.ts)
   └─> Forwards to backend: POST ${BACKEND_URL}/api/ask
       └─> Body: { question, modelName }

4. Backend Route (routes/ask.py)
   ├─> Validates request with Pydantic (QuestionRequest)
   │   ├─> question: 1-5000 chars
   │   ├─> modelName: required
   │   └─> subject: optional filter
   └─> Calls answer_question()

5. RAG Orchestration (core/rag.py - answer_question)
   ├─> Step 1: Generate Queries
   │   └─> rag_utils.generate_queries()
   │       ├─> Dense query: OpenAI embeddings (3072 dims)
   │       └─> Sparse query: BM25 encoding
   │
   ├─> Step 2: Apply Hybrid Weighting
   │   └─> rag_utils.apply_hybrid_weighting()
   │       ├─> Dense weight: 0.7 (semantic search)
   │       └─> Sparse weight: 0.3 (keyword search)
   │
   ├─> Step 3: Build Filter (if subject provided)
   │   └─> rag_utils.build_filter()
   │       └─> Pinecone metadata filter
   │
   ├─> Step 4: Retrieve from Pinecone
   │   └─> pinecone_query.retrieve_matches()
   │       ├─> Query Pinecone with hybrid vectors
   │       ├─> top_k: 30 results
   │       ├─> namespace: "my-namespace"
   │       └─> Returns matches with scores
   │
   ├─> Step 5: Filter Matches
   │   └─> pinecone_query.filter_matches_by_threshold()
   │       ├─> Calculate statistics (mean, std)
   │       ├─> Adaptive threshold: mean - 0.5*std
   │       ├─> Minimum threshold: 0.65
   │       └─> Keep at least top 3 matches
   │
   ├─> Step 6: Build Context
   │   └─> rag_utils.build_context_text()
   │       ├─> Extract text from matches
   │       ├─> Deduplicate (Jaccard similarity > 0.85)
   │       ├─> Truncate to max tokens (8000)
   │       └─> Join with separators
   │
   ├─> Step 7: Build Prompts
   │   ├─> prompt_builder.build_system_prompt()
   │   │   └─> Detailed RAG instructions
   │   └─> prompt_builder.build_user_prompt()
   │       └─> Context + Question formatted
   │
   └─> Step 8: Query LLM
       └─> query_llm.query_llm()
           ├─> Client: OpenRouter (OpenAI-compatible)
           ├─> Model: User-selected model
           ├─> Temperature: 0.3 (focused)
           ├─> Max tokens: 3000
           └─> Returns answer

6. Response Processing (routes/ask.py)
   ├─> Convert metadata to Pydantic models
   ├─> Build QuestionResponse:
   │   ├─> answer: string
   │   ├─> relevant_chunks: List[str]
   │   └─> sources_metadata: List[SourceMetadata]
   └─> Return validated response

7. Frontend Display
   ├─> useChatLogic receives response
   ├─> Adds AI message to chat
   └─> ChatMessages renders answer with sources
```

### Data Flow

**Request:**
```json
POST /api/ask

{
  "question": "What is the main topic of the document?",
  "modelName": "openai/gpt-4o",
  "subject": null  // optional
}
```

**Response:**
```json
{
  "answer": "Based on the documents provided, the main topic is...",
  "relevant_chunks": [
    "Text chunk 1...",
    "Text chunk 2..."
  ],
  "sources_metadata": [
    {
      "source_file": "document.pdf",
      "page_number": 5,
      "text": "Original chunk text...",
      "subjects": "programming, python"
    }
  ]
}
```

**Validation:** Pydantic models `QuestionRequest` and `QuestionResponse`

---

## 4. Key Configuration Parameters

### Backend (app/config.py)

```python
# Chunking
CHUNK_SIZE = 1000          # Larger chunks for better context
CHUNK_OVERLAP = 200        # More overlap for continuity
CHUNK_MIN_SIZE = 100       # Filter tiny chunks

# Pinecone
TOP_K = 30                 # More results for better recall
PINECONE_METRIC = "cosine" # Better than dotproduct
PINECONE_EMBEDDING_DIMENSIONS = 3072  # text-embedding-3-large

# RAG
HYBRID_WEIGHT_RATIO = 0.7  # 70% semantic, 30% keyword
SIMILARITY_THRESHOLD = 0.65  # Adaptive threshold baseline
TEMPERATURE = 0.3          # Low for focused answers
MAX_TOKENS = 3000          # LLM response limit
MAX_CONTEXT_TOKENS = 8000  # Context size limit
```

### Frontend (useChatLogic.ts)

```typescript
const [modelName, setModelName] = useState("openai/gpt-4o");
// Model is dynamically loaded from backend
```

---

## 5. Error Handling

### Frontend
- Network errors → Toast notifications
- Invalid responses → Error messages in chat
- File upload failures → User feedback
- Model loading failures → Fallback to defaults

### Backend
- Pydantic validation → 400 Bad Request
- Processing errors → 500 Internal Server Error
- Per-document error handling → Continue processing other docs
- Detailed logging at all stages

---

## 6. Security & Validation

### Input Validation
- ✅ File type restrictions (.pdf only)
- ✅ File size limits (50MB)
- ✅ File count limits (20 files)
- ✅ Question length limits (5000 chars)
- ✅ Model name validation

### Output Validation
- ✅ Pydantic response models
- ✅ Type-safe frontend interfaces
- ✅ Sanitized error messages

---

## 7. Performance Optimizations

### Embedding Generation
- ✅ Batch processing (embed_documents)
- ✅ Concurrent PDF processing (ThreadPoolExecutor)
- ✅ Optimized Pinecone batch size (100 vectors)

### Context Building
- ✅ Deduplication (remove similar chunks)
- ✅ Token-aware truncation
- ✅ Adaptive filtering (statistical thresholds)

### Retrieval
- ✅ Hybrid search (semantic + keyword)
- ✅ Cosine similarity metric
- ✅ Increased TOP_K for better recall

---

## 8. Monitoring & Logging

Each stage logs:
- ✅ Request details (question, model, files)
- ✅ Processing metrics (chunk counts, scores)
- ✅ Performance data (tokens, durations)
- ✅ Error traces (full stack traces)

---

## Summary

This RAG pipeline provides:
1. **Dynamic Model Selection** - User chooses from 10+ OpenRouter models
2. **Robust Document Processing** - Semantic chunking, cleaning, tagging
3. **Advanced Retrieval** - Hybrid search with adaptive filtering
4. **Intelligent Context Building** - Deduplication and truncation
5. **Optimized Prompting** - Clear instructions for accurate answers
6. **Type-Safe API** - Pydantic validation throughout
7. **Comprehensive Error Handling** - Graceful degradation
8. **Performance Optimized** - Batching, concurrency, caching

# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Configure API Keys

Edit `backend/.env`:

```bash
# Your OpenRouter API key (get it from https://openrouter.ai/keys)
OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here

# Your Pinecone credentials (get from https://app.pinecone.io/)
PINECONE_API_KEY=your-actual-pinecone-key
PINECONE_ENV=us-east-1
PINECONE_INDEX_NAME=your-index-name
```

### Step 2: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Run the Server

```bash
uvicorn app.main:app --reload
```

Visit: http://localhost:8000/api/health-check

## ✅ What You Get

- **100+ AI Models**: Access to GPT-4, Claude, Gemini, Llama, and more via OpenRouter
- **Smart Search**: Hybrid vector + keyword search with Pinecone
- **PDF Processing**: Upload and search through your documents
- **Cost Effective**: Choose the right model for each task

## 🎯 Quick Examples

### Use Different Models

In your frontend or API calls:

```json
{
  "question": "Explain quantum computing",
  "modelName": "openai/gpt-4-turbo-preview"
}
```

Or switch to Claude:

```json
{
  "question": "Explain quantum computing",
  "modelName": "anthropic/claude-3-sonnet"
}
```

### Popular Model Options

| Model | Use Case | Cost |
|-------|----------|------|
| `openai/gpt-3.5-turbo` | Fast, cheap queries | $ |
| `openai/gpt-4-turbo-preview` | Complex reasoning | $$$ |
| `anthropic/claude-3-haiku` | Fast, balanced | $ |
| `anthropic/claude-3-sonnet` | Best quality/price | $$ |
| `anthropic/claude-3-opus` | Most capable | $$$$ |
| `google/gemini-pro` | Google's latest | $$ |

See all models: https://openrouter.ai/models

## 🔧 Troubleshooting

### "LLM client not initialized"
- Check `OPENROUTER_API_KEY` is set in `.env`
- Verify you have credits on OpenRouter

### "Pinecone connection error"
- Verify `PINECONE_API_KEY` is correct
- Check index exists and dimension is 3072

### "Model not found"
- Use OpenRouter format: `provider/model-name`
- Example: `openai/gpt-4` not `gpt-4`

## 📚 Learn More

- [Full Documentation](README.md)
- [Migration Guide](MIGRATION_GUIDE.md)
- [OpenRouter Docs](https://openrouter.ai/docs)
- [Pinecone Docs](https://docs.pinecone.io/)

## 💡 Pro Tips

1. **Set Default Model**: Edit `DEFAULT_LLM_MODEL` in `.env` to avoid specifying it every time
2. **Save Money**: Use GPT-3.5 for simple tasks, GPT-4 only when needed
3. **Test Models**: OpenRouter makes it easy to test different models without code changes
4. **Monitor Usage**: Check your OpenRouter dashboard for usage and costs

## 🆘 Need Help?

1. Check the logs: Look for `✓` or `✗` in startup logs
2. Test health: `curl http://localhost:8000/api/health-check`
3. Read full docs: See `README.md` for detailed information

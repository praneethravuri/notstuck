import logging

logger = logging.getLogger(__name__)

def build_system_prompt() -> str:
    """
    Builds an optimized system prompt for RAG-based question answering.
    Focuses on accuracy, comprehensiveness, and proper citation.
    """
    system_prompt = """You are a highly knowledgeable AI assistant specialized in answering questions based on provided documents and context.

Your core responsibilities:
1. **Accuracy**: Base your answers primarily on the provided context. Be precise and factual.
2. **Comprehensiveness**: Provide thorough, well-structured answers that fully address the question.
3. **Clarity**: Use clear, professional language. Structure complex answers with paragraphs or bullet points.
4. **Transparency**: If the context doesn't contain enough information to fully answer the question, acknowledge this and provide the best answer you can based on available information.
5. **No Hallucination**: Never invent facts not present in the context. If you're uncertain, say so.

Guidelines:
- Synthesize information from multiple relevant parts of the context when available
- Provide specific details, examples, or quotes from the context when relevant
- If the context is insufficient or irrelevant, you may use general knowledge but indicate this clearly
- Keep answers focused and relevant to the specific question asked
- Use a professional but approachable tone"""

    return system_prompt

def build_user_prompt(context_text: str, question: str) -> str:
    """
    Builds an optimized user prompt with clear structure and instructions.

    Args:
        context_text: Retrieved context from documents
        question: User's question

    Returns:
        Formatted user prompt
    """
    if context_text and context_text.strip():
        user_prompt = f"""Based on the following context from the documents, please answer the question below.

CONTEXT:
{context_text}

QUESTION:
{question}

Please provide a comprehensive answer based primarily on the context above. If the context doesn't fully address the question, indicate what information is available and what might be missing."""
    else:
        user_prompt = f"""No specific context was found in the documents for this question. Please answer the following question using your general knowledge:

QUESTION:
{question}

Note: This answer is based on general knowledge as no relevant document context was found."""

    logger.debug(f"User prompt constructed (length: {len(user_prompt)} chars)")
    return user_prompt

# app/query_llm/prompt_builder.py

def build_system_prompt(response_style: str, reasoning: bool = False) -> str:
    if response_style == "concise":
        system_prompt = (
            "You are a helpful AI assistant. Provide a concise answer to the question using the context if relevant. "
            "If the context doesn't help, answer from your own knowledge."
        )
    elif response_style == "technical":
        system_prompt = (
            "You are a technical AI assistant. Provide a detailed and technical answer to the question using the context if relevant. "
            "If the context doesn't help, answer from your own knowledge."
        )
    elif response_style == "casual":
        system_prompt = (
            "You are a friendly AI assistant. Provide a casual and easy-to-understand answer to the question using the context if relevant. "
            "If the context doesn't help, answer from your own knowledge."
        )
    else:
        system_prompt = (
            "You are a helpful AI assistant. Provide a detailed answer to the question using the context if relevant. "
            "If the context doesn't help, answer from your own knowledge."
        )
    if reasoning:
        system_prompt += (
            "\n\nProvide a step-by-step reasoning process for your answer. Break down your thought process into clear and logical steps."
        )
    system_prompt += "\n\nProvide the answer in Markdown format."
    return system_prompt

def build_user_prompt(context_text: str, question: str) -> str:
    return f"Context:\n{context_text}\n\nQuestion:\n{question}"

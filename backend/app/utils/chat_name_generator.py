# backend/app/utils/chat_name_generator.py
from openai import OpenAI
import datetime
from app.config import OPENAI_API_KEY

client = OpenAI()
client.api_key = OPENAI_API_KEY

async def generate_chat_name_from_llm(question: str) -> str:
    prompt = (
        f"Generate a concise chat title for a conversation about the following topic:\n\n"
        f"'{question}'\n\n"
        "Title:"
    )
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that generates conversation titles."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=10,
        )
        chat_name = response.choices[0].message.content.strip()
        return chat_name
    except Exception as e:
        print(e)
        # Fallback to a default title if the LLM call fails.
        return f"Chat {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}"

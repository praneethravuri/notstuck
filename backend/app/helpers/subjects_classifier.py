import logging
from app.clients.openai_client import openai_client

logger = logging.getLogger(__name__)

def detect_subjects(text: str) -> str:
    """
    Uses the OpenAI API to determine the subject of a given text.
    The prompt instructs the model to return a single word representing the primary subject.
    """
    try:
        prompt = (
            "Based on the following text, identify the primary subjects. "
            "Return ONLY a comma-separated list of relevant subjects.\n\n"
            f"Text:\n{text[:3000]}\n\nSubjects:"
        )
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a text classification assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=25
        )
        raw = response.choices[0].message.content.lower().strip()
        subjects = sorted(
            list(set([s.strip() for s in raw.split(",") if s.strip()]))
        )
        logger.info("Detected subjects: %s", subjects)
        return subjects
    except Exception as e:
        logger.error("Error detecting subject: %s", e, exc_info=True)
        return "general"

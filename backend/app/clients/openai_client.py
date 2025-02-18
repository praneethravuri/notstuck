import logging
from openai import OpenAI
from app.config import OPENAI_API_KEY

logger = logging.getLogger(__name__)

try:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
    logger.info("OpenAI client initialized successfully.")
except Exception as e:
    logger.error("Failed to initialize OpenAI client.", exc_info=True)
    openai_client = None

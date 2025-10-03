"""
Subject Classification Module

This module provides text classification functionality to detect subjects/topics
in a given text using LLM-based classification.
"""
import logging
from typing import List
from app.clients.openai_client import openai_client

logger = logging.getLogger(__name__)

def detect_subjects(text: str, max_text_length: int = 3000) -> List[str]:
    """
    Uses an LLM to determine the primary subjects of a given text.

    Args:
        text: The text to classify
        max_text_length: Maximum length of text to process (default: 3000 chars)

    Returns:
        List[str]: Sorted list of unique subject identifiers

    Example:
        >>> text = "Python is a programming language used for web development..."
        >>> subjects = detect_subjects(text)
        >>> print(subjects)
        ['programming', 'python', 'web development']
    """
    if not openai_client:
        logger.error("LLM client is not initialized")
        return ["general"]

    try:
        # Truncate text to max length
        truncated_text = text[:max_text_length]

        prompt = (
            "Based on the following text, identify the primary subjects. "
            "Return ONLY a comma-separated list of relevant subjects.\n\n"
            f"Text:\n{truncated_text}\n\nSubjects:"
        )

        response = openai_client.chat.completions.create(
            model="openai/gpt-4o",  # Using OpenRouter format
            messages=[
                {"role": "system", "content": "You are a text classification assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=25
        )

        raw = response.choices[0].message.content.lower().strip()

        # Parse and clean the subjects
        subjects = sorted(
            list(set([s.strip() for s in raw.split(",") if s.strip()]))
        )

        logger.info("Detected subjects: %s", subjects)
        return subjects

    except Exception as e:
        logger.error("Error detecting subject: %s", e, exc_info=True)
        return ["general"]


def classify_text(text: str, categories: List[str]) -> str:
    """
    Classifies text into one of the provided categories.

    Args:
        text: The text to classify
        categories: List of possible categories

    Returns:
        str: The most appropriate category

    Example:
        >>> text = "How do I install Python packages?"
        >>> categories = ["programming", "design", "business", "general"]
        >>> category = classify_text(text, categories)
        >>> print(category)
        'programming'
    """
    if not openai_client:
        logger.error("LLM client is not initialized")
        return categories[0] if categories else "general"

    try:
        categories_str = ", ".join(categories)
        prompt = (
            f"Classify the following text into ONE of these categories: {categories_str}\n\n"
            f"Text: {text[:1000]}\n\n"
            "Return ONLY the category name, nothing else."
        )

        response = openai_client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[
                {"role": "system", "content": "You are a text classification assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=10
        )

        category = response.choices[0].message.content.strip().lower()

        # Validate the response is in the categories
        if category in [c.lower() for c in categories]:
            logger.info(f"Classified text as: {category}")
            return category
        else:
            logger.warning(f"Invalid category '{category}', defaulting to first category")
            return categories[0] if categories else "general"

    except Exception as e:
        logger.error("Error classifying text: %s", e, exc_info=True)
        return categories[0] if categories else "general"

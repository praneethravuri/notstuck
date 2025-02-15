import re
from typing import Dict
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def clean_text(text: str) -> str:
    """
    Cleans the input text using tokenization, noise removal,
    normalization, stopword removal, and lemmatization.
    """
    # Tokenization
    tokens = word_tokenize(text)
    
    # Remove Noise: remove punctuation and other non-word characters
    cleaned_tokens = [re.sub(r'[^\w\s]', '', token) for token in tokens]
    
    # Normalization: convert to lowercase
    cleaned_tokens = [token.lower() for token in cleaned_tokens]
    
    # Remove Stopwords
    stop_words = set(stopwords.words('english'))
    cleaned_tokens = [token for token in cleaned_tokens if token not in stop_words and token.strip() != '']
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    cleaned_tokens = [lemmatizer.lemmatize(token) for token in cleaned_tokens]
    
    # Rejoin tokens into a string
    return ' '.join(cleaned_tokens)
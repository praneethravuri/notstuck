# get_embedding_function.py

import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

# Load environment variables from .env
load_dotenv()

# Read OPENAI_API_KEY from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_embedding_function():
    return OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model="text-embedding-3-small")

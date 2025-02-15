import re
import nltk

def clean_pdf_text(text):
    ascii_text = text.encode('ascii', 'ignore').decode('ascii')
    tokens = nltk.word_tokenize(ascii_text)
    cleaned_text = " ".join(tokens)
    
    return cleaned_text
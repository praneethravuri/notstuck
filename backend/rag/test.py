import os
from dotenv import load_dotenv
from llama_cloud_services import LlamaParse
from llama_index.core import SimpleDirectoryReader

# Load environment variables (including LLAMA_CLOUD_API_KEY)
load_dotenv()

# Define the path to your data directory
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data")

# Set up the LlamaParse parser
parser = LlamaParse(
    result_type="markdown"  # "markdown" and "text" are available
)

# Configure the file extractor to use LlamaParse for ALL file types
file_extractor = {".*": parser}  # Use wildcard to parse all file types

# Use SimpleDirectoryReader to parse all files in the directory
documents = SimpleDirectoryReader(
    input_dir=DATA_PATH,
    recursive=True,
    file_extractor=file_extractor
).load_data()

# Print the contents of the documents
for doc in documents:
    print(doc.text)
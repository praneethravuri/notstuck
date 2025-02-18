import logging
import logging.handlers
from app.config import LOG_FILE_PATH

# Create a logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Create a file handler that logs debug and higher level messages
file_handler = logging.handlers.RotatingFileHandler(LOG_FILE_PATH, maxBytes=10**6, backupCount=3)
file_handler.setLevel(logging.DEBUG)

# Create a console handler for output to the terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and set it for both handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

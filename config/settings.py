"""Application settings and configuration constants."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============================================================================
# APPLICATION INFO
# ============================================================================
APP_NAME = "DexGA"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Document Extraction using Gemma with Localization"

# ============================================================================
# DIRECTORY CONFIGURATION
# ============================================================================
BASE_DIR = Path(__file__).parent.parent
TEMP_DIR = BASE_DIR / "temp_storage"
LOG_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
TEMP_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# ============================================================================
# PDF PROCESSING CONFIGURATION
# ============================================================================
MAX_PDF_PAGES = 2
MAX_FILE_SIZE_MB = 10
ALLOWED_EXTENSIONS = {".pdf"}
PDF_QUALITY = 150  # DPI for PDF rendering

# ============================================================================
# DOCUMENT PROCESSING
# ============================================================================
CHUNK_SIZE = 500  # Tokens per chunk
CHUNK_OVERLAP = 50  # Token overlap between chunks
TEXT_EXTRACTION_METHOD = "pymupdf"  # PDF extraction method

# ============================================================================
# GEMMA LLM CONFIGURATION
# Note: Using Gemma 4 E2B for vision/image understanding capabilities
# ============================================================================
MODEL_NAME = os.getenv("MODEL_NAME", "gemma-4:e2b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL_TIMEOUT = 120  # Seconds
TEMPERATURE = 0.7
MAX_TOKENS = 2048
TOP_P = 0.9
TOP_K = 40

# ============================================================================
# SESSION & STORAGE
# ============================================================================
SESSION_TIMEOUT_MINUTES = 30
CHAT_HISTORY_LIMIT = 50
CACHE_TTL = 3600  # Cache time-to-live in seconds
AUTO_CLEANUP_ENABLED = True
CLEANUP_INTERVAL_HOURS = 1

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = LOG_DIR / "app.log"
ERROR_LOG_FILE = LOG_DIR / "error.log"
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10 MB

# ============================================================================
# STREAMLIT CONFIGURATION
# ============================================================================
STREAMLIT_THEME = "light"
PAGE_LAYOUT = "wide"
INITIAL_SIDEBAR_STATE = "expanded"

# ============================================================================
# UI CONFIGURATION
# ============================================================================
UPLOAD_ACCEPT_MULTIPLE_FILES = False
CHAT_INPUT_PLACEHOLDER = "Ask a question about your document..."
DOCUMENT_VIEWER_HEIGHT = 600
MAX_DISPLAY_CHARS = 1000

# ============================================================================
# FEATURE FLAGS
# ============================================================================
ENABLE_CACHING = True
ENABLE_LOGGING = True
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
VERBOSE_OUTPUT = os.getenv("VERBOSE_OUTPUT", "False").lower() == "true"

# ============================================================================
# VALIDATION RULES
# ============================================================================
MIN_QUERY_LENGTH = 3
MAX_QUERY_LENGTH = 500
REQUIRED_FIELDS = ["query", "document"]

# ============================================================================
# REGEX PATTERNS
# ============================================================================
EMAIL_PATTERN = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
PHONE_PATTERN = r"\+?1?\d{9,15}"
DATE_PATTERN = r"\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2}"

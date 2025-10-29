# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration centrale de l'application OCR"""

    # Google Cloud Vision API
    GOOGLE_CREDENTIALS_PATH = os.getenv(
        'GOOGLE_APPLICATION_CREDENTIALS',
        'credentials/google_credentials.json'
    )

    # Vision API Settings
    VISION_API_FEATURES = [
        'DOCUMENT_TEXT_DETECTION',  # Pour OCR structuré
    ]

    # Image Processing
    DPI_DEFAULT = 300  # Vision API recommande 300 DPI
    MAX_IMAGE_SIZE = 20_000_000  # 20 MB max par image
    IMAGE_FORMAT = 'PNG'  # PNG ou JPEG

    # Cache Settings
    CACHE_ENABLED = True
    CACHE_DIR = '.cache/vision_api'
    CACHE_TTL = 86400 * 30  # 30 jours

    # API Rate Limiting
    MAX_REQUESTS_PER_MINUTE = 1800  # Limite Google
    BATCH_SIZE = 16  # Vision API supporte le batch

    # Font Detection & Mapping
    FONT_CONFIDENCE_THRESHOLD = 0.7
    DEFAULT_SERIF_FONT = 'Times New Roman'
    DEFAULT_SANS_SERIF_FONT = 'Arial'
    DEFAULT_MONOSPACE_FONT = 'Courier New'

    # Formatting Thresholds
    MIN_FONT_SIZE_DIFFERENCE = 1.5  # Points pour détecter changements
    PARAGRAPH_SPACING_THRESHOLD = 1.5  # Multiple de line height
    CENTER_ALIGNMENT_TOLERANCE = 0.1  # 10% de la largeur

    # Text Processing
    PRESERVE_HYPHENATION = False
    FIX_COMMON_OCR_ERRORS = True
    SPELL_CHECK_ENABLED = False  # Vision API est déjà très précis

    # Performance
    PARALLEL_PROCESSING = True
    MAX_WORKERS = 4  # Pour conversion PDF parallèle

    # Output
    PRESERVE_PAGE_BREAKS = False
    CREATE_WORD_STYLES = True
    OPTIMIZE_DOCUMENT = True

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_DIR = 'logs'
    LOG_ROTATION = '10 MB'

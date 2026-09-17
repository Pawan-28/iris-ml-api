import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.config import settings


BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"

log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

logger = logging.getLogger("ml_api")
logger.setLevel(log_level)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5 * 1024 * 1024,
    backupCount=3
)
file_handler.setLevel(log_level)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(log_level)
console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
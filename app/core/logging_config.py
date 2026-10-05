import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path


APP_LOGGER_NAME = "app"

LOG_DIR = Path(
    os.getenv(
        "LOG_DIR",
        Path.home() / ".local" / "state" / "chatgpt-clone-backend" / "logs",
    )
)

LOG_FILE = LOG_DIR / "app.log"

LOG_MAX_BYTES = 10 * 1024 * 1024  # 10 MB
LOG_BACKUP_COUNT = 5

LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)


def configure_logging() -> None:
    """
    Configure application logging.

    Application logs are kept under the dedicated application logger
    instead of modifying the global/root logger.

    This makes the configuration safe to use with Uvicorn, FastAPI,
    pytest, and other third-party logging systems.
    """

    logger = logging.getLogger(APP_LOGGER_NAME)

    logger.setLevel(logging.INFO)

    # Prevent messages from being handled again by the root logger.
    logger.propagate = False

    formatter = logging.Formatter(LOG_FORMAT)

    # Avoid installing duplicate handlers if this function is called
    # more than once during development/reload/testing.
    if logger.handlers:
        return

    # Console handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    # File handler
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

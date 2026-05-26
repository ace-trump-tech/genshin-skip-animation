# utils/logger.py
import logging
import sys
from pathlib import Path

def setup_logger(level=logging.INFO, log_file="assets/logs/run.log"):
    """
    Setup a logger that outputs to both console and a log file.

    :param level: Logging level (e.g., logging.INFO, logging.DEBUG)
    :param log_file: Path to the log file (relative or absolute)
    :return: Configured logger instance
    """
    # Ensure the log directory exists
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("GenshinAutoSkip")
    logger.setLevel(level)

    # Avoid adding duplicate handlers if called multiple times
    if logger.handlers:
        return logger

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(console_handler)

    # File handler
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(file_handler)

    return logger

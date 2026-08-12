"""Logging Utilities Module (Final Version)

This module provides logging configuration and utilities
for the crawling system with colored output support.
"""
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from app.config import settings


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output"""

    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
    }
    RESET = '\033[0m'

    def format(self, record):
        # Add color to level name
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.RESET}"
        return super().format(record)


class CrawlerLogger:
    """Custom logger for crawler operations"""

    def __init__(self, name: str = "crawler"):
        """
        Initialize logger.

        Args:
            name: Logger name
        """
        self.logger = logging.getLogger(name)
        self._configured = False

    def setup(
        self,
        level: int = logging.INFO,
        log_file: Optional[Path] = None,
        colored: bool = True,
    ) -> None:
        """
        Setup logger with console and file handlers.

        Args:
            level: Logging level
            log_file: Path to log file
            colored: Use colored output
        """
        if self._configured:
            return

        self.logger.setLevel(level)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)

        if colored:
            console_format = ColoredFormatter(
                '[%(levelname)s] %(message)s'
            )
        else:
            console_format = logging.Formatter(
                '[%(levelname)s] %(message)s'
            )

        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)

        # File handler (if specified)
        if log_file:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(level)
            file_format = logging.Formatter(
                '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            )
            file_handler.setFormatter(file_format)
            self.logger.addHandler(file_handler)

        self._configured = True

    def info(self, message: str) -> None:
        """Log info message"""
        self.logger.info(message)

    def error(self, message: str) -> None:
        """Log error message"""
        self.logger.error(message)

    def warning(self, message: str) -> None:
        """Log warning message"""
        self.logger.warning(message)

    def debug(self, message: str) -> None:
        """Log debug message"""
        self.logger.debug(message)


def setup_logging(
    log_dir: Optional[Path] = None,
    level: int = logging.INFO,
) -> CrawlerLogger:
    """
    Setup global logging configuration.

    Args:
        log_dir: Directory for log files
        level: Logging level

    Returns:
        Configured logger instance
    """
    log_dir = log_dir or settings.log_dir

    # Create log file path
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"crawl_{timestamp}.log"

    # Create and setup logger
    logger = CrawlerLogger("crawler")
    logger.setup(level=level, log_file=log_file, colored=True)

    return logger


# Global logger instance
_logger: Optional[CrawlerLogger] = None


def get_logger() -> CrawlerLogger:
    """
    Get global logger instance.

    Returns:
        Logger instance
    """
    global _logger
    if _logger is None:
        _logger = setup_logging()
    return _logger
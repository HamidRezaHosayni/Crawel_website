"""Utilities Module

This module provides utility functions and classes for
error handling, retry logic, hashing, logging, and time management.
"""
from app.utils.errors import (
    CrawlerError,
    CrawlError,
    TemporaryError,
    PermanentError,
    RateLimitError,
    NetworkError,
    ServerError,
    ClientError,
    ContentExtractionError,
    StorageError,
    DatabaseError,
    ConfigurationError,
)
from app.utils.hashing import sha256_hash, md5_hash, content_fingerprint
from app.utils.logging import CrawlerLogger, setup_logging, get_logger
from app.utils.retry import (
    RetryConfig,
    retry_on_temporary_error,
    retry_on_rate_limit,
    retry_on_network_error,
    async_retry,
    calculate_backoff_delay,
    is_retryable_status_code,
    get_retry_delay_for_status,
)
from app.utils.time import (
    get_utc_now,
    format_timestamp,
    format_duration,
    is_stale,
    generate_session_timestamp,
)

__all__ = [
    # Errors
    "CrawlerError",
    "CrawlError",
    "TemporaryError",
    "PermanentError",
    "RateLimitError",
    "NetworkError",
    "ServerError",
    "ClientError",
    "ContentExtractionError",
    "StorageError",
    "DatabaseError",
    "ConfigurationError",
    # Hashing
    "sha256_hash",
    "md5_hash",
    "content_fingerprint",
    # Logging
    "CrawlerLogger",
    "setup_logging",
    "get_logger",
    # Retry
    "RetryConfig",
    "retry_on_temporary_error",
    "retry_on_rate_limit",
    "retry_on_network_error",
    "async_retry",
    "calculate_backoff_delay",
    "is_retryable_status_code",
    "get_retry_delay_for_status",
    # Time
    "get_utc_now",
    "format_timestamp",
    "format_duration",
    "is_stale",
    "generate_session_timestamp",
]
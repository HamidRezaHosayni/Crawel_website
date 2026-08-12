"""Custom Exceptions Module

This module defines custom exceptions for the crawling system
to provide better error handling and retry logic.
"""


class CrawlerError(Exception):
    """Base exception for all crawler errors"""
    pass


class CrawlError(CrawlerError):
    """Error during page crawling"""

    def __init__(self, message: str, url: str = None, status_code: int = None):
        self.url = url
        self.status_code = status_code
        super().__init__(message)


class TemporaryError(CrawlerError):
    """Temporary error that should be retried"""

    def __init__(self, message: str, retry_after: float = None):
        self.retry_after = retry_after
        super().__init__(message)


class PermanentError(CrawlerError):
    """Permanent error that should not be retried"""
    pass


class RateLimitError(TemporaryError):
    """Rate limit error (HTTP 429)"""

    def __init__(self, message: str, retry_after: float = None):
        super().__init__(message, retry_after)


class NetworkError(TemporaryError):
    """Network-related error (timeout, connection refused, etc.)"""
    pass


class ServerError(TemporaryError):
    """Server error (HTTP 5xx)"""

    def __init__(self, message: str, status_code: int):
        self.status_code = status_code
        super().__init__(message)


class ClientError(PermanentError):
    """Client error (HTTP 4xx except 429)"""

    def __init__(self, message: str, status_code: int):
        self.status_code = status_code
        super().__init__(message)


class ContentExtractionError(CrawlerError):
    """Error during content extraction"""
    pass


class StorageError(CrawlerError):
    """Error during file storage"""
    pass


class DatabaseError(CrawlerError):
    """Error during database operations"""
    pass


class ConfigurationError(CrawlerError):
    """Error in configuration"""
    pass
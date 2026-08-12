"""URL Validation Module

This module provides URL validation functionality to filter out
invalid or unwanted URLs before crawling.

Validation Rules:
- Only allow http and https schemes
- Reject URLs with invalid schemes (mailto, javascript, tel, data, blob)
- Reject URLs with skipped file extensions (.jpg, .pdf, .exe, etc.)
- Ensure URL is properly formatted
"""
from typing import Optional
from urllib.parse import urlparse

from app.config import settings


class URLValidator:
    """URL Validator for filtering invalid URLs"""

    def __init__(
        self,
        skip_extensions: Optional[set[str]] = None,
        skip_schemes: Optional[set[str]] = None,
    ) -> None:
        """
        Initialize validator with custom skip rules.

        Args:
            skip_extensions: Set of file extensions to skip (e.g., {".jpg", ".pdf"})
            skip_schemes: Set of URL schemes to skip (e.g., {"mailto", "javascript"})
        """
        self.skip_extensions = skip_extensions or settings.skip_extensions
        self.skip_schemes = skip_schemes or settings.skip_schemes

    def is_valid(self, url: str) -> bool:
        """
        Check if a URL is valid and should be crawled.

        Args:
            url: URL to validate

        Returns:
            True if URL is valid, False otherwise

        Examples:
            >>> validator = URLValidator()
            >>> validator.is_valid("https://example.com/docs")
            True
            >>> validator.is_valid("https://example.com/image.jpg")
            False
            >>> validator.is_valid("mailto:test@example.com")
            False
        """
        if not url or not url.strip():
            return False

        url = url.strip()

        # Parse URL
        try:
            parsed = urlparse(url)
        except Exception:
            return False

        # Check scheme
        scheme = parsed.scheme.lower()
        if scheme in self.skip_schemes:
            return False

        # Only allow http and https
        if scheme not in ("http", "https"):
            return False

        # Check if host exists
        if not parsed.netloc:
            return False

        # Check file extension
        path = parsed.path.lower()
        if self._has_skipped_extension(path):
            return False

        return True

    def _has_skipped_extension(self, path: str) -> bool:
        """
        Check if path has a skipped file extension.

        Args:
            path: URL path

        Returns:
            True if path has skipped extension, False otherwise
        """
        for ext in self.skip_extensions:
            if path.endswith(ext):
                return True
        return False

    def validate_batch(self, urls: list[str]) -> list[str]:
        """
        Validate a batch of URLs.

        Args:
            urls: List of URLs to validate

        Returns:
            List of valid URLs
        """
        valid_urls = []
        for url in urls:
            if self.is_valid(url):
                valid_urls.append(url)
        return valid_urls
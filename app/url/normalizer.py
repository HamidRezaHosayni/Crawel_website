"""URL Normalization Module

This module provides URL normalization functionality to ensure consistent
URL representation and prevent duplicate crawling.

Normalization Rules (Strict Approach):
- Remove URL fragments (#section)
- Remove ALL query parameters (?key=value)
- Remove trailing slashes (except for root path)
- Lowercase scheme and host
- Remove default ports (80 for HTTP, 443 for HTTPS)
- Convert relative URLs to absolute
- Handle protocol-relative URLs (//example.com)
"""
from typing import Optional
from urllib.parse import urljoin, urlparse, urlunparse


class URLNormalizer:
    """URL Normalizer with strict query parameter removal"""

    def __init__(self, base_url: Optional[str] = None) -> None:
        """
        Initialize normalizer with optional base URL.

        Args:
            base_url: Base URL for resolving relative URLs
        """
        self.base_url = base_url

    def normalize(self, url: str) -> str:
        """
        Normalize a URL by applying standard normalization rules.

        Args:
            url: URL to normalize

        Returns:
            Normalized URL string

        Examples:
            >>> normalizer = URLNormalizer()
            >>> normalizer.normalize("https://Example.COM:443/path/?query=1#section")
            'https://example.com/path'
            >>> normalizer.normalize("https://example.com")
            'https://example.com'
        """
        if not url or not url.strip():
            return ""

        url = url.strip()

        # Handle protocol-relative URLs
        if url.startswith("//"):
            if self.base_url:
                base_scheme = urlparse(self.base_url).scheme
                url = f"{base_scheme}:{url}"
            else:
                url = f"https:{url}"

        # Handle relative URLs
        if self.base_url and not url.startswith(("http://", "https://")):
            url = urljoin(self.base_url, url)

        # Parse URL
        parsed = urlparse(url)

        # Validate scheme
        if parsed.scheme not in ("http", "https"):
            return ""

        # Lowercase scheme and host
        scheme = parsed.scheme.lower()
        netloc = parsed.netloc.lower()

        # Remove default ports
        if ":" in netloc:
            host, port = netloc.rsplit(":", 1)
            if (scheme == "http" and port == "80") or (scheme == "https" and port == "443"):
                netloc = host
            else:
                netloc = f"{host}:{port}"

        # Normalize path
        path = parsed.path

        # Remove trailing slash (except for root)
        if path != "/" and path.endswith("/"):
            path = path.rstrip("/")

        # If path is empty, set to root
        if not path:
            path = "/"

        # Remove query parameters (strict approach)
        query = ""

        # Remove fragment
        fragment = ""

        # Reconstruct URL
        normalized = urlunparse((scheme, netloc, path, "", query, fragment))

        return normalized

    def normalize_batch(self, urls: list[str]) -> list[str]:
        """
        Normalize a batch of URLs.

        Args:
            urls: List of URLs to normalize

        Returns:
            List of normalized URLs (empty strings removed)
        """
        normalized_urls = []
        for url in urls:
            normalized = self.normalize(url)
            if normalized:
                normalized_urls.append(normalized)
        return normalized_urls
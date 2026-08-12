"""Domain Policy Module

This module provides domain management functionality to ensure
crawling stays within allowed domains.

Domain Policy Rules:
- Extract domain from URL
- Compare domains for same-domain checking
- Handle www subdomain (www.example.com = example.com)
- Case-insensitive domain comparison
"""
from typing import Optional
from urllib.parse import urlparse


class DomainPolicy:
    """Domain Policy for controlling which domains can be crawled"""

    def __init__(self, allowed_domain: str, allow_www: bool = True) -> None:
        """
        Initialize domain policy.

        Args:
            allowed_domain: The main domain allowed for crawling
            allow_www: Whether to allow www subdomain as same domain

        Examples:
            >>> policy = DomainPolicy("example.com")
            >>> policy.is_same_domain("https://example.com/docs")
            True
            >>> policy.is_same_domain("https://www.example.com/docs")
            True
            >>> policy.is_same_domain("https://google.com")
            False
        """
        self.allowed_domain = self._normalize_domain(allowed_domain)
        self.allow_www = allow_www

    def _normalize_domain(self, domain: str) -> str:
        """
        Normalize domain by removing www and lowercasing.

        Args:
            domain: Domain to normalize

        Returns:
            Normalized domain
        """
        domain = domain.strip().lower()

        # Remove scheme if present
        if domain.startswith(("http://", "https://")):
            parsed = urlparse(domain)
            domain = parsed.netloc or parsed.path

        # Remove www prefix
        if domain.startswith("www."):
            domain = domain[4:]

        # Remove port if present
        if ":" in domain:
            domain = domain.split(":")[0]

        return domain

    def extract_domain(self, url: str) -> Optional[str]:
        """
        Extract domain from URL.

        Args:
            url: URL to extract domain from

        Returns:
            Extracted domain or None if invalid

        Examples:
            >>> policy = DomainPolicy("example.com")
            >>> policy.extract_domain("https://www.example.com/docs")
            'example.com'
        """
        try:
            parsed = urlparse(url)
            domain = parsed.netloc
            return self._normalize_domain(domain)
        except Exception:
            return None

    def is_same_domain(self, url: str) -> bool:
        """
        Check if URL belongs to the allowed domain.

        Args:
            url: URL to check

        Returns:
            True if URL is same domain, False otherwise
        """
        url_domain = self.extract_domain(url)
        if not url_domain:
            return False

        # Direct match
        if url_domain == self.allowed_domain:
            return True

        # Check www variant if allowed
        if self.allow_www:
            if url_domain == f"www.{self.allowed_domain}":
                return True
            if self.allowed_domain == f"www.{url_domain}":
                return True

        return False

    def filter_same_domain(self, urls: list[str]) -> list[str]:
        """
        Filter URLs to only include same-domain URLs.

        Args:
            urls: List of URLs to filter

        Returns:
            List of same-domain URLs
        """
        return [url for url in urls if self.is_same_domain(url)]

    def get_allowed_domain(self) -> str:
        """
        Get the allowed domain.

        Returns:
            Allowed domain string
        """
        return self.allowed_domain
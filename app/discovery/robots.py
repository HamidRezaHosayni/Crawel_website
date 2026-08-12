"""Robots.txt Parser Module

This module provides functionality to parse robots.txt files and
extract sitemap URLs.
"""
from typing import Optional
from urllib.parse import urljoin, urlparse

from app.discovery.http_client import DiscoveryHTTPClient
from app.url.normalizer import URLNormalizer


class RobotsParser:
    """Parser for robots.txt files"""

    def __init__(self, base_url: str) -> None:
        """
        Initialize robots parser.

        Args:
            base_url: Base URL of the website (e.g., https://example.com)
        """
        self.base_url = base_url
        self.robots_url = urljoin(base_url, "/robots.txt")
        self.sitemap_urls: list[str] = []
        self._content: Optional[str] = None
        self._normalizer = URLNormalizer(base_url)

    async def fetch_and_parse(self, client: DiscoveryHTTPClient) -> bool:
        """
        Fetch and parse robots.txt file.

        Args:
            client: HTTP client for fetching

        Returns:
            True if robots.txt was successfully fetched and parsed
        """
        content = await client.fetch_text(self.robots_url)

        if content is None:
            return False

        self._content = content
        self._parse_content()
        return True

    def _parse_content(self) -> None:
        """Parse robots.txt content and extract sitemap URLs"""
        if not self._content:
            return

        self.sitemap_urls = []

        for line in self._content.splitlines():
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith("#"):
                continue

            # Look for Sitemap directive (case-insensitive)
            if line.lower().startswith("sitemap:"):
                sitemap_url = line[8:].strip()

                # Handle relative URLs
                if not sitemap_url.startswith(("http://", "https://")):
                    sitemap_url = urljoin(self.base_url, sitemap_url)

                # Normalize URL
                normalized = self._normalizer.normalize(sitemap_url)
                if normalized:
                    self.sitemap_urls.append(normalized)

    def get_sitemap_urls(self) -> list[str]:
        """
        Get list of sitemap URLs found in robots.txt.

        Returns:
            List of sitemap URLs
        """
        return self.sitemap_urls

    def is_allowed(self, path: str, user_agent: str = "*") -> bool:
        """
        Check if path is allowed for crawling.

        Note: This is a simplified implementation. For production,
        consider using urllib.robotparser.

        Args:
            path: URL path to check
            user_agent: User-Agent to check against

        Returns:
            True if path is allowed, False otherwise
        """
        if not self._content:
            return True  # If no robots.txt, assume allowed

        # Simplified implementation - just check for Disallow
        # In production, use urllib.robotparser.RobotFileParser
        for line in self._content.splitlines():
            line = line.strip()
            if line.lower().startswith("disallow:"):
                disallowed_path = line[9:].strip()
                if disallowed_path and path.startswith(disallowed_path):
                    return False

        return True
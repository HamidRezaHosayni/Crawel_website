"""Lightweight HTTP Client for Discovery

This module provides a lightweight HTTP client for fetching robots.txt
and sitemap files without using a full browser.
"""
import asyncio
from typing import Optional

import httpx

from app.config import settings


class DiscoveryHTTPClient:
    """HTTP Client for lightweight discovery requests"""

    def __init__(
        self,
        timeout: float = 30.0,
        user_agent: str = "Mozilla/5.0 (compatible; WebDatasetCrawler/1.0)",
    ) -> None:
        """
        Initialize HTTP client.

        Args:
            timeout: Request timeout in seconds
            user_agent: User-Agent header for requests
        """
        self.timeout = timeout
        self.user_agent = user_agent
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self) -> "DiscoveryHTTPClient":
        """Async context manager entry"""
        await self._create_client()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit"""
        await self.close()

    async def _create_client(self) -> None:
        """Create HTTP client if not exists"""
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(self.timeout),
                headers={"User-Agent": self.user_agent},
                follow_redirects=True,
                http2=True,
            )

    async def close(self) -> None:
        """Close HTTP client"""
        if self._client:
            await self._client.aclose()
            self._client = None

    async def fetch_text(self, url: str) -> Optional[str]:
        """
        Fetch URL content as text.

        Args:
            url: URL to fetch

        Returns:
            Response text or None if failed

        Raises:
            httpx.HTTPError: If request fails after retries
        """
        if not self._client:
            await self._create_client()

        try:
            response = await self._client.get(url)
            response.raise_for_status()
            return response.text
        except httpx.HTTPError as e:
            # Log error but don't raise - discovery should be resilient
            print(f"[DISCOVERY] Failed to fetch {url}: {e}")
            return None

    async def fetch_bytes(self, url: str) -> Optional[bytes]:
        """
        Fetch URL content as bytes.

        Args:
            url: URL to fetch

        Returns:
            Response bytes or None if failed
        """
        if not self._client:
            await self._create_client()

        try:
            response = await self._client.get(url)
            response.raise_for_status()
            return response.content
        except httpx.HTTPError as e:
            print(f"[DISCOVERY] Failed to fetch {url}: {e}")
            return None

    async def url_exists(self, url: str) -> bool:
        """
        Check if URL exists (HEAD request).

        Args:
            url: URL to check

        Returns:
            True if URL exists (200 status), False otherwise
        """
        if not self._client:
            await self._create_client()

        try:
            response = await self._client.head(url)
            return response.status_code == 200
        except httpx.HTTPError:
            return False
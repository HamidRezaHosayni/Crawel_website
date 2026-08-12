"""Crawl4AI Client Module

This module provides a wrapper around Crawl4AI for web crawling
with JavaScript rendering and content extraction.
"""
import asyncio
from typing import Optional

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

from app.crawler.browser import BrowserManager
from app.models.crawl_result import CrawlResult


class Crawl4AIClient:
    """Client for Crawl4AI web crawling"""

    def __init__(self, browser_manager: BrowserManager) -> None:
        """
        Initialize Crawl4AI client.

        Args:
            browser_manager: Browser manager for configuration
        """
        self.browser_manager = browser_manager
        self._crawler: Optional[AsyncWebCrawler] = None

    async def __aenter__(self) -> "Crawl4AIClient":
        """Async context manager entry"""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit"""
        await self.stop()

    async def start(self) -> None:
        """Start the crawler and browser"""
        if self._crawler is None:
            browser_config = self.browser_manager.get_browser_config()
            self._crawler = AsyncWebCrawler(config=browser_config)
            await self._crawler.__aenter__()

    async def stop(self) -> None:
        """Stop the crawler and browser"""
        if self._crawler:
            await self._crawler.__aexit__(None, None, None)
            self._crawler = None

    async def crawl(
        self,
        url: str,
    ) -> CrawlResult:
        """
        Crawl a single URL with JavaScript rendering.

        Args:
            url: URL to crawl

        Returns:
            CrawlResult with extracted content and metadata
        """
        if not self._crawler:
            await self.start()

        try:
            # Create minimal run config compatible with Crawl4AI 0.9.2
            run_config = CrawlerRunConfig(
                # Only use parameters that exist in 0.9.2
                cache_mode="bypass",  # Always fetch fresh content
                screenshot=False,  # Don't take screenshots
            )

            # Perform crawl
            result = await self._crawler.arun(url, config=run_config)

            # Check if crawl was successful
            if not result or not result.success:
                error_message = "Unknown error"
                if result and hasattr(result, "error_message"):
                    error_message = result.error_message
                elif result and hasattr(result, "error"):
                    error_message = str(result.error)
                
                return CrawlResult(
                    url=url,
                    normalized_url=url,
                    success=False,
                    error_message=error_message,
                )

            # Extract content
            markdown_content = None
            if hasattr(result, "markdown"):
                markdown_content = result.markdown
            elif hasattr(result, "markdown_v2"):
                markdown_content = result.markdown_v2
            elif hasattr(result, "content"):
                markdown_content = result.content

            # Extract metadata
            title = None
            content_type = None
            canonical_url = None
            
            if hasattr(result, "metadata") and result.metadata:
                if isinstance(result.metadata, dict):
                    title = result.metadata.get("title")
                    content_type = result.metadata.get("content_type")
                    canonical_url = result.metadata.get("canonical")

            # Extract status code
            status_code = None
            if hasattr(result, "status_code"):
                status_code = result.status_code
            elif hasattr(result, "response") and hasattr(result.response, "status"):
                status_code = result.response.status

            # Extract discovered links
            discovered_urls = []
            if hasattr(result, "links") and result.links:
                # Handle different link formats
                if isinstance(result.links, dict):
                    # Format: {"internal": [...], "external": [...]}
                    internal_links = result.links.get("internal", [])
                    external_links = result.links.get("external", [])
                    all_links = internal_links + external_links
                    
                    for link in all_links:
                        if isinstance(link, dict) and "href" in link:
                            discovered_urls.append(link["href"])
                        elif isinstance(link, str):
                            discovered_urls.append(link)
                
                elif isinstance(result.links, list):
                    # Format: [link1, link2, ...]
                    for link in result.links:
                        if isinstance(link, dict) and "href" in link:
                            discovered_urls.append(link["href"])
                        elif isinstance(link, str):
                            discovered_urls.append(link)

            return CrawlResult(
                url=url,
                normalized_url=url,
                success=True,
                status_code=status_code,
                content_type=content_type,
                markdown_content=markdown_content,
                title=title,
                canonical_url=canonical_url,
                discovered_urls=discovered_urls,
            )

        except asyncio.TimeoutError:
            return CrawlResult(
                url=url,
                normalized_url=url,
                success=False,
                error_message="Page load timeout",
            )
        except Exception as e:
            return CrawlResult(
                url=url,
                normalized_url=url,
                success=False,
                error_message=str(e),
            )

    async def crawl_batch(
        self,
        urls: list[str],
        delay: float = 1.0,
    ) -> list[CrawlResult]:
        """
        Crawl multiple URLs with delay between requests.

        Args:
            urls: List of URLs to crawl
            delay: Delay between requests in seconds

        Returns:
            List of CrawlResult objects
        """
        results = []

        for url in urls:
            result = await self.crawl(url)
            results.append(result)

            # Delay between requests to avoid rate limiting
            if delay > 0:
                await asyncio.sleep(delay)

        return results
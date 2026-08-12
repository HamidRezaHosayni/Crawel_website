"""Page Crawler Module

This module provides the main page crawling logic that combines
Crawl4AI crawling with content extraction and link discovery.
"""
import hashlib
from typing import Optional, List, Tuple

from app.crawler.crawl4ai_client import Crawl4AIClient
from app.models.crawl_result import CrawlResult
from app.url.domain import DomainPolicy
from app.url.normalizer import URLNormalizer
from app.url.validator import URLValidator


class PageCrawler:
    """Main page crawler with content extraction"""

    def __init__(
        self,
        crawl_client: Crawl4AIClient,
        domain_policy: DomainPolicy,
        normalizer: URLNormalizer,
        validator: URLValidator,
    ) -> None:
        """
        Initialize page crawler.

        Args:
            crawl_client: Crawl4AI client
            domain_policy: Domain policy for filtering
            normalizer: URL normalizer
            validator: URL validator
        """
        self.crawl_client = crawl_client
        self.domain_policy = domain_policy
        self.normalizer = normalizer
        self.validator = validator

    async def crawl_page(
        self,
        url: str,
        normalized_url: str,
    ) -> Tuple[CrawlResult, List[str]]:
        """
        Crawl a page and extract content and links.

        Args:
            url: Original URL
            normalized_url: Normalized URL

        Returns:
            Tuple of (CrawlResult, list of new discovered URLs)
        """
        # Crawl the page
        result = await self.crawl_client.crawl(url)

        if not result.success:
            return result, []

        # Generate content hash
        if result.markdown_content:
            content_hash = self._generate_content_hash(result.markdown_content)
            result = result.model_copy(update={"content_hash": content_hash})

        # Extract and filter discovered URLs
        new_urls = self._process_discovered_urls(result.discovered_urls)

        return result, new_urls

    def _process_discovered_urls(self, discovered_urls: List[str]) -> List[str]:
        """
        Process discovered URLs: normalize, validate, and filter.

        Args:
            discovered_urls: Raw discovered URLs

        Returns:
            List of valid, normalized, same-domain URLs
        """
        valid_urls = []
        seen_urls = set()

        for url in discovered_urls:
            if not url:
                continue

            # Normalize URL
            normalized = self.normalizer.normalize(url)

            if not normalized:
                continue

            # Skip if already seen in this batch
            if normalized in seen_urls:
                continue

            # Validate URL
            if not self.validator.is_valid(normalized):
                continue

            # Check domain policy
            if not self.domain_policy.is_same_domain(normalized):
                continue

            seen_urls.add(normalized)
            valid_urls.append(normalized)

        return valid_urls

    def _generate_content_hash(self, content: str) -> str:
        """
        Generate SHA-256 hash of content.

        Args:
            content: Content string

        Returns:
            SHA-256 hash hex string
        """
        return hashlib.sha256(content.encode("utf-8")).hexdigest()
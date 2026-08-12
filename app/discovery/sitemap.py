"""Sitemap Parser Module

This module provides functionality to parse XML sitemaps,
including sitemap index files with recursive processing.
"""
from typing import Optional
from xml.etree import ElementTree

from bs4 import BeautifulSoup

from app.config import settings
from app.discovery.http_client import DiscoveryHTTPClient
from app.models.sitemap import SitemapDocument, SitemapStatus, SitemapType
from app.url.normalizer import URLNormalizer


class SitemapParser:
    """Parser for XML sitemaps"""

    # XML namespaces commonly used in sitemaps
    SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"

    def __init__(self, base_url: str) -> None:
        """
        Initialize sitemap parser.

        Args:
            base_url: Base URL of the website
        """
        self.base_url = base_url
        self._normalizer = URLNormalizer(base_url)

    async def parse_sitemap(
        self,
        sitemap_url: str,
        client: DiscoveryHTTPClient,
    ) -> tuple[list[str], list[str], SitemapType]:
        """
        Parse a sitemap file and extract URLs.

        Args:
            sitemap_url: URL of the sitemap file
            client: HTTP client for fetching

        Returns:
            Tuple of (page_urls, sitemap_urls, sitemap_type)
        """
        content = await client.fetch_text(sitemap_url)

        if content is None:
            return [], [], SitemapType.UNKNOWN

        try:
            # Parse XML
            root = ElementTree.fromstring(content)

            # Determine sitemap type
            root_tag = root.tag.lower()

            if "sitemapindex" in root_tag:
                # This is a sitemap index
                sitemap_urls = self._parse_sitemap_index(root)
                return [], sitemap_urls, SitemapType.SITEMAP_INDEX

            elif "urlset" in root_tag:
                # This is a regular sitemap
                page_urls = self._parse_urlset(root)
                return page_urls, [], SitemapType.URLSET

            else:
                # Unknown type
                return [], [], SitemapType.UNKNOWN

        except ElementTree.ParseError as e:
            print(f"[SITEMAP] XML parse error for {sitemap_url}: {e}")
            return [], [], SitemapType.UNKNOWN

    def _parse_sitemap_index(self, root: ElementTree.Element) -> list[str]:
        """
        Parse sitemap index and extract child sitemap URLs.

        Args:
            root: XML root element

        Returns:
            List of child sitemap URLs
        """
        sitemap_urls = []

        # Handle namespace
        ns = {"sm": self.SITEMAP_NS}

        # Try with namespace first
        sitemap_elements = root.findall(".//sm:sitemap/sm:loc", ns)

        # If no results, try without namespace
        if not sitemap_elements:
            sitemap_elements = root.findall(".//sitemap/loc")

        # If still no results, try generic approach
        if not sitemap_elements:
            sitemap_elements = root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap/{http://www.sitemaps.org/schemas/sitemap/0.9}loc")

        for loc in sitemap_elements:
            if loc.text:
                url = self._normalizer.normalize(loc.text.strip())
                if url:
                    sitemap_urls.append(url)

        return sitemap_urls

    def _parse_urlset(self, root: ElementTree.Element) -> list[str]:
        """
        Parse URL set and extract page URLs.

        Args:
            root: XML root element

        Returns:
            List of page URLs
        """
        page_urls = []

        # Handle namespace
        ns = {"sm": self.SITEMAP_NS}

        # Try with namespace first
        url_elements = root.findall(".//sm:url/sm:loc", ns)

        # If no results, try without namespace
        if not url_elements:
            url_elements = root.findall(".//url/loc")

        # If still no results, try generic approach
        if not url_elements:
            url_elements = root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc")

        for loc in url_elements:
            if loc.text:
                url = self._normalizer.normalize(loc.text.strip())
                if url:
                    page_urls.append(url)

        return page_urls

    async def discover_default_sitemaps(
        self,
        client: DiscoveryHTTPClient,
    ) -> list[str]:
        """
        Discover sitemaps from common default paths.

        Args:
            client: HTTP client for fetching

        Returns:
            List of discovered sitemap URLs
        """
        discovered = []

        for path in settings.default_sitemap_paths:
            sitemap_url = f"{self.base_url.rstrip('/')}{path}"

            # Check if URL exists
            if await client.url_exists(sitemap_url):
                normalized = self._normalizer.normalize(sitemap_url)
                if normalized:
                    discovered.append(normalized)

        return discovered
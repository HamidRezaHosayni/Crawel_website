"""Link Extractor Module

This module provides functionality to extract links from HTML pages.
"""
from typing import Optional
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from app.url.domain import DomainPolicy
from app.url.normalizer import URLNormalizer
from app.url.validator import URLValidator


class LinkExtractor:
    """Extractor for HTML links"""

    def __init__(
        self,
        base_url: str,
        domain_policy: DomainPolicy,
        normalizer: URLNormalizer,
        validator: URLValidator,
    ) -> None:
        """
        Initialize link extractor.

        Args:
            base_url: Base URL for resolving relative links
            domain_policy: Domain policy for filtering
            normalizer: URL normalizer
            validator: URL validator
        """
        self.base_url = base_url
        self.domain_policy = domain_policy
        self.normalizer = normalizer
        self.validator = validator

    def extract_links(self, html: str) -> list[str]:
        """
        Extract all valid links from HTML content.

        Args:
            html: HTML content

        Returns:
            List of valid, normalized URLs
        """
        if not html:
            return []

        try:
            soup = BeautifulSoup(html, "lxml")
        except Exception as e:
            print(f"[EXTRACT] HTML parse error: {e}")
            return []

        links = set()

        # Extract all <a> tags
        for anchor in soup.find_all("a", href=True):
            href = anchor["href"]

            # Skip empty hrefs
            if not href or href.startswith("#"):
                continue

            # Convert relative URL to absolute
            absolute_url = urljoin(self.base_url, href)

            # Normalize URL
            normalized = self.normalizer.normalize(absolute_url)

            if not normalized:
                continue

            # Validate URL
            if not self.validator.is_valid(normalized):
                continue

            # Check domain policy
            if not self.domain_policy.is_same_domain(normalized):
                continue

            links.add(normalized)

        return list(links)

    def extract_canonical(self, html: str) -> Optional[str]:
        """
        Extract canonical URL from HTML.

        Args:
            html: HTML content

        Returns:
            Canonical URL or None
        """
        if not html:
            return None

        try:
            soup = BeautifulSoup(html, "lxml")

            # Find canonical link
            canonical_link = soup.find("link", rel="canonical")

            if canonical_link and canonical_link.get("href"):
                canonical_url = canonical_link["href"]
                absolute_url = urljoin(self.base_url, canonical_url)
                return self.normalizer.normalize(absolute_url)

        except Exception as e:
            print(f"[EXTRACT] Canonical extraction error: {e}")

        return None

    def extract_title(self, html: str) -> Optional[str]:
        """
        Extract page title from HTML.

        Args:
            html: HTML content

        Returns:
            Page title or None
        """
        if not html:
            return None

        try:
            soup = BeautifulSoup(html, "lxml")

            title_tag = soup.find("title")
            if title_tag and title_tag.string:
                return title_tag.string.strip()

        except Exception as e:
            print(f"[EXTRACT] Title extraction error: {e}")

        return None
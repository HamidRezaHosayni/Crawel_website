"""Discovery Service Module

This module provides functionality for discovering URLs from
sitemaps, robots.txt, and HTML pages with recursive processing.
"""
from typing import List, Set
from collections import deque

from app.database.repositories.sitemap_repository import SitemapRepository
from app.database.repositories.url_repository import URLRepository
from app.discovery.http_client import DiscoveryHTTPClient
from app.discovery.robots import RobotsParser
from app.discovery.sitemap import SitemapParser
from app.models.sitemap import SitemapStatus, SitemapType
from app.models.url import URLSource
from app.url.domain import DomainPolicy
from app.url.normalizer import URLNormalizer
from app.url.validator import URLValidator


class DiscoveryService:
    """Service for URL discovery from various sources"""

    def __init__(
        self,
        url_repo: URLRepository,
        sitemap_repo: SitemapRepository,
        domain_policy: DomainPolicy,
        normalizer: URLNormalizer,
        validator: URLValidator,
    ) -> None:
        """
        Initialize discovery service.

        Args:
            url_repo: URL repository instance
            sitemap_repo: Sitemap repository instance
            domain_policy: Domain policy for filtering
            normalizer: URL normalizer
            validator: URL validator
        """
        self.url_repo = url_repo
        self.sitemap_repo = sitemap_repo
        self.domain_policy = domain_policy
        self.normalizer = normalizer
        self.validator = validator

    async def discover_from_robots(self, base_url: str) -> int:
        """
        Discover URLs from robots.txt file.

        This method:
        1. Fetches and parses robots.txt
        2. Extracts sitemap URLs
        3. Processes each sitemap

        Args:
            base_url: Base URL of the website

        Returns:
            Number of URLs discovered
        """
        robots_parser = RobotsParser(base_url)

        async with DiscoveryHTTPClient() as client:
            # Fetch and parse robots.txt
            success = await robots_parser.fetch_and_parse(client)

            if not success:
                print(f"[DISCOVERY] No robots.txt found at {base_url}")
                return 0

            # Get sitemap URLs from robots.txt
            sitemap_urls = robots_parser.get_sitemap_urls()

            if not sitemap_urls:
                print(f"[DISCOVERY] No sitemaps found in robots.txt")
                return 0

            print(f"[DISCOVERY] Found {len(sitemap_urls)} sitemap(s) in robots.txt")

            # Process each sitemap
            total_urls = 0
            for sitemap_url in sitemap_urls:
                urls_found = await self._process_sitemap(sitemap_url, client, source="robots")
                total_urls += urls_found

            return total_urls

    async def discover_from_default_sitemaps(self, base_url: str) -> int:
        """
        Discover URLs from default sitemap paths.

        This method checks common sitemap paths if robots.txt
        didn't provide any sitemaps.

        Args:
            base_url: Base URL of the website

        Returns:
            Number of URLs discovered
        """
        sitemap_parser = SitemapParser(base_url)

        async with DiscoveryHTTPClient() as client:
            # Discover sitemaps from default paths
            sitemap_urls = await sitemap_parser.discover_default_sitemaps(client)

            if not sitemap_urls:
                print(f"[DISCOVERY] No sitemaps found at default paths")
                return 0

            print(f"[DISCOVERY] Found {len(sitemap_urls)} sitemap(s) at default paths")

            # Process each sitemap
            total_urls = 0
            for sitemap_url in sitemap_urls:
                urls_found = await self._process_sitemap(sitemap_url, client, source="default")
                total_urls += urls_found

            return total_urls

    async def _process_sitemap(
        self,
        sitemap_url: str,
        client: DiscoveryHTTPClient,
        source: str = "robots",
    ) -> int:
        """
        Process a single sitemap with recursive support.

        This method:
        1. Checks if sitemap was already processed
        2. Parses sitemap (URL set or sitemap index)
        3. For sitemap index, recursively processes child sitemaps
        4. For URL set, adds URLs to database

        Args:
            sitemap_url: URL of the sitemap
            client: HTTP client for fetching
            source: Source of the sitemap

        Returns:
            Number of URLs discovered
        """
        # Normalize sitemap URL
        normalized_url = self.normalizer.normalize(sitemap_url)

        if not normalized_url:
            return 0

        # Check if already processed
        if await self.sitemap_repo.is_processed(normalized_url):
            print(f"[SITEMAP] Already processed: {normalized_url}")
            return 0

        # Mark as processing
        await self.sitemap_repo.create_or_update(
            url=sitemap_url,
            normalized_url=normalized_url,
            source=source,
        )
        await self.sitemap_repo.mark_processing(normalized_url)

        # Parse sitemap
        sitemap_parser = SitemapParser(self.domain_policy.get_allowed_domain())
        page_urls, child_sitemaps, sitemap_type = await sitemap_parser.parse_sitemap(
            normalized_url,
            client,
        )

        # Handle different sitemap types
        if sitemap_type == SitemapType.SITEMAP_INDEX:
            # This is a sitemap index - process child sitemaps recursively
            print(f"[SITEMAP] Processing sitemap index: {normalized_url}")

            total_urls = 0
            for child_sitemap in child_sitemaps:
                urls_found = await self._process_sitemap(child_sitemap, client, source="sitemap_index")
                total_urls += urls_found

            # Mark as processed
            await self.sitemap_repo.mark_processed(
                normalized_url=normalized_url,
                sitemap_type=sitemap_type,
                urls_found=total_urls,
                sitemaps_found=len(child_sitemaps),
            )

            return total_urls

        elif sitemap_type == SitemapType.URLSET:
            # This is a regular sitemap - add URLs to database
            print(f"[SITEMAP] Processing URL set: {normalized_url} ({len(page_urls)} URLs)")

            urls_added = await self._add_urls_to_database(page_urls, URLSource.SITEMAP)

            # Mark as processed
            await self.sitemap_repo.mark_processed(
                normalized_url=normalized_url,
                sitemap_type=sitemap_type,
                urls_found=urls_added,
            )

            return urls_added

        else:
            # Unknown type or failed to parse
            await self.sitemap_repo.mark_failed(
                normalized_url=normalized_url,
                error_message="Unknown sitemap type or parse error",
            )
            return 0

    async def _add_urls_to_database(
        self,
        urls: List[str],
        source: URLSource,
        depth: int = 0,
        parent_url: str = None,
    ) -> int:
        """
        Add URLs to database with validation and filtering.

        Args:
            urls: List of URLs to add
            source: Source of the URLs
            depth: Crawl depth
            parent_url: Parent URL that discovered these URLs

        Returns:
            Number of URLs added
        """
        urls_added = 0

        for url in urls:
            # Normalize URL
            normalized = self.normalizer.normalize(url)

            if not normalized:
                continue

            # Validate URL
            if not self.validator.is_valid(normalized):
                continue

            # Check domain policy
            if not self.domain_policy.is_same_domain(normalized):
                continue

            # Add to database
            try:
                is_new = await self.url_repo.upsert_url(
                    url=url,
                    normalized_url=normalized,
                    domain=self.domain_policy.get_allowed_domain(),
                    source=source,
                    depth=depth,
                    parent_url=parent_url,
                )

                if is_new:
                    urls_added += 1

            except Exception as e:
                print(f"[DISCOVERY] Error adding URL {normalized}: {e}")
                continue

        return urls_added

    async def discover_from_html(
        self,
        html: str,
        parent_url: str,
        depth: int = 0,
    ) -> int:
        """
        Discover URLs from HTML content.

        This method extracts links from HTML and adds them to database.

        Args:
            html: HTML content
            parent_url: URL of the page containing these links
            depth: Crawl depth

        Returns:
            Number of URLs discovered
        """
        from app.discovery.link_extractor import LinkExtractor

        link_extractor = LinkExtractor(
            base_url=parent_url,
            domain_policy=self.domain_policy,
            normalizer=self.normalizer,
            validator=self.validator,
        )

        # Extract links from HTML
        discovered_urls = link_extractor.extract_links(html)

        if not discovered_urls:
            return 0

        # Add to database
        urls_added = await self._add_urls_to_database(
            urls=discovered_urls,
            source=URLSource.HTML,
            depth=depth + 1,
            parent_url=parent_url,
        )

        return urls_added

    async def initial_discovery(self, root_url: str) -> int:
        """
        Perform initial discovery from robots.txt and default sitemaps.

        This method is called at the start of a crawl session.

        Args:
            root_url: Root URL of the website

        Returns:
            Total number of URLs discovered
        """
        print(f"[DISCOVERY] Starting initial discovery for {root_url}")

        # Add root URL to database
        normalized_root = self.normalizer.normalize(root_url)
        await self.url_repo.upsert_url(
            url=root_url,
            normalized_url=normalized_root,
            domain=self.domain_policy.get_allowed_domain(),
            source=URLSource.SEED,
            depth=0,
        )

        total_urls = 1  # Count root URL

        # Discover from robots.txt
        urls_from_robots = await self.discover_from_robots(root_url)
        total_urls += urls_from_robots

        # If robots.txt didn't provide sitemaps, try default paths
        if urls_from_robots == 0:
            urls_from_defaults = await self.discover_from_default_sitemaps(root_url)
            total_urls += urls_from_defaults

        print(f"[DISCOVERY] Initial discovery complete: {total_urls} URLs discovered")

        return total_urls
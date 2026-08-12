"""Main Entry Point

This module provides the main entry point for the web crawler
application, including CLI parsing, dependency injection, and
graceful shutdown handling.
"""
import asyncio
import signal
import sys
from pathlib import Path
from typing import Optional

import typer

from app.cli.parser import validate_url, validate_limit, validate_delay, validate_output
from app.config import settings
from app.crawler.browser import BrowserManager
from app.crawler.crawl4ai_client import Crawl4AIClient
from app.crawler.page_crawler import PageCrawler
from app.database.mongo import mongo_connection
from app.database.repositories.counter_repository import CounterRepository
from app.database.repositories.session_repository import SessionRepository
from app.database.repositories.sitemap_repository import SitemapRepository
from app.database.repositories.url_repository import URLRepository
from app.database.indexes import create_all_indexes
from app.discovery.link_extractor import LinkExtractor
from app.extraction.content_extractor import ContentExtractor
from app.extraction.content_filter import ContentFilter
from app.extraction.markdown_cleaner import MarkdownCleaner
from app.services.crawl_service import CrawlService
from app.services.discovery_service import DiscoveryService
from app.services.recovery_service import RecoveryService
from app.services.session_service import SessionService
from app.storage.file_counter import FileCounter
from app.storage.text_storage import TextStorage
from app.url.domain import DomainPolicy
from app.url.normalizer import URLNormalizer
from app.url.validator import URLValidator
from app.utils.logging import setup_logging


# Create Typer app
app = typer.Typer(
    name="web-crawler",
    help="Professional Web Crawler for Dataset Collection",
    add_completion=False,
)

# Global flag for graceful shutdown
_shutdown_requested = False


def signal_handler(signum, frame):
    """Handle Ctrl+C and other termination signals"""
    global _shutdown_requested
    print("\n[SYSTEM] Shutdown signal received. Finishing current operation...")
    _shutdown_requested = True


@app.command()
def crawl(
    url: str = typer.Argument(
        ...,
        help="Root URL to crawl (e.g., https://example.com)",
        callback=validate_url,
    ),
    limit: Optional[int] = typer.Option(
        None,
        "--limit",
        "-l",
        help="Maximum number of pages to crawl (None for unlimited)",
        callback=validate_limit,
    ),
    headless: bool = typer.Option(
        True,
        "--headless/--no-headless",
        help="Run browser in headless mode (default: headless)",
    ),
    delay: float = typer.Option(
        1.0,
        "--delay",
        "-d",
        help="Delay between crawls in seconds (default: 1.0)",
        callback=validate_delay,
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output directory for TXT files (default: ./data)",
        callback=validate_output,
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose logging",
    ),
):
    """
    Crawl a website and collect content for dataset creation.

    Examples:
        python -m app.main https://example.com
        python -m app.main https://example.com --limit 100
        python -m app.main https://example.com --limit 50 --no-headless
        python -m app.main https://example.com --delay 2.0 --output ./mydata
    """
    # Apply CLI options to settings
    settings.headless = headless
    settings.crawl_delay = delay

    if output:
        settings.output_dir = output

    # Setup logging
    import logging
    log_level = logging.DEBUG if verbose else logging.INFO
    logger = setup_logging()

    # Print startup message
    print("\n" + "=" * 60)
    print("WEB CRAWLER - Dataset Collection System")
    print("=" * 60)
    print(f"Target URL   : {url}")
    print(f"Limit        : {limit if limit else 'Unlimited'}")
    print(f"Headless     : {headless}")
    print(f"Delay        : {delay}s")
    print(f"Output       : {settings.output_dir}")
    print(f"Verbose      : {verbose}")
    print("=" * 60 + "\n")

    # Run async main function
    try:
        asyncio.run(_async_main(url, limit, log_level))
    except KeyboardInterrupt:
        print("\n[SYSTEM] Crawl interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n[ERROR] Crawl failed: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


async def _async_main(url: str, limit: Optional[int], log_level: int) -> None:
    """
    Async main function that runs the crawl.

    Args:
        url: Root URL to crawl
        limit: Maximum pages to crawl
        log_level: Logging level
    """
    # Setup signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Ensure output directories exist
    settings.ensure_directories()

    # Connect to MongoDB
    print("[DB] Connecting to MongoDB...")
    database = await mongo_connection.connect()

    # Create indexes
    print("[DB] Creating indexes...")
    await create_all_indexes(database)

    # Initialize repositories
    url_repo = URLRepository(database)
    session_repo = SessionRepository(database)
    sitemap_repo = SitemapRepository(database)
    counter_repo = CounterRepository(database)

    # Initialize URL utilities
    domain_policy = DomainPolicy(url)
    normalizer = URLNormalizer(url)
    validator = URLValidator()

    # Initialize services
    session_service = SessionService(session_repo)
    discovery_service = DiscoveryService(
        url_repo=url_repo,
        sitemap_repo=sitemap_repo,
        domain_policy=domain_policy,
        normalizer=normalizer,
        validator=validator,
    )
    recovery_service = RecoveryService(url_repo)

    # Initialize crawler components
    browser_manager = BrowserManager(
        headless=settings.headless,
        chrome_channel=settings.chrome_channel,
        browser_type=settings.browser_type,
    )
    crawl_client = Crawl4AIClient(browser_manager)
    page_crawler = PageCrawler(
        crawl_client=crawl_client,
        domain_policy=domain_policy,
        normalizer=normalizer,
        validator=validator,
    )

    # Initialize extraction components
    markdown_cleaner = MarkdownCleaner()
    content_extractor = ContentExtractor(markdown_cleaner)
    content_filter = ContentFilter()

    # Initialize storage components
    text_storage = TextStorage(settings.output_dir)
    file_counter = FileCounter(counter_repo)

    # Initialize crawl service
    crawl_service = CrawlService(
        url_repo=url_repo,
        session_service=session_service,
        discovery_service=discovery_service,
        recovery_service=recovery_service,
        page_crawler=page_crawler,
        content_extractor=content_extractor,
        content_filter=content_filter,
        text_storage=text_storage,
        file_counter=file_counter,
        domain_policy=domain_policy,
        normalizer=normalizer,
        validator=validator,
    )

    try:
        # Start crawl
        await crawl_service.run_crawl(url, limit)

    finally:
        # Cleanup: close browser
        print("\n[CLEANUP] Closing browser...")
        await crawl_client.stop()

        # Cleanup: disconnect from MongoDB
        print("[CLEANUP] Disconnecting from MongoDB...")
        await mongo_connection.disconnect()

        print("[CLEANUP] Done.\n")


def main():
    """Main entry point"""
    app()


if __name__ == "__main__":
    main()
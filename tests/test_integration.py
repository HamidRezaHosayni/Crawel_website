"""Integration Tests

These tests require MongoDB to be running and test the full
crawling pipeline with a real website.
"""
import asyncio
import os
from pathlib import Path

import pytest

# Skip integration tests unless explicitly requested
pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def event_loop():
    """Create event loop for module-scoped async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def mongo_database():
    """Setup test MongoDB database"""
    from motor.motor_asyncio import AsyncIOMotorClient

    client = AsyncIOMotorClient("mongodb://localhost:27017")
    database = client["web_crawler_test"]

    # Clean up before test
    await database.urls.delete_many({})
    await database.crawl_sessions.delete_many({})
    await database.sitemaps.delete_many({})
    await database.counters.delete_many({})

    yield database

    # Clean up after test
    await database.urls.delete_many({})
    await database.crawl_sessions.delete_many({})
    await database.sitemaps.delete_many({})
    await database.counters.delete_many({})

    client.close()


@pytest.mark.asyncio
async def test_full_crawl_pipeline(mongo_database):
    """Test the complete crawl pipeline with example.com"""
    from app.crawler.browser import BrowserManager
    from app.crawler.crawl4ai_client import Crawl4AIClient
    from app.crawler.page_crawler import PageCrawler
    from app.database.repositories.counter_repository import CounterRepository
    from app.database.repositories.session_repository import SessionRepository
    from app.database.repositories.sitemap_repository import SitemapRepository
    from app.database.repositories.url_repository import URLRepository
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

    # Setup
    test_url = "https://example.com"
    test_output_dir = Path("./test_data")
    test_output_dir.mkdir(parents=True, exist_ok=True)

    # Initialize components
    url_repo = URLRepository(mongo_database)
    session_repo = SessionRepository(mongo_database)
    sitemap_repo = SitemapRepository(mongo_database)
    counter_repo = CounterRepository(mongo_database)

    domain_policy = DomainPolicy(test_url)
    normalizer = URLNormalizer(test_url)
    validator = URLValidator()

    session_service = SessionService(session_repo)
    discovery_service = DiscoveryService(
        url_repo=url_repo,
        sitemap_repo=sitemap_repo,
        domain_policy=domain_policy,
        normalizer=normalizer,
        validator=validator,
    )
    recovery_service = RecoveryService(url_repo)

    browser_manager = BrowserManager(headless=True)
    crawl_client = Crawl4AIClient(browser_manager)
    page_crawler = PageCrawler(
        crawl_client=crawl_client,
        domain_policy=domain_policy,
        normalizer=normalizer,
        validator=validator,
    )

    markdown_cleaner = MarkdownCleaner()
    content_extractor = ContentExtractor(markdown_cleaner)
    content_filter = ContentFilter()

    text_storage = TextStorage(test_output_dir)
    file_counter = FileCounter(counter_repo)

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
        # Run crawl with limit 1
        await crawl_service.run_crawl(test_url, limit=1)

        # Verify results
        # 1. Check that at least one file was created
        txt_files = list(test_output_dir.glob("*.txt"))
        assert len(txt_files) >= 1, "No TXT files were created"

        # 2. Check that file has content
        first_file = txt_files[0]
        content = first_file.read_text(encoding="utf-8")
        assert len(content) > 0, "File is empty"

        # 3. Check that content doesn't contain raw URLs
        assert "https://example.com" not in content, "URL should be removed from content"

        # 4. Check MongoDB state
        completed_count = await url_repo.get_completed_count("example.com")
        assert completed_count >= 1, "No URLs marked as completed"

        # 5. Check session was created
        session_id = session_service.get_current_session_id()
        assert session_id is not None, "No session was created"
        assert "example.com" in session_id, "Session ID should contain domain"

    finally:
        # Cleanup
        await crawl_client.stop()

        # Remove test data
        import shutil
        if test_output_dir.exists():
            shutil.rmtree(test_output_dir)


@pytest.mark.asyncio
async def test_url_deduplication(mongo_database):
    """Test that duplicate URLs are not crawled twice"""
    from app.database.repositories.url_repository import URLRepository
    from app.models.url import URLSource

    url_repo = URLRepository(mongo_database)

    # Add same URL twice
    url = "https://example.com/docs"
    normalized = "https://example.com/docs"

    is_new_1 = await url_repo.upsert_url(
        url=url,
        normalized_url=normalized,
        domain="example.com",
        source=URLSource.SITEMAP,
    )

    is_new_2 = await url_repo.upsert_url(
        url=url,
        normalized_url=normalized,
        domain="example.com",
        source=URLSource.HTML,
    )

    # First insert should be new, second should be update
    assert is_new_1 is True
    assert is_new_2 is False

    # Check that only one document exists
    doc = await url_repo.get_by_normalized_url(normalized)
    assert doc is not None
    assert len(doc.get("sources", [])) == 2  # Both sources should be recorded


@pytest.mark.asyncio
async def test_atomic_claim(mongo_database):
    """Test that URL claim is atomic"""
    from app.database.repositories.url_repository import URLRepository
    from app.models.url import URLSource

    url_repo = URLRepository(mongo_database)

    # Add a pending URL
    await url_repo.upsert_url(
        url="https://example.com/test",
        normalized_url="https://example.com/test",
        domain="example.com",
        source=URLSource.SEED,
    )

    # Claim the URL
    claimed = await url_repo.claim_next_url("example.com")
    assert claimed is not None
    assert claimed["status"] == "processing"

    # Try to claim again - should return None
    claimed_again = await url_repo.claim_next_url("example.com")
    assert claimed_again is None


@pytest.mark.asyncio
async def test_file_counter_atomic(mongo_database):
    """Test that file counter generates unique numbers"""
    from app.database.repositories.counter_repository import CounterRepository

    counter_repo = CounterRepository(mongo_database)

    # Get multiple file numbers
    numbers = []
    for _ in range(10):
        num = await counter_repo.get_next_file_number()
        numbers.append(num)

    # All numbers should be unique
    assert len(numbers) == len(set(numbers)), "File numbers are not unique"

    # Numbers should be sequential
    assert numbers == list(range(1, 11)), "File numbers are not sequential"
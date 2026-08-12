"""Crawl Service Module (Updated with Graceful Shutdown)

This module provides the main crawl orchestration logic that
coordinates discovery, crawling, extraction, and storage with
graceful shutdown support.
"""
import asyncio
from typing import Optional

from app.config import settings
from app.crawler.page_crawler import PageCrawler
from app.database.repositories.url_repository import URLRepository
from app.extraction.content_extractor import ContentExtractor
from app.extraction.content_filter import ContentFilter
from app.models.session import SessionStatus
from app.models.url import URLSource
from app.services.discovery_service import DiscoveryService
from app.services.recovery_service import RecoveryService
from app.services.session_service import SessionService
from app.services.shutdown_service import ShutdownService, shutdown_service as global_shutdown
from app.storage.file_counter import FileCounter
from app.storage.text_storage import TextStorage
from app.url.domain import DomainPolicy
from app.url.normalizer import URLNormalizer
from app.url.validator import URLValidator


class CrawlService:
    """Main crawl orchestration service with graceful shutdown"""

    def __init__(
        self,
        url_repo: URLRepository,
        session_service: SessionService,
        discovery_service: DiscoveryService,
        recovery_service: RecoveryService,
        page_crawler: PageCrawler,
        content_extractor: ContentExtractor,
        content_filter: ContentFilter,
        text_storage: TextStorage,
        file_counter: FileCounter,
        domain_policy: DomainPolicy,
        normalizer: URLNormalizer,
        validator: URLValidator,
        shutdown_service: Optional[ShutdownService] = None,
    ) -> None:
        """
        Initialize crawl service.

        Args:
            url_repo: URL repository instance
            session_service: Session service instance
            discovery_service: Discovery service instance
            recovery_service: Recovery service instance
            page_crawler: Page crawler instance
            content_extractor: Content extractor instance
            content_filter: Content filter instance
            text_storage: Text storage instance
            file_counter: File counter instance
            domain_policy: Domain policy instance
            normalizer: URL normalizer instance
            validator: URL validator instance
            shutdown_service: Shutdown service instance
        """
        self.url_repo = url_repo
        self.session_service = session_service
        self.discovery_service = discovery_service
        self.recovery_service = recovery_service
        self.page_crawler = page_crawler
        self.content_extractor = content_extractor
        self.content_filter = content_filter
        self.text_storage = text_storage
        self.file_counter = file_counter
        self.domain_policy = domain_policy
        self.normalizer = normalizer
        self.validator = validator
        self.shutdown_service = shutdown_service or global_shutdown

    async def run_crawl(self, root_url: str, limit: Optional[int] = None) -> None:
        """
        Run the complete crawl process with graceful shutdown support.

        Args:
            root_url: Root URL to crawl
            limit: Maximum pages to crawl (None for unlimited)
        """
        # Create session
        session_id = await self.session_service.create_session(root_url, limit)
        print(f"\n[CRAWL] Starting crawl session: {session_id}")
        print(f"[CRAWL] Root URL: {root_url}")
        print(f"[CRAWL] Limit: {limit if limit else 'Unlimited'}")
        print(f"[CRAWL] Press Ctrl+C to stop gracefully\n")

        try:
            # Recover stale processing URLs
            domain = self.domain_policy.get_allowed_domain()
            await self.recovery_service.recover_stale_processing(domain)

            # Check for shutdown before discovery
            if self.shutdown_service.is_shutdown_requested():
                print("[CRAWL] Shutdown requested before discovery. Exiting...")
                await self.session_service.complete_session(SessionStatus.INTERRUPTED)
                return

            # Initial discovery
            urls_discovered = await self.discovery_service.initial_discovery(root_url)
            await self.session_service.record_urls_discovered(urls_discovered)

            # Main crawl loop
            await self._crawl_loop()

            # Complete session
            await self.session_service.complete_session(SessionStatus.COMPLETED)

            # Print final statistics
            await self._print_final_stats()

        except Exception as e:
            print(f"\n[CRAWL] Crawl failed with error: {e}")
            await self.session_service.complete_session(SessionStatus.FAILED)
            raise

    async def _crawl_loop(self) -> None:
        """
        Main crawl loop that processes URLs from the queue.
        Checks for shutdown signal between crawls.
        """
        domain = self.domain_policy.get_allowed_domain()

        while True:
            # Check for shutdown signal
            if self.shutdown_service.is_shutdown_requested():
                print("\n[CRAWL] Shutdown requested. Stopping after current operation...")
                break

            # Check if we can crawl more (limit enforcement)
            if not await self.session_service.can_crawl_more():
                print(f"\n[CRAWL] Limit reached. Stopping crawl.")
                break

            # Claim next pending URL atomically
            url_doc = await self.url_repo.claim_next_url(domain)

            if not url_doc:
                # No more pending URLs
                print(f"\n[CRAWL] No more pending URLs. Crawl complete.")
                break

            # Process the URL (this will complete even if shutdown is requested)
            await self._process_url(url_doc)

            # Delay between crawls to avoid rate limiting
            if settings.crawl_delay > 0:
                await asyncio.sleep(settings.crawl_delay)

    async def _process_url(self, url_doc: dict) -> None:
        """
        Process a single URL: crawl, extract, save, discover.

        This method will complete even if shutdown is requested,
        ensuring no URL is left in processing state.

        Args:
            url_doc: URL document from database
        """
        url = url_doc.get("url")
        normalized_url = url_doc.get("normalized_url")
        depth = url_doc.get("depth", 0)

        print(f"[CRAWL] Processing: {normalized_url}")

        try:
            # Crawl the page
            crawl_result, new_urls = await self.page_crawler.crawl_page(url, normalized_url)

            if not crawl_result.success:
                # Crawl failed
                error_msg = crawl_result.error_message or "Unknown error"
                retry_count = url_doc.get("retry_count", 0) + 1

                if retry_count <= settings.max_retries:
                    # Retry the URL
                    print(f"[RETRY] Retry {retry_count}/{settings.max_retries} for {normalized_url}: {error_msg}")
                    await self.url_repo.retry_url(normalized_url)
                else:
                    # Max retries reached
                    print(f"[FAILED] Max retries reached for {normalized_url}: {error_msg}")
                    await self.url_repo.mark_failed(normalized_url, error_msg, retry_count)
                    await self.session_service.record_page_failed()
                    await self.session_service.record_page_processed()  # اضافه کنید


                return

            # Check content validity
            is_valid, reason = self.content_filter.is_valid_content(
                crawl_result.markdown_content or "",
                crawl_result.status_code,
            )

            if not is_valid:
                print(f"[SKIPPED] {normalized_url}: {reason}")
                await self.url_repo.mark_skipped(normalized_url, reason)
                await self.session_service.record_page_skipped()
                await self.session_service.record_page_processed()  # اضافه کنید
                return

            # Extract and clean content
            cleaned_content = self.content_extractor.extract_from_markdown(
                crawl_result.markdown_content or ""
            )

            # Get next file number
            file_number = await self.file_counter.get_next_number()

            # Save content to file
            content_file = self.text_storage.save(cleaned_content, file_number)

            # Mark URL as completed
            await self.url_repo.mark_completed(
                normalized_url=normalized_url,
                file_number=file_number,
                content_file=content_file,
                status_code=crawl_result.status_code,
                content_type=crawl_result.content_type,
                canonical_url=crawl_result.canonical_url,
                content_hash=crawl_result.content_hash,
            )

            # Record page crawled
            pages_crawled = await self.session_service.record_page_crawled()
            await self.session_service.record_page_processed()  # اضافه کنید


            print(f"[SAVED] {normalized_url} → {content_file} (Page {pages_crawled})")

            # Discover new URLs from this page
            if new_urls:
                urls_added = 0
                for new_url in new_urls:
                    try:
                        # Normalize new URL
                        normalized_new = self.normalizer.normalize(new_url)

                        if not normalized_new:
                            continue

                        # Add to database
                        is_new = await self.url_repo.upsert_url(
                            url=new_url,
                            normalized_url=normalized_new,
                            domain=self.domain_policy.get_allowed_domain(),
                            source=URLSource.HTML,
                            depth=depth + 1,
                            parent_url=normalized_url,
                        )

                        if is_new:
                            urls_added += 1

                    except Exception as e:
                        print(f"[DISCOVERY] Error adding URL {new_url}: {e}")
                        continue

                if urls_added > 0:
                    await self.session_service.record_urls_discovered(urls_added)
                    print(f"[DISCOVERY] Discovered {urls_added} new URL(s) from {normalized_url}")

        except Exception as e:
            print(f"[ERROR] Unexpected error processing {normalized_url}: {e}")
            await self.url_repo.mark_failed(normalized_url, str(e), 0)
            await self.session_service.record_page_failed()
            await self.session_service.record_page_processed()  # اضافه کنید


    async def _print_final_stats(self) -> None:
        """Print final crawl statistics"""
        stats = await self.session_service.get_session_stats()
        domain = self.domain_policy.get_allowed_domain()

        # Get database counts
        pending_count = await self.url_repo.get_pending_count(domain)
        completed_count = await self.url_repo.get_completed_count(domain)
        failed_count = await self.url_repo.get_failed_count(domain)
        skipped_count = await self.url_repo.get_skipped_count(domain)
        total_count = await self.url_repo.get_total_count(domain)

        # Get storage stats
        total_files = self.text_storage.get_total_files()
        total_size_mb = self.text_storage.get_total_size_mb()

        print("\n" + "=" * 60)
        print("CRAWL COMPLETED")
        print("=" * 60)
        print(f"Root URL       : {stats.get('root_url')}")
        print(f"Session ID     : {stats.get('session_id')}")
        print(f"Limit          : {stats.get('limit') if stats.get('limit') else 'Unlimited'}")
        print(f"Pages Crawled  : {stats.get('pages_crawled', 0)}")
        print(f"Pages Failed   : {stats.get('pages_failed', 0)}")
        print(f"Pages Skipped  : {stats.get('pages_skipped', 0)}")
        print(f"URLs Discovered: {stats.get('urls_discovered', 0)}")
        print(f"Files Created  : {total_files}")
        print(f"Total Size     : {total_size_mb:.2f} MB")
        print()
        print("Database Status:")
        print(f"  Total URLs   : {total_count}")
        print(f"  Completed    : {completed_count}")
        print(f"  Pending      : {pending_count}")
        print(f"  Failed       : {failed_count}")
        print(f"  Skipped      : {skipped_count}")
        print()
        print(f"Output: {settings.output_dir}")
        print("=" * 60)
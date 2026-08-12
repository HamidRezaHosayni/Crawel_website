"""Session Service Module

This module provides functionality for managing crawl sessions,
including session creation, limit enforcement, and session tracking.
"""
from datetime import datetime
from typing import Optional

from app.database.repositories.session_repository import SessionRepository
from app.models.session import SessionStatus
from app.url.domain import DomainPolicy


class SessionService:
    """Service for managing crawl sessions"""

    def __init__(self, session_repo: SessionRepository) -> None:
        """
        Initialize session service.

        Args:
            session_repo: Session repository instance
        """
        self.session_repo = session_repo
        self._current_session_id: Optional[str] = None

    def generate_session_id(self, root_url: str) -> str:
        """
        Generate session ID from domain and timestamp.

        Format: {domain}_{YYYYMMDD}_{HHMMSS}

        Args:
            root_url: Root URL of the crawl

        Returns:
            Session ID string

        Examples:
            >>> service = SessionService(repo)
            >>> service.generate_session_id("https://example.com")
            'example.com_20260812_143025'
        """
        # Extract domain
        domain_policy = DomainPolicy(root_url)
        domain = domain_policy.get_allowed_domain()

        # Generate timestamp
        now = datetime.utcnow()
        timestamp = now.strftime("%Y%m%d_%H%M%S")

        # Combine domain and timestamp
        session_id = f"{domain}_{timestamp}"

        return session_id

    async def create_session(
        self,
        root_url: str,
        limit: Optional[int] = None,
    ) -> str:
        """
        Create a new crawl session.

        Args:
            root_url: Root URL being crawled
            limit: Maximum pages to crawl (None for unlimited)

        Returns:
            Session ID
        """
        session_id = self.generate_session_id(root_url)

        # Extract domain
        domain_policy = DomainPolicy(root_url)
        root_domain = domain_policy.get_allowed_domain()

        # Create session in database
        await self.session_repo.create_session(
            session_id=session_id,
            root_url=root_url,
            root_domain=root_domain,
            limit=limit,
        )

        self._current_session_id = session_id

        return session_id

    async def can_crawl_more(self) -> bool:
        """
        Check if current session can crawl more pages.

        This method respects the --limit parameter by checking
        if pages_crawled has reached the limit.

        Returns:
            True if more pages can be crawled
        """
        if not self._current_session_id:
            return False

        return await self.session_repo.can_crawl_more(self._current_session_id)

    async def record_page_crawled(self) -> int:
        """
        Record that a page was successfully crawled.

        Returns:
            New pages crawled count
        """
        if not self._current_session_id:
            return 0

        return await self.session_repo.increment_pages_crawled(self._current_session_id)

    async def record_page_failed(self) -> None:
        """Record that a page crawl failed"""
        if not self._current_session_id:
            return

        await self.session_repo.increment_pages_failed(self._current_session_id)

    async def record_page_skipped(self) -> None:
        """Record that a page was skipped"""
        if not self._current_session_id:
            return

        await self.session_repo.increment_pages_skipped(self._current_session_id)

    async def record_urls_discovered(self, count: int) -> None:
        """
        Record that URLs were discovered.

        Args:
            count: Number of URLs discovered
        """
        if not self._current_session_id:
            return

        await self.session_repo.add_urls_discovered(self._current_session_id, count)

    async def get_pages_crawled(self) -> int:
        """
        Get current pages crawled count.

        Returns:
            Number of pages crawled
        """
        if not self._current_session_id:
            return 0

        return await self.session_repo.get_pages_crawled(self._current_session_id)

    async def complete_session(
        self,
        status: SessionStatus = SessionStatus.COMPLETED,
    ) -> None:
        """
        Mark current session as completed.

        Args:
            status: Final session status
        """
        if not self._current_session_id:
            return

        await self.session_repo.complete_session(self._current_session_id, status)

    async def get_session_stats(self) -> dict:
        """
        Get current session statistics.

        Returns:
            Dictionary with session statistics
        """
        if not self._current_session_id:
            return {}

        session = await self.session_repo.get_session(self._current_session_id)

        if not session:
            return {}

        return {
            "session_id": session.get("session_id"),
            "root_url": session.get("root_url"),
            "root_domain": session.get("root_domain"),
            "limit": session.get("limit"),
            "pages_crawled": session.get("pages_crawled", 0),
            "pages_failed": session.get("pages_failed", 0),
            "pages_skipped": session.get("pages_skipped", 0),
            "urls_discovered": session.get("urls_discovered", 0),
            "status": session.get("status"),
            "started_at": session.get("started_at"),
            "finished_at": session.get("finished_at"),
        }

    async def record_page_processed(self) -> int:
        """
        Record that a page was processed (crawled, failed, or skipped).

        Returns:
            New pages processed count
        """
        if not self._current_session_id:
            return 0

        return await self.session_repo.increment_pages_processed(self._current_session_id)

    def get_current_session_id(self) -> Optional[str]:
        """
        Get current session ID.

        Returns:
            Current session ID or None
        """
        return self._current_session_id
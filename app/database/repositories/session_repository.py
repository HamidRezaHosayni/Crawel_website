"""Session Repository for MongoDB"""
from datetime import datetime
from typing import Optional, Dict, Any

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.session import CrawlSession, SessionStatus


class SessionRepository:
    """Repository for Crawl Session documents"""

    COLLECTION_NAME = "crawl_sessions"

    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        """
        Initialize repository.

        Args:
            database: MongoDB database instance
        """
        self.collection = database[self.COLLECTION_NAME]

    async def create_indexes(self) -> None:
        """Create necessary indexes"""
        # Index on session_id
        await self.collection.create_index(
            "session_id",
            unique=True,
            name="idx_session_id_unique",
        )

        # Index on root_domain for filtering
        await self.collection.create_index(
            "root_domain",
            name="idx_root_domain",
        )

    async def create_session(
        self,
        session_id: str,
        root_url: str,
        root_domain: str,
        limit: Optional[int] = None,
    ) -> None:
        """
        Create a new crawl session.
        """
        now = datetime.utcnow()

        document = {
            "session_id": session_id,
            "root_url": root_url,
            "root_domain": root_domain,
            "limit": limit,
            "pages_crawled": 0,
            "pages_failed": 0,
            "pages_skipped": 0,
            "pages_processed": 0,  # اضافه کنید
            "urls_discovered": 0,
            "status": SessionStatus.RUNNING.value,
            "started_at": now,
            "finished_at": None,
            "error_message": None,
        }

        await self.collection.insert_one(document)

    async def increment_pages_crawled(self, session_id: str) -> int:
        """
        Increment pages crawled counter.

        Args:
            session_id: Session identifier

        Returns:
            New pages crawled count
        """
        filter_query = {"session_id": session_id}

        update_operation = {
            "$inc": {"pages_crawled": 1},
        }

        result = await self.collection.find_one_and_update(
            filter_query,
            update_operation,
            return_document=True,
        )

        return result.get("pages_crawled", 0) if result else 0

    async def increment_pages_failed(self, session_id: str) -> None:
        """
        Increment pages failed counter.

        Args:
            session_id: Session identifier
        """
        filter_query = {"session_id": session_id}

        update_operation = {
            "$inc": {"pages_failed": 1},
        }

        await self.collection.update_one(filter_query, update_operation)

    async def increment_pages_skipped(self, session_id: str) -> None:
        """
        Increment pages skipped counter.

        Args:
            session_id: Session identifier
        """
        filter_query = {"session_id": session_id}

        update_operation = {
            "$inc": {"pages_skipped": 1},
        }

        await self.collection.update_one(filter_query, update_operation)

    async def add_urls_discovered(self, session_id: str, count: int) -> None:
        """
        Add to URLs discovered counter.

        Args:
            session_id: Session identifier
            count: Number of URLs discovered
        """
        filter_query = {"session_id": session_id}

        update_operation = {
            "$inc": {"urls_discovered": count},
        }

        await self.collection.update_one(filter_query, update_operation)

    async def get_pages_crawled(self, session_id: str) -> int:
        """
        Get current pages crawled count.

        Args:
            session_id: Session identifier

        Returns:
            Number of pages crawled
        """
        document = await self.collection.find_one({"session_id": session_id})
        return document.get("pages_crawled", 0) if document else 0

    async def can_crawl_more(self, session_id: str) -> bool:
        """
        Check if session can crawl more pages (respecting limit).

        Args:
            session_id: Session identifier

        Returns:
            True if more pages can be crawled
        """
        document = await self.collection.find_one({"session_id": session_id})

        if not document:
            return False

        limit = document.get("limit")
        
        # Use pages_processed instead of pages_crawled
        pages_processed = document.get("pages_processed", 0)

        # If no limit, always can crawl
        if limit is None:
            return True

        return pages_processed < limit

    async def complete_session(self, session_id: str, status: SessionStatus = SessionStatus.COMPLETED) -> None:
        """
        Mark session as completed.

        Args:
            session_id: Session identifier
            status: Final session status
        """
        now = datetime.utcnow()

        filter_query = {"session_id": session_id}

        update_operation = {
            "$set": {
                "status": status.value,
                "finished_at": now,
            },
        }

        await self.collection.update_one(filter_query, update_operation)

    async def increment_pages_processed(self, session_id: str) -> int:
        """
        Increment total pages processed counter (crawled + failed + skipped).

        Args:
            session_id: Session identifier

        Returns:
            New pages processed count
        """
        filter_query = {"session_id": session_id}

        update_operation = {
            "$inc": {"pages_processed": 1},
        }

        result = await self.collection.find_one_and_update(
            filter_query,
            update_operation,
            return_document=True,
        )

        return result.get("pages_processed", 0) if result else 0

    async def get_pages_processed(self, session_id: str) -> int:
        """
        Get current pages processed count.

        Args:
            session_id: Session identifier

        Returns:
            Number of pages processed
        """
        document = await self.collection.find_one({"session_id": session_id})
        return document.get("pages_processed", 0) if document else 0
    
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get session document.

        Args:
            session_id: Session identifier

        Returns:
            Session document or None
        """
        return await self.collection.find_one({"session_id": session_id})
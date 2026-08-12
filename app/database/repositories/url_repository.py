"""URL Repository for MongoDB"""
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.url import URLDocument, URLStatus, URLSource


class URLRepository:
    """Repository for URL documents"""

    COLLECTION_NAME = "urls"

    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        """
        Initialize repository.

        Args:
            database: MongoDB database instance
        """
        self.collection = database[self.COLLECTION_NAME]

    async def create_indexes(self) -> None:
        """Create necessary indexes"""
        # Unique index on normalized_url for deduplication
        await self.collection.create_index(
            "normalized_url",
            unique=True,
            name="idx_normalized_url_unique",
        )

        # Index for queue processing (status + updated_at)
        await self.collection.create_index(
            [("status", 1), ("updated_at", 1)],
            name="idx_status_updated",
        )

        # Index for domain filtering
        await self.collection.create_index(
            "domain",
            name="idx_domain",
        )

    async def upsert_url(
        self,
        url: str,
        normalized_url: str,
        domain: str,
        source: URLSource,
        depth: int = 0,
        parent_url: Optional[str] = None,
    ) -> bool:
        """
        Insert or update a URL document.

        Args:
            url: Original URL
            normalized_url: Normalized URL (unique key)
            domain: Domain name
            source: Source where URL was discovered
            depth: Crawl depth
            parent_url: Parent URL that discovered this URL

        Returns:
            True if new document was inserted, False if updated
        """
        now = datetime.utcnow()

        filter_query = {"normalized_url": normalized_url}

        # Update operation: add source to sources array if not exists
        update_operation = {
            "$setOnInsert": {
                "url": url,
                "normalized_url": normalized_url,
                "domain": domain,
                "status": URLStatus.PENDING.value,
                "depth": depth,
                "parent_url": parent_url,
                "created_at": now,
                "retry_count": 0,
            },
            "$set": {
                "updated_at": now,
            },
            "$addToSet": {
                "sources": source.value,
            },
        }

        result = await self.collection.update_one(
            filter_query,
            update_operation,
            upsert=True,
        )

        return result.upserted_id is not None

    async def claim_next_url(self, domain: str) -> Optional[Dict[str, Any]]:
        """
        Atomically claim the next pending URL for processing.

        This method uses find_one_and_update to ensure that in a
        multi-worker environment, no two workers can claim the same URL.

        Args:
            domain: Domain to filter URLs

        Returns:
            URL document or None if no pending URLs
        """
        now = datetime.utcnow()

        filter_query = {
            "status": URLStatus.PENDING.value,
            "domain": domain,
        }

        update_operation = {
            "$set": {
                "status": URLStatus.PROCESSING.value,
                "updated_at": now,
            },
        }

        # Atomically find and update
        document = await self.collection.find_one_and_update(
            filter_query,
            update_operation,
            sort=[("created_at", 1)],  # FIFO: oldest first
            return_document=True,  # Return updated document
        )

        return document


    async def mark_completed(
        self,
        normalized_url: str,
        file_number: int,
        content_file: str,  # این حالا فقط "45.txt" است
        status_code: Optional[int] = None,
        content_type: Optional[str] = None,
        canonical_url: Optional[str] = None,
        content_hash: Optional[str] = None,
    ) -> None:
            """Mark URL as completed with crawl results."""
            now = datetime.utcnow()

            filter_query = {"normalized_url": normalized_url}

            update_operation = {
                "$set": {
                    "status": URLStatus.COMPLETED.value,
                    "file_number": file_number,
                    "content_file": content_file,  # فقط نام فایل
                    "status_code": status_code,
                    "content_type": content_type,
                    "canonical_url": canonical_url,
                    "content_hash": content_hash,
                    "completed_at": now,
                    "updated_at": now,
                },
            }

            await self.collection.update_one(filter_query, update_operation)


    async def mark_failed(
        self,
        normalized_url: str,
        error_message: str,
        retry_count: int,
    ) -> None:
        """
        Mark URL as failed.

        Args:
            normalized_url: Normalized URL
            error_message: Error message
            retry_count: Number of retries attempted
        """
        now = datetime.utcnow()

        filter_query = {"normalized_url": normalized_url}

        update_operation = {
            "$set": {
                "status": URLStatus.FAILED.value,
                "error_message": error_message,
                "retry_count": retry_count,
                "updated_at": now,
            },
        }

        await self.collection.update_one(filter_query, update_operation)

    async def mark_skipped(self, normalized_url: str, reason: str) -> None:
        """
        Mark URL as skipped.

        Args:
            normalized_url: Normalized URL
            reason: Reason for skipping
        """
        now = datetime.utcnow()

        filter_query = {"normalized_url": normalized_url}

        update_operation = {
            "$set": {
                "status": URLStatus.SKIPPED.value,
                "error_message": reason,
                "updated_at": now,
            },
        }

        await self.collection.update_one(filter_query, update_operation)

    async def retry_url(self, normalized_url: str) -> None:
        """
        Mark URL for retry (set back to pending).

        Args:
            normalized_url: Normalized URL
        """
        now = datetime.utcnow()

        filter_query = {"normalized_url": normalized_url}

        update_operation = {
            "$set": {
                "status": URLStatus.PENDING.value,
                "updated_at": now,
            },
            "$inc": {
                "retry_count": 1,
            },
        }

        await self.collection.update_one(filter_query, update_operation)

    async def recover_stale_processing(
        self,
        domain: str,
        timeout_minutes: int = 10,
    ) -> int:
        """
        Recover URLs stuck in processing state.

        Args:
            domain: Domain to filter URLs
            timeout_minutes: Timeout threshold in minutes

        Returns:
            Number of URLs recovered
        """
        threshold = datetime.utcnow() - timedelta(minutes=timeout_minutes)

        filter_query = {
            "status": URLStatus.PROCESSING.value,
            "domain": domain,
            "updated_at": {"$lt": threshold},
        }

        update_operation = {
            "$set": {
                "status": URLStatus.PENDING.value,
                "updated_at": datetime.utcnow(),
            },
        }

        result = await self.collection.update_many(filter_query, update_operation)
        return result.modified_count

    async def get_pending_count(self, domain: str) -> int:
        """
        Get count of pending URLs.

        Args:
            domain: Domain to filter

        Returns:
            Number of pending URLs
        """
        filter_query = {
            "status": URLStatus.PENDING.value,
            "domain": domain,
        }
        return await self.collection.count_documents(filter_query)

    async def get_completed_count(self, domain: str) -> int:
        """
        Get count of completed URLs.

        Args:
            domain: Domain to filter

        Returns:
            Number of completed URLs
        """
        filter_query = {
            "status": URLStatus.COMPLETED.value,
            "domain": domain,
        }
        return await self.collection.count_documents(filter_query)

    async def get_failed_count(self, domain: str) -> int:
        """
        Get count of failed URLs.

        Args:
            domain: Domain to filter

        Returns:
            Number of failed URLs
        """
        filter_query = {
            "status": URLStatus.FAILED.value,
            "domain": domain,
        }
        return await self.collection.count_documents(filter_query)

    async def get_skipped_count(self, domain: str) -> int:
        """
        Get count of skipped URLs.

        Args:
            domain: Domain to filter

        Returns:
            Number of skipped URLs
        """
        filter_query = {
            "status": URLStatus.SKIPPED.value,
            "domain": domain,
        }
        return await self.collection.count_documents(filter_query)

    async def get_total_count(self, domain: str) -> int:
        """
        Get total count of URLs.

        Args:
            domain: Domain to filter

        Returns:
            Total number of URLs
        """
        filter_query = {"domain": domain}
        return await self.collection.count_documents(filter_query)

    async def get_by_normalized_url(self, normalized_url: str) -> Optional[Dict[str, Any]]:
        """
        Get URL document by normalized URL.

        Args:
            normalized_url: Normalized URL

        Returns:
            URL document or None
        """
        return await self.collection.find_one({"normalized_url": normalized_url})

    async def reset_failed_urls(self, domain: str) -> int:
        """
        Reset all failed URLs back to pending status.

        Args:
            domain: Domain to filter URLs

        Returns:
            Number of URLs reset
        """
        now = datetime.utcnow()

        filter_query = {
            "status": URLStatus.FAILED.value,
            "domain": domain,
        }

        update_operation = {
            "$set": {
                "status": URLStatus.PENDING.value,
                "updated_at": now,
                "error_message": None,
                "retry_count": 0,
            },
        }

        result = await self.collection.update_many(filter_query, update_operation)
        return result.modified_count

    async def url_exists(self, normalized_url: str) -> bool:
        """
        Check if URL exists in database.

        Args:
            normalized_url: Normalized URL

        Returns:
            True if URL exists
        """
        result = await self.collection.find_one(
            {"normalized_url": normalized_url},
            {"_id": 1},
        )
        return result is not None
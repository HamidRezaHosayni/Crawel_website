"""Sitemap Repository for MongoDB"""
from datetime import datetime
from typing import Optional, Dict, Any

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.sitemap import SitemapStatus, SitemapType


class SitemapRepository:
    """Repository for Sitemap documents"""

    COLLECTION_NAME = "sitemaps"

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
            name="idx_sitemap_normalized_url_unique",
        )

    async def sitemap_exists(self, normalized_url: str) -> bool:
        """
        Check if sitemap already exists in database.

        Args:
            normalized_url: Normalized sitemap URL

        Returns:
            True if sitemap exists
        """
        result = await self.collection.find_one(
            {"normalized_url": normalized_url},
            {"_id": 1},
        )
        return result is not None

    async def is_processed(self, normalized_url: str) -> bool:
        """
        Check if sitemap has been processed.

        Args:
            normalized_url: Normalized sitemap URL

        Returns:
            True if sitemap is processed
        """
        document = await self.collection.find_one(
            {"normalized_url": normalized_url},
            {"status": 1},
        )
        return document.get("status") == SitemapStatus.PROCESSED.value if document else False

    async def create_or_update(
        self,
        url: str,
        normalized_url: str,
        source: str = "robots",
    ) -> bool:
        """
        Create or update sitemap document.

        Args:
            url: Original sitemap URL
            normalized_url: Normalized sitemap URL
            source: Source where sitemap was discovered

        Returns:
            True if new document was inserted
        """
        now = datetime.utcnow()

        filter_query = {"normalized_url": normalized_url}

        update_operation = {
            "$setOnInsert": {
                "url": url,
                "normalized_url": normalized_url,
                "status": SitemapStatus.DISCOVERED.value,
                "sitemap_type": SitemapType.UNKNOWN.value,
                "urls_found": 0,
                "sitemaps_found": 0,
                "source": source,
                "discovered_at": now,
                "processed_at": None,
            },
            "$set": {
                "updated_at": now,
            },
        }

        result = await self.collection.update_one(
            filter_query,
            update_operation,
            upsert=True,
        )

        return result.upserted_id is not None

    async def mark_processing(self, normalized_url: str) -> None:
        """
        Mark sitemap as processing.

        Args:
            normalized_url: Normalized sitemap URL
        """
        now = datetime.utcnow()

        filter_query = {"normalized_url": normalized_url}

        update_operation = {
            "$set": {
                "status": SitemapStatus.PROCESSING.value,
                "updated_at": now,
            },
        }

        await self.collection.update_one(filter_query, update_operation)

    async def mark_processed(
        self,
        normalized_url: str,
        sitemap_type: SitemapType,
        urls_found: int,
        sitemaps_found: int = 0,
    ) -> None:
        """
        Mark sitemap as processed.

        Args:
            normalized_url: Normalized sitemap URL
            sitemap_type: Type of sitemap
            urls_found: Number of URLs found
            sitemaps_found: Number of child sitemaps found (for index)
        """
        now = datetime.utcnow()

        filter_query = {"normalized_url": normalized_url}

        update_operation = {
            "$set": {
                "status": SitemapStatus.PROCESSED.value,
                "sitemap_type": sitemap_type.value,
                "urls_found": urls_found,
                "sitemaps_found": sitemaps_found,
                "processed_at": now,
                "updated_at": now,
            },
        }

        await self.collection.update_one(filter_query, update_operation)

    async def mark_failed(self, normalized_url: str, error_message: str) -> None:
        """
        Mark sitemap as failed.

        Args:
            normalized_url: Normalized sitemap URL
            error_message: Error message
        """
        now = datetime.utcnow()

        filter_query = {"normalized_url": normalized_url}

        update_operation = {
            "$set": {
                "status": SitemapStatus.FAILED.value,
                "error_message": error_message,
                "updated_at": now,
            },
        }

        await self.collection.update_one(filter_query, update_operation)

    async def get_by_normalized_url(self, normalized_url: str) -> Optional[Dict[str, Any]]:
        """
        Get sitemap document by normalized URL.

        Args:
            normalized_url: Normalized sitemap URL

        Returns:
            Sitemap document or None
        """
        return await self.collection.find_one({"normalized_url": normalized_url})
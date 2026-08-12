"""Counter Repository for MongoDB"""
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorDatabase


class CounterRepository:
    """Repository for atomic counter operations"""

    COLLECTION_NAME = "counters"

    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        """
        Initialize repository.

        Args:
            database: MongoDB database instance
        """
        self.collection = database[self.COLLECTION_NAME]

    async def get_next_file_number(self) -> int:
        """
        Atomically get next file number.

        This method uses find_one_and_update with $inc to ensure
        that even in multi-worker environments, no two workers
        can get the same file number.

        Returns:
            Next file number (starting from 1)
        """
        filter_query = {"_id": "file_counter"}

        update_operation = {
            "$inc": {"seq": 1},
        }

        result = await self.collection.find_one_and_update(
            filter_query,
            update_operation,
            upsert=True,  # Create if not exists
            return_document=True,  # Return updated document
        )

        return result.get("seq", 1) if result else 1

    async def get_current_file_number(self) -> int:
        """
        Get current file number without incrementing.

        Returns:
            Current file number (0 if not initialized)
        """
        document = await self.collection.find_one({"_id": "file_counter"})
        return document.get("seq", 0) if document else 0
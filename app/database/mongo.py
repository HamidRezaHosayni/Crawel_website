"""MongoDB Connection Manager"""
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config import settings


class MongoDBConnection:
    """MongoDB Connection Manager"""

    def __init__(self) -> None:
        """Initialize connection manager"""
        self._client: Optional[AsyncIOMotorClient] = None
        self._database: Optional[AsyncIOMotorDatabase] = None

    async def connect(self) -> AsyncIOMotorDatabase:
        """
        Connect to MongoDB.

        Returns:
            MongoDB database instance
        """
        if self._client is None:
            self._client = AsyncIOMotorClient(
                settings.mongo_uri,
                # Connection pool settings
                maxPoolSize=50,
                minPoolSize=10,
                # Timeout settings
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000,
                socketTimeoutMS=30000,
            )
            self._database = self._client[settings.mongo_database]

        return self._database

    async def disconnect(self) -> None:
        """Close MongoDB connection"""
        if self._client:
            self._client.close()
            self._client = None
            self._database = None

    def get_database(self) -> Optional[AsyncIOMotorDatabase]:
        """
        Get current database instance.

        Returns:
            Database instance or None if not connected
        """
        return self._database

    async def health_check(self) -> bool:
        """
        Check MongoDB connection health.

        Returns:
            True if connection is healthy
        """
        try:
            if self._client:
                await self._client.admin.command("ping")
                return True
        except Exception:
            pass
        return False


# Singleton instance
mongo_connection = MongoDBConnection()
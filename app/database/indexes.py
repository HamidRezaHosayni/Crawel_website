"""Database Index Manager"""
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database.repositories.counter_repository import CounterRepository
from app.database.repositories.session_repository import SessionRepository
from app.database.repositories.sitemap_repository import SitemapRepository
from app.database.repositories.url_repository import URLRepository


async def create_all_indexes(database: AsyncIOMotorDatabase) -> None:
    """
    Create all necessary indexes for all collections.

    Args:
        database: MongoDB database instance
    """
    # Create URL indexes
    url_repo = URLRepository(database)
    await url_repo.create_indexes()

    # Create Session indexes
    session_repo = SessionRepository(database)
    await session_repo.create_indexes()

    # Create Sitemap indexes
    sitemap_repo = SitemapRepository(database)
    await sitemap_repo.create_indexes()

    # Counter collection doesn't need indexes (uses _id)
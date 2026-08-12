"""Database Module

This module provides MongoDB connection and repository functionality.
"""
from app.database.mongo import MongoDBConnection, mongo_connection
from app.database.repositories.counter_repository import CounterRepository
from app.database.repositories.session_repository import SessionRepository
from app.database.repositories.sitemap_repository import SitemapRepository
from app.database.repositories.url_repository import URLRepository
from app.database.indexes import create_all_indexes

__all__ = [
    "MongoDBConnection",
    "mongo_connection",
    "URLRepository",
    "SessionRepository",
    "CounterRepository",
    "SitemapRepository",
    "create_all_indexes",
]
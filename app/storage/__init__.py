"""Storage Module

This module provides functionality for storing crawled content
as TXT files with atomic write operations and unique file numbering.
"""
from app.storage.file_counter import FileCounter
from app.storage.text_storage import TextStorage

__all__ = [
    "TextStorage",
    "FileCounter",
]
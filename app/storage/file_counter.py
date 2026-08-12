"""File Counter Module

This module provides a simplified interface for generating unique
file numbers using MongoDB atomic counters.
"""
from app.database.repositories.counter_repository import CounterRepository


class FileCounter:
    """File counter for generating unique file numbers"""

    def __init__(self, counter_repo: CounterRepository) -> None:
        """
        Initialize file counter.

        Args:
            counter_repo: Counter repository instance
        """
        self.counter_repo = counter_repo

    async def get_next_number(self) -> int:
        """
        Get next unique file number.

        This method atomically increments the counter and returns
        the new value, ensuring uniqueness even in multi-worker
        environments.

        Returns:
            Next file number (starting from 1)
        """
        return await self.counter_repo.get_next_file_number()

    async def get_current_number(self) -> int:
        """
        Get current file number without incrementing.

        Returns:
            Current file number (0 if not initialized)
        """
        return await self.counter_repo.get_current_file_number()
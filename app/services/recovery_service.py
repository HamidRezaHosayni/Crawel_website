"""Recovery Service Module

This module provides functionality for recovering URLs that are
stuck in processing state due to crashes or interruptions.
"""
from app.config import settings
from app.database.repositories.url_repository import URLRepository


class RecoveryService:
    """Service for recovering stuck URLs"""

    def __init__(self, url_repo: URLRepository) -> None:
        """
        Initialize recovery service.

        Args:
            url_repo: URL repository instance
        """
        self.url_repo = url_repo

    async def recover_stale_processing(self, domain: str) -> int:
        """
        Recover URLs stuck in processing state.

        This method finds URLs that have been in processing state
        for longer than the configured timeout and resets them
        to pending state.

        Args:
            domain: Domain to filter URLs

        Returns:
            Number of URLs recovered
        """
        timeout_minutes = settings.stale_processing_timeout_minutes

        print(f"[RECOVERY] Checking for stale processing URLs (timeout: {timeout_minutes} minutes)")

        # Recover stale URLs
        recovered_count = await self.url_repo.recover_stale_processing(
            domain=domain,
            timeout_minutes=timeout_minutes,
        )

        if recovered_count > 0:
            print(f"[RECOVERY] Recovered {recovered_count} stale processing URLs")
        else:
            print(f"[RECOVERY] No stale processing URLs found")

        return recovered_count
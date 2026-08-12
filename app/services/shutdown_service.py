"""Shutdown Service Module

This module provides functionality for graceful shutdown handling,
ensuring that in-progress crawls complete before the application exits.
"""
import asyncio
import signal
from typing import Optional


class ShutdownService:
    """Service for managing graceful shutdown"""

    def __init__(self):
        """Initialize shutdown service"""
        self._shutdown_requested = False
        self._shutdown_event = asyncio.Event()

    def request_shutdown(self) -> None:
        """
        Request graceful shutdown.

        This method sets the shutdown flag and signals the event.
        It's safe to call multiple times.
        """
        if not self._shutdown_requested:
            self._shutdown_requested = True
            self._shutdown_event.set()
            print("\n[SHUTDOWN] Graceful shutdown requested. Finishing current operation...")

    def is_shutdown_requested(self) -> bool:
        """
        Check if shutdown has been requested.

        Returns:
            True if shutdown was requested
        """
        return self._shutdown_requested

    async def wait_for_shutdown(self) -> None:
        """
        Wait for shutdown signal.

        This method blocks until shutdown is requested.
        """
        await self._shutdown_event.wait()

    def setup_signal_handlers(self, loop: Optional[asyncio.AbstractEventLoop] = None) -> None:
        """
        Setup signal handlers for SIGINT and SIGTERM.

        Args:
            loop: Event loop to add signal handlers to
        """
        if loop is None:
            loop = asyncio.get_running_loop()

        # Handle SIGINT (Ctrl+C)
        loop.add_signal_handler(
            signal.SIGINT,
            self.request_shutdown
        )

        # Handle SIGTERM (kill command)
        loop.add_signal_handler(
            signal.SIGTERM,
            self.request_shutdown
        )

    def reset(self) -> None:
        """Reset shutdown state (useful for testing)"""
        self._shutdown_requested = False
        self._shutdown_event.clear()


# Global shutdown service instance
shutdown_service = ShutdownService()
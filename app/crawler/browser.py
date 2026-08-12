"""Browser Configuration Module

This module provides browser configuration for Crawl4AI,
ensuring it uses the native Chrome installation with JavaScript rendering.
"""
from typing import Optional

from crawl4ai import BrowserConfig


class BrowserManager:
    """Manager for browser configuration"""

    def __init__(
        self,
        headless: bool = True,
        chrome_channel: str = "chrome",
        browser_type: str = "chromium",
    ) -> None:
        """
        Initialize browser manager.

        Args:
            headless: Run browser in headless mode
            chrome_channel: Chrome channel to use (chrome for native Chrome)
            browser_type: Browser type (chromium, firefox, webkit)
        """
        self.headless = headless
        self.chrome_channel = chrome_channel
        self.browser_type = browser_type
        self._browser_config: Optional[BrowserConfig] = None

    def get_browser_config(self) -> BrowserConfig:
        """
        Get browser configuration for Crawl4AI.

        This configuration ensures that:
        1. Native Chrome is used (not Playwright's bundled Chromium)
        2. JavaScript is fully rendered
        3. Headless mode is enabled for server environments

        Returns:
            BrowserConfig instance compatible with Crawl4AI 0.9.2
        """
        if self._browser_config is None:
            self._browser_config = BrowserConfig(
                browser_type=self.browser_type,
                chrome_channel=self.chrome_channel,
                headless=self.headless,
                # Viewport for consistent rendering
                viewport_width=1920,
                viewport_height=1080,
                # User agent to avoid bot detection
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
            )

        return self._browser_config

    def get_playwright_launch_args(self) -> dict:
        """
        Get Playwright launch arguments for testing.

        Returns:
            Dictionary of launch arguments
        """
        return {
            "channel": self.chrome_channel,
            "headless": self.headless,
        }
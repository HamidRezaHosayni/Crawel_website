"""CLI Parser Module

This module provides command-line argument parsing functionality
using Typer with support for all crawl options.
"""
from pathlib import Path
from typing import Optional

import typer

from app.config import Settings


# Create Typer app
app = typer.Typer(
    name="web-crawler",
    help="Professional Web Crawler for Dataset Collection",
    add_completion=False,
)


class CLIOptions:
    """Container for CLI options"""

    def __init__(
        self,
        url: str,
        limit: Optional[int] = None,
        headless: bool = True,
        delay: float = 1.0,
        output: Optional[Path] = None,
        verbose: bool = False,
    ):
        """
        Initialize CLI options.

        Args:
            url: Root URL to crawl
            limit: Maximum pages to crawl
            headless: Run browser in headless mode
            delay: Delay between crawls in seconds
            output: Output directory for TXT files
            verbose: Enable verbose logging
        """
        self.url = url
        self.limit = limit
        self.headless = headless
        self.delay = delay
        self.output = output
        self.verbose = verbose

    def apply_to_settings(self, settings: Settings) -> Settings:
        """
        Apply CLI options to settings.

        Args:
            settings: Application settings

        Returns:
            Updated settings
        """
        # Apply headless setting
        settings.headless = self.headless

        # Apply delay setting
        settings.crawl_delay = self.delay

        # Apply output directory if specified
        if self.output:
            settings.output_dir = self.output

        return settings


def parse_arguments() -> CLIOptions:
    """
    Parse command-line arguments.

    This function is called by main.py to get CLI options.

    Returns:
        CLIOptions instance

    Raises:
        typer.Exit: If arguments are invalid
    """
    # We'll use a different approach since Typer handles args differently
    # This is a placeholder - actual parsing happens in main.py
    raise NotImplementedError("Use main.py for CLI parsing")


def validate_url(url: str) -> str:
    """
    Validate URL format.

    Args:
        url: URL to validate

    Returns:
        Validated URL

    Raises:
        typer.BadParameter: If URL is invalid
    """
    from urllib.parse import urlparse

    try:
        parsed = urlparse(url)

        if not parsed.scheme:
            # Add https:// if no scheme
            url = f"https://{url}"
            parsed = urlparse(url)

        if parsed.scheme not in ("http", "https"):
            raise typer.BadParameter(
                f"Invalid URL scheme: {parsed.scheme}. Must be http or https."
            )

        if not parsed.netloc:
            raise typer.BadParameter(
                f"Invalid URL: {url}. Missing domain."
            )

        return url

    except Exception as e:
        raise typer.BadParameter(f"Invalid URL: {url}. Error: {e}")


def validate_limit(limit: Optional[int]) -> Optional[int]:
    """
    Validate limit parameter.

    Args:
        limit: Limit value

    Returns:
        Validated limit

    Raises:
        typer.BadParameter: If limit is invalid
    """
    if limit is not None and limit < 1:
        raise typer.BadParameter(
            f"Invalid limit: {limit}. Must be >= 1 or None for unlimited."
        )

    return limit


def validate_delay(delay: float) -> float:
    """
    Validate delay parameter.

    Args:
        delay: Delay value in seconds

    Returns:
        Validated delay

    Raises:
        typer.BadParameter: If delay is invalid
    """
    if delay < 0:
        raise typer.BadParameter(
            f"Invalid delay: {delay}. Must be >= 0."
        )

    return delay


def validate_output(output: Optional[Path]) -> Optional[Path]:
    """
    Validate output directory.

    Args:
        output: Output directory path

    Returns:
        Validated output path

    Raises:
        typer.BadParameter: If output is invalid
    """
    if output is None:
        return None

    # Convert to absolute path
    output = output.absolute()

    # Check if path exists and is a directory
    if output.exists() and not output.is_dir():
        raise typer.BadParameter(
            f"Output path exists but is not a directory: {output}"
        )

    # Try to create directory if it doesn't exist
    try:
        output.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise typer.BadParameter(
            f"Cannot create output directory: {output}. Error: {e}"
        )

    return output
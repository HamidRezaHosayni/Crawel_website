"""Time Utilities Module

This module provides time-related utilities for the crawling system.
"""
from datetime import datetime, timedelta
from typing import Optional


def get_utc_now() -> datetime:
    """
    Get current UTC time.

    Returns:
        Current UTC datetime
    """
    return datetime.utcnow()


def format_timestamp(dt: datetime) -> str:
    """
    Format datetime as ISO string.

    Args:
        dt: Datetime object

    Returns:
        ISO formatted string
    """
    return dt.isoformat() + "Z"


def format_duration(seconds: float) -> str:
    """
    Format duration in human-readable format.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string

    Examples:
        >>> format_duration(90)
        '1m 30s'
        >>> format_duration(3661)
        '1h 1m 1s'
    """
    if seconds < 60:
        return f"{seconds:.1f}s"

    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60

    if minutes < 60:
        return f"{minutes}m {remaining_seconds:.0f}s"

    hours = minutes // 60
    remaining_minutes = minutes % 60

    return f"{hours}h {remaining_minutes}m {remaining_seconds:.0f}s"


def is_stale(
    timestamp: datetime,
    timeout_minutes: int = 10,
) -> bool:
    """
    Check if a timestamp is stale (older than timeout).

    Args:
        timestamp: Timestamp to check
        timeout_minutes: Timeout threshold in minutes

    Returns:
        True if timestamp is stale
    """
    threshold = get_utc_now() - timedelta(minutes=timeout_minutes)
    return timestamp < threshold


def generate_session_timestamp() -> str:
    """
    Generate timestamp for session ID.

    Returns:
        Timestamp string in format YYYYMMDD_HHMMSS
    """
    return get_utc_now().strftime("%Y%m%d_%H%M%S")
"""Retry Utilities Module

This module provides retry decorators with exponential backoff
for handling temporary failures in network requests, crawling,
and database operations.
"""
import asyncio
import random
from functools import wraps
from typing import Callable, Type, Tuple, Optional

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
    wait_random_exponential,
    before_sleep_log,
    RetryError,
)

from app.utils.errors import (
    TemporaryError,
    RateLimitError,
    NetworkError,
    ServerError,
    PermanentError,
)


class RetryConfig:
    """Configuration for retry behavior"""

    def __init__(
        self,
        max_attempts: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        multiplier: float = 2.0,
        jitter: bool = True,
    ):
        """
        Initialize retry configuration.

        Args:
            max_attempts: Maximum number of retry attempts
            initial_delay: Initial delay in seconds
            max_delay: Maximum delay in seconds
            multiplier: Backoff multiplier
            jitter: Whether to add random jitter to delays
        """
        self.max_attempts = max_attempts
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.multiplier = multiplier
        self.jitter = jitter


# Default retry configurations
DEFAULT_RETRY_CONFIG = RetryConfig(
    max_attempts=3,
    initial_delay=1.0,
    max_delay=30.0,
    multiplier=2.0,
    jitter=True,
)

RATE_LIMIT_RETRY_CONFIG = RetryConfig(
    max_attempts=5,
    initial_delay=5.0,  # Longer initial delay for rate limits
    max_delay=120.0,    # Longer max delay
    multiplier=2.0,
    jitter=True,
)

NETWORK_RETRY_CONFIG = RetryConfig(
    max_attempts=5,
    initial_delay=1.0,
    max_delay=60.0,
    multiplier=2.0,
    jitter=True,
)


def get_wait_strategy(config: RetryConfig):
    """
    Get wait strategy based on configuration.

    Args:
        config: Retry configuration

    Returns:
        Tenacity wait strategy
    """
    if config.jitter:
        # Random exponential backoff with jitter
        return wait_random_exponential(
            min=config.initial_delay,
            max=config.max_delay,
            multiplier=config.multiplier,
        )
    else:
        # Pure exponential backoff
        return wait_exponential(
            min=config.initial_delay,
            max=config.max_delay,
            multiplier=config.multiplier,
        )


def retry_on_temporary_error(
    config: RetryConfig = DEFAULT_RETRY_CONFIG,
    exceptions: Tuple[Type[Exception], ...] = (TemporaryError,),
):
    """
    Decorator for retrying on temporary errors with exponential backoff.

    Args:
        config: Retry configuration
        exceptions: Tuple of exception types to retry on

    Returns:
        Decorator function

    Examples:
        >>> @retry_on_temporary_error()
        ... async def fetch_page(url: str) -> str:
        ...     # This will retry on TemporaryError
        ...     pass
    """
    wait_strategy = get_wait_strategy(config)

    return retry(
        retry=retry_if_exception_type(exceptions),
        stop=stop_after_attempt(config.max_attempts),
        wait=wait_strategy,
        before_sleep=before_sleep_log(None, None) if False else None,
        reraise=True,
    )


def retry_on_rate_limit(config: RetryConfig = RATE_LIMIT_RETRY_CONFIG):
    """
    Decorator specifically for rate limit errors (HTTP 429).

    Uses longer delays and more attempts than default retry.

    Args:
        config: Retry configuration

    Returns:
        Decorator function
    """
    wait_strategy = get_wait_strategy(config)

    return retry(
        retry=retry_if_exception_type((RateLimitError, TemporaryError)),
        stop=stop_after_attempt(config.max_attempts),
        wait=wait_strategy,
        reraise=True,
    )


def retry_on_network_error(config: RetryConfig = NETWORK_RETRY_CONFIG):
    """
    Decorator for network-related errors.

    Args:
        config: Retry configuration

    Returns:
        Decorator function
    """
    wait_strategy = get_wait_strategy(config)

    return retry(
        retry=retry_if_exception_type((NetworkError, TemporaryError)),
        stop=stop_after_attempt(config.max_attempts),
        wait=wait_strategy,
        reraise=True,
    )


def async_retry(
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    multiplier: float = 2.0,
    jitter: bool = True,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Optional[Callable] = None,
):
    """
    Async retry decorator with exponential backoff.

    This is a custom implementation that provides more control
    than tenacity for async functions.

    Args:
        max_attempts: Maximum number of attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        multiplier: Backoff multiplier
        jitter: Whether to add random jitter
        exceptions: Tuple of exception types to retry on
        on_retry: Callback function called before each retry

    Returns:
        Decorator function

    Examples:
        >>> @async_retry(max_attempts=3, exceptions=(NetworkError,))
        ... async def fetch_data():
        ...     # This will retry on NetworkError
        ...     pass
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            delay = initial_delay

            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    # Don't retry on last attempt
                    if attempt == max_attempts - 1:
                        raise

                    # Call retry callback if provided
                    if on_retry:
                        await on_retry(attempt + 1, e)

                    # Calculate delay with jitter
                    current_delay = delay
                    if jitter:
                        current_delay = delay * (0.5 + random.random())

                    # Log retry
                    print(f"[RETRY] Attempt {attempt + 1}/{max_attempts} failed: {e}. Retrying in {current_delay:.1f}s...")

                    # Wait before retry
                    await asyncio.sleep(current_delay)

                    # Exponential backoff
                    delay = min(delay * multiplier, max_delay)

            # Should never reach here, but just in case
            raise last_exception

        return wrapper
    return decorator


def calculate_backoff_delay(
    attempt: int,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    multiplier: float = 2.0,
    jitter: bool = True,
) -> float:
    """
    Calculate backoff delay for a given attempt.

    Args:
        attempt: Attempt number (0-based)
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        multiplier: Backoff multiplier
        jitter: Whether to add random jitter

    Returns:
        Delay in seconds

    Examples:
        >>> calculate_backoff_delay(0)
        1.0
        >>> calculate_backoff_delay(1)
        2.0
        >>> calculate_backoff_delay(2)
        4.0
    """
    delay = initial_delay * (multiplier ** attempt)
    delay = min(delay, max_delay)

    if jitter:
        delay = delay * (0.5 + random.random())

    return delay


def is_retryable_status_code(status_code: int) -> bool:
    """
    Check if HTTP status code is retryable.

    Args:
        status_code: HTTP status code

    Returns:
        True if status code is retryable

    Examples:
        >>> is_retryable_status_code(429)
        True
        >>> is_retryable_status_code(500)
        True
        >>> is_retryable_status_code(404)
        False
    """
    # 429: Too Many Requests (rate limit)
    if status_code == 429:
        return True

    # 5xx: Server errors
    if 500 <= status_code < 600:
        return True

    # 408: Request Timeout
    if status_code == 408:
        return True

    # Other status codes are not retryable
    return False


def get_retry_delay_for_status(status_code: int) -> float:
    """
    Get recommended retry delay for a given status code.

    Args:
        status_code: HTTP status code

    Returns:
        Recommended delay in seconds
    """
    if status_code == 429:
        # Rate limit: longer delay
        return 5.0
    elif 500 <= status_code < 600:
        # Server error: moderate delay
        return 2.0
    elif status_code == 408:
        # Timeout: short delay
        return 1.0
    else:
        # Default
        return 1.0
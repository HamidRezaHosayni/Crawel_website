"""Content Filter Module

This module provides functionality to filter out low-quality
or irrelevant content from crawled pages.
"""
import re
from typing import Optional


class ContentFilter:
    """Filter for low-quality or irrelevant content"""

    # Minimum content length to consider valid
    MIN_CONTENT_LENGTH = 100

    # Common phrases that indicate low-quality pages
    LOW_QUALITY_INDICATORS = [
        r'access denied',
        r'404 not found',
        r'page not found',
        r'under construction',
        r'coming soon',
        r'please enable javascript',
        r'enable cookies',
        r'browser not supported',
        r'upgrade your browser',
    ]

    # Error pages patterns
    ERROR_PATTERNS = [
        r'http error \d+',
        r'error \d+',
        r'internal server error',
        r'bad gateway',
        r'service unavailable',
        r'gateway timeout',
    ]

    def __init__(
        self,
        min_length: int = MIN_CONTENT_LENGTH,
        custom_indicators: Optional[list] = None,
    ) -> None:
        """
        Initialize content filter.

        Args:
            min_length: Minimum content length
            custom_indicators: Additional low-quality indicators
        """
        self.min_length = min_length

        # Compile patterns for performance
        self.low_quality_patterns = [
            re.compile(pattern, re.IGNORECASE)
            for pattern in self.LOW_QUALITY_INDICATORS
        ]

        self.error_patterns = [
            re.compile(pattern, re.IGNORECASE)
            for pattern in self.ERROR_PATTERNS
        ]

        # Add custom indicators
        if custom_indicators:
            for indicator in custom_indicators:
                self.low_quality_patterns.append(
                    re.compile(indicator, re.IGNORECASE)
                )

    def is_valid_content(
        self,
        content: str,
        status_code: Optional[int] = None,
    ) -> tuple[bool, str]:
        """
        Check if content is valid and should be saved.

        Args:
            content: Content to check
            status_code: HTTP status code (optional)

        Returns:
            Tuple of (is_valid, reason_if_invalid)
        """
        # Check status code
        if status_code is not None:
            if status_code >= 400:
                return False, f"HTTP error status: {status_code}"

        # Check if content is empty
        if not content or not content.strip():
            return False, "Empty content"

        # Check minimum length
        if len(content.strip()) < self.min_length:
            return False, f"Content too short ({len(content.strip())} chars)"

        # Check for low-quality indicators
        for pattern in self.low_quality_patterns:
            if pattern.search(content):
                return False, f"Low-quality indicator found: {pattern.pattern}"

        # Check for error patterns
        for pattern in self.error_patterns:
            if pattern.search(content):
                return False, f"Error page detected: {pattern.pattern}"

        # Content is valid
        return True, ""

    def should_skip_by_title(self, title: Optional[str]) -> tuple[bool, str]:
        """
        Check if page should be skipped based on title.

        Args:
            title: Page title

        Returns:
            Tuple of (should_skip, reason)
        """
        if not title:
            return False, ""

        title_lower = title.lower()

        # Skip error pages
        error_titles = [
            '404',
            'not found',
            'page not found',
            'access denied',
            'forbidden',
            'internal server error',
            'under construction',
            'coming soon',
        ]

        for error in error_titles:
            if error in title_lower:
                return True, f"Error page title: {title}"

        return False, ""

    def estimate_quality_score(self, content: str) -> float:
        """
        Estimate content quality score (0.0 to 1.0).

        This is a simple heuristic based on content characteristics.

        Args:
            content: Content to score

        Returns:
            Quality score between 0.0 and 1.0
        """
        if not content:
            return 0.0

        score = 0.0

        # Length factor (up to 0.3)
        length = len(content)
        if length > 10000:
            score += 0.3
        elif length > 5000:
            score += 0.25
        elif length > 1000:
            score += 0.2
        elif length > 500:
            score += 0.1
        else:
            score += 0.05

        # Code block factor (up to 0.4)
        code_blocks = content.count('```')
        if code_blocks >= 10:
            score += 0.4
        elif code_blocks >= 5:
            score += 0.3
        elif code_blocks >= 2:
            score += 0.2
        elif code_blocks >= 1:
            score += 0.1

        # Heading factor (up to 0.2)
        headings = content.count('\n#')
        if headings >= 5:
            score += 0.2
        elif headings >= 3:
            score += 0.15
        elif headings >= 1:
            score += 0.1

        # List factor (up to 0.1)
        lists = content.count('\n-') + content.count('\n*') + content.count('\n1.')
        if lists >= 5:
            score += 0.1
        elif lists >= 2:
            score += 0.05

        return min(score, 1.0)
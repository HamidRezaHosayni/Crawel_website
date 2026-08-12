"""Hashing Utilities Module

This module provides hashing functionality for content deduplication.
"""
import hashlib
from typing import Optional


def sha256_hash(content: str) -> str:
    """
    Generate SHA-256 hash of content.

    Args:
        content: Content string

    Returns:
        SHA-256 hex digest

    Examples:
        >>> sha256_hash("hello world")
        'b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9'
    """
    if not content:
        return ""

    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def md5_hash(content: str) -> str:
    """
    Generate MD5 hash of content.

    Note: MD5 is not cryptographically secure but is faster
    and sufficient for content deduplication.

    Args:
        content: Content string

    Returns:
        MD5 hex digest
    """
    if not content:
        return ""

    return hashlib.md5(content.encode('utf-8')).hexdigest()


def content_fingerprint(content: str) -> str:
    """
    Generate a fingerprint for content.

    This creates a normalized hash that ignores whitespace
    differences, useful for detecting near-duplicate content.

    Args:
        content: Content string

    Returns:
        Content fingerprint hash
    """
    if not content:
        return ""

    # Normalize whitespace
    normalized = ' '.join(content.split())

    return sha256_hash(normalized)
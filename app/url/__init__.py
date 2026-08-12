"""URL Module

This module provides URL normalization, validation, and domain management.
"""
from app.url.domain import DomainPolicy
from app.url.normalizer import URLNormalizer
from app.url.validator import URLValidator

__all__ = [
    "URLNormalizer",
    "URLValidator",
    "DomainPolicy",
]
"""Web Crawler Application

A professional web crawling system for dataset collection with:
- Persistent URL queue with MongoDB
- Sitemap and robots.txt discovery
- JavaScript rendering with native Chrome
- Atomic file storage
- Resume capability
- Rate limiting with exponential backoff
"""

__version__ = "1.0.0"
__author__ = "Web Crawler Team"

from app.config import settings

__all__ = [
    "settings",
    "__version__",
]
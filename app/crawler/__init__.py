"""Crawler Module

This module provides web crawling functionality using Crawl4AI
with native Chrome and JavaScript rendering.
"""
from app.crawler.browser import BrowserManager
from app.crawler.crawl4ai_client import Crawl4AIClient
from app.crawler.page_crawler import PageCrawler

__all__ = [
    "BrowserManager",
    "Crawl4AIClient",
    "PageCrawler",
]
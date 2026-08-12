"""Crawl Result Model"""
from typing import Optional, List

from pydantic import BaseModel, Field


class CrawlResult(BaseModel):
    """نتیجه Crawl یک صفحه"""
    url: str
    normalized_url: str

    success: bool
    status_code: Optional[int] = None
    content_type: Optional[str] = None
    error_message: Optional[str] = None

    # محتوای استخراج شده
    markdown_content: Optional[str] = None
    title: Optional[str] = None
    canonical_url: Optional[str] = None
    content_hash: Optional[str] = None

    # لینک‌های کشف شده
    discovered_urls: List[str] = Field(default_factory=list)

    # زمان پاسخ
    response_time_ms: Optional[int] = None

    class Config:
        frozen = True  # Immutable
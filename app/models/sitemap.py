"""Sitemap Model for MongoDB Documents"""
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class SitemapStatus(str, Enum):
    """وضعیت پردازش Sitemap"""
    DISCOVERED = "discovered"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"


class SitemapType(str, Enum):
    """نوع Sitemap"""
    URLSET = "urlset"
    SITEMAP_INDEX = "sitemap_index"
    UNKNOWN = "unknown"


class SitemapDocument(BaseModel):
    """Schema برای یک Sitemap در MongoDB"""
    url: str = Field(..., description="URL فایل Sitemap")
    normalized_url: str = Field(..., description="URL نرمال‌سازی شده (Unique Key)")

    status: SitemapStatus = Field(default=SitemapStatus.DISCOVERED, description="وضعیت پردازش")
    sitemap_type: SitemapType = Field(default=SitemapType.UNKNOWN, description="نوع Sitemap")

    urls_found: int = Field(default=0, ge=0, description="تعداد URLهای استخراج شده")
    sitemaps_found: int = Field(default=0, ge=0, description="تعداد Sitemapهای داخلی (برای Index)")

    source: str = Field(default="robots", description="منبع کشف (robots یا manual)")

    error_message: Optional[str] = Field(default=None, description="پیام خطا در صورت شکست")

    discovered_at: datetime = Field(default_factory=datetime.utcnow)
    processed_at: Optional[datetime] = Field(default=None)

    class Config:
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "url": "https://example.com/sitemap.xml",
                "normalized_url": "https://example.com/sitemap.xml",
                "status": "processed",
                "sitemap_type": "urlset",
                "urls_found": 150,
            }
        }
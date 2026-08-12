"""URL Model for MongoDB Documents"""
from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field, HttpUrl


class URLStatus(str, Enum):
    """وضعیت‌های ممکن برای یک URL"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class URLSource(str, Enum):
    """منبع کشف URL"""
    SEED = "seed"
    SITEMAP = "sitemap"
    ROBOTS = "robots"
    HTML = "html"


class URLDocument(BaseModel):
    """Schema برای یک URL در MongoDB"""
    url: str = Field(..., description="URL اصلی")
    normalized_url: str = Field(..., description="URL نرمال‌سازی شده (Unique Key)")
    domain: str = Field(..., description="دامنه اصلی")

    status: URLStatus = Field(default=URLStatus.PENDING, description="وضعیت فعلی")

    sources: List[URLSource] = Field(default_factory=list, description="منابع کشف")

    depth: int = Field(default=0, ge=0, description="عمق در گراف لینک‌ها")
    parent_url: Optional[str] = Field(default=None, description="URL والد که این لینک از آن کشف شده")

    # Metadata
    status_code: Optional[int] = Field(default=None, description="HTTP Status Code")
    content_type: Optional[str] = Field(default=None, description="Content-Type Header")
    canonical_url: Optional[str] = Field(default=None, description="Canonical URL از HTML")
    content_hash: Optional[str] = Field(default=None, description="SHA-256 محتوای نهایی")

    # Storage
    file_number: Optional[int] = Field(default=None, ge=1, description="شماره فایل TXT")
    content_file: Optional[str] = Field(default=None, description="مسیر فایل ذخیره شده")

    # Retry
    retry_count: int = Field(default=0, ge=0, description="تعداد تلاش‌های مجدد")
    max_retries: int = Field(default=3, ge=0, description="حداکثر تعداد Retry")
    error_message: Optional[str] = Field(default=None, description="پیام آخرین خطا")

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(default=None)

    class Config:
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "url": "https://example.com/docs",
                "normalized_url": "https://example.com/docs",
                "domain": "example.com",
                "status": "pending",
                "sources": ["sitemap"],
                "depth": 1,
            }
        }


class URLCreate(BaseModel):
    """Schema برای ایجاد URL جدید"""
    url: str
    normalized_url: str
    domain: str
    source: URLSource
    depth: int = 0
    parent_url: Optional[str] = None
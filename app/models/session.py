"""Crawl Session Model"""
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class SessionStatus(str, Enum):
    """وضعیت Session"""
    RUNNING = "running"
    COMPLETED = "completed"
    STOPPED = "stopped"
    INTERRUPTED = "interrupted"
    FAILED = "failed"


class CrawlSession(BaseModel):
    """Schema برای Session Crawl"""
    session_id: str = Field(..., description="شناسه یکتای Session")
    root_url: str = Field(..., description="URL اصلی شروع")
    root_domain: str = Field(..., description="دامنه اصلی")

    limit: Optional[int] = Field(default=None, ge=1, description="حداکثر تعداد صفحات برای Crawl")

    pages_crawled: int = Field(default=0, ge=0, description="تعداد صفحات موفق")
    pages_failed: int = Field(default=0, ge=0, description="تعداد صفحات ناموفق")
    pages_skipped: int = Field(default=0, ge=0, description="تعداد صفحات رد شده")
    pages_processed: int = Field(default=0, ge=0, description="تعداد کل صفحات پردازش شده")
    urls_discovered: int = Field(default=0, ge=0, description="تعداد کل URLهای کشف شده")

    status: SessionStatus = Field(default=SessionStatus.RUNNING)

    started_at: datetime = Field(default_factory=datetime.utcnow)
    finished_at: Optional[datetime] = Field(default=None)

    error_message: Optional[str] = None

    class Config:
        use_enum_values = True
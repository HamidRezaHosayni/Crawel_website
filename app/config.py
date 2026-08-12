"""Application Configuration"""
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """تنظیمات اصلی برنامه از Environment Variables"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # MongoDB
    mongo_uri: str = Field(default="mongodb://localhost:27017")
    mongo_database: str = Field(default="web_dataset")

    # Storage
    output_dir: Path = Field(default=Path("./data"))
    log_dir: Path = Field(default=Path("./logs"))

    # Crawl Settings
    headless: bool = Field(default=True)
    crawl_delay: float = Field(default=1.0, ge=0, description="تأخیر بین Crawlها (ثانیه)")
    max_retries: int = Field(default=3, ge=0)
    stale_processing_timeout_minutes: int = Field(default=10, ge=1)

    # Browser
    browser_type: str = Field(default="chromium")
    chrome_channel: str = Field(default="chrome")

    # URLs
    default_sitemap_paths: list[str] = Field(
        default_factory=lambda: [
            "/sitemap.xml",
            "/sitemap_index.xml",
            "/sitemap-index.xml",
            "/sitemapindex.xml",
        ]
    )

    # File Extensions to Skip
    skip_extensions: set[str] = Field(
        default_factory=lambda: {
            ".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".bmp",
            ".mp4", ".mp3", ".wav", ".avi", ".mov",
            ".zip", ".rar", ".7z", ".tar", ".gz",
            ".exe", ".msi", ".dmg", ".app",
            ".iso", ".bin",
            ".pdf", ".doc", ".docx", ".xls", ".xlsx",
            ".css", ".js", ".woff", ".woff2", ".ttf", ".eot",
        }
    )

    # Skipped URL Schemes
    skip_schemes: set[str] = Field(
        default_factory=lambda: {
            "mailto", "javascript", "tel", "data", "blob", "ftp",
        }
    )

    def ensure_directories(self) -> None:
        """ایجاد دایرکتوری‌های مورد نیاز"""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)


# Singleton Instance
settings = Settings()
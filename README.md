```markdown
<div dir="rtl" align="center">

# 🕷️ Web Crawler
### Professional Dataset Collection System

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Crawl4AI](https://img.shields.io/badge/Crawl4AI-0.9.2-green.svg)](https://github.com/unclecode/crawl4ai)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.0+-green.svg)](https://www.mongodb.com/)
[![Playwright](https://img.shields.io/badge/Playwright-1.47-purple.svg)](https://playwright.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Production Ready](https://img.shields.io/badge/status-production--ready-brightgreen.svg)]()

**سیستم حرفه‌ای Crawl وب برای جمع‌آوری Dataset متنی، کدهای برنامه‌نویسی و مستندات فنی**

[🚀 شروع سریع](#-شروع-سریع) • [📖 نصب](#-نصب-و-راهاندازی) • [⚙️ راهنما](#-پارامترهای-cli) • [💡 مثال‌ها](#-مثالهای-کاربردی) • [🐛 عیب‌یابی](#-عیبیابی)

---

</div>

## 📋 فهرست مطالب

- [✨ ویژگی‌ها](#-ویژگیها)
- [🏗️ معماری سیستم](#-معماری-سیستم)
- [📋 پیش‌نیازها](#-پیشنیازها)
- [🛠️ نصب و راه‌اندازی](#-نصب-و-راهاندازی)
- [⚡ شروع سریع](#-شروع-سریع)
- [⚙️ پارامترهای CLI](#-پارامترهای-cli)
- [💡 مثال‌های کاربردی](#-مثالهای-کاربردی)
- [🎯 دستورات Makefile](#-دستورات-makefile)
- [🗄️ ساختار دیتابیس](#-ساختار-دیتابیس)
- [📁 ساختار فایل‌ها](#-ساختار-فایلها)
- [🎓 نکات حرفه‌ای](#-نکات-حرفهای)
- [🐛 عیب‌یابی](#-عیبیابی)
- [🌐 سایت‌های مناسب برای Crawl](#-سایتهای-مناسب-برای-crawl)
- [❓ سوالات متداول](#-سوالات-متداول)
- [🤝 مشارکت](#-مشارکت)
- [📄 مجوز](#-مجوز)

---

## ✨ ویژگی‌ها

<div dir="rtl">

| ویژگی | توضیح |
|:---:|---|
| 🌐 | **JavaScript Rendering** - رندر کامل صفحات React و SPA با Native Chrome |
| 🗺️ | **Sitemap Discovery** - کشف و پردازش Recursive از Sitemap Index |
| 🤖 | **robots.txt Support** - رعایت کامل قوانین robots.txt |
| 🔄 | **Resume Capability** - ادامه Crawl پس از Crash یا Restart |
| 💾 | **Persistent Queue** - صف URL در MongoDB با Atomic Claim |
| 📝 | **Clean Output** - خروجی TXT تمیز با حفظ Code Blockها |
| ⚡ | **Rate Limiting** - Exponential Backoff هوشمند با Jitter |
| 🛑 | **Graceful Shutdown** - توقف امن با Ctrl+C بدون از دست دادن داده |
| 📊 | **Session Management** - مدیریت Session با `--limit` هوشمند |
| 🎯 | **URL Deduplication** - جلوگیری از Crawl تکراری در سطح MongoDB |
| 🔒 | **Same-Domain Policy** - محدود کردن Crawl به دامنه هدف |
| 📈 | **Session Tracking** - پیگیری کامل آمار هر Session |

</div>

---

## 🏗️ معماری سیستم

<div dir="rtl">

معماری این سیستم بر اساس اصول **Clean Architecture** و **Separation of Concerns** طراحی شده است:

```
┌─────────────────────────────────────────────────────────┐
│                   CLI Layer (Typer)                     │
├─────────────────────────────────────────────────────────┤
│              Orchestration Layer                        │
│  ┌─────────────┬─────────────┬────────────────────┐    │
│  │   Session   │  Discovery  │    Crawl Service   │    │
│  │   Service   │   Service   │   (Orchestrator)   │    │
│  └─────────────┴─────────────┴────────────────────┘    │
├─────────────────────────────────────────────────────────┤
│                  Core Services Layer                    │
│  ┌────────────┬────────────┬────────────────────────┐  │
│  │  Crawler   │ Extraction │        Storage         │  │
│  │ (Crawl4AI) │  Pipeline  │  (Atomic File Write)   │  │
│  └────────────┴────────────┴────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│              Persistence Layer (MongoDB)                │
│  ┌──────────┬──────────┬──────────┬─────────────────┐  │
│  │   URLs   │ Sessions │ Sitemaps │    Counters     │  │
│  └──────────┴──────────┴──────────┴─────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 🔄 جریان داده (Data Flow)

```
URL Input → Seed Discovery → robots.txt + Sitemap
    ↓
URL Normalization + Validation + Domain Check
    ↓
MongoDB Queue (Persistent, Atomic Claim)
    ↓
Crawl4AI (Native Chrome, JS Rendering)
    ↓
Markdown Extraction + Code Block Preservation
    ↓
Content Cleaning (URL Removal, Noise Reduction)
    ↓
Atomic TXT Storage (data/1.txt, data/2.txt, ...)
    ↓
New URLs Discovery → Back to Queue
```

</div>

---

## 📋 پیش‌نیازها

<div dir="rtl">

قبل از شروع، مطمئن شوید این موارد روی سیستم شما نصب هستند:

| ابزار | نسخه | لینک دانلود |
|-------|------|-------------|
| **Python** | 3.11 یا بالاتر | [python.org](https://www.python.org/downloads/) |
| **MongoDB** | 6.0 یا بالاتر | [mongodb.com](https://www.mongodb.com/try/download/community) |
| **Google Chrome** | آخرین نسخه | [google.com/chrome](https://www.google.com/chrome/) |
| **Git** | 2.30+ | [git-scm.com](https://git-scm.com/) |
| **Docker** (اختیاری) | 20.10+ | [docker.com](https://www.docker.com/) |

### ⚠️ نکته مهم

این پروژه از **Google Chrome نصب شده روی سیستم** استفاده می‌کند (Native Chrome) و به Chromium دانلود شده توسط Playwright وابسته نیست. این کار باعث:

- ✅ سرعت بیشتر
- ✅ Fingerprint طبیعی‌تر
- ✅ جلوگیری از شناسایی به عنوان Bot
- ✅ مصرف کمتر Disk

می‌شود.

</div>

---

## 🛠️ نصب و راه‌اندازی

<div dir="rtl">

### مرحله ۱: Clone کردن پروژه

```bash
git clone https://github.com/YOUR-USERNAME/web-crawler.git
cd web-crawler
```

### مرحله ۲: ایجاد Virtual Environment

```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### مرحله ۳: نصب Dependencyها

```bash
# نصب پکیج‌های اصلی
pip install -r requirements.txt

# نصب پکیج‌های تست (اختیاری)
pip install -r requirements-test.txt
```

### مرحله ۴: راه‌اندازی MongoDB

#### روش ۱: استفاده از Docker (توصیه می‌شود)

```bash
# راه‌اندازی MongoDB با Docker
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -v mongodb_data:/data/db \
  mongo:latest

# بررسی وضعیت
docker ps | grep mongo
```

#### روش ۲: نصب MongoDB روی سیستم

برای نصب MongoDB، به [مستندات رسمی](https://www.mongodb.com/docs/manual/installation/) مراجعه کنید.

### مرحله ۵: تنظیم Environment Variables

فایل `.env` را از نمونه ایجاد کنید:

```bash
cp .env.example .env
```

سپس فایل `.env` را ویرایش کنید:

```bash
# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017
MONGO_DATABASE=web_dataset

# Storage Paths
OUTPUT_DIR=./data
LOG_DIR=./logs

# Crawl Settings
HEADLESS=true
CRAWL_DELAY=1.0
MAX_RETRIES=3
STALE_PROCESSING_TIMEOUT_MINUTES=10

# Browser Settings
BROWSER_TYPE=chromium
CHROME_CHANNEL=chrome
```

### مرحله ۶: تست نصب

```bash
# اجرای یک تست سریع
python -m app.main https://example.com --limit 3

# اگر همه چیز درست بود، این خروجی را می‌بینید:
# ============================================================
# WEB CRAWLER - Dataset Collection System
# ============================================================
```

</div>

---

## ⚡ شروع سریع

<div dir="rtl">

برای شروع سریع، این ۳ دستور کافی است:

```bash
# ۱. راه‌اندازی MongoDB (با Docker)
docker run -d --name mongodb -p 27017:27017 mongo:latest

# ۲. نصب Dependencyها
pip install -r requirements.txt

# ۳. اجرای Crawler
python -m app.main https://docs.python.org/3/tutorial/ --limit 10
```

بعد از اجرای موفق، فایل‌های TXT در دایرکتوری `data/` ایجاد می‌شوند.

</div>

---

## ⚙️ پارامترهای CLI

<div dir="rtl">

### 📋 لیست کامل پارامترها

```bash
python -m app.main [OPTIONS] URL
```

| پارامتر | نوع | پیش‌فرض | توضیح |
|---------|-----|---------|--------|
| `URL` | **Argument** | - | URL اصلی برای Crawl (اجباری) |
| `--limit`, `-l` | `int` | `None` (نامحدود) | حداکثر تعداد صفحات برای Crawl |
| `--headless` | `flag` | `True` | اجرای Browser در حالت Headless |
| `--show-browser` | `flag` | `False` | نمایش Browser (برای Debug) |
| `--delay`, `-d` | `float` | `1.0` | تأخیر بین Crawlها (ثانیه) |
| `--output`, `-o` | `Path` | `./data` | دایرکتوری خروجی فایل‌های TXT |
| `--verbose`, `-v` | `flag` | `False` | نمایش لاگ‌های دقیق‌تر |
| `--reset-failed` | `flag` | `False` | Reset کردن URLهای Failed به Pending |

### 🔍 توضیح کامل هر پارامتر

#### `URL` (Argument اجباری)

URL اصلی که Crawler از آن شروع می‌کند. همه URLهای کشف شده باید از همین دامنه باشند.

```bash
python -m app.main https://example.com
```

#### `--limit`, `-l`

حداکثر تعداد صفحاتی که Crawler پردازش می‌کند. این شامل صفحات **Crawl شده + Failed + Skipped** می‌شود.

```bash
# فقط ۵۰ صفحه Crawl کن
python -m app.main https://example.com --limit 50

# بدون محدودیت (تا زمانی که URL جدیدی باقی بماند)
python -m app.main https://example.com
```

#### `--headless`

حالت پیش‌فرض: Browser بدون نمایش UI اجرا می‌شود. مناسب برای سرورها و محیط‌های headless.

```bash
python -m app.main https://example.com --limit 10
```

#### `--show-browser`

Browser به صورت گرافیکی نمایش داده می‌شود. مناسب برای Debug و مشاهده فرآیند Crawl.

```bash
python -m app.main https://example.com --limit 5 --show-browser
```

#### `--delay`, `-d`

تأخیر بین Crawlها به ثانیه. برای جلوگیری از Rate Limiting سایت‌های حساس.

```bash
# ۳ ثانیه تأخیر بین هر Crawl
python -m app.main https://example.com --delay 3.0
```

#### `--output`, `-o`

دایرکتوری خروجی برای ذخیره فایل‌های TXT.

```bash
python -m app.main https://example.com --output ./my_dataset
```

#### `--verbose`, `-v`

نمایش لاگ‌های دقیق‌تر برای Debug.

```bash
python -m app.main https://example.com --verbose
```

#### `--reset-failed`

تمام URLهای Failed در دیتابیس را به Pending برمی‌گرداند. برای اجرای مجدد URLهایی که قبلاً fail شده‌اند.

```bash
python -m app.main https://example.com --limit 100 --reset-failed
```

### 🌐 Environment Variables

علاوه بر پارامترهای CLI، این متغیرها در فایل `.env` قابل تنظیم هستند:

| متغیر | پیش‌فرض | توضیح |
|--------|---------|--------|
| `MONGO_URI` | `mongodb://localhost:27017` | آدرس اتصال به MongoDB |
| `MONGO_DATABASE` | `web_dataset` | نام دیتابیس |
| `OUTPUT_DIR` | `./data` | دایرکتوری خروجی |
| `LOG_DIR` | `./logs` | دایرکتوری لاگ‌ها |
| `HEADLESS` | `true` | حالت Headless |
| `CRAWL_DELAY` | `1.0` | تأخیر پیش‌فرض بین Crawlها |
| `MAX_RETRIES` | `3` | حداکثر تعداد تلاش مجدد |
| `STALE_PROCESSING_TIMEOUT_MINUTES` | `10` | Timeout برای Recovery |
| `BROWSER_TYPE` | `chromium` | نوع Browser |
| `CHROME_CHANNEL` | `chrome` | کانال Chrome |

</div>

---

## 💡 مثال‌های کاربردی

<div dir="rtl">

### مثال ۱: Crawl ساده با محدودیت

```bash
python -m app.main https://docs.python.org/3/tutorial/ --limit 100
```

### مثال ۲: Crawl بدون محدودیت

```bash
python -m app.main https://docs.python.org/3/
```

> ⚠️ **توجه**: این دستور ممکن است برای مدت طولانی اجرا شود!

### مثال ۳: Crawl با تأخیر بیشتر (برای سایت‌های حساس)

```bash
python -m app.main https://example.com --limit 50 --delay 3.0
```

### مثال ۴: Crawl با Browser قابل مشاهده (برای Debug)

```bash
python -m app.main https://example.com --limit 10 --show-browser
```

### مثال ۵: Crawl با خروجی سفارشی

```bash
python -m app.main https://example.com --limit 100 --output ./my_dataset
```

### مثال ۶: Crawl با لاگ دقیق

```bash
python -m app.main https://example.com --limit 20 --verbose
```

### مثال ۷: ادامه Crawl قبلی با Reset URLهای Failed

```bash
python -m app.main https://example.com --limit 200 --reset-failed
```

### مثال ۸: ترکیب همه پارامترها

```bash
python -m app.main https://docs.python.org/3/ \
    --limit 200 \
    --delay 2.0 \
    --output ./python_docs_dataset \
    --verbose
```

### مثال ۹: سایت‌های پیشنهادی برای تست

```bash
# مستندات Python - عالی برای Dataset ML
python -m app.main https://docs.python.org/3/tutorial/ --limit 50

# مستندات FastAPI
python -m app.main https://fastapi.tiangolo.com/ --limit 50

# HackTricks - عالی برای Cybersecurity
python -m app.main https://book.hacktricks.xyz/ --limit 100

# مستندات Django
python -m app.main https://docs.djangoproject.com/en/5.0/ --limit 100

# DigitalOcean Tutorials
python -m app.main https://www.digitalocean.com/community/tutorials --limit 100
```

</div>

---

## 🎯 دستورات Makefile

<div dir="rtl">

برای سادگی در استفاده، یک `Makefile` حرفه‌ای ارائه شده است:

### 📦 نصب

| دستور | توضیح |
|-------|--------|
| `make install` | نصب Dependencyهای اصلی |
| `make install-test` | نصب Dependencyهای تست |
| `make install-all` | نصب همه Dependencyها |

### 🧪 تست

| دستور | توضیح |
|-------|--------|
| `make test` | اجرای همه تست‌ها |
| `make test-unit` | اجرای فقط Unit Testها |
| `make test-integration` | اجرای Integration Testها |
| `make test-coverage` | اجرای تست‌ها با Coverage Report |

### 🕷️ Crawl

| دستور | توضیح |
|-------|--------|
| `make crawl URL=... LIMIT=N` | Crawl با محدودیت |
| `make crawl-unlimited URL=...` | Crawl بدون محدودیت |
| `make crawl-headless URL=... LIMIT=N` | Crawl با Browser قابل مشاهده |
| `make crawl-verbose URL=... LIMIT=N` | Crawl با لاگ دقیق |
| `make crawl-example` | اجرای نمونه با example.com |
| `make crawl-reset URL=... LIMIT=N` | Crawl با Reset Failed URLs |

### 🗄️ MongoDB

| دستور | توضیح |
|-------|--------|
| `make mongo-start` | راه‌اندازی MongoDB با Docker |
| `make mongo-stop` | توقف MongoDB |
| `make mongo-shell` | باز کردن MongoDB Shell |

### 🧹 Cleanup

| دستور | توضیح |
|-------|--------|
| `make clean` | پاک کردن همه کش‌ها و داده‌ها |
| `make clean-data` | پاک کردن فقط data و logs |

### 📖 راهنما

| دستور | توضیح |
|-------|--------|
| `make help` | نمایش همه دستورات |

### مثال‌ها

```bash
# نصب همه چیز
make install-all

# راه‌اندازی MongoDB
make mongo-start

# Crawl سریع
make crawl-example

# Crawl سایت مشخص
make crawl URL=https://docs.python.org/3/ LIMIT=50

# اجرای تست‌ها
make test

# پاک کردن همه چیز
make clean
```

</div>

---

## 🗄️ ساختار دیتابیس

<div dir="rtl">

### 📊 Collections

#### ۱. `urls`

ذخیره تمام URLها و وضعیت Crawl آن‌ها.

```json
{
    "_id": "ObjectId",
    "url": "https://example.com/docs",
    "normalized_url": "https://example.com/docs",
    "domain": "example.com",
    "status": "completed",
    "sources": ["sitemap", "html"],
    "depth": 2,
    "parent_url": "https://example.com/",
    "status_code": 200,
    "content_type": "text/html",
    "canonical_url": "https://example.com/docs",
    "content_hash": "abc123...",
    "file_number": 25,
    "content_file": "25.txt",
    "retry_count": 0,
    "error_message": null,
    "created_at": "2026-08-12T10:00:00Z",
    "updated_at": "2026-08-12T10:05:00Z",
    "completed_at": "2026-08-12T10:05:00Z"
}
```

#### ۲. `crawl_sessions`

پیگیری هر Session Crawl.

```json
{
    "_id": "ObjectId",
    "session_id": "example.com_20260812_100000",
    "root_url": "https://example.com",
    "root_domain": "example.com",
    "limit": 100,
    "pages_crawled": 50,
    "pages_failed": 3,
    "pages_skipped": 5,
    "pages_processed": 58,
    "urls_discovered": 1500,
    "status": "completed",
    "started_at": "2026-08-12T10:00:00Z",
    "finished_at": "2026-08-12T10:30:00Z"
}
```

#### ۳. `sitemaps`

ذخیره Sitemapهای کشف شده برای جلوگیری از پردازش مجدد.

```json
{
    "_id": "ObjectId",
    "url": "https://example.com/sitemap.xml",
    "normalized_url": "https://example.com/sitemap.xml",
    "status": "processed",
    "sitemap_type": "urlset",
    "urls_found": 150,
    "sitemaps_found": 0,
    "source": "robots",
    "discovered_at": "2026-08-12T10:00:00Z",
    "processed_at": "2026-08-12T10:01:00Z"
}
```

#### ۴. `counters`

Counterهای Atomic برای تولید شماره فایل.

```json
{
    "_id": "file_counter",
    "seq": 125
}
```

### 📈 وضعیت‌های URL

| وضعیت | توضیح |
|-------|--------|
| `pending` | در صف انتظار برای Crawl |
| `processing` | در حال Crawl (اگر برنامه Crash کند، بعد از ۱۰ دقیقه به Pending برمی‌گردد) |
| `completed` | Crawl موفق و فایل ذخیره شد |
| `failed` | Crawl ناموفق (بعد از ۳ تلاش) |
| `skipped` | عمداً Crawl نشد (مثلاً محتوای خالی) |

</div>

---

## 📁 ساختار فایل‌ها

<div dir="rtl">

```
web-crawler/
│
├── app/                          # کد اصلی برنامه
│   ├── __init__.py
│   ├── main.py                   # Entry Point
│   ├── config.py                 # تنظیمات
│   │
│   ├── cli/                      # Command Line Interface
│   │   └── parser.py
│   │
│   ├── crawler/                  # Crawl4AI Integration
│   │   ├── browser.py
│   │   ├── crawl4ai_client.py
│   │   └── page_crawler.py
│   │
│   ├── discovery/                # URL Discovery
│   │   ├── http_client.py
│   │   ├── robots.py
│   │   ├── sitemap.py
│   │   └── link_extractor.py
│   │
│   ├── url/                      # URL Management
│   │   ├── normalizer.py
│   │   ├── validator.py
│   │   └── domain.py
│   │
│   ├── database/                 # MongoDB Layer
│   │   ├── mongo.py
│   │   ├── indexes.py
│   │   └── repositories/
│   │       ├── url_repository.py
│   │       ├── session_repository.py
│   │       ├── sitemap_repository.py
│   │       └── counter_repository.py
│   │
│   ├── extraction/               # Content Extraction
│   │   ├── markdown_cleaner.py
│   │   ├── content_extractor.py
│   │   └── content_filter.py
│   │
│   ├── storage/                  # File Storage
│   │   ├── text_storage.py
│   │   └── file_counter.py
│   │
│   ├── services/                 # Business Logic
│   │   ├── crawl_service.py
│   │   ├── discovery_service.py
│   │   ├── session_service.py
│   │   ├── recovery_service.py
│   │   └── shutdown_service.py
│   │
│   ├── models/                   # Pydantic Models
│   │   ├── url.py
│   │   ├── session.py
│   │   ├── crawl_result.py
│   │   └── sitemap.py
│   │
│   └── utils/                    # Utilities
│       ├── errors.py
│       ├── retry.py
│       ├── hashing.py
│       ├── logging.py
│       └── time.py
│
├── tests/                        # تست‌ها
│   ├── conftest.py
│   ├── test_url_normalizer.py
│   ├── test_url_validator.py
│   ├── test_domain_policy.py
│   ├── test_markdown_cleaner.py
│   ├── test_sitemap.py
│   ├── test_content_filter.py
│   └── test_integration.py
│
├── data/                         # خروجی فایل‌های TXT (auto-created)
├── logs/                         # فایل‌های لاگ (auto-created)
│
├── Makefile                      # دستورات ساده
├── requirements.txt              # Dependencyهای اصلی
├── requirements-test.txt         # Dependencyهای تست
├── pyproject.toml                # تنظیمات pytest
├── .env.example                  # نمونه Environment Variables
├── .gitignore
└── README.md                     # این فایل
```

</div>

---

## 🎓 نکات حرفه‌ای

<div dir="rtl">

### 💡 ۱. همیشه با `--limit` شروع کنید

قبل از اجرای Crawl بدون محدودیت، همیشه با `--limit` کم شروع کنید تا رفتار سایت را بسنجید:

```bash
# ابتدا ۵۰ صفحه تست کنید
python -m app.main https://example.com --limit 50

# بررسی کیفیت فایل‌ها
cat data/*.txt | wc -l
ls -lh data/

# اگر خوب بود، افزایش دهید
python -m app.main https://example.com --limit 500
```

### 💡 ۲. از `--delay` برای سایت‌های حساس استفاده کنید

برای سایت‌هایی که Rate Limiting دارند:

```bash
# ۳ ثانیه تأخیر بین هر Crawl
python -m app.main https://example.com --delay 3.0
```

### 💡 ۳. با `--show-browser` Debug کنید

اگر Crawl با مشکل مواجه شد، Browser را نمایش دهید:

```bash
python -m app.main https://example.com --limit 5 --show-browser
```

### 💡 ۴. Resume کردن Crawl

اگر برنامه متوقف شد، دوباره اجرا کنید. سیستم از جایی که متوقف شده ادامه می‌دهد:

```bash
# اجرای اولیه
python -m app.main https://example.com --limit 500

# اگر متوقف شد (Ctrl+C یا Crash)
# فقط دوباره اجرا کنید - ادامه می‌دهد
python -m app.main https://example.com --limit 500
```

### 💡 ۵. Reset کردن URLهای Failed

اگر سایت موقتاً مشکل داشت و حالا درست است:

```bash
python -m app.main https://example.com --limit 200 --reset-failed
```

### 💡 ۶. بررسی آمار Session

در پایان هر Crawl، آمار کامل نمایش داده می‌شود:

```
============================================================
CRAWL COMPLETED
============================================================
Root URL       : https://example.com
Session ID     : example.com_20260812_100000
Limit          : 100
Pages Crawled  : 95
Pages Failed   : 3
Pages Skipped  : 2
URLs Discovered: 1500
Files Created  : 95
Total Size     : 15.5 MB
============================================================
```

### 💡 ۷. انتخاب سایت‌های مناسب

برای بهترین نتیجه، سایت‌هایی را انتخاب کنید که:

- ✅ HTML ساده دارند (نه SPA پیچیده)
- ✅ محتوای آموزشی دارند
- ✅ Anti-bot قوی ندارند
- ✅ API رسمی یا Dataset عمومی ندارند

### 💡 ۸. استفاده از منابع رسمی

برای منابع بزرگ، از روش‌های رسمی استفاده کنید:

| منبع | بهترین روش |
|------|------------|
| **Wikipedia** | `wikiextractor` + Wikipedia Dumps |
| **Stack Overflow** | Stack Exchange Data Dump |
| **GitHub Code** | GitHub Public Dataset |
| **Exploit-DB** | `git clone https://gitlab.com/exploit-database/exploitdb.git` |
| **CVE/NVD** | NVD JSON Feeds |

</div>

---

## 🐛 عیب‌یابی

<div dir="rtl">

### ❌ Chrome پیدا نمی‌شود

**ارور:**

```
BrowserType.launch_persistent_context: Executable doesn't exist
```

**راه‌حل:**

```bash
# بررسی نصب Chrome
which google-chrome

# اگر نصب نیست
sudo apt install google-chrome-stable  # Ubuntu/Debian
```

### ❌ MongoDB اتصال برقرار نمی‌شود

**ارور:**

```
Connection refused: mongodb://localhost:27017
```

**راه‌حل:**

```bash
# بررسی وضعیت MongoDB
docker ps | grep mongo

# اگر اجرا نیست
make mongo-start

# یا با systemctl
sudo systemctl start mongod
```

### ❌ `ERR_TOO_MANY_REDIRECTS`

**ارور:**

```
Page.goto: net::ERR_TOO_MANY_REDIRECTS
```

**علت:** سایت به URLهایی که محتوای paywalled دارند، redirect loop می‌کند.

**راه‌حل:** طبیعی است. این URLها به درستی `failed` mark می‌شوند.

### ❌ `Empty content`

**ارور:**

```
[SKIPPED] https://example.com/page: Empty content
```

**علت:** صفحه محتوای مفیدی ندارد (مثلاً صفحه login یا paywall).

**راه‌حل:** طبیعی است. سیستم این صفحات را skip می‌کند.

### ❌ تست‌ها Fail می‌شوند

```bash
# نصب Dependencyهای تست
make install-test

# اجرای تست با جزئیات بیشتر
python -m pytest tests/ -v --tb=long
```

### ❌ Browser.close error در پایان

**ارور:**

```
[ERROR] Crawl failed: Browser.close: Connection closed while reading from the driver
```

**علت:** هنگام Ctrl+C، connection بسته شده است.

**راه‌حل:** طبیعی است. داده‌ها از دست نمی‌روند. فقط یک پیام هشدار است.

### ❌ `--limit` کار نمی‌کند

**علت:** ممکن است از نسخه قدیمی استفاده می‌کنید.

**راه‌حل:**

```bash
# اطمینان از آخرین نسخه
git pull origin main
pip install -r requirements.txt --upgrade
```

</div>

---

## 🌐 سایت‌های مناسب برای Crawl

<div dir="rtl">

### ✅ سایت‌های عالی (تست شده)

| سایت | توضیح | دستور نمونه |
|------|--------|-------------|
| **Python Docs** | مستندات رسمی Python | `python -m app.main https://docs.python.org/3/tutorial/ --limit 100` |
| **FastAPI Docs** | مستندات FastAPI | `python -m app.main https://fastapi.tiangolo.com/ --limit 50` |
| **Django Docs** | مستندات Django | `python -m app.main https://docs.djangoproject.com/en/5.0/ --limit 100` |
| **HackTricks** | Cybersecurity Knowledge | `python -m app.main https://book.hacktricks.xyz/ --limit 100` |
| **Real Python** | آموزش‌های Python | `python -m app.main https://realpython.com --limit 50` |
| **DigitalOcean** | آموزش‌های Linux | `python -m app.main https://www.digitalocean.com/community/tutorials --limit 100` |

### ⚠️ سایت‌های با تلاش

| سایت | چالش | توصیه |
|------|------|-------|
| **Stack Overflow** | Rate Limiting سخت | از Stack Exchange Data Dump استفاده کنید |
| **GitHub** | SPA + Anti-bot | از GitHub Public Dataset استفاده کنید |
| **Medium** | Anti-bot قوی | از Medium API استفاده کنید |

### ❌ سایت‌های نامناسب

| سایت | دلیل | جایگزین |
|------|------|---------|
| **Wikipedia** | Dump رسمی + API قوی | `wikiextractor` |
| **Exploit-DB** | Cloudflare + Git رسمی | `git clone https://gitlab.com/exploit-database/exploitdb.git` |
| **Google/Facebook/Twitter** | API رسمی + ToS | استفاده از API رسمی |
| **Amazon/E-commerce** | Anti-bot قوی + ToS | اصلاً Crawl نکنید |

### 📊 راهنمای تصمیم

```
آیا سایت API رسمی دارد؟
  ├─ بله → از API استفاده کنید
  └─ خیر → آیا Dataset عمومی دارد؟
             ├─ بله → از Dataset استفاده کنید
             └─ خیر → آیا محتوای آموزشی دارد؟
                        ├─ بله → ✅ استفاده از Crawler
                        └─ خیر → ❌ Crawl نکنید
```

</div>

---

## ❓ سوالات متداول

<div dir="rtl">

### ❓ آیا بدون `--limit` برنامه نامحدود کار می‌کند؟

**پاسخ:** بله، تا زمانی که URL `pending` در صف وجود دارد. اما همیشه با `--limit` کم شروع کنید.

### ❓ اگر برنامه Crash کند چه می‌شود؟

**پاسخ:** سیستم Resume دارد! فقط دوباره همان دستور را اجرا کنید. URLهای `processing` بعد از ۱۰ دقیقه به `pending` برمی‌گردند.

### ❓ چرا برخی URLها fail می‌شوند؟

**پاسخ:** طبیعی است. دلایل:
- سایت Rate Limit دارد
- URL paywalled است
- سایت Anti-bot دارد
- محتوای مفید ندارد

### ❓ آیا می‌توانم همزمان چند Crawl اجرا کنم؟

**پاسخ:** بله! چون MongoDB Atomic Claim دارد. اما برای سایت یکسان توصیه نمی‌شود (Rate Limit).

### ❓ چطور بفهمم Crawl تمام شده؟

**پاسخ:** وقتی این پیام را دیدید:

```
[CRAWL] No more pending URLs. Crawl complete.
============================================================
CRAWL COMPLETED
============================================================
```

### ❓ آیا می‌توانم سایت‌های غیر انگلیسی (فارسی، عربی و...) را Crawl کنم؟

**پاسخ:** بله! سیستم کاملاً Unicode-aware است و محتوای هر زبانی را به درستی ذخیره می‌کند.

### ❓ فایل‌های خروجی چه فرمتی دارند؟

**پاسخ:** فایل‌های TXT در دایرکتوری `data/` با نام‌های `1.txt`, `2.txt`, `3.txt` و... بدون Metadata اضافی. محتوای Markdown تمیز با حفظ Code Blockها.

### ❓ آیا می‌توانم خروجی را به فرمت دیگری (JSON, JSONL) تبدیل کنم؟

**پاسخ:** در نسخه فعلی فقط TXT پشتیبانی می‌شود. اما معماری به گونه‌ای طراحی شده که اضافه کردن فرمت‌های دیگر آسان باشد.

### ❓ چقدر فضا نیاز دارم؟

**پاسخ:**
- خود پروژه: ~۱۰۰ MB
- MongoDB: ~۱ MB برای هر ۱۰۰۰ URL
- داده‌های خروجی: ~۱ MB برای هر ۵۰ صفحه (بسته به محتوا)

### ❓ آیا این پروژه قانونی است؟

**پاسخ:**
- ✅ Crawl کردن محتوای عمومی قانونی است
- ⚠️ همیشه `robots.txt` را بررسی کنید
- ⚠️ از Rate Limiting استفاده کنید
- ❌ محتوای paywalled یا private را Crawl نکنید
- ❌ به سرورها آسیب نزنید (تأخیر مناسب داشته باشید)

</div>

---

## 🤝 مشارکت

<div dir="rtl">

مشارکت‌ها bienvenida هستند! برای تغییرات مهم، ابتدا Issue باز کنید.

### مراحل مشارکت:

```bash
# ۱. Fork کنید
# ۲. Clone کنید
git clone https://github.com/YOUR-USERNAME/web-crawler.git
cd web-crawler

# ۳. Branch جدید بسازید
git checkout -b feature/amazing-feature

# ۴. تغییرات را commit کنید
git commit -m "Add amazing feature"

# ۵. Push کنید
git push origin feature/amazing-feature

# ۶. Pull Request باز کنید
```

### 📋 Guidelines

- ✅ قبل از تغییرات بزرگ، Issue باز کنید
- ✅ تست‌ها را اجرا کنید (`make test`)
- ✅ Type Hintها را رعایت کنید
- ✅ Docstring بنویسید
- ✅ Clean Code اصول را رعایت کنید

</div>

---

## 📄 مجوز

<div dir="rtl">

این پروژه تحت مجوز **MIT License** منتشر شده است - برای جزئیات فایل [LICENSE](LICENSE) را مشاهده کنید.

```
MIT License

Copyright (c) 2026 Web Crawler

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

</div>

---

<div dir="rtl" align="center">

### 🌟 اگر این پروژه برایتان مفید بود، ستاره بدهید!

**ساخته شده با ❤️ برای جمع‌آوری Datasetهای فنی**

[⬆ بازگشت به بالا](#-web-crawler)

</div>
```

این نسخه از README.md کاملاً تمیز و آماده برای GitHub است. تمام escape characters حذف شده‌اند و تمام Markdown syntax‌ها به صورت صحیح نوشته شده‌اند. کافی است این محتوا را مستقیماً در فایل `README.md` پروژه خود کپی کنید.

ویژگی‌های این نسخه:
- ✅ Badges به درستی render می‌شوند
- ✅ جداول با فرمت استاندارد GitHub
- ✅ Code blocks با syntax highlighting مناسب
- ✅ لینک‌های داخلی فهرست مطالب به درستی کار می‌کنند
- ✅ پشتیبانی کامل از RTL برای متن فارسی
- ✅ ساختار درختی فایل‌ها به صورت خوانا
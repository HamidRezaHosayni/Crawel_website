<div align="center">

# 🕷️ Web Crawler
### Professional Dataset Collection System

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Crawl4AI](https://img.shields.io/badge/Crawl4AI-0.9.2-green.svg)](https://github.com/unclecode/crawl4ai)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.0+-green.svg)](https://www.mongodb.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Production Ready](https://img.shields.io/badge/status-production--ready-brightgreen.svg)]()

**سیستم حرفه‌ای Crawl وب برای جمع‌آوری Dataset**

[🚀 شروع سریع](#-شروع-سریع) • [📖 نصب](#-نصب-و-راهاندازی) • [⚙️ راهنما](#-پارامترهای-cli) • [💡 مثال‌ها](#-مثالهای-کاربردی) • [🐛 عیب‌یابی](#-عیبیابی)

---

</div>

## 📋 فهرست مطالب

- [✨ ویژگی‌ها](#-ویژگیها)
- [🏗️ معماری](#️-معماری-سیستم)
- [📋 پیش‌نیازها](#-پیشنیازها)
- [🛠️ نصب](#️-نصب-و-راهاندازی)
- [⚡ شروع سریع](#-شروع-سریع)
- [⚙️ پارامترهای CLI](#️-پارامترهای-cli)
- [💡 مثال‌ها](#-مثالهای-کاربردی)
- [🎯 دستورات Makefile](#-دستورات-makefile)
- [🗄️ دیتابیس](#️-ساختار-دیتابیس)
- [📁 ساختار فایل‌ها](#-ساختار-فایلها)
- [🎓 نکات حرفه‌ای](#-نکات-حرفهای)
- [🐛 عیب‌یابی](#-عیبیابی)
- [🌐 سایت‌های مناسب](#-سایتهای-مناسب-برای-crawl)
- [❓ سوالات متداول](#-سوالات-متداول)
- [🤝 مشارکت](#-مشارکت)
- [📄 مجوز](#-مجوز)

---

## ✨ ویژگی‌ها

<div align="center">

| ویژگی | توضیح |
|:---:|---|
| 🌐 | **JavaScript Rendering** - رندر کامل صفحات React و SPA با Native Chrome |
| 🗺️ | **Sitemap Discovery** - کشف و پردازش Recursive از Sitemap Index |
| 🤖 | **robots.txt Support** - رعایت کامل قوانین robots.txt |
| 🔄 | **Resume Capability** - ادامه Crawl پس از Crash یا Restart |
| 💾 | **Persistent Queue** - صف URL در MongoDB با Atomic Claim |
| 📝 | **Clean Output** - خروجی TXT تمیز با حفظ Code Blockها |
| ⚡ | **Rate Limiting** - Exponential Backoff هوشمند |
| 🛑 | **Graceful Shutdown** - توقف امن با Ctrl+C |
| 📊 | **Session Management** - مدیریت Session با `--limit` |
| 🎯 | **URL Deduplication** - جلوگیری از Crawl تکراری |

</div>

---

## 🏗️ معماری سیستم

<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web Crawler - Professional Dataset Collection System</title>
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Vazirmatn Font for Persian -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    
    <!-- Prism.js for Syntax Highlighting -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-json.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-yaml.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-makefile.min.js"></script>
    
    <style>
        * {
            font-family: 'Vazirmatn', sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #e2e8f0;
            scroll-behavior: smooth;
        }
        
        code, pre, .mono {
            font-family: 'JetBrains Mono', monospace !important;
            direction: ltr;
            text-align: left;
        }
        
        pre {
            direction: ltr;
            text-align: left;
        }
        
        .gradient-text {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .glass-card {
            background: rgba(30, 41, 59, 0.6);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(148, 163, 184, 0.1);
        }
        
        .hover-card {
            transition: all 0.3s ease;
        }
        
        .hover-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(102, 126, 234, 0.2);
            border-color: rgba(102, 126, 234, 0.3);
        }
        
        .nav-link {
            transition: all 0.2s ease;
        }
        
        .nav-link:hover {
            color: #a78bfa;
            padding-right: 0.5rem;
        }
        
        .code-block {
            position: relative;
            border-radius: 0.5rem;
            overflow: hidden;
        }
        
        .code-block::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2rem;
            background: #1a1a1a;
            z-index: 1;
        }
        
        .copy-btn {
            position: absolute;
            top: 0.5rem;
            right: 0.5rem;
            z-index: 10;
            background: rgba(102, 126, 234, 0.2);
            border: 1px solid rgba(102, 126, 234, 0.4);
            padding: 0.25rem 0.75rem;
            border-radius: 0.375rem;
            font-size: 0.75rem;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .copy-btn:hover {
            background: rgba(102, 126, 234, 0.4);
        }
        
        .feature-icon {
            width: 3rem;
            height: 3rem;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 0.75rem;
            font-size: 1.5rem;
        }
        
        .badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        
        .badge-success {
            background: rgba(16, 185, 129, 0.2);
            color: #6ee7b7;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }
        
        .badge-warning {
            background: rgba(251, 191, 36, 0.2);
            color: #fcd34d;
            border: 1px solid rgba(251, 191, 36, 0.3);
        }
        
        .badge-info {
            background: rgba(59, 130, 246, 0.2);
            color: #93c5fd;
            border: 1px solid rgba(59, 130, 246, 0.3);
        }
        
        .badge-danger {
            background: rgba(239, 68, 68, 0.2);
            color: #fca5a5;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }
        
        table {
            border-collapse: collapse;
            width: 100%;
        }
        
        th {
            background: rgba(102, 126, 234, 0.2);
            color: #c7d2fe;
            font-weight: 600;
        }
        
        th, td {
            padding: 0.75rem 1rem;
            text-align: right;
            border-bottom: 1px solid rgba(148, 163, 184, 0.1);
        }
        
        tr:hover td {
            background: rgba(148, 163, 184, 0.05);
        }
        
        .toc-link {
            display: block;
            padding: 0.5rem 1rem;
            color: #94a3b8;
            border-right: 2px solid transparent;
            transition: all 0.2s;
        }
        
        .toc-link:hover {
            color: #a78bfa;
            border-right-color: #a78bfa;
            background: rgba(167, 139, 250, 0.1);
        }
        
        .hero-glow {
            position: absolute;
            width: 500px;
            height: 500px;
            background: radial-gradient(circle, rgba(102, 126, 234, 0.15) 0%, transparent 70%);
            border-radius: 50%;
            pointer-events: none;
        }
        
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #1e293b;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #475569;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #667eea;
        }
        
        @media (max-width: 1024px) {
            .sidebar {
                display: none;
            }
        }
        
        .terminal {
            background: #0f0f0f;
            border: 1px solid #333;
            border-radius: 0.5rem;
            overflow: hidden;
        }
        
        .terminal-header {
            background: #1a1a1a;
            padding: 0.5rem 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            border-bottom: 1px solid #333;
        }
        
        .terminal-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }
        
        .dot-red { background: #ff5f56; }
        .dot-yellow { background: #ffbd2e; }
        .dot-green { background: #27c93f; }
        
        .terminal-body {
            padding: 1rem;
            direction: ltr;
            text-align: left;
        }
        
        .prompt {
            color: #10b981;
        }
        
        .command {
            color: #e2e8f0;
        }
    </style>
</head>
<body>

<!-- Hero Section -->
<header class="relative overflow-hidden">
    <div class="hero-glow" style="top: -200px; right: -200px;"></div>
    <div class="hero-glow" style="bottom: -200px; left: -200px; background: radial-gradient(circle, rgba(118, 75, 162, 0.15) 0%, transparent 70%);"></div>
    
    <div class="container mx-auto px-6 py-20 relative z-10">
        <div class="text-center">
            <div class="inline-block mb-6">
                <span class="badge badge-info">v1.0.0</span>
                <span class="badge badge-success ml-2">Production Ready</span>
            </div>
            
            <h1 class="text-6xl md:text-7xl font-extrabold mb-6">
                <span class="gradient-text">Web Crawler</span>
            </h1>
            
            <p class="text-xl md:text-2xl text-slate-300 mb-4 max-w-3xl mx-auto">
                سیستم حرفه‌ای Crawl وب برای جمع‌آوری Dataset
            </p>
            
            <p class="text-slate-400 mb-8 max-w-2xl mx-auto">
                ابزار پیشرفته برای جمع‌آوری داده‌های متنی، مستندات فنی، کدهای برنامه‌نویسی و دستورات از وب‌سایت‌ها با پشتیبانی از JavaScript، MongoDB و ذخیره‌سازی Atomic
            </p>
            
            <div class="flex flex-wrap gap-4 justify-center mb-12">
                <a href="#quick-start" class="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 px-8 py-3 rounded-lg font-semibold transition-all transform hover:scale-105 shadow-lg shadow-purple-500/20">
                    🚀 شروع سریع
                </a>
                <a href="#installation" class="glass-card hover-card px-8 py-3 rounded-lg font-semibold">
                    📖 نصب و راه‌اندازی
                </a>
                <a href="#cli-options" class="glass-card hover-card px-8 py-3 rounded-lg font-semibold">
                    ⚙️ راهنمای CLI
                </a>
            </div>
            
            <div class="flex flex-wrap gap-6 justify-center text-sm text-slate-400">
                <div class="flex items-center gap-2">
                    <span class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                    <span>Python 3.11+</span>
                </div>
                <div class="flex items-center gap-2">
                    <span class="w-2 h-2 bg-blue-500 rounded-full"></span>
                    <span>Crawl4AI 0.9.2</span>
                </div>
                <div class="flex items-center gap-2">
                    <span class="w-2 h-2 bg-green-600 rounded-full"></span>
                    <span>MongoDB</span>
                </div>
                <div class="flex items-center gap-2">
                    <span class="w-2 h-2 bg-purple-500 rounded-full"></span>
                    <span>Native Chrome</span>
                </div>
            </div>
        </div>
    </div>
</header>

<!-- Main Layout -->
<div class="container mx-auto px-6 flex gap-8 relative">
    
    <!-- Sidebar TOC -->
    <aside class="sidebar w-64 sticky top-8 self-start hidden lg:block">
        <div class="glass-card rounded-xl p-4">
            <h3 class="text-lg font-bold mb-4 text-slate-200">📑 فهرست مطالب</h3>
            <nav class="space-y-1">
                <a href="#features" class="toc-link">✨ ویژگی‌ها</a>
                <a href="#architecture" class="toc-link">🏗️ معماری</a>
                <a href="#requirements" class="toc-link">📋 پیش‌نیازها</a>
                <a href="#installation" class="toc-link">🛠️ نصب</a>
                <a href="#quick-start" class="toc-link">⚡ شروع سریع</a>
                <a href="#cli-options" class="toc-link">⚙️ پارامترهای CLI</a>
                <a href="#examples" class="toc-link">💡 مثال‌ها</a>
                <a href="#makefile" class="toc-link">🎯 دستورات Makefile</a>
                <a href="#database" class="toc-link">🗄️ دیتابیس</a>
                <a href="#file-structure" class="toc-link">📁 ساختار فایل‌ها</a>
                <a href="#best-practices" class="toc-link">🎓 نکات حرفه‌ای</a>
                <a href="#troubleshooting" class="toc-link">🐛 عیب‌یابی</a>
                <a href="#websites" class="toc-link">🌐 سایت‌های مناسب</a>
                <a href="#faq" class="toc-link">❓ سوالات متداول</a>
                <a href="#license" class="toc-link">📄 مجوز</a>
            </nav>
        </div>
    </aside>
    
    <!-- Main Content -->
    <main class="flex-1 max-w-5xl pb-20">
        
        <!-- Features Section -->
        <section id="features" class="mb-16 scroll-mt-8">
            <h2 class="text-4xl font-bold mb-8 gradient-text">✨ ویژگی‌های کلیدی</h2>
            
            <div class="grid md:grid-cols-2 gap-6">
                <div class="glass-card hover-card rounded-xl p-6">
                    <div class="feature-icon bg-gradient-to-br from-blue-500 to-cyan-500 mb-4">🌐</div>
                    <h3 class="text-xl font-bold mb-2">JavaScript Rendering</h3>
                    <p class="text-slate-400">رندر کامل صفحات React و SPA با Native Chrome بدون نیاز به Chromium دانلود شده</p>
                </div>
                
                <div class="glass-card hover-card rounded-xl p-6">
                    <div class="feature-icon bg-gradient-to-br from-green-500 to-emerald-500 mb-4">🗺️</div>
                    <h3 class="text-xl font-bold mb-2">Sitemap Discovery</h3>
                    <p class="text-slate-400">کشف و پردازش Recursive از Sitemap Index با پشتیبانی از robots.txt</p>
                </div>
                
                <div class="glass-card hover-card rounded-xl p-6">
                    <div class="feature-icon bg-gradient-to-br from-purple-500 to-pink-500 mb-4">🔄</div>
                    <h3 class="text-xl font-bold mb-2">Resume Capability</h3>
                    <p class="text-slate-400">ادامه Crawl پس از Crash یا Restart با State مدیریت شده در MongoDB</p>
                </div>
                
                <div class="glass-card hover-card rounded-xl p-6">
                    <div class="feature-icon bg-gradient-to-br from-yellow-500 to-orange-500 mb-4">💾</div>
                    <h3 class="text-xl font-bold mb-2">Persistent Queue</h3>
                    <p class="text-slate-400">صف URL در MongoDB با Atomic Claim و Deduplication</p>
                </div>
                
                <div class="glass-card hover-card rounded-xl p-6">
                    <div class="feature-icon bg-gradient-to-br from-red-500 to-pink-500 mb-4">📝</div>
                    <h3 class="text-xl font-bold mb-2">Clean Output</h3>
                    <p class="text-slate-400">خروجی TXT تمیز بدون URL، با حفظ کامل Code Blockها</p>
                </div>
                
                <div class="glass-card hover-card rounded-xl p-6">
                    <div class="feature-icon bg-gradient-to-br from-indigo-500 to-purple-500 mb-4">⚡</div>
                    <h3 class="text-xl font-bold mb-2">Rate Limiting</h3>
                    <p class="text-slate-400">Exponential Backoff هوشمند برای جلوگیری از Rate Limit</p>
                </div>
                
                <div class="glass-card hover-card rounded-xl p-6">
                    <div class="feature-icon bg-gradient-to-br from-teal-500 to-cyan-500 mb-4">🛑</div>
                    <h3 class="text-xl font-bold mb-2">Graceful Shutdown</h3>
                    <p class="text-slate-400">توقف امن با Ctrl+C و اتمام عملیات جاری</p>
                </div>
                
                <div class="glass-card hover-card rounded-xl p-6">
                    <div class="feature-icon bg-gradient-to-br from-fuchsia-500 to-purple-500 mb-4">📊</div>
                    <h3 class="text-xl font-bold mb-2">Session Management</h3>
                    <p class="text-slate-400">مدیریت Session با --limit برای کنترل دقیق تعداد صفحات</p>
                </div>
            </div>
        </section>
        
        <!-- Architecture Section -->
        <section id="architecture" class="mb-16 scroll-mt-8">
            <h2 class="text-4xl font-bold mb-8 gradient-text">🏗️ معماری سیستم</h2>
            
            <div class="glass-card rounded-xl p-8 mb-6">
                <h3 class="text-2xl font-bold mb-4">جریان داده (Data Flow)</h3>
                
                <div class="terminal">
                    <div class="terminal-header">
                        <div class="terminal-dot dot-red"></div>
                        <div class="terminal-dot dot-yellow"></div>
                        <div class="terminal-dot dot-green"></div>
                        <span class="text-slate-400 text-sm ml-4">system-flow.txt</span>
                    </div>
                    <div class="terminal-body mono">
<pre class="text-slate-300 text-sm leading-relaxed">
┌─────────────────────────────────────────────────────────────────┐
│                      USER / CLI Layer                            │
│  python -m app.main https://example.com --limit 100             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Orchestration Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Session    │  │  Discovery   │  │   Recovery   │          │
│  │   Service    │  │   Service    │  │   Service    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Processing Layer                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Crawl4AI   │  │   Markdown   │  │   Content    │          │
│  │  + Chrome    │  │   Cleaner    │  │   Filter     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Persistence Layer                             │
│  ┌───────────────────┐  ┌───────────────────────────┐          │
│  │     MongoDB       │  │    TXT Files (Atomic)     │          │
│  │  - urls           │  │    data/1.txt             │          │
│  │  - sessions       │  │    data/2.txt             │          │
│  │  - sitemaps       │  │    data/3.txt             │          │
│  │  - counters       │  │    ...                    │          │
│  └───────────────────┘  └───────────────────────────┘          │
└─────────────────────────────────────────────────────────────────┘
</pre>
                    </div>
                </div>
            </div>
            
            <div class="grid md:grid-cols-3 gap-4">
                <div class="glass-card rounded-lg p-4">
                    <h4 class="font-bold text-blue-400 mb-2">🔵 Discovery Layer</h4>
                    <ul class="text-sm text-slate-400 space-y-1">
                        <li>• robots.txt Parser</li>
                        <li>• Sitemap Index (Recursive)</li>
                        <li>• HTML Link Extractor</li>
                    </ul>
                </div>
                
                <div class="glass-card rounded-lg p-4">
                    <h4 class="font-bold text-green-400 mb-2">🟢 Crawling Layer</h4>
                    <ul class="text-sm text-slate-400 space-y-1">
                        <li>• Crawl4AI + Native Chrome</li>
                        <li>• JavaScript Rendering</li>
                        <li>• URL Deduplication</li>
                    </ul>
                </div>
                
                <div class="glass-card rounded-lg p-4">
                    <h4 class="font-bold text-purple-400 mb-2">🟣 Storage Layer</h4>
                    <ul class="text-sm text-slate-400 space-y-1">
                        <li>• Atomic File Write</li>
                        <li>• MongoDB Persistence</li>
                        <li>• Resume Support</li>
                    </ul>
                </div>
            </div>
        </section>
        
        <!-- Requirements Section -->
        <section id="requirements" class="mb-16 scroll-mt-8">
            <h2 class="text-4xl font-bold mb-8 gradient-text">📋 پیش‌نیازها</h2>
            
            <div class="grid md:grid-cols-2 gap-6">
                <div class="glass-card rounded-xl p-6">
                    <h3 class="text-xl font-bold mb-4 flex items-center gap-2">
                        <span class="text-2xl">🐍</span> Python 3.11+
                    </h3>
                    <p class="text-slate-400 mb-3">نسخه ۳.۱۱ یا بالاتر پایتون</p>
                    <div class="terminal">
                        <div class="terminal-body">
                            <span class="prompt">$</span> <span class="command">python3 --version</span>
                        </div>
                    </div>
                </div>
                
                <div class="glass-card rounded-xl p-6">
                    <h3 class="text-xl font-bold mb-4 flex items-center gap-2">
                        <span class="text-2xl">🍃</span> MongoDB
                    </h3>
                    <p class="text-slate-400 mb-3">دیتابیس برای Persistent Queue</p>
                    <div class="terminal">
                        <div class="terminal-body">
                            <span class="prompt">$</span> <span class="command">mongod --version</span>
                        </div>
                    </div>
                </div>
                
                <div class="glass-card rounded-xl p-6">
                    <h3 class="text-xl font-bold mb-4 flex items-center gap-2">
                        <span class="text-2xl">🌐</span> Google Chrome
                    </h3>
                    <p class="text-slate-400 mb-3">برای رندر JavaScript (Native)</p>
                    <div class="terminal">
                        <div class="terminal-body">
                            <span class="prompt">$</span> <span class="command">google-chrome --version</span>
                        </div>
                    </div>
                </div>
                
                <div class="glass-card rounded-xl p-6">
                    <h3 class="text-xl font-bold mb-4 flex items-center gap-2">
                        <span class="text-2xl">🐳</span> Docker (اختیاری)
                    </h3>
                    <p class="text-slate-400 mb-3">برای اجرای آسان MongoDB</p>
                    <div class="terminal">
                        <div class="terminal-body">
                            <span class="prompt">$</span> <span class="command">docker --version</span>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- Installation Section -->
        <section id="installation" class="mb-16 scroll-mt-8">
            <h2 class="text-4xl font-bold mb-8 gradient-text">🛠️ نصب و راه‌اندازی</h2>
            
            <div class="space-y-6">
                <!-- Step 1 -->
                <div class="glass-card rounded-xl p-6">
                    <div class="flex items-start gap-4">
                        <div class="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center font-bold text-white">1</div>
                        <div class="flex-1">
                            <h3 class="text-xl font-bold mb-3">کلون کردن پروژه</h3>
                            <div class="code-block">
                                <button class="copy-btn" onclick="copyCode(this)">📋 کپی</button>
                                <pre><code class="language-bash">git clone https://github.com/yourusername/web-crawler.git
cd web-crawler</code></pre>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Step 2 -->
                <div class="glass-card rounded-xl p-6">
                    <div class="flex items-start gap-4">
                        <div class="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center font-bold text-white">2</div>
                        <div class="flex-1">
                            <h3 class="text-xl font-bold mb-3">ایجاد Virtual Environment</h3>
                            <div class="code-block">
                                <button class="copy-btn" onclick="copyCode(this)">📋 کپی</button>
                                <pre><code class="language-bash"># ایجاد محیط مجازی
python3 -m venv venv

# فعال‌سازی در Linux/macOS
source venv/bin/activate

# فعال‌سازی در Windows
venv\Scripts\activate</code></pre>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Step 3 -->
                <div class="glass-card rounded-xl p-6">
                    <div class="flex items-start gap-4">
                        <div class="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center font-bold text-white">3</div>
                        <div class="flex-1">
                            <h3 class="text-xl font-bold mb-3">نصب Dependency ها</h3>
                            <div class="code-block">
                                <button class="copy-btn" onclick="copyCode(this)">📋 کپی</button>
                                <pre><code class="language-bash"># نصب پکیج‌های اصلی
pip install -r requirements.txt

# نصب پکیج‌های تست (اختیاری)
pip install -r requirements-test.txt</code></pre>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Step 4 -->
                <div class="glass-card rounded-xl p-6">
                    <div class="flex items-start gap-4">
                        <div class="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center font-bold text-white">4</div>
                        <div class="flex-1">
                            <h3 class="text-xl font-bold mb-3">تنظیم Environment Variables</h3>
                            <div class="code-block">
                                <button class="copy-btn" onclick="copyCode(this)">📋 کپی</button>
                                <pre><code class="language-bash"># کپی فایل نمونه
cp .env.example .env

# ویرایش فایل
nano .env</code></pre>
                            </div>
                            
                            <h4 class="font-bold mt-4 mb-2">محتوای فایل <code class="bg-slate-700 px-2 py-1 rounded">.env</code>:</h4>
                            <div class="code-block">
                                <button class="copy-btn" onclick="copyCode(this)">📋 کپی</button>
                                <pre><code class="language-bash"># MongoDB Configuration
MONGO_URI=mongodb://localhost:27017
MONGO_DATABASE=web_dataset

# Storage
OUTPUT_DIR=./data
LOG_DIR=./logs

# Crawl Settings
HEADLESS=true
CRAWL_DELAY=1.0
MAX_RETRIES=3
STALE_PROCESSING_TIMEOUT_MINUTES=10

# Browser
BROWSER_TYPE=chromium
CHROME_CHANNEL=chrome</code></pre>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Step 5 -->
                <div class="glass-card rounded-xl p-6">
                    <div class="flex items-start gap-4">
                        <div class="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center font-bold text-white">5</div>
                        <div class="flex-1">
                            <h3 class="text-xl font-bold mb-3">راه‌اندازی MongoDB</h3>
                            
                            <h4 class="font-bold mt-4 mb-2 text-blue-400">روش ۱: با Docker (پیشنهادی)</h4>
                            <div class="code-block">
                                <button class="copy-btn" onclick="copyCode(this)">📋 کپی</button>
                                <pre><code class="language-bash"># یا با Makefile
make mongo-start

# یا مستقیم با Docker
docker run -d --name mongodb -p 27017:27017 mongo:latest</code></pre>
                            </div>
                            
                            <h4 class="font-bold mt-4 mb-2 text-green-400">روش ۲: نصب محلی MongoDB</h4>
                            <div class="code-block">
                                <button class="copy-btn" onclick="copyCode(this)">📋 کپی</button>
                                <pre><code class="language-bash"># Ubuntu/Debian
sudo apt install mongodb
sudo systemctl start mongodb

# macOS
brew install mongodb-community
brew services start mongodb-community</code></pre>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Step 6 -->
                <div class="glass-card rounded-xl p-6">
                    <div class="flex items-start gap-4">
                        <div class="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center font-bold text-white">✓</div>
                        <div class="flex-1">
                            <h3 class="text-xl font-bold mb-3">تست نصب</h3>
                            <div class="code-block">
                                <button class="copy-btn" onclick="copyCode(this)">📋 کپی</button>
                                <pre><code class="language-bash"># بررسی CLI
python -m app.main --help

# اجرای تست سریع
make crawl-example</code></pre>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- Quick Start Section -->
        <section id="quick-start" class="mb-16 scroll-mt-8">
            <h2 class="text-4xl font-bold mb-8 gradient-text">⚡ شروع سریع</h2>
            
            <div class="glass-card rounded-xl p-8">
                <h3 class="text-2xl font-bold mb-4">اولین Crawl شما در ۳۰ ثانیه</h3>
                
                <div class="terminal mb-6">
                    <div class="terminal-header">
                        <div class="terminal-dot dot-red"></div>
                        <div class="terminal-dot dot-yellow"></div>
                        <div class="terminal-dot dot-green"></div>
                        <span class="text-slate-400 text-sm ml-4">terminal</span>
                    </div>
                    <div class="terminal-body">
<pre><span class="prompt">$</span> <span class="command">python -m app.main https://docs.python.org/3/tutorial/ --limit 5</span>

<span class="text-cyan-400">============================================================</span>
<span class="text-cyan-400">WEB CRAWLER - Dataset Collection System</span>
<span class="text-cyan-400">============================================================</span>
Target URL   : https://docs.python.org/3/tutorial/
Limit        : 5
Headless     : True
<span class="text-cyan-400">============================================================</span>

[DB] Connecting to MongoDB...
[DB] Creating indexes...

[CRAWL] Starting crawl session: docs.python.org_20260812_...
[DISCOVERY] Found 1 sitemap(s) in robots.txt
[DISCOVERY] Initial discovery complete: 45 URLs discovered

[CRAWL] Processing: https://docs.python.org/3/tutorial/
[INIT].... → Crawl4AI 0.9.2
[FETCH]... ↓ https://docs.python.org/3/tutorial/  | ✓
[COMPLETE] ● https://docs.python.org/3/tutorial/  | ✓
[SAVED] https://docs.python.org/3/tutorial/ → 1.txt (Page 1)

<span class="text-green-400">============================================================</span>
<span class="text-green-400">CRAWL COMPLETED</span>
<span class="text-green-400">============================================================</span>
Pages Crawled  : 5
Files Created  : 5
Total Size     : 0.12 MB
<span class="text-green-400">============================================================</span></pre>
                    </div>
                </div>
                
                <div class="bg-gradient-to-r from-indigo-500/10 to-purple-500/10 border border-indigo-500/30 rounded-lg p-4">
                    <p class="text-slate-300">
                        <strong class="text-indigo-400">💡 نکته:</strong> 
                        فایل‌های خروجی در دایرکتوری <code class="bg-slate-700 px-2 py-1 rounded">data/</code> با نام‌های <code class="bg-slate-700 px-2 py-1 rounded">1.txt</code>, <code class="bg-slate-700 px-2 py-1 rounded">2.txt</code> و ... ذخیره می‌شوند.
                    </p>
                </div>
            </div>
        </section>
        
        <!-- CLI Options Section -->
        <section id="cli-options" class="mb-16 scroll-mt-8">
            <h2 class="text-4xl font-bold mb-8 gradient-text">⚙️ پارامترهای CLI</h2>
            
            <div class="glass-card rounded-xl p-6 mb-6">
                <h3 class="text-xl font-bold mb-4">سینتکس پایه</h3>
                <div class="code-block">
                    <button class="copy-btn" onclick="copyCode(this)">📋 کپی</button>
                    <pre><code class="language-bash">python -m app.main &lt;URL&gt; [OPTIONS]</code></pre>
                </div>
            </div>
            
            <div class="glass-card rounded-xl overflow-hidden">
                <div class="overflow-x-auto">
                    <table>
                        <thead>
                            <tr>
                                <th style="width: 20%;">پارامتر</th>
                                <th style="width: 15%;">نوع</th>
                                <th style="width: 15%;">پیش‌فرض</th>
                                <th>توضیح</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td class="mono text-blue-400 font-semibold">URL</td>
                                <td><span class="badge badge-danger">اجباری</span></td>
                                <td class="mono text-slate-400">-</td>
                                <td>URL اصلی برای Crawl</td>
                            </tr>
                            <tr>
                                <td class="mono text-green-400 font-semibold">--limit, -l</td>
                                <td><span class="badge badge-info">int</span></td>
                                <td class="mono text-slate-400">None (نامحدود)</td>
                                <td>حداکثر تعداد صفحات برای Crawl</td>
                            </tr>
                            <tr>
                                <td class="mono text-green-400 font-semibold">--headless</td>
                                <td><span class="badge badge-info">flag</span></td>
                                <td class="mono text-slate-400">True</td>
                                <td>حالت بدون نمایش browser (پیش‌فرض)</td>
                            </tr>
                            <tr>
                                <td class="mono text-green-400 font-semibold">--show-browser</td>
                                <td><span class="badge badge-info">flag</span></td>
                                <td class="mono text-slate-400">False</td>
                                <td>نمایش browser (برای debugging)</td>
                            </tr>
                            <tr>
                                <td class="mono text-green-400 font-semibold">--delay, -d</td>
                                <td><span class="badge badge-info">float</span></td>
                                <td class="mono text-slate-400">1.0</td>
                                <td>تأخیر بین Crawlها (ثانیه)</td>
                            </tr>
                            <tr>
                                <td class="mono text-green-400 font-semibold">--output, -o</td>
                                <td><span class="badge badge-info">Path</span></td>
                                <td class="mono text-slate-400">./data</td>
                                <td>دایرکتوری خروجی فایل‌های TXT</td>
                            </tr>
                            <tr>
                                <td class="mono text-green-400 font-semibold">--verbose, -v</td>
                                <td><span class="badge badge-info">flag</span></td>
                                <td class="mono text-slate-400">False</td>
                                <td>فعال‌سازی لاگ‌های دقیق (DEBUG)</td>
                            </tr>
                            <tr>
                                <td class="mono text-green-400 font-semibold">--reset-failed</td>
                                <td><span class="badge badge-warning">flag</span></td>
                                <td class="mono text-slate-400">False</td>
                                <td>بازگرداندن URLهای failed به pending</td>
                            </tr>
                            <tr>
                                <td class="mono text-green-400 font-semibold">--help</td>
                                <td><span class="badge badge-info">flag</span></td>
                                <td class="mono text-slate-400">-</td>
                                <td>نمایش راهنما</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </section>
        
        <!-- Examples Section -->
        <section id="examples" class="mb-16 scroll-mt-8">
            <h2 class="text-4xl font-bold mb-8 gradient-text">💡 مثال‌های کاربردی</h2>
            
            <div class="space-y-4">
                <!-- Example 1 -->
                <div class="glass-card rounded-xl p-6">
                    <h3 class="text-lg font-bold mb-3 flex items-center gap-2">
                        <span class="text-2xl">🟢</span> Crawl ساده با محدودیت
                    </h3>
                    <div class="code-block">
                        <button class="copy-btn" onclick="copyCode(this)">📋 کپی</button>
                        <pre><code class="language-bash">python -m app.main https://docs.python.org/3/ --limit 100</code></pre>
                    </div>
                    <p class="text-slate-400 mt-3 text-sm">۱۰۰ صفحه اول را از مستندات Python استخراج می‌کند.</p>
                </div>
                
                <!-- Example 2 -->
                <div class="glass-card rounded-xl p-6">
                    <h3 class="text-lg font-bold mb-3 flex items-center gap-2">
                        <span class="text-2xl">🟡</span> Crawl بدون محدودیت
                    </h3>
                    <div class="code-block">
                        <button class="copy-btn" onclick="copyCode(this)">📋 کپی</button>
                        <pre><code class="language-bash">python -m app.main https://fastapi.tiangolo.com/</code></pre>
                    </div>
                    <p class="text-slate-400 mt-3 text-sm">تمام صفحات قابل دسترسی را Crawl می‌کند تا صف خالی شود.</p>
                </div>
                
                <!-- Example 3 -->
                <div class="glass-card rounded-xl p-6">
                    <h3 class="text-lg font-bold mb-3 flex items-center gap-2">
                        <span class="text-2xl">🔵</span> Crawl با browser قابل مشاهده (برای Debug)
                    </h3>
                    <div class="code-block">
                        <button class="copy-btn" onclick="copyCode(this)">📋 کپی</button>
                        <pre><code class="language-bash">python -m app.main https://example.com --limit 5 --show-browser</code></pre>
                    </div>
                    <p class="text-slate-400 mt-3 text-sm">Browser را نمایش می‌دهد تا ببینید چگونه صفحه رندر می‌شود.</p>
                </div>
                
                <!-- Example 4 -->
                <div class="glass-card rounded-xl p-6">
                    <h3 class="text-lg font-bold mb-3 flex items-center gap-2">
                        <span class="text-2xl">🟣</span> Crawl با تأخیر بیشتر (برای سایت‌های حساس)
                    </h3>
                    <div class="code-block">
                        <button class="copy-btn" onclick="copyCode(this)">📋 کپی</button>
                        <pre><code class="language-bash">python -m app.main https://example.com --limit 50 --delay 3.0</code></pre>
                    </div>
                    <p class="text-slate-400 mt-3 text-sm">۳ ثانیه بین هر Crawl صبر می‌کند تا از Rate Limit جلوگیری شود.</p>
                </div>
                
                <!-- Example 5 -->
                <div class="glass-card rounded-xl p-6">
                    <h3 class="text-lg font-bold mb-3 flex items-center gap-2">
                        <span class="text-2xl">🟠</span> Crawl با خروجی سفارشی
                    </h3>
                    <div class="code-block">
                        <button class="copy-btn" onclick="copyCode(this)">📋 کپی</button>
                        <pre><code class="language-bash">python -m app.main https://example.com --limit 100 --output ./my_dataset</code></pre>
                    </div>
                    <p class="text-slate-400 mt-3 text-sm">فایل‌ها را در دایرکتوری دلخواه ذخیره می‌کند.</p>
                </div>
                
                <!-- Example 6 -->
                <div class="glass-card rounded-xl p-6">
                    <h3 class="text-lg font-bold mb-3 flex items-center gap-2">
                        <span class="text-2xl">🔴</span> ادامه Crawl با Reset کردن failed ها
                    </h3>
                    <div class="code-block">
                        <button class="copy-btn" onclick="copyCode(this)">📋 کپی</button>
                        <pre><code class="language-bash">python -m app.main https://example.com --limit 100 --reset-failed</code></pre>
                    </div>
                    <p class="text-slate-400 mt-3 text-sm">URLهای failed قبلی را دوباره به صف اضافه می‌کند.</p>
                </div>
                
                <!-- Example 7 -->
                <div class="glass-card rounded-xl p-6">
                    <h3 class="text-lg font-bold mb-3 flex items-center gap-2">
                        <span class="text-2xl">⚪</span> Crawl ترکیبی با همه گزینه‌ها
                    </h3>
                    <div class="code-block">
                        <button class="copy-btn" onclick="copyCode(this)">📋 کپی</button>
                        <pre><code class="language-bash">python -m app.main https://example.com \
    --limit 200 \
    --delay 2.0 \
    --output ./dataset_v2 \
    --verbose \
    --reset-failed</code></pre>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- Makefile Section -->
        <section id="makefile" class="mb-16 scroll-mt-8">
            <h2 class="text-4xl font-bold mb-8 gradient-text">🎯 دستورات Makefile</h2>
            
            <p class="text-slate-400 mb-6">برای ساده‌سازی کار، یک Makefile با دستورات پرکاربرد آماده شده است:</p>
            
            <div class="glass-card rounded-xl overflow-hidden">
                <div class="overflow-x-auto">
                    <table>
                        <thead>
                            <tr>
                                <th>دستور</th>
                                <th>توضیح</th>
                                <th>مثال</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td class="mono text-green-400 font-semibold">make install</td>
                                <td>نصب پکیج‌های اصلی</td>
                                <td class="mono text-xs text-slate-400">pip install -r requirements.txt</td>
                            </tr>
                            <tr>
                                <td class="mono text-green-400 font-semibold">make install-test</td>
                                <td>نصب پکیج‌های تست</td>
                                <td class="mono text-xs text-slate-400">pip install -r requirements-test.txt</td>
                            </tr>
                            <tr>
                                <td class="mono text-blue-400 font-semibold">make test</td>
                                <td>اجرای تمام تست‌ها</td>
                                <td class="mono text-xs text-slate-400">pytest tests/</td>
                            </tr>
                            <tr>
                                <td class="mono text-blue-400 font-semibold">make test-coverage</td>
                                <td>اجرای تست با گزارش Coverage</td>
                                <td class="mono text-xs text-slate-400">htmlcov/index.html</td>
                            </tr>
                            <tr>
                                <td class="mono text-purple-400 font-semibold">make crawl</td>
                                <td>Crawl با URL و Limit دلخواه</td>
                                <td class="mono text-xs text-slate-400">URL=... LIMIT=100</td>
                            </tr>
                            <tr>
                                <td class="mono text-purple-400 font-semibold">make crawl-example</td>
                                <td>تست سریع با example.com</td>
                                <td class="mono text-xs text-slate-400">5 صفحه از example.com</td>
                            </tr>
                            <tr>
                                <td class="mono text-yellow-400 font-semibold">make crawl-headless</td>
                                <td>Crawl با browser قابل مشاهده</td>
                                <td class="mono text-xs text-slate-400">برای debugging</td>
                            </tr>
                            <tr>
                                <td class="mono text-red-400 font-semibold">make mongo-start</td>
                                <td>شروع MongoDB با Docker</td>
                                <td class="mono text-xs text-slate-400">docker run mongo</td>
                            </tr>
                            <tr>
                                <td class="mono text-red-400 font-semibold">make clean</td>
                                <td>پاک کردن data, logs و cache</td>
                                <td class="mono text-xs text-slate-400">rm -rf data/ logs/</td>
                            </tr>
                            <tr>
                                <td class="mono text-slate-400 font-semibold">make help</td>
                                <td>نمایش همه دستورات</td>
                                <td class="mono text-xs text-slate-400">راهنمای کامل</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            
            <div class="mt-6 glass-card rounded-xl p-6">
                <h3 class="text-xl font-bold mb-4">مثال‌های استفاده از Makefile:</h3>
                <div class="code-block">
                    <button class="copy-btn" onclick="copyCode(this)">📋 کپی</button>
                    <pre><code class="language-bash"># نصب کامل
make install-all

# تست سریع
make crawl-example

# Crawl حرفه‌ای
make crawl URL=https://docs.python.org/3/ LIMIT=100

# شروع MongoDB
make mongo-start

# اجرای تست‌ها
make test

# پاک کردن
make clean</code></pre>
                </div>
            </div>
        </section>
        
        <!-- Database Section -->
        <section id="database" class="mb-16 scroll-mt-8">
            <h2 class="text-4xl font-bold mb-8 gradient-text">🗄️ ساختار دیتابیس</h2>
            
            <p class="text-slate-400 mb-6">MongoDB برای مدیریت State برنامه استفاده می‌شود. ۴ Collection اصلی:</p>
            
            <div class="grid md:grid-cols-2 gap-6 mb-6">
                <div class="glass-card rounded-xl p-6">
                    <h3 class="text-xl font-bold mb-3 text-blue-400">📋 urls</h3>
                    <p class="text-slate-400 text-sm mb-3">لیست تمام URLهای کشف شده</p>
                    <div class="code-block">
                        <pre><code class="language-json">{
  "_id": "ObjectId",
  "url": "https://example.com/page",
  "normalized_url": "https://example.com/page",
  "domain": "example.com",
  "status": "completed",
  "sources": ["sitemap", "html"],
  "depth": 2,
  "file_number": 45,
  "content_file": "45.txt",
  "status_code": 200,
  "content_hash": "abc123...",
  "retry_count": 0
}</code></pre>
                    </div>
                </div>
                
                <div class="glass-card rounded-xl p-6">
                    <h3 class="text-xl font-bold mb-3 text-green-400">📊 crawl_sessions</h3>
                    <p class="text-slate-400 text-sm mb-3">مدیریت Sessionهای Crawl</p>
                    <div class="code-block">
                        <pre><code class="language-json">{
  "session_id": "example.com_20260812_143025",
  "root_url": "https://example.com",
  "root_domain": "example.com",
  "limit": 100,
  "pages_crawled": 45,
  "pages_failed": 3,
  "pages_skipped": 10,
  "urls_discovered": 542,
  "status": "completed",
  "started_at": "ISODate",
  "finished_at": "ISODate"
}</code></pre>
                    </div>
                </div>
                
                <div class="glass-card rounded-xl p-6">
                    <h3 class="text-xl font-bold mb-3 text-purple-400">🗺️ sitemaps</h3>
                    <p class="text-slate-400 text-sm mb-3">Track کردن Sitemapهای پردازش شده</p>
                    <div class="code-block">
                        <pre><code class="language-json">{
  "url": "https://example.com/sitemap.xml",
  "normalized_url": "https://example.com/sitemap.xml",
  "status": "processed",
  "sitemap_type": "urlset",
  "urls_found": 150,
  "sitemaps_found": 0,
  "source": "robots"
}</code></pre>
                    </div>
                </div>
                
                <div class="glass-card rounded-xl p-6">
                    <h3 class="text-xl font-bold mb-3 text-yellow-400">🔢 counters</h3>
                    <p class="text-slate-400 text-sm mb-3">شمارنده‌های Atomic (مثل file_number)</p>
                    <div class="code-block">
                        <pre><code class="language-json">{
  "_id": "file_counter",
  "seq": 45
}</code></pre>
                    </div>
                </div>
            </div>
            
            <div class="glass-card rounded-xl p-6">
                <h3 class="text-xl font-bold mb-4">🔄 وضعیت‌های URL (URL Status)</h3>
                <div class="grid md:grid-cols-2 gap-3">
                    <div class="flex items-center gap-3 p-3 bg-slate-800/50 rounded-lg">
                        <span class="badge badge-warning">pending</span>
                        <span class="text-slate-300 text-sm">در صف Crawl</span>
                    </div>
                    <div class="flex items-center gap-3 p-3 bg-slate-800/50 rounded-lg">
                        <span class="badge badge-info">processing</span>
                        <span class="text-slate-300 text-sm">در حال Crawl</span>
                    </div>
                    <div class="flex items-center gap-3 p-3 bg-slate-800/50 rounded-lg">
                        <span class="badge badge-success">completed</span>
                        <span class="text-slate-300 text-sm">با موفقیت Crawl شد</span>
                    </div>
                    <div class="flex items-center gap-3 p-3 bg-slate-800/50 rounded-lg">
                        <span class="badge badge-danger">failed</span>
                        <span class="text-slate-300 text-sm">Crawl ناموفق بود</span>
                    </div>
                    <div class="flex items-center gap-3 p-3 bg-slate-800/50 rounded-lg">
                        <span class="badge" style="background: rgba(156, 163, 175, 0.2); color: #d1d5db; border: 1px solid rgba(156, 163, 175, 0.3);">skipped</span>
                        <span class="text-slate-300 text-sm">عمداً نادیده گرفته شد</span>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- File Structure Section -->
        <section id="file-structure" class="mb-16 scroll-mt-8">
            <h2 class="text-4xl font-bold mb-8 gradient-text">📁 ساختار فایل‌ها</h2>
            
            <div class="glass-card rounded-xl p-6">
                <div class="code-block">
                    <button class="copy-btn" onclick="copyCode(this)">📋 کپی</button>
                    <pre><code class="language-bash">web-crawler/
│
├── app/                           # کد اصلی برنامه
│   ├── __init__.py                # Package init
│   ├── main.py                    # Entry point
│   ├── config.py                  # Configuration
│   │
│   ├── cli/                       # Command-line interface
│   │   └── parser.py              # Argument parser
│   │
│   ├── crawler/                   # Crawler engine
│   │   ├── browser.py             # Browser configuration
│   │   ├── crawl4ai_client.py     # Crawl4AI wrapper
│   │   └── page_crawler.py        # Page crawler
│   │
│   ├── database/                  # Database layer
│   │   ├── mongo.py               # MongoDB connection
│   │   ├── indexes.py             # Index manager
│   │   └── repositories/          # Data access layer
│   │       ├── url_repository.py
│   │       ├── session_repository.py
│   │       ├── counter_repository.py
│   │       └── sitemap_repository.py
│   │
│   ├── discovery/                 # URL discovery
│   │   ├── http_client.py         # HTTP client
│   │   ├── robots.py              # robots.txt parser
│   │   ├── sitemap.py             # Sitemap parser
│   │   └── link_extractor.py      # HTML link extractor
│   │
│   ├── extraction/                # Content extraction
│   │   ├── content_extractor.py
│   │   ├── content_filter.py
│   │   └── markdown_cleaner.py
│   │
│   ├── models/                    # Pydantic models
│   │   ├── url.py
│   │   ├── session.py
│   │   ├── crawl_result.py
│   │   └── sitemap.py
│   │
│   ├── services/                  # Business logic
│   │   ├── crawl_service.py       # Main orchestrator
│   │   ├── discovery_service.py
│   │   ├── session_service.py
│   │   ├── recovery_service.py
│   │   └── shutdown_service.py
│   │
│   ├── storage/                   # File storage
│   │   ├── text_storage.py        # TXT file writer
│   │   └── file_counter.py        # File number generator
│   │
│   ├── url/                       # URL utilities
│   │   ├── normalizer.py          # URL normalization
│   │   ├── validator.py           # URL validation
│   │   └── domain.py              # Domain policy
│   │
│   └── utils/                     # Utilities
│       ├── errors.py              # Custom exceptions
│       ├── retry.py               # Retry logic
│       ├── hashing.py             # Hashing utilities
│       ├── logging.py             # Logging
│       └── time.py                # Time utilities
│
├── data/                          # Output TXT files (auto-generated)
│   ├── 1.txt
│   ├── 2.txt
│   └── ...
│
├── logs/                          # Log files (auto-generated)
│   └── crawl_YYYYMMDD_HHMMSS.log
│
├── tests/                         # Unit & Integration tests
│   ├── conftest.py
│   ├── test_url_normalizer.py
│   ├── test_url_validator.py
│   ├── test_domain_policy.py
│   ├── test_markdown_cleaner.py
│   ├── test_sitemap.py
│   ├── test_content_filter.py
│   └── test_integration.py
│
├── .env                           # Environment variables
├── .env.example                   # Environment template
├── .gitignore
├── Makefile                       # Build automation
├── requirements.txt               # Python dependencies
├── requirements-test.txt          # Test dependencies
├── pyproject.toml                 # Project config
└── README.md                      # This file</code></pre>
                </div>
            </div>
        </section>
        
        <!-- Best Practices Section -->
        <section id="best-practices" class="mb-16 scroll-mt-8">
            <h2 class="text-4xl font-bold mb-8 gradient-text">🎓 نکات حرفه‌ای</h2>
            
            <div class="space-y-4">
                <div class="glass-card rounded-xl p-6 border-r-4 border-green-500">
                    <h3 class="text-lg font-bold mb-2 text-green-400">✅ همیشه با --limit شروع کنید</h3>
                    <p class="text-slate-400">ابتدا با تعداد کم (مثلاً ۱۰-۵۰) تست کنید، سپس تعداد را افزایش دهید.</p>
                    <div class="code-block mt-3">
                        <pre><code class="language-bash"># ابتدا تست
python -m app.main https://example.com --limit 20

# سپس افزایش
python -m app.main https://example.com --limit 500</code></pre>
                    </div>
                </div>
                
                <div class="glass-card rounded-xl p-6 border-r-4 border-blue-500">
                    <h3 class="text-lg font-bold mb-2 text-blue-400">✅ به robots.txt احترام بگذارید</h3>
                    <p class="text-slate-400">قبل از Crawl هر سایتی، robots.txt را بررسی کنید.</p>
                    <div class="code-block mt-3">
                        <pre><code class="language-bash">curl https://example.com/robots.txt</code></pre>
                    </div>
                </div>
                
                <div class="glass-card rounded-xl p-6 border-r-4 border-yellow-500">
                    <h3 class="text-lg font-bold mb-2 text-yellow-400">✅ تأخیر مناسب تنظیم کنید</h3>
                    <p class="text-slate-400">برای سایت‌های حساس، از <code class="bg-slate-700 px-2 py-1 rounded">--delay 2.0</code> یا بیشتر استفاده کنید.</p>
                </div>
                
                <div class="glass-card rounded-xl p-6 border-r-4 border-purple-500">
                    <h3 class="text-lg font-bold mb-2 text-purple-400">✅ از Resume capability استفاده کنید</h3>
                    <p class="text-slate-400">اگر Crawl متوقف شد، نیازی به شروع مجدد نیست. فقط دوباره اجرا کنید.</p>
                    <p class="text-slate-400 mt-2 text-sm">برای ادامه پس از کرش: URLهای pending خودکار Crawl می‌شوند.</p>
                </div>
                
                <div class="glass-card rounded-xl p-6 border-r-4 border-red-500">
                    <h3 class="text-lg font-bold mb-2 text-red-400">❌ هرگز سایت‌های زیر را Crawl نکنید</h3>
                    <ul class="text-slate-400 mt-3 space-y-2">
                        <li>• <strong>Wikipedia</strong>: از <code class="bg-slate-700 px-2 py-1 rounded">wikiextractor</code> استفاده کنید</li>
                        <li>• <strong>Exploit-DB</strong>: از Git repository رسمی استفاده کنید</li>
                        <li>• <strong>GitHub</strong>: از API یا Git clone استفاده کنید</li>
                        <li>• <strong>Stack Overflow</strong>: از Data Dump استفاده کنید</li>
                        <li>• <strong>سایت‌های با Cloudflare Enterprise</strong>: تقریباً غیرممکن</li>
                    </ul>
                </div>
            </div>
        </section>
        
        <!-- Troubleshooting Section -->
        <section id="troubleshooting" class="mb-16 scroll-mt-8">
            <h2 class="text-4xl font-bold mb-8 gradient-text">🐛 عیب‌یابی</h2>
            
            <div class="space-y-4">
                <details class="glass-card rounded-xl p-6">
                    <summary class="font-bold cursor-pointer flex items-center justify-between">
                        <span>❌ Chrome پیدا نمی‌شود</span>
                        <span class="text-slate-400">▼</span>
                    </summary>
                    <div class="mt-4 text-slate-400">
                        <p class="mb-3">Google Chrome باید روی سیستم نصب باشد:</p>
                        <div class="code-block">
                            <pre><code class="language-bash"># Linux
which google-chrome

# macOS
ls /Applications/Google\ Chrome.app

# نصب در Ubuntu
sudo apt install google-chrome-stable</code></pre>
                        </div>
                    </div>
                </details>
                
                <details class="glass-card rounded-xl p-6">
                    <summary class="font-bold cursor-pointer flex items-center justify-between">
                        <span>❌ MongoDB اتصال برقرار نمی‌شود</span>
                        <span class="text-slate-400">▼</span>
                    </summary>
                    <div class="mt-4 text-slate-400">
                        <div class="code-block">
                            <pre><code class="language-bash"># بررسی وضعیت MongoDB
docker ps | grep mongo

# یا
systemctl status mongodb

# شروع مجدد
make mongo-start</code></pre>
                        </div>
                    </div>
                </details>
                
                <details class="glass-card rounded-xl p-6">
                    <summary class="font-bold cursor-pointer flex items-center justify-between">
                        <span>❌ ERR_TOO_MANY_REDIRECTS</span>
                        <span class="text-slate-400">▼</span>
                    </summary>
                    <div class="mt-4 text-slate-400">
                        <p>این خطا <strong>طبیعی</strong> است و به دلیل سایت‌های paywalled رخ می‌دهد.</p>
                        <p class="mt-2">سیستم به درستی این URLها را به عنوان <code class="bg-slate-700 px-2 py-1 rounded">failed</code> mark می‌کند.</p>
                    </div>
                </details>
                
                <details class="glass-card rounded-xl p-6">
                    <summary class="font-bold cursor-pointer flex items-center justify-between">
                        <span>❌ تست‌ها fail می‌شوند</span>
                        <span class="text-slate-400">▼</span>
                    </summary>
                    <div class="mt-4 text-slate-400">
                        <div class="code-block">
                            <pre><code class="language-bash"># نصب پکیج‌های تست
make install-test

# اجرای تست با جزئیات
python -m pytest tests/ -v --tb=long

# فقط Unit tests
make test-unit</code></pre>
                        </div>
                    </div>
                </details>
                
                <details class="glass-card rounded-xl p-6">
                    <summary class="font-bold cursor-pointer flex items-center justify-between">
                        <span>❌ URLها دوباره Crawl می‌شوند</span>
                        <span class="text-slate-400">▼</span>
                    </summary>
                    <div class="mt-4 text-slate-400">
                        <p>این اتفاق نباید بیفتد چون MongoDB Deduplication دارد.</p>
                        <p class="mt-2">اگر رخ داد، دیتابیس را پاک کنید:</p>
                        <div class="code-block">
                            <pre><code class="language-bash"># پاک کردن کامل دیتابیس
docker exec -it mongodb mongosh web_dataset --eval "db.dropDatabase()"</code></pre>
                        </div>
                    </div>
                </details>
                
                <details class="glass-card rounded-xl p-6">
                    <summary class="font-bold cursor-pointer flex items-center justify-between">
                        <span>❌ Typer Error: Secondary flag</span>
                        <span class="text-slate-400">▼</span>
                    </summary>
                    <div class="mt-4 text-slate-400">
                        <p>نسخه‌های typer و click را آپگرید کنید:</p>
                        <div class="code-block">
                            <pre><code class="language-bash">pip install --upgrade "click>=8.1.7" "typer>=0.12.5"</code></pre>
                        </div>
                    </div>
                </details>
            </div>
        </section>
        
        <!-- Websites Section -->
        <section id="websites" class="mb-16 scroll-mt-8">
            <h2 class="text-4xl font-bold mb-8 gradient-text">🌐 سایت‌های مناسب برای Crawl</h2>
            
            <div class="grid md:grid-cols-2 gap-6">
                <div class="glass-card rounded-xl p-6">
                    <h3 class="text-xl font-bold mb-4 text-green-400">✅ سایت‌های عالی برای Crawler</h3>
                    <ul class="space-y-3">
                        <li class="flex items-start gap-2">
                            <span class="text-green-400">●</span>
                            <div>
                                <div class="font-semibold">مستندات Python</div>
                                <code class="text-xs text-slate-400">docs.python.org/3/</code>
                            </div>
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="text-green-400">●</span>
                            <div>
                                <div class="font-semibold">FastAPI Documentation</div>
                                <code class="text-xs text-slate-400">fastapi.tiangolo.com</code>
                            </div>
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="text-green-400">●</span>
                            <div>
                                <div class="font-semibold">HackTricks</div>
                                <code class="text-xs text-slate-400">book.hacktricks.xyz</code>
                            </div>
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="text-green-400">●</span>
                            <div>
                                <div class="font-semibold">DigitalOcean Tutorials</div>
                                <code class="text-xs text-slate-400">digitalocean.com/community/tutorials</code>
                            </div>
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="text-green-400">●</span>
                            <div>
                                <div class="font-semibold">Real Python</div>
                                <code class="text-xs text-slate-400">realpython.com</code>
                            </div>
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="text-green-400">●</span>
                            <div>
                                <div class="font-semibold">OWASP</div>
                                <code class="text-xs text-slate-400">owasp.org</code>
                            </div>
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="text-green-400">●</span>
                            <div>
                                <div class="font-semibold">Linux Man Pages</div>
                                <code class="text-xs text-slate-400">man7.org/linux/man-pages/</code>
                            </div>
                        </li>
                    </ul>
                </div>
                
                <div class="glass-card rounded-xl p-6">
                    <h3 class="text-xl font-bold mb-4 text-red-400">❌ سایت‌های نامناسب (از روش‌های جایگزین استفاده کنید)</h3>
                    <ul class="space-y-3">
                        <li class="flex items-start gap-2">
                            <span class="text-red-400">●</span>
                            <div>
                                <div class="font-semibold">Wikipedia</div>
                                <div class="text-xs text-slate-400">→ از wikiextractor استفاده کنید</div>
                            </div>
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="text-red-400">●</span>
                            <div>
                                <div class="font-semibold">Exploit-DB</div>
                                <div class="text-xs text-slate-400">→ git clone از GitLab</div>
                            </div>
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="text-red-400">●</span>
                            <div>
                                <div class="font-semibold">Stack Overflow</div>
                                <div class="text-xs text-slate-400">→ Stack Exchange Data Dump</div>
                            </div>
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="text-red-400">●</span>
                            <div>
                                <div class="font-semibold">GitHub Repos</div>
                                <div class="text-xs text-slate-400">→ git clone</div>
                            </div>
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="text-red-400">●</span>
                            <div>
                                <div class="font-semibold">Google/Facebook/Twitter</div>
                                <div class="text-xs text-slate-400">→ API رسمی</div>
                            </div>
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="text-red-400">●</span>
                            <div>
                                <div class="font-semibold">Amazon/E-commerce</div>
                                <div class="text-xs text-slate-400">→ Crawl ممنوع</div>
                            </div>
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="text-red-400">●</span>
                            <div>
                                <div class="font-semibold">سایت‌های با Cloudflare</div>
                                <div class="text-xs text-slate-400">→ تقریباً غیرممکن</div>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </section>
        
        <!-- FAQ Section -->
        <section id="faq" class="mb-16 scroll-mt-8">
            <h2 class="text-4xl font-bold mb-8 gradient-text">❓ سوالات متداول</h2>
            
            <div class="space-y-4">
                <details class="glass-card rounded-xl p-6">
                    <summary class="font-bold cursor-pointer flex items-center justify-between">
                        <span>آیا بدون --limit نامحدود کار می‌کند؟</span>
                        <span class="text-slate-400">▼</span>
                    </summary>
                    <div class="mt-4 text-slate-400">
                        <p>بله! اگر <code class="bg-slate-700 px-2 py-1 rounded">--limit</code> را مشخص نکنید، تا زمانی که URL pending در صف وجود دارد، Crawl ادامه می‌یابد.</p>
                        <div class="code-block mt-3">
                            <pre><code class="language-bash">python -m app.main https://example.com</code></pre>
                        </div>
                    </div>
                </details>
                
                <details class="glass-card rounded-xl p-6">
                    <summary class="font-bold cursor-pointer flex items-center justify-between">
                        <span>آیا می‌توانم Crawl متوقف شده را ادامه دهم؟</span>
                        <span class="text-slate-400">▼</span>
                    </summary>
                    <div class="mt-4 text-slate-400">
                        <p>بله! سیستم Resume capability دارد. کافی است دوباره همان دستور را اجرا کنید:</p>
                        <div class="code-block mt-3">
                            <pre><code class="language-bash"># دوباره اجرا کنید - URLهای completed نادیده گرفته می‌شوند
python -m app.main https://example.com --limit 1000</code></pre>
                        </div>
                    </div>
                </details>
                
                <details class="glass-card rounded-xl p-6">
                    <summary class="font-bold cursor-pointer flex items-center justify-between">
                        <span>چرا برخی صفحات fail می‌شوند؟</span>
                        <span class="text-slate-400">▼</span>
                    </summary>
                    <div class="mt-4 text-slate-400">
                        <p>دلایل طبیعی:</p>
                        <ul class="list-disc pr-5 mt-2 space-y-1">
                            <li>صفحات paywalled (نیاز به login)</li>
                            <li>Anti-bot detection</li>
                            <li>Redirect loop</li>
                            <li>Timeout</li>
                            <li>404 pages</li>
                        </ul>
                        <p class="mt-3">این رفتار <strong>طبیعی</strong> و مورد انتظار است.</p>
                    </div>
                </details>
                
                <details class="glass-card rounded-xl p-6">
                    <summary class="font-bold cursor-pointer flex items-center justify-between">
                        <span>چگونه URLها Deduplication می‌شوند؟</span>
                        <span class="text-slate-400">▼</span>
                    </summary>
                    <div class="mt-4 text-slate-400">
                        <p>از سه لایه Deduplication استفاده می‌شود:</p>
                        <ol class="list-decimal pr-5 mt-2 space-y-1">
                            <li><strong>URL Normalization</strong>: حذف fragment, query params, trailing slash</li>
                            <li><strong>MongoDB Unique Index</strong>: روی normalized_url</li>
                            <li><strong>URL Validator</strong>: فیلتر کردن URLهای غیرمجاز</li>
                        </ol>
                    </div>
                </details>
                
                <details class="glass-card rounded-xl p-6">
                    <summary class="font-bold cursor-pointer flex items-center justify-between">
                        <span>آیا محتوای JavaScript رندر می‌شود؟</span>
                        <span class="text-slate-400">▼</span>
                    </summary>
                    <div class="mt-4 text-slate-400">
                        <p>بله! با استفاده از Native Chrome، تمام صفحات React، Vue، Angular و SPAها به درستی رندر می‌شوند.</p>
                    </div>
                </details>
                
                <details class="glass-card rounded-xl p-6">
                    <summary class="font-bold cursor-pointer flex items-center justify-between">
                        <span>آیا Code Blockها حفظ می‌شوند؟</span>
                        <span class="text-slate-400">▼</span>
                    </summary>
                    <div class="mt-4 text-slate-400">
                        <p>بله! سیستم هوشمندانه Code Blockها را تشخیص می‌دهد و:</p>
                        <ul class="list-disc pr-5 mt-2 space-y-1">
                            <li>Code Blockها (<code>```...```</code>) کاملاً حفظ می‌شوند</li>
                            <li>Inline code (<code>`...`</code>) حفظ می‌شود</li>
                            <li>URLهای خام از متن حذف می‌شوند</li>
                            <li>Markdown links به text تبدیل می‌شوند</li>
                        </ul>
                    </div>
                </details>
            </div>
        </section>
        
        <!-- License Section -->
        <section id="license" class="mb-16 scroll-mt-8">
            <h2 class="text-4xl font-bold mb-8 gradient-text">📄 مجوز و مشارکت</h2>
            
            <div class="glass-card rounded-xl p-8 text-center">
                <div class="text-6xl mb-4">🤝</div>
                <h3 class="text-2xl font-bold mb-4">MIT License</h3>
                <p class="text-slate-400 mb-6">این پروژه تحت مجوز MIT منتشر شده است.</p>
                
                <div class="bg-slate-800/50 rounded-lg p-6 text-right">
                    <h4 class="font-bold mb-3 text-indigo-400">مشارکت در پروژه</h4>
                    <ol class="list-decimal pr-5 space-y-2 text-slate-300">
                        <li>پروژه را Fork کنید</li>
                        <li>Branch جدید بسازید: <code class="bg-slate-700 px-2 py-1 rounded">git checkout -b feature/amazing</code></li>
                        <li>تغییرات خود را commit کنید</li>
                        <li>Push کنید: <code class="bg-slate-700 px-2 py-1 rounded">git push origin feature/amazing</code></li>
                        <li>Pull Request باز کنید</li>
                    </ol>
                </div>
                
                <div class="mt-6 flex justify-center gap-4 flex-wrap">
                    <a href="#" class="bg-slate-800 hover:bg-slate-700 px-6 py-3 rounded-lg font-semibold transition-all">
                        ⭐ Star on GitHub
                    </a>
                    <a href="#" class="bg-slate-800 hover:bg-slate-700 px-6 py-3 rounded-lg font-semibold transition-all">
                        🐛 Report Issue
                    </a>
                    <a href="#" class="bg-slate-800 hover:bg-slate-700 px-6 py-3 rounded-lg font-semibold transition-all">
                        💬 Discussion
                    </a>
                </div>
            </div>
        </section>
        
        <!-- Footer -->
        <footer class="text-center py-8 border-t border-slate-800">
            <p class="text-slate-400">
                ساخته شده با <span class="text-red-500">❤️</span> برای جامعه Developer
            </p>
            <p class="text-slate-500 text-sm mt-2">
                © 2026 Web Crawler. All rights reserved.
            </p>
        </footer>
        
    </main>
</div>

<script>
// Copy to clipboard function
function copyCode(button) {
    const codeBlock = button.nextElementSibling;
    const code = codeBlock.textContent;
    
    navigator.clipboard.writeText(code).then(() => {
        const originalText = button.textContent;
        button.textContent = '✓ کپی شد!';
        button.style.background = 'rgba(16, 185, 129, 0.4)';
        
        setTimeout(() => {
            button.textContent = originalText;
            button.style.background = '';
        }, 2000);
    });
}

// Smooth scroll for navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add scroll animation
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

document.querySelectorAll('section').forEach(section => {
    section.style.opacity = '0';
    section.style.transform = 'translateY(20px)';
    section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(section);
});
</script>

</body>
</html>
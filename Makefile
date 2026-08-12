# ============================================
# Web Crawler - Makefile
# ============================================

# Variables
PYTHON := python3
PIP := pip3
APP_MODULE := app.main
DEFAULT_URL := https://example.com
DEFAULT_LIMIT := 5

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m # No Color

# ============================================
# Installation
# ============================================

.PHONY: install
install: ## Install main dependencies
	@echo "$(GREEN)Installing main dependencies...$(NC)"
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)Installation complete!$(NC)"

.PHONY: install-test
install-test: ## Install test dependencies
	@echo "$(GREEN)Installing test dependencies...$(NC)"
	$(PIP) install -r requirements-test.txt
	@echo "$(GREEN)Test dependencies installed!$(NC)"

.PHONY: install-all
install-all: install install-test ## Install all dependencies

.PHONY: install-playwright
install-playwright: ## Install Playwright browsers (if needed)
	@echo "$(YELLOW)Note: This project uses native Chrome, not Playwright browsers.$(NC)"
	@echo "$(YELLOW)Only run this if you need Playwright's bundled browsers.$(NC)"
	$(PYTHON) -m playwright install chromium

# ============================================
# Testing
# ============================================

.PHONY: test
test: ## Run all tests
	@echo "$(GREEN)Running all tests...$(NC)"
	$(PYTHON) -m pytest tests/ -v --tb=short

.PHONY: test-unit
test-unit: ## Run unit tests only
	@echo "$(GREEN)Running unit tests...$(NC)"
	$(PYTHON) -m pytest tests/ -v --tb=short -m "not integration"

.PHONY: test-integration
test-integration: ## Run integration tests only
	@echo "$(GREEN)Running integration tests...$(NC)"
	$(PYTHON) -m pytest tests/test_integration.py -v --tb=short

.PHONY: test-coverage
test-coverage: ## Run tests with coverage report
	@echo "$(GREEN)Running tests with coverage...$(NC)"
	$(PYTHON) -m pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html
	@echo "$(GREEN)Coverage report generated: htmlcov/index.html$(NC)"

# ============================================
# Crawling
# ============================================

.PHONY: crawl
crawl: ## Crawl a URL (usage: make crawl URL=https://example.com LIMIT=10)
	@echo "$(GREEN)Starting crawl: $(URL)$(NC)"
	$(PYTHON) -m $(APP_MODULE) $(URL) --limit $(LIMIT)

.PHONY: crawl-unlimited
crawl-unlimited: ## Crawl a URL without limit (usage: make crawl-unlimited URL=https://example.com)
	@echo "$(GREEN)Starting unlimited crawl: $(URL)$(NC)"
	$(PYTHON) -m $(APP_MODULE) $(URL)

.PHONY: crawl-headless
crawl-headless: ## Crawl with visible browser (for debugging)
	@echo "$(GREEN)Starting crawl with visible browser: $(URL)$(NC)"
	$(PYTHON) -m $(APP_MODULE) $(URL) --limit $(LIMIT) --no-headless

.PHONY: crawl-verbose
crawl-verbose: ## Crawl with verbose logging
	@echo "$(GREEN)Starting verbose crawl: $(URL)$(NC)"
	$(PYTHON) -m $(APP_MODULE) $(URL) --limit $(LIMIT) --verbose

.PHONY: crawl-example
crawl-example: ## Crawl example.com with limit 5 (quick test)
	@echo "$(GREEN)Running example crawl...$(NC)"
	$(PYTHON) -m $(APP_MODULE) $(DEFAULT_URL) --limit $(DEFAULT_LIMIT)

# ============================================
# Database
# ============================================

.PHONY: mongo-start
mongo-start: ## Start MongoDB (using Docker)
	@echo "$(GREEN)Starting MongoDB...$(NC)"
	docker run -d --name mongodb -p 27017:27017 mongo:latest

.PHONY: mongo-stop
mongo-stop: ## Stop MongoDB (Docker)
	@echo "$(GREEN)Stopping MongoDB...$(NC)"
	docker stop mongodb || true
	docker rm mongodb || true

.PHONY: mongo-shell
mongo-shell: ## Open MongoDB shell
	@echo "$(GREEN)Opening MongoDB shell...$(NC)"
	docker exec -it mongodb mongosh

# ============================================
# Cleanup
# ============================================

.PHONY: clean
clean: ## Clean data, logs, and cache files
	@echo "$(YELLOW)Cleaning project...$(NC)"
	rm -rf data/
	rm -rf logs/
	rm -rf __pycache__/
	rm -rf app/__pycache__/
	rm -rf app/*/__pycache__/
	rm -rf tests/__pycache__/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "$(GREEN)Clean complete!$(NC)"

.PHONY: clean-data
clean-data: ## Clean only data and logs (keep code)
	@echo "$(YELLOW)Cleaning data and logs...$(NC)"
	rm -rf data/
	rm -rf logs/
	@echo "$(GREEN)Data and logs cleaned!$(NC)"

# ============================================
# Development
# ============================================

.PHONY: lint
lint: ## Run linting (if flake8 is installed)
	@echo "$(GREEN)Running linter...$(NC)"
	$(PYTHON) -m flake8 app/ tests/ --max-line-length=120 || echo "flake8 not installed"

.PHONY: format
format: ## Format code (if black is installed)
	@echo "$(GREEN)Formatting code...$(NC)"
	$(PYTHON) -m black app/ tests/ --line-length=120 || echo "black not installed"

.PHONY: type-check
type-check: ## Run type checking (if mypy is installed)
	@echo "$(GREEN)Running type checker...$(NC)"
	$(PYTHON) -m mypy app/ --ignore-missing-imports || echo "mypy not installed"

# ============================================
# Help
# ============================================

.PHONY: help
help: ## Show this help message
	@echo "$(GREEN)Web Crawler - Available Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Examples:$(NC)"
	@echo "  make install"
	@echo "  make crawl URL=https://example.com LIMIT=100"
	@echo "  make test"
	@echo "  make clean"
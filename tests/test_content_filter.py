"""Tests for Content Filter"""
import pytest

from app.extraction.content_filter import ContentFilter


class TestContentFilter:
    """Test cases for ContentFilter"""

    def test_valid_content(self):
        """Test that valid content passes filter"""
        filter = ContentFilter()
        content = "This is a valid content with enough characters to pass the minimum length filter." * 5
        is_valid, reason = filter.is_valid_content(content)
        assert is_valid is True
        assert reason == ""

    def test_empty_content(self):
        """Test that empty content is filtered"""
        filter = ContentFilter()
        is_valid, reason = filter.is_valid_content("")
        assert is_valid is False
        assert "Empty" in reason

    def test_short_content(self):
        """Test that short content is filtered"""
        filter = ContentFilter(min_length=100)
        is_valid, reason = filter.is_valid_content("Too short")
        assert is_valid is False
        assert "too short" in reason.lower()

    def test_error_status_code(self):
        """Test that error status codes are filtered"""
        filter = ContentFilter()
        content = "Some content that is long enough to pass the filter." * 5
        is_valid, reason = filter.is_valid_content(content, status_code=404)
        assert is_valid is False
        assert "404" in reason

    def test_server_error_status_code(self):
        """Test that server error status codes are filtered"""
        filter = ContentFilter()
        content = "Some content that is long enough to pass the filter." * 5
        is_valid, reason = filter.is_valid_content(content, status_code=500)
        assert is_valid is False
        assert "500" in reason

    def test_low_quality_indicator(self):
        """Test that low-quality indicators are detected"""
        filter = ContentFilter()
        content = "Access denied. You do not have permission to view this page. " * 10
        is_valid, reason = filter.is_valid_content(content)
        assert is_valid is False
        assert "access denied" in reason.lower()

    def test_404_page_detection(self):
        """Test that 404 pages are detected"""
        filter = ContentFilter()
        content = "404 Not Found. The page you are looking for does not exist. " * 10
        is_valid, reason = filter.is_valid_content(content)
        assert is_valid is False

    def test_under_construction_detection(self):
        """Test that under construction pages are detected"""
        filter = ContentFilter()
        content = "Under construction. Please check back later. " * 10
        is_valid, reason = filter.is_valid_content(content)
        assert is_valid is False

    def test_skip_by_title_404(self):
        """Test skipping pages with 404 title"""
        filter = ContentFilter()
        should_skip, reason = filter.should_skip_by_title("404 - Page Not Found")
        assert should_skip is True
        assert "404" in reason.lower()

    def test_skip_by_title_normal(self):
        """Test that normal titles are not skipped"""
        filter = ContentFilter()
        should_skip, reason = filter.should_skip_by_title("Python Documentation")
        assert should_skip is False

    def test_skip_by_title_none(self):
        """Test that None title is not skipped"""
        filter = ContentFilter()
        should_skip, reason = filter.should_skip_by_title(None)
        assert should_skip is False

    def test_quality_score_with_code(self):
        """Test quality score with code blocks"""
        filter = ContentFilter()
        content = "# Title\n\nSome text.\n\n```python\nprint('hello')\n```\n\nMore text."
        score = filter.estimate_quality_score(content)
        assert score > 0.0

    def test_quality_score_empty(self):
        """Test quality score with empty content"""
        filter = ContentFilter()
        score = filter.estimate_quality_score("")
        assert score == 0.0

    def test_custom_min_length(self):
        """Test custom minimum length"""
        filter = ContentFilter(min_length=10)
        is_valid, reason = filter.is_valid_content("Short but valid")
        assert is_valid is True

    def test_custom_indicators(self):
        """Test custom low-quality indicators"""
        filter = ContentFilter(custom_indicators=[r"custom error"])
        content = "This page has a custom error message. " * 10
        is_valid, reason = filter.is_valid_content(content)
        assert is_valid is False
        assert "custom error" in reason.lower()
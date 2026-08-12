"""Tests for URL Validator"""
import pytest

from app.url.validator import URLValidator


class TestURLValidator:
    """Test cases for URLValidator"""

    def test_validate_http_url(self):
        """Test validating HTTP URL"""
        validator = URLValidator()
        assert validator.is_valid("http://example.com/page") is True

    def test_validate_https_url(self):
        """Test validating HTTPS URL"""
        validator = URLValidator()
        assert validator.is_valid("https://example.com/page") is True

    def test_validate_mailto_url(self):
        """Test validating mailto URL (should be invalid)"""
        validator = URLValidator()
        assert validator.is_valid("mailto:test@example.com") is False

    def test_validate_javascript_url(self):
        """Test validating javascript URL (should be invalid)"""
        validator = URLValidator()
        assert validator.is_valid("javascript:void(0)") is False

    def test_validate_tel_url(self):
        """Test validating tel URL (should be invalid)"""
        validator = URLValidator()
        assert validator.is_valid("tel:+1234567890") is False

    def test_validate_data_url(self):
        """Test validating data URL (should be invalid)"""
        validator = URLValidator()
        assert validator.is_valid("data:text/plain;base64,SGVsbG8=") is False

    def test_validate_blob_url(self):
        """Test validating blob URL (should be invalid)"""
        validator = URLValidator()
        assert validator.is_valid("blob:https://example.com/uuid") is False

    def test_validate_ftp_url(self):
        """Test validating FTP URL (should be invalid)"""
        validator = URLValidator()
        assert validator.is_valid("ftp://example.com/file") is False

    def test_validate_image_url(self):
        """Test validating image URL (should be invalid)"""
        validator = URLValidator()
        assert validator.is_valid("https://example.com/image.jpg") is False
        assert validator.is_valid("https://example.com/image.png") is False
        assert validator.is_valid("https://example.com/image.gif") is False
        assert validator.is_valid("https://example.com/image.svg") is False

    def test_validate_video_url(self):
        """Test validating video URL (should be invalid)"""
        validator = URLValidator()
        assert validator.is_valid("https://example.com/video.mp4") is False
        assert validator.is_valid("https://example.com/video.avi") is False

    def test_validate_archive_url(self):
        """Test validating archive URL (should be invalid)"""
        validator = URLValidator()
        assert validator.is_valid("https://example.com/file.zip") is False
        assert validator.is_valid("https://example.com/file.rar") is False

    def test_validate_executable_url(self):
        """Test validating executable URL (should be invalid)"""
        validator = URLValidator()
        assert validator.is_valid("https://example.com/setup.exe") is False

    def test_validate_pdf_url(self):
        """Test validating PDF URL (should be invalid)"""
        validator = URLValidator()
        assert validator.is_valid("https://example.com/document.pdf") is False

    def test_validate_css_url(self):
        """Test validating CSS URL (should be invalid)"""
        validator = URLValidator()
        assert validator.is_valid("https://example.com/style.css") is False

    def test_validate_js_url(self):
        """Test validating JS URL (should be invalid)"""
        validator = URLValidator()
        assert validator.is_valid("https://example.com/script.js") is False

    def test_validate_html_url(self):
        """Test validating HTML URL (should be valid)"""
        validator = URLValidator()
        assert validator.is_valid("https://example.com/page.html") is True
        assert validator.is_valid("https://example.com/page.htm") is True

    def test_validate_empty_url(self):
        """Test validating empty URL"""
        validator = URLValidator()
        assert validator.is_valid("") is False
        assert validator.is_valid("   ") is False

    def test_validate_url_without_scheme(self):
        """Test validating URL without scheme"""
        validator = URLValidator()
        assert validator.is_valid("example.com/page") is False

    def test_validate_batch(self):
        """Test validating a batch of URLs"""
        validator = URLValidator()
        urls = [
            "https://example.com/page1",
            "https://example.com/image.jpg",
            "mailto:test@example.com",
            "https://example.com/page2",
        ]
        result = validator.validate_batch(urls)
        assert len(result) == 2
        assert "https://example.com/page1" in result
        assert "https://example.com/page2" in result

    def test_validate_case_insensitive_extension(self):
        """Test that extension check is case-insensitive"""
        validator = URLValidator()
        assert validator.is_valid("https://example.com/IMAGE.JPG") is False
        assert validator.is_valid("https://example.com/image.JpG") is False
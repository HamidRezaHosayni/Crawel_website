"""Tests for Markdown Cleaner"""
import pytest

from app.extraction.markdown_cleaner import MarkdownCleaner


class TestMarkdownCleaner:
    """Test cases for MarkdownCleaner"""

    def test_remove_raw_url(self):
        """Test removing raw URLs from text"""
        cleaner = MarkdownCleaner()
        content = "Check https://example.com for more info."
        result = cleaner.clean(content)
        assert "https://example.com" not in result
        assert "Check" in result
        assert "for more info" in result

    def test_convert_markdown_link_to_text(self):
        """Test converting markdown links to just text"""
        cleaner = MarkdownCleaner()
        content = "See [documentation](https://example.com/docs) for details."
        result = cleaner.clean(content)
        assert "documentation" in result
        assert "https://example.com/docs" not in result
        assert "[documentation]" not in result

    def test_preserve_code_block(self):
        """Test that code blocks are preserved completely"""
        cleaner = MarkdownCleaner()
        content = '''
Here is some code:

```python
url = "https://api.example.com/data"
response = requests.get(url)
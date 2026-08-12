"""Content Extractor Module

This module provides functionality to extract meaningful content
from crawled pages and convert it to clean markdown.
"""
import hashlib
from typing import Optional

from bs4 import BeautifulSoup, Tag

from app.extraction.markdown_cleaner import MarkdownCleaner


class ContentExtractor:
    """Extractor for meaningful content from pages"""

    # Tags that typically contain main content
    CONTENT_TAGS = [
        'article',
        'main',
        '[role="main"]',
        '.content',
        '.post-content',
        '.article-content',
        '.entry-content',
        '.documentation',
        '.doc-content',
    ]

    # Tags to remove (navigation, ads, etc.)
    REMOVE_TAGS = [
        'nav',
        'header',
        'footer',
        'aside',
        'script',
        'style',
        'noscript',
        'iframe',
        '[role="navigation"]',
        '[role="banner"]',
        '[role="complementary"]',
        '.sidebar',
        '.nav',
        '.menu',
        '.advertisement',
        '.ads',
        '.social-share',
        '.comments',
        '.related-posts',
        '.breadcrumb',
        '.pagination',
    ]

    def __init__(self, markdown_cleaner: Optional[MarkdownCleaner] = None) -> None:
        """
        Initialize content extractor.

        Args:
            markdown_cleaner: Markdown cleaner instance
        """
        self.cleaner = markdown_cleaner or MarkdownCleaner()

    def extract_from_markdown(self, markdown: str) -> str:
        """
        Extract and clean content from markdown.

        Args:
            markdown: Raw markdown content

        Returns:
            Cleaned markdown content
        """
        if not markdown:
            return ""

        # Clean the markdown
        cleaned = self.cleaner.clean(markdown)

        return cleaned

    def extract_from_html(self, html: str) -> str:
        """
        Extract main content from HTML and convert to text.

        This method is a fallback when markdown extraction fails.
        It attempts to find the main content area and extract text.

        Args:
            html: Raw HTML content

        Returns:
            Extracted text content
        """
        if not html:
            return ""

        try:
            soup = BeautifulSoup(html, 'lxml')
        except Exception:
            return ""

        # Remove unwanted tags
        self._remove_unwanted_tags(soup)

        # Try to find main content area
        main_content = self._find_main_content(soup)

        if main_content:
            text = main_content.get_text(separator='\n', strip=True)
        else:
            # Fallback: use body or entire document
            body = soup.find('body')
            if body:
                text = body.get_text(separator='\n', strip=True)
            else:
                text = soup.get_text(separator='\n', strip=True)

        # Clean the extracted text
        text = self._clean_extracted_text(text)

        return text

    def _remove_unwanted_tags(self, soup: BeautifulSoup) -> None:
        """
        Remove unwanted tags from HTML.

        Args:
            soup: BeautifulSoup instance
        """
        for selector in self.REMOVE_TAGS:
            try:
                for element in soup.select(selector):
                    element.decompose()
            except Exception:
                # Some selectors might not be valid
                continue

    def _find_main_content(self, soup: BeautifulSoup) -> Optional[Tag]:
        """
        Find the main content area in HTML.

        Args:
            soup: BeautifulSoup instance

        Returns:
            Main content element or None
        """
        for selector in self.CONTENT_TAGS:
            try:
                element = soup.select_one(selector)
                if element:
                    return element
            except Exception:
                continue

        return None

    def _clean_extracted_text(self, text: str) -> str:
        """
        Clean extracted text content.

        Args:
            text: Raw extracted text

        Returns:
            Cleaned text
        """
        # Split into lines
        lines = text.split('\n')

        # Clean each line
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if line:
                cleaned_lines.append(line)

        # Join and normalize
        result = '\n'.join(cleaned_lines)

        # Remove excessive blank lines
        import re
        result = re.sub(r'\n{3,}', '\n\n', result)

        return result.strip()

    def generate_hash(self, content: str) -> str:
        """
        Generate SHA-256 hash of content for deduplication.

        Args:
            content: Content string

        Returns:
            SHA-256 hex digest
        """
        if not content:
            return ""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def get_content_length(self, content: str) -> int:
        """
        Get content length in characters.

        Args:
            content: Content string

        Returns:
            Content length
        """
        return len(content) if content else 0
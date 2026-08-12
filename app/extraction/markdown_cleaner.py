"""Markdown Cleaner Module

This module provides functionality to clean markdown content by:
- Removing all raw URLs (https://example.com)
- Converting markdown links [text](url) to just text
- Preserving code blocks completely (no URL removal inside)
- Removing tracking pixels and empty links
- Normalizing whitespace
"""
import re
from typing import List, Tuple


class MarkdownCleaner:
    """Cleaner for markdown content with code block preservation"""

    # Regex patterns
    # Matches raw URLs: http://... or https://...
    RAW_URL_PATTERN = re.compile(
        r'https?://[^\s<>\[\]()"\'`,;]+',
        re.IGNORECASE
    )

    # Matches markdown links: [text](url)
    # Captures: group(1) = text, group(2) = url
    MARKDOWN_LINK_PATTERN = re.compile(
        r'\[([^\]]*)\]\(([^)]+)\)'
    )

    # Matches code blocks: ```...```
    CODE_BLOCK_PATTERN = re.compile(
        r'```[\s\S]*?```',
        re.MULTILINE
    )

    # Matches inline code: `...`
    INLINE_CODE_PATTERN = re.compile(
        r'`[^`\n]+`'
    )

    # Matches image links: ![alt](url)
    IMAGE_PATTERN = re.compile(
        r'!\[([^\]]*)\]\([^)]+\)'
    )

    # Matches empty markdown links: [](url) or [text]()
    EMPTY_LINK_PATTERN = re.compile(
        r'\[\s*\]\([^)]+\)|\[[^\]]*\]\(\s*\)'
    )

    def __init__(self) -> None:
        """Initialize markdown cleaner"""
        self._placeholder_prefix = "__CODE_BLOCK_PLACEHOLDER_"
        self._inline_placeholder_prefix = "__INLINE_CODE_PLACEHOLDER_"

    def clean(self, markdown: str) -> str:
        """
        Clean markdown content by removing URLs while preserving code blocks.

        This method uses a multi-step approach:
        1. Extract all code blocks and replace with placeholders
        2. Extract all inline code and replace with placeholders
        3. Clean the remaining text (remove URLs, links, etc.)
        4. Restore code blocks and inline code

        Args:
            markdown: Raw markdown content

        Returns:
            Cleaned markdown content

        Examples:
            >>> cleaner = MarkdownCleaner()
            >>> content = '''
            ... Check https://example.com for more info.
            ... See [docs](https://example.com/docs) for details.
            ...
            ... ```python
            ... url = "https://api.example.com"  # This URL is preserved
            ... ```
            ... '''
            >>> print(cleaner.clean(content))
            Check  for more info.
            See docs for details.
            <BLANKLINE>
            ```python
            url = "https://api.example.com"  # This URL is preserved
            ```
        """
        if not markdown or not markdown.strip():
            return ""

        # Step 1: Extract code blocks
        code_blocks: List[str] = []
        processed = self._extract_and_replace(
            markdown,
            self.CODE_BLOCK_PATTERN,
            code_blocks,
            self._placeholder_prefix,
        )

        # Step 2: Extract inline code
        inline_codes: List[str] = []
        processed = self._extract_and_replace(
            processed,
            self.INLINE_CODE_PATTERN,
            inline_codes,
            self._inline_placeholder_prefix,
        )

        # Step 3: Clean the text
        processed = self._clean_text(processed)

        # Step 4: Restore inline code first
        processed = self._restore_placeholders(
            processed,
            inline_codes,
            self._inline_placeholder_prefix,
        )

        # Step 5: Restore code blocks
        processed = self._restore_placeholders(
            processed,
            code_blocks,
            self._placeholder_prefix,
        )

        # Step 6: Normalize whitespace
        processed = self._normalize_whitespace(processed)

        return processed

    def _extract_and_replace(
        self,
        text: str,
        pattern: re.Pattern,
        storage: List[str],
        prefix: str,
    ) -> str:
        """
        Extract matches and replace with placeholders.

        Args:
            text: Input text
            pattern: Regex pattern to find
            storage: List to store extracted matches
            prefix: Placeholder prefix

        Returns:
            Text with placeholders
        """
        def replacer(match: re.Match) -> str:
            idx = len(storage)
            storage.append(match.group(0))
            return f"{prefix}{idx}__"

        return pattern.sub(replacer, text)

    def _restore_placeholders(
        self,
        text: str,
        storage: List[str],
        prefix: str,
    ) -> str:
        """
        Restore placeholders with original content.

        Args:
            text: Text with placeholders
            storage: List of stored content
            prefix: Placeholder prefix

        Returns:
            Text with restored content
        """
        for idx, content in enumerate(storage):
            placeholder = f"{prefix}{idx}__"
            text = text.replace(placeholder, content)
        return text

    def _clean_text(self, text: str) -> str:
        """
        Clean text by removing URLs and markdown links.

        Args:
            text: Input text (with placeholders)

        Returns:
            Cleaned text
        """
        # Remove image links completely
        text = self.IMAGE_PATTERN.sub('', text)

        # Remove empty markdown links
        text = self.EMPTY_LINK_PATTERN.sub('', text)

        # Convert markdown links [text](url) to just text
        text = self.MARKDOWN_LINK_PATTERN.sub(r'\1', text)

        # Remove raw URLs
        text = self.RAW_URL_PATTERN.sub('', text)

        # Remove multiple spaces that may have been created
        text = re.sub(r'[ \t]+', ' ', text)

        return text

    def _normalize_whitespace(self, text: str) -> str:
        """
        Normalize whitespace in text.

        Args:
            text: Input text

        Returns:
            Text with normalized whitespace
        """
        # Split into lines
        lines = text.split('\n')

        # Clean each line
        cleaned_lines = []
        for line in lines:
            # Trim trailing whitespace
            line = line.rstrip()
            cleaned_lines.append(line)

        # Join and remove excessive blank lines
        result = '\n'.join(cleaned_lines)

        # Replace 3+ consecutive newlines with 2
        result = re.sub(r'\n{3,}', '\n\n', result)

        # Trim leading and trailing whitespace
        result = result.strip()

        return result

    def remove_empty_blocks(self, text: str) -> str:
        """
        Remove completely empty sections and headings without content.

        Args:
            text: Input text

        Returns:
            Text with empty sections removed
        """
        # Remove lines that are only whitespace
        lines = text.split('\n')
        non_empty = [line for line in lines if line.strip()]
        return '\n'.join(non_empty)
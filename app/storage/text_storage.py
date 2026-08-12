"""Text Storage Module - FIXED VERSION

This module provides functionality to store crawled content as TXT files
using atomic file operations to prevent corrupted or partial files.
"""
import os
import tempfile
from pathlib import Path
from typing import Optional

from app.config import settings


class TextStorage:
    """Storage manager for TXT files with atomic write operations"""

    def __init__(self, output_dir: Optional[Path] = None) -> None:
        """
        Initialize text storage.

        Args:
            output_dir: Output directory for TXT files
        """
        self.output_dir = output_dir or settings.output_dir
        self._ensure_output_dir()

    def _ensure_output_dir(self) -> None:
        """Ensure output directory exists"""
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save(
        self,
        content: str,
        file_number: int,
    ) -> str:
        """
        Save content to a TXT file using atomic write operation.
        
        Returns the filename only (e.g., "45.txt") to avoid path issues.
        """
        if file_number < 1:
            raise ValueError(f"Invalid file_number: {file_number}. Must be >= 1")

        if not content:
            raise ValueError("Content cannot be empty")

        # Generate filename
        filename = f"{file_number}.txt"
        final_path = self.output_dir / filename

        # Use atomic write operation
        self._atomic_write(final_path, content)

        # ✅ راه حل قطعی: فقط نام فایل را برگردانید
        # از مسیر نسبی یا مطلق استفاده نکنید تا مشکلات Path رفع شود
        return filename

    def _atomic_write(self, final_path: Path, content: str) -> None:
        """
        Perform atomic write operation.
        """
        temp_file = None

        try:
            # Create temporary file in the same directory
            fd, temp_path = tempfile.mkstemp(
                dir=str(final_path.parent),
                prefix=".tmp_",
                suffix=".txt",
            )

            temp_file = Path(temp_path)

            # Write content to temp file
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                f.write(content)

            # Atomically rename temp file to final name
            os.replace(temp_path, final_path)
            temp_file = None

        except Exception as e:
            # Clean up temp file if it exists
            if temp_file and temp_file.exists():
                try:
                    temp_file.unlink()
                except Exception:
                    pass

            raise IOError(f"Failed to write file {final_path}: {e}") from e

    def file_exists(self, file_number: int) -> bool:
        """Check if file with given number exists."""
        filename = f"{file_number}.txt"
        file_path = self.output_dir / filename
        return file_path.exists()

    def get_file_path(self, file_number: int) -> Path:
        """Get file path for given file number."""
        filename = f"{file_number}.txt"
        return self.output_dir / filename

    def delete_file(self, file_number: int) -> bool:
        """Delete file with given number."""
        file_path = self.get_file_path(file_number)
        if file_path.exists():
            file_path.unlink()
            return True
        return False

    def get_total_files(self) -> int:
        """Get total number of TXT files in output directory."""
        if not self.output_dir.exists():
            return 0
        return len(list(self.output_dir.glob("*.txt")))

    def get_total_size_bytes(self) -> int:
        """Get total size of all TXT files in bytes."""
        if not self.output_dir.exists():
            return 0
        total_size = 0
        for file_path in self.output_dir.glob("*.txt"):
            total_size += file_path.stat().st_size
        return total_size

    def get_total_size_mb(self) -> float:
        """Get total size of all TXT files in megabytes."""
        return self.get_total_size_bytes() / (1024 * 1024)
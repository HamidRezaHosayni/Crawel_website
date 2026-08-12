"""CLI Module

This module provides command-line interface functionality
for the web crawler application.
"""
from app.cli.parser import (
    validate_url,
    validate_limit,
    validate_delay,
    validate_output,
    CLIOptions,
)

__all__ = [
    "validate_url",
    "validate_limit",
    "validate_delay",
    "validate_output",
    "CLIOptions",
]
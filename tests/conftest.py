"""Pytest Configuration and Shared Fixtures"""
import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sample_markdown_content() -> str:
    """Sample markdown content for testing"""
    return """
# Example Documentation

This is a sample documentation page.

Check https://example.com for more information.

See [the docs](https://example.com/docs) for details.

## Code Example

```python
def hello():
    url = "https://api.example.com/data"  # This URL should be preserved
    print("Hello, World!")
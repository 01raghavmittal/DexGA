"""Pytest configuration and fixtures."""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def test_pdf_path():
    """Fixture for test PDF path."""
    return "tests/fixtures/sample.pdf"


@pytest.fixture
def test_document_text():
    """Fixture for test document text."""
    return """
    Sample Document for Testing
    
    This is a test document with multiple paragraphs.
    It contains information for testing extraction capabilities.
    
    Key Information:
    - Document type: Test
    - Purpose: Unit testing
    - Status: Active
    """


@pytest.fixture
def test_session():
    """Fixture for test session."""
    from app.utils.session_manager import SessionManager
    session = SessionManager.create_session()
    yield session
    SessionManager.delete_session(session.session_id)


@pytest.fixture
def test_cache():
    """Fixture for test cache."""
    from app.storage.session_cache import SessionCache
    cache = SessionCache()
    yield cache
    cache.clear()


@pytest.fixture
def test_cleanup_manager():
    """Fixture for test cleanup manager."""
    from app.storage.cleanup import CleanupManager
    manager = CleanupManager(enabled=False)
    yield manager

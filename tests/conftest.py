"""Pytest test configuration and fixtures."""
import os
import pytest
import mongomock
from kundli.db.database import set_test_db

@pytest.fixture(autouse=True, scope="session")
def setup_test_database():
    """Ensure tests run against an isolated in-memory MongoMock database."""
    os.environ["USE_MONGOMOCK"] = "1"
    mock_client = mongomock.MongoClient()
    test_db = mock_client["test_kundli_db"]
    set_test_db(test_db)
    yield test_db

"""Fixtures for tests."""

from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def resource_dir() -> Path:
    """Provide a pytest fixture for accessing the directory containing test resources.

    This fixture is scoped to the session, ensuring that all tests in the session
    share the same instance. It resolves the path to the `resources` directory
    relative to the file in which the fixture is defined.

    Returns:
        Path: The absolute path to the directory containing test resources.

    """
    return Path(__file__).parent / "resources"

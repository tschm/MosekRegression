"""Fixtures for tests."""

from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def resource_dir():
    return Path(__file__).parent / "resources"

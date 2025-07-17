"""Fixtures for tests."""

from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def resource_dir():
    return Path(__file__).parent / "resources"


@pytest.fixture
def project_root():
    """Fixture that provides the project root directory.

    Returns:
        Path: The path to the project root directory.
    """
    return Path(__file__).parent.parent.parent


@pytest.fixture
def env_content(project_root: Path):
    """Fixture that provides the content of the .env file as a dictionary.

    Returns:
        dict: A dictionary containing the key-value pairs from the .env file.
    """
    # Get the project root directory
    env_file_path = project_root / ".env"

    from dotenv import dotenv_values

    return dotenv_values(env_file_path)

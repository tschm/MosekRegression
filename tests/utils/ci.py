"""Utilities for testing in CI environments."""

import os


def is_ci_environment() -> bool:
    """Check if the current runtime environment is a Continuous Integration (CI) environment.

    This function inspects predefined environment variables commonly utilized by various CI
    platforms such as GitHub Actions, Travis CI, Jenkins, and others. If any of the specified
    environment variables are found in the current runtime's environment, the function determines
    that the runtime is a CI environment.

    Returns:
        bool: True if the environment is a CI environment, False otherwise.

    """
    ci_vars = [
        "CI",  # Generic CI flag
        "GITHUB_ACTIONS",  # GitHub Actions
        "TRAVIS",  # Travis CI
        "CIRCLECI",  # CircleCI
        "GITLAB_CI",  # GitLab CI
        "JENKINS_HOME",  # Jenkins
        # "TEAMCITY_VERSION",  # TeamCity
        "CODEBUILD_BUILD_ID",  # AWS CodeBuild
    ]

    print({var: var in os.environ for var in ci_vars})

    return any(var in os.environ for var in ci_vars)

import os


def is_ci_environment():
    """
    Check if the code is running in a CI environment.
    This uses common CI environment variables.
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

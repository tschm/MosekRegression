"""Tests for the least squares (LSQ) portfolio optimization."""

import os
from pathlib import Path

import pandas as pd
import pytest

try:
    from mosek import Env, Error, feature

    MOSEK_AVAILABLE = True
except ImportError:
    MOSEK_AVAILABLE = False

try:
    from mosek_tools.solver import lsq_pos as ll
except ImportError:
    ll = None


def has_valid_mosek_license() -> bool:
    """Check if Mosek has a valid license."""
    if not MOSEK_AVAILABLE:
        return False
    try:
        with Env() as env:
            env.checkoutlicense(feature.pton)
    except Error:
        return False
    else:
        return True


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


def lsq_pos(matrix: pd.DataFrame, rhs: pd.Series) -> pd.Series:
    """Compute the least squares solution to a linear matrix equation, with the constraint.

    The solution must be non-negative. The function takes a matrix and right-hand-side
    vector, and returns a pandas Series with the resulting coefficients.

    Args:
        matrix: A pandas DataFrame representing the matrix of the equation.
        rhs: A pandas Series representing the right-hand-side vector of the equation.

    Returns:
        pandas.Series: A Series containing the coefficients of the least squares solution
        that satisfy the non-negativity constraint.

    """
    return pd.Series(index=matrix.columns, data=ll(matrix.values, rhs.values))


def sharpe_ratio(ts):
    """Calculate the Sharpe Ratio for a given time series of returns.

    The Sharpe Ratio is a measure of risk-adjusted return, which compares the
    average return of an investment to its standard deviation. It is scaled here
    by a factor of 16 to annualize the result, assuming 16 periods.

    Args:
        ts: A pandas Series representing the time series of returns for
            which the Sharpe Ratio will be calculated.

    Returns:
        float: The annualized Sharpe Ratio for the given time series.

    """
    return 16 * ts.mean() / ts.std()


@pytest.mark.skipif(
    not MOSEK_AVAILABLE or is_ci_environment() or not has_valid_mosek_license(),
    reason="Test requires valid Mosek license",
)
def test_lsq(resource_dir: Path) -> None:
    """Test the least squares (LSQ) portfolio optimization for different strategies.

    Including minimum variance and tracking an index. This test ensures that
    portfolio weights are computed correctly using least squares optimization
    under different conditions.

    Args:
        resource_dir (Path): Directory containing the CSV data file used for
            the test. The file should contain historical stock prices and an
            index.

    Raises:
        AssertionError: If the test fails when executed within a local
            development environment that correctly applies portfolio optimization.

    """
    data = pd.read_csv(resource_dir / "data.csv", index_col=0, parse_dates=True).ffill()
    returns = data.pct_change().fillna(0.0)

    stocks = ["GOOG", "T", "AAPL", "GS", "IBM"]
    index = "^GSPC"

    rhs_zero = pd.Series(index=data.index, data=0.0)

    w_min = lsq_pos(matrix=data[stocks].pct_change().fillna(0.0), rhs=rhs_zero)
    w_track = lsq_pos(matrix=data[stocks], rhs=data[index])

    d: dict[str, pd.Series] = {}
    d["Min Variance"] = (returns[stocks] * w_min).sum(axis=1)
    d["Index"] = returns[index]
    d["1/N"] = returns[stocks].mean(axis=1)
    d["Tracking"] = (returns[stocks] * w_track).sum(axis=1)
    frame = pd.DataFrame(d)

    # apply some simple diagnostics
    print("Annualized Sharpe ratio")
    print(frame.apply(sharpe_ratio))
    print("Standard deviation of returns")
    print(frame.std())


def test_ci() -> None:
    """Test if the test is being run in a CI environment."""
    is_ci_environment()

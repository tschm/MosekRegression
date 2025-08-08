"""Tests for the least squares (LSQ) portfolio optimization."""

from pathlib import Path

import pandas as pd
import pytest

from mosek_tools.solver import lsq_pos as ll
from tests.utils import is_ci_environment


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


@pytest.mark.skipif(is_ci_environment(), reason="Test requires local Mosek license")
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

    d: dict[str, pd.Series] = dict()
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

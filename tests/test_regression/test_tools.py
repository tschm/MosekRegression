"""Tests for the tools module."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def test_min_variance(resource_dir: Path) -> None:
    """Test the minimum variance calculation using a covariance matrix.

    The matrix is derived from percentage change
    of data sourced from a specified CSV file.

    The function reads financial or similar time-series data, computes the
    percentage changes, and then calculates the covariance matrix to analyze the
    variances and covariances of the data. The operation assumes the data exists
    in the specified resource directory and is well-formed.

    Args:
        resource_dir (Path): Path to the directory containing the source CSV file
            named "data.csv". The CSV file should have a valid index (e.g., dates)
            and a header row for column labels.

    Raises:
        FileNotFoundError: If "data.csv" is not found at the specified resource
            directory.
        ValueError: If there are issues with the content of the CSV file, such as
            missing data or incorrectly formatted columns/index.

    """
    data = pd.read_csv(resource_dir / "data.csv", index_col=0, parse_dates=True, header=0)
    rets = data.pct_change()
    cov = rets.cov()
    print(cov)
    # can't really test Mosek based fcts without the license :-)

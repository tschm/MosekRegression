"""Demo of minimum variance portfolio optimization."""


# /// script
# dependencies = [
#     "marimo==0.18.4",
#     "pandas",
#     "mosektools",
# ]
#
# [tool.uv.sources]
# mosektools = { path = "../..", editable=true }
#
# ///

import marimo

__generated_with = "0.10.19"
app = marimo.App()

with app.setup:
    from pathlib import Path

    import marimo as mo  # noqa: F401
    import pandas as pd

    from mosek_tools.solver import lsq_pos as ll

    path = Path(__file__).parent

    data = pd.read_csv(path / "data" / "data.csv", index_col=0, parse_dates=True).ffill()


@app.cell
def _():
    mo.md(r"""# Minimum Variance""")
    return


@app.function
def lsq_pos(matrix, rhs):
    """Solve a least squares problem with positivity constraints.

    Args:
        matrix: The matrix in the least squares problem.
        rhs: The right-hand side vector.

    Returns:
        pandas.Series: Solution vector with positivity constraints.
    """
    return pd.Series(index=matrix.columns, data=ll(matrix.values, rhs.values))


@app.function
def sharpe_ratio(ts):
    """Calculate the annualized Sharpe ratio of a time series.

    Args:
        ts: Time series of returns.

    Returns:
        float: Annualized Sharpe ratio.
    """
    return 16 * ts.mean() / ts.std()


@app.cell
def _():
    # load data from csv file
    # data = pd.read_csv(path / "data" / "data.csv", index_col=0, parse_dates=True).ffill()
    returns = data.pct_change().fillna(0.0)

    stocks = ["GOOG", "T", "AAPL", "GS", "IBM"]
    index = "^GSPC"
    return index, returns, stocks


@app.cell
def _(index, returns, stocks):
    # construct a rhs
    pd.Series(index=data.index, data=0.0)

    # only works on a machine with an active Mosek license
    # w_min = lsq_pos(matrix=data[stocks].pct_change().fillna(0.0), rhs=rhs_zero)
    # w_track = lsq_pos(matrix=data[stocks], rhs=data[index])

    d = dict()
    # d["Min Variance"] = (returns[stocks] * w_min).sum(axis=1)
    d["Index"] = returns[index]
    d["1/N"] = returns[stocks].mean(axis=1)
    # d["Tracking"] = (returns[stocks] * w_track).sum(axis=1)
    frame = pd.DataFrame(d)

    # apply some simple diagnostics
    print("Annualized Sharpe ratio")
    print(frame.apply(sharpe_ratio))
    print("Standard deviation of returns")
    print(frame.std())


if __name__ == "__main__":
    app.run()

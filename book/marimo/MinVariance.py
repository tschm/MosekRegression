"""Demo of minimum variance portfolio optimization."""

# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "pandas==2.3.1",
#     "numpy==2.3.1"
# ]
# ///

import marimo

__generated_with = "0.10.19"
app = marimo.App()

with app.setup:
    from pathlib import Path

    import marimo as mo  # noqa: F401
    import pandas as pd

    path = Path(__file__).parent

    data = pd.read_csv(path / "data" / "data.csv", index_col=0, parse_dates=True).ffill()


@app.cell
def _():
    mo.md(r"""# Minimum Variance""")
    return


@app.cell
def _(__file__):
    from mosek_tools.solver import lsq_pos as ll

    # path = Path(__file__).parent

    def lsq_pos(matrix, rhs):
        return pd.Series(index=matrix.columns, data=ll(matrix.values, rhs.values))

    def sharpe_ratio(ts):
        return 16 * ts.mean() / ts.std()

    return sharpe_ratio, ll, lsq_pos


@app.cell
def _():
    # load data from csv file
    # data = pd.read_csv(path / "data" / "data.csv", index_col=0, parse_dates=True).ffill()
    returns = data.pct_change().fillna(0.0)

    stocks = ["GOOG", "T", "AAPL", "GS", "IBM"]
    index = "^GSPC"
    return index, returns, stocks


@app.cell
def _(Sharpe_Ratio, index, lsq_pos, returns, stocks):
    # construct a rhs
    rhs_zero = pd.Series(index=data.index, data=0.0)

    w_min = lsq_pos(matrix=data[stocks].pct_change().fillna(0.0), rhs=rhs_zero)
    w_track = lsq_pos(matrix=data[stocks], rhs=data[index])

    d = dict()
    d["Min Variance"] = (returns[stocks] * w_min).sum(axis=1)
    d["Index"] = returns[index]
    d["1/N"] = returns[stocks].mean(axis=1)
    d["Tracking"] = (returns[stocks] * w_track).sum(axis=1)
    frame = pd.DataFrame(d)

    # apply some simple diagnostics
    print("Annualized Sharpe ratio")
    print(frame.apply(Sharpe_Ratio))
    print("Standard deviation of returns")
    print(frame.std())
    return d, frame, rhs_zero, w_min, w_track


if __name__ == "__main__":
    app.run()

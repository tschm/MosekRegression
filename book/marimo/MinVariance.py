import marimo

__generated_with = "0.10.19"
app = marimo.App()


@app.cell
def _(mo):
    mo.md(r"""# Minimum Variance""")
    return


@app.cell
def _(__file__):
    import os
    from pathlib import Path

    import pandas as pd

    from mosek_tools.solver import lsq_pos as ll

    path = Path(__file__).parent

    def lsq_pos(matrix, rhs):
        return pd.Series(index=matrix.columns, data=ll(matrix.values, rhs.values))

    def Sharpe_Ratio(ts):
        return 16 * ts.mean() / ts.std()

    return Path, Sharpe_Ratio, ll, lsq_pos, os, path, pd


@app.cell
def _(path, pd):
    # load data from csv file
    data = pd.read_csv(path / "data" / "data.csv", index_col=0, parse_dates=True).ffill()
    returns = data.pct_change().fillna(0.0)

    stocks = ["GOOG", "T", "AAPL", "GS", "IBM"]
    index = "^GSPC"
    return data, index, returns, stocks


@app.cell
def _(Sharpe_Ratio, data, index, lsq_pos, pd, returns, stocks):
    # construct a rhs
    rhsZero = pd.Series(index=data.index, data=0.0)

    wMin = lsq_pos(matrix=data[stocks].pct_change().fillna(0.0), rhs=rhsZero)
    wTrack = lsq_pos(matrix=data[stocks], rhs=data[index])

    d = dict()
    d["Min Variance"] = (returns[stocks] * wMin).sum(axis=1)
    d["Index"] = returns[index]
    d["1/N"] = returns[stocks].mean(axis=1)
    d["Tracking"] = (returns[stocks] * wTrack).sum(axis=1)
    frame = pd.DataFrame(d)

    # apply some simple diagnostics
    print("Annualized Sharpe ratio")
    print(frame.apply(Sharpe_Ratio))
    print("Standard deviation of returns")
    print(frame.std())
    return d, frame, rhsZero, wMin, wTrack


@app.cell
def _():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()

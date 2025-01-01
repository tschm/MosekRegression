import marimo

__generated_with = "0.9.27"
app = marimo.App()


@app.cell
def __(mo):
    mo.md(
        r"""
        # Minimum Variance
        """
    )
    return


@app.cell
def __():
    import os

    import pandas as pd

    from mosek_tools.solver import lsq_pos as ll

    def lsq_pos(matrix, rhs):
        return pd.Series(index=matrix.columns, data=ll(matrix.values, rhs.values))

    def Sharpe_Ratio(ts):
        return 16 * ts.mean() / ts.std()

    return Sharpe_Ratio, ll, lsq_pos, os, pd


@app.cell
def __(os, pd):
    # load data from csv file
    data = pd.read_csv(os.path.join("data", "data.csv"), index_col=0, parse_dates=True).ffill()
    returns = data.pct_change().fillna(0.0)

    stocks = ["GOOG", "T", "AAPL", "GS", "IBM"]
    index = "^GSPC"
    return data, index, returns, stocks


@app.cell
def __(Sharpe_Ratio, data, index, lsq_pos, pd, returns, stocks):
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
def __():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()

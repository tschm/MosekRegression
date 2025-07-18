"""Demo of lasso regression predictor."""

import marimo

__generated_with = "0.10.19"
app = marimo.App()


@app.cell
def _(mo):
    mo.md(r"""# Predictor""")
    return


@app.cell
def _(__file__):
    from pathlib import Path

    import numpy as np
    import pandas as pd

    from mosek_tools.solver import lasso as ll

    path = Path(__file__).parent

    def normalize(ts):
        return ts / np.linalg.norm(ts.values, 2)

    def lasso(X, y, lamb):
        return pd.Series(index=X.columns, data=ll(X.values, y.values, lamb))

    return Path, lasso, ll, normalize, np, path, pd


@app.cell
def _(lasso, normalize, np, path, pd):
    # load data from csv files
    data = pd.read_csv(path / "data" / "data.csv", index_col=0, parse_dates=True)

    stock = data["GS"]
    r = stock.pct_change()

    x = pd.DataFrame({a: r.ewm(com=a, min_periods=30).mean() for a in [2, 3, 5, 8, 13, 21, 34, 55, 89]})

    # shift returns as we are trying to predict the next day return...
    y = r.shift(-1)

    x = x.truncate(before="01-02-2010").fillna(0.0)
    y = y.truncate(before="01-02-2010").fillna(0.0)

    x = x.apply(normalize)
    y = normalize(y)
    w = lasso(x, y, 0.005)

    print(w)
    print(np.corrcoef((x * w).sum(axis=1), y))
    return x, data, r, stock, w, y


@app.cell
def _():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()

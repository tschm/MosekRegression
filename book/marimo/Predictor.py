import marimo

__generated_with = "0.9.27"
app = marimo.App()


@app.cell
def __(mo):
    mo.md(
        r"""
        # Predictor
        """
    )
    return


@app.cell
def __():
    import numpy as np
    import pandas as pd

    from mosek_tools.solver import lasso as ll

    def normalize(ts):
        return ts / np.linalg.norm(ts.values, 2)

    def lasso(X, y, lamb):
        return pd.Series(index=X.columns, data=ll(X.values, y.values, lamb))

    return lasso, ll, normalize, np, pd


app._unparsable_cell(
    r"""
    # load data from csv files
        data = pd.read_csv(\"data/data.csv\", index_col=0, parse_dates=True)

        stock = data[\"GS\"]
        r = stock.pct_change()

        X = pd.DataFrame({a: r.ewm(com=a, min_periods=30).mean() for a in [2, 3, 5, 8, 13, 21, 34, 55, 89]})

        # shift returns as we are trying to predict the next day return...
        y = r.shift(-1)

        X = X.truncate(before=\"01-02-2010\").fillna(0.0)
        y = y.truncate(before=\"01-02-2010\").fillna(0.0)

        X = X.apply(normalize)
        y = normalize(y)
        w = lasso(X, y, 0.005)

        print(w)
        print(np.corrcoef((X*w).sum(axis=1), y))
    """,
    name="__",
)


@app.cell
def __():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()

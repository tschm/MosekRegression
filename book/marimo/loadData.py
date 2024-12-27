import marimo

__generated_with = "0.9.27"
app = marimo.App()


@app.cell
def __(mo):
    mo.md(
        r"""
        # Load Data
        """
    )
    return


@app.cell
def __():
    import yfinance as yf

    data = yf.download(tickers = "SPY AAPL GOOG MSFT GS IBM T ^GSPC",  # list of tickers
                       period = "10y",                  # time period
                       interval = "1d",                 # trading interval
                       prepost = False,                 # download pre/post market hours data?
                       repair = True)                   # repair obvious price errors e.g. 100x?

    prices = data["Adj Close"]
    prices.to_csv("data/data.csv")
    return data, prices, yf


@app.cell
def __():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()

"""Download data from Yahoo Finance."""

# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "loguru==0.7.2",
#     "yfinance==0.2.63",
#     "scipy==1.15.0"
# ]
# ///
from loguru import logger


def _download():
    import yfinance as yf

    data = yf.download(
        tickers="SPY AAPL GOOG MSFT GS IBM T ^GSPC",  # list of tickers
        period="10y",  # time period
        interval="1d",  # trading interval
        prepost=False,  # download pre/post market hours data?
        repair=True,
    )  # repair obvious price errors e.g. 100x?

    logger.info(data.head())
    logger.info(data["Close"].tail())

    prices = data["Close"]
    prices.to_csv("book/data/data.csv")
    return prices


if __name__ == "__main__":
    _download()

import pandas as pd
import pytest

from mosek_tools.solver import lsq_pos as ll
from tests.utils.ci import is_ci_environment


def lsq_pos(matrix, rhs):
    return pd.Series(index=matrix.columns, data=ll(matrix.values, rhs.values))


def Sharpe_Ratio(ts):
    return 16 * ts.mean() / ts.std()


@pytest.mark.skipif(is_ci_environment(), reason="Test requires local Mosek license")
def test_lsq(resource_dir):
    data = pd.read_csv(resource_dir / "data.csv", index_col=0, parse_dates=True).ffill()
    returns = data.pct_change().fillna(0.0)

    stocks = ["GOOG", "T", "AAPL", "GS", "IBM"]
    index = "^GSPC"

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

from __future__ import annotations

import pandas as pd


def test_min_variance(resource_dir):
    data = pd.read_csv(resource_dir / "data.csv", index_col=0, parse_dates=True, header=0)
    rets = data.pct_change()
    cov = rets.cov()
    print(cov)
    # can't really test Mosek based fcts without the license :-)

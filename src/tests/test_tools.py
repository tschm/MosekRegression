from __future__ import annotations

import os

import pandas as pd


def test_min_variance(resource_dir):
    data = pd.read_csv(resource_dir / "data.csv", index_col=0, parse_dates=True, header=0)
    rets = data.pct_change()
    cov = rets.cov()
    print(cov)
    # can't really test Mosek based fcts without the license :-)


def test_license():
    print(os.environ["MOSEKLM_LICENSE_FILE"])

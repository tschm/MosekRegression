import os
from datetime import datetime
import pandas as pd

import solver as sl

from config import MOSEKLICENSEFILE, DATAPATH

os.environ["MOSEKLM_LICENSE_FILE"] = MOSEKLICENSEFILE


### load data from csv files
data = pd.read_csv(os.path.join(DATAPATH, "data.csv"), index_col=0, parse_dates=True)

### compute returns
returns = data.pct_change(fill_method="ffill").fillna(0.0)

### compute portfolio weights (for a set of portfolios)
w = dict()
w["a"] = sl.experiment1(returns.truncate(before=datetime(2010, 1, 1), after=datetime(2012, 1, 1)))
w["b"] = sl.experiment2(returns.truncate(before=datetime(2010, 1, 1), after=datetime(2012, 1, 1)), lev=1.5)
w = pd.DataFrame(w)

### weights
print w
print w.apply(sl.report)

### profit per strategy
profit = pd.DataFrame(
    {key: (returns.truncate(before=datetime(2012, 1, 1)) * w[key]).sum(axis=1) for key in w.keys()})

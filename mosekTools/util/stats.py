def ann_Sharpe_ratio(ts):
    return 16 * ts.mean() / ts.std()


def returns(frame):
    def __compute_return(ts):
        ts = ts.dropna()
        return ts.diff() / ts.shift(1)

    return frame.apply(__compute_return).fillna(value=0.0)

def rolling_window(frame, n=100):
    data = dict()
    for i, t in enumerate(frame.index[n - 1:], start=n):
        data[t] = frame.ix[frame.index[i - n:i]]

    # don't use a panel here, a panel would create one big box (3D) where the sparsity of this problem is lost
    # make sure you apply proper sorting when you use this dictionary
    return data



import pandas
import numpy
import matplotlib.pyplot as mPlot


def plot(profit, fig=None, title="", bins=20):
    if fig:
        # figure is given
        pass
    else:
        fig = mPlot.figure()

    fig.subplots_adjust(hspace=1.0)

    axes1 = fig.add_subplot(4, 1, (1, 2))
    axes2 = fig.add_subplot(4, 1, 3, sharex=axes1)
    axes3 = fig.add_subplot(4, 1, 4)

    profit.cumsum().plot(ax=axes1)
    axes1.set_title(title)
    axes1.legend(["Profit accumulated"], loc=2)
    axes1.grid(True)

    hw = drawdown(profit)
    hw.plot(color="r", ax=axes2)
    axes2.grid(True)
    axes2.legend(["Drawdown"], loc=2)

    profit.hist(bins=bins, ax=axes3)
    axes3.legend(["Profit histogram"], loc=2)


def drawdown(profit):
    accumulated_profit = profit.cumsum()
    high_water_mark = pandas.TimeSeries(index=accumulated_profit.index)

    moving_max_value = 0
    for t in high_water_mark.index:
        moving_max_value = max(moving_max_value, accumulated_profit[t])
        high_water_mark[t] = moving_max_value

    return high_water_mark - accumulated_profit


def summary(profit):
    x = profit.describe()

    d = dict()
    d["kurtosis"] = profit.kurt()
    d["skewness"] = profit.skew()
    d["Annualized Sharpe ratio"] = numpy.sqrt(262) * profit.mean() / profit.std()

    #w = profit.copy()
    #w[w > 0] = 0
    #std = numpy.sqrt(numpy.mean(w * x))

    #d["Annualized Sortino ratio"] = numpy.sqrt(262) * profit.mean() / std
    d["Max Drawdown"] = drawdown(profit).max()
    d["Profit Last"] = profit.tail(1).sum()
    d["Profit Last 5"] = profit.tail(5).sum()

    d["Profit YTD"] = profit.resample("A", how="sum").tail(1).values[0]
    d["Profit MTD"] = profit.resample("M", how="sum").tail(1).values[0]

    return x.append(pandas.Series(d))
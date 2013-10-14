from mosekTools.data.yahoo import get_data_yahoo
import datetime as dt

from nose.tools import raises, assert_almost_equal

s = dt.datetime(2012,  1,  1)
e = dt.datetime(2012, 12, 31)

@raises(IOError)
def test_load_wrong_symbol():
    get_data_yahoo(symbols=["SYMBOL UNKNOWN"], start=s, end=e)


def test_load_correct_symbol():
    op = get_data_yahoo(symbols=["T"], start=s, end=e, type="Open")
    assert_almost_equal(op.values[-1], 33.13, delta=1e-10)
    assert_almost_equal(op.values[0], 30.46, delta=1e-10)


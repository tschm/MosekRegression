from unittest import TestCase
from datetime import datetime
from nose.tools import raises

from mosekTools.data.Data import get_data_yahoo

s = datetime(2012, 1, 1)
e = datetime(2012, 12, 31)


class TestData(TestCase):
    @raises(IOError)
    def test_load_wrong_symbol(self):
        get_data_yahoo(symbols=["SYMBOL UNKNOWN"], start=s, end=e)

    def test_load_correct_symbol(self):
        op = get_data_yahoo(symbols=["T"], start=s, end=e, series="Open")
        self.assertAlmostEqual(op.values[-1], 33.13, delta=1e-10)
        self.assertAlmostEqual(op.values[0], 30.46, delta=1e-10)
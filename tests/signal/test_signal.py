from mosekTools.signal.signal import rolling_window
from unittest import TestCase

import pandas as pd


class TestSignal(TestCase):
    def test_rolllingwindow(self):
        x = pd.DataFrame(index=[0, 1, 2, 3, 4, 5],
                         data=[[1.0, 1.0], [2.0, 1.5], [3.0, 2.0], [2.0, 3.0], [4.0, 5.0], [6.0, 2.0]])
        a = rolling_window(x, 2)

        assert a[1].index[0] == 0
        assert a[1].index[1] == 1
        assert a.keys() == [1, 2, 3, 4, 5]
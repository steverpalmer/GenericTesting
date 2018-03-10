# Copyright 2018 Steve Palmer

"""A library of generic test for the datetime classes."""

import datetime
import unittest

from hypothesis import strategies as st

from src import *

class timedeltaTests(EqualityTests, TotalOrderingTests, VectorSpaceTests):
    """Tests of timedelta class properties."""

    zero = datetime.timedelta()
    abs_zero = zero
    scalar_one = 1.0


@Given({ClassUnderTest: st.integers(min_value=-864000000000, max_value=864000000000).map(lambda i: datetime.timedelta(milliseconds=i)),
        ScalarT: st.integers(min_value=-100, max_value=100).map(lambda i: i / 10.0)})
class Test_timedelta(timedeltaTests):
    pass

SUITE = unittest.TestSuite()
SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_timedelta))
TR = unittest.TextTestRunner(verbosity=2)
TR.run(SUITE)

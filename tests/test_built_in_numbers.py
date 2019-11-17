#!/usr/bin/env python3
# Copyright 2018 Steve Palmer

"""A test of the generic_test.built_in_tests using the built-in numbers types."""

import unittest
import fractions

from hypothesis import strategies as st

from generic_testing import *


@Given({ClassUnderTest: st.integers()})
class Test_int(intTests):
    pass


FRACTIONS_RANGE = 10000000000


@Given({ClassUnderTest: st.fractions(min_value=fractions.Fraction(-FRACTIONS_RANGE),
                                     max_value=fractions.Fraction(FRACTIONS_RANGE),
                                     max_denominator=FRACTIONS_RANGE)})
class Test_Fraction(FractionTests):
    pass


FLOATS_RANGE = 1e30


@Given({ClassUnderTest: st.floats(min_value=-FLOATS_RANGE, max_value=FLOATS_RANGE)})
class Test_float(floatTests):
    pass


COMPLEX_RANGE = 1e10


@Given({ClassUnderTest: st.complex_numbers(0.0, COMPLEX_RANGE,
                                           allow_nan=False, allow_infinity=False)})
class Test_complex(complexTests):
    pass


__all__ = ('Test_int', 'Test_Fraction', 'Test_float', 'Test_complex')


if __name__ == '__main__':
    SUITE = unittest.TestSuite()
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_int))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_Fraction))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_float))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_complex))
    TR = unittest.TextTestRunner(verbosity=1)
    TR.run(SUITE)

#!/usr/bin/env python3
# Copyright 2018 Steve Palmer

"""A test of the generic_test.built_in_tests using the built-in numbers types."""

import unittest
import fractions

from hypothesis import strategies as st

from generic_testing_test_context import generic_testing


@generic_testing.Given({generic_testing.ClassUnderTest: st.integers()})
class Test_int(generic_testing.intTests):
    pass


FRACTIONS_RANGE = 10000000000


@generic_testing.Given({generic_testing.ClassUnderTest: st.fractions(min_value=fractions.Fraction(-FRACTIONS_RANGE),
                                                                     max_value=fractions.Fraction(FRACTIONS_RANGE),
                                                                     max_denominator=FRACTIONS_RANGE)})
class Test_Fraction(generic_testing.FractionTests):
    pass


FLOATS_RANGE = 1e30


@generic_testing.Given({generic_testing.ClassUnderTest: st.floats(min_value=-FLOATS_RANGE, max_value=FLOATS_RANGE)})
class Test_float(generic_testing.floatTests):
    pass


COMPLEX_RANGE = 1e10


@generic_testing.Given({generic_testing.ClassUnderTest: st.complex_numbers(0.0, COMPLEX_RANGE,
                                                                           allow_nan=False, allow_infinity=False)})
class Test_complex(generic_testing.complexTests):
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

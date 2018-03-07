#!/usr/bin/env python3
# Copyright 2018 Steve Palmer

"""A test of the generic_test.built_in_tests using the built-in numbers types."""

import unittest
import fractions

from hypothesis import strategies as st

from src import *


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


# :TODO: This is under consideration (https://github.com/HypothesisWorks/hypothesis-python/issues/1076), but here's my quick&dirty attempt
@st.cacheable
@st.base_defines_strategy(True)
def complex_numbers(min_real_value=None, max_real_value=None, min_imag_value=None, max_imag_value=None, allow_nan=None, allow_infinity=None):
    """Returns a strategy that generates complex numbers.

    Examples from this strategy shrink by shrinking their component real
    and imaginary parts.

    """
    from hypothesis.searchstrategy.numbers import ComplexStrategy
    return ComplexStrategy(
        st.tuples(
            st.floats(min_value=min_real_value, max_value=max_real_value, allow_nan=allow_nan, allow_infinity=allow_infinity),
            st.floats(min_value=min_imag_value, max_value=max_imag_value, allow_nan=allow_nan, allow_infinity=allow_infinity)))


COMPLEX_RANGE = 1e10


@Given({ClassUnderTest: complex_numbers(-COMPLEX_RANGE, COMPLEX_RANGE,
                                        -COMPLEX_RANGE, COMPLEX_RANGE,
                                        allow_nan=False, allow_infinity=False)})
class Test_complex(complexTests):
    pass


__all__ = ('Test_int', 'Test_Fraction', 'Test_float', 'Test_complex')


if __name__ == '__main__':
    SUITE = unittest.TestSuite()
    name = None  # :TRICK: need to introdcue 'name' before iterating through locals
    value = None  # :TRICK: need to introdcue 'value' before iterating through locals
    for name, value in locals().items():
        if name.startswith('Test_'):
            SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(value))
    TR = unittest.TextTestRunner(verbosity=1)
    TR.run(SUITE)

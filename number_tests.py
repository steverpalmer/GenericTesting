#!/usr/bin/env python3
"""
Copyright 2018 Steve Palmer
"""

import unittest
import numbers
import fractions

from hypothesis import strategies as st

from isclose import IsClose
from core import base_test_modifier
from equality_test import EqualityTests
from arithmetic_tests import FieldTests, AbsoluteValueTests, FloorDivModTests, ExponentiationTests, ConjugateTests, RoundingTests, QuotientTests
from ordering_tests import TotalOrderingOverNumbersTests
from lattice_tests import BitwiseTests


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


class _ComplexTests(EqualityTests, FieldTests, AbsoluteValueTests):

    def test_010_zero_type(self):
        self.assertTrue(isinstance(self.zero, numbers.Complex))

    def test_011_one_type(self):
        self.assertTrue(isinstance(self.one, numbers.Complex))

    def test_012_real_zero_type(self):
        self.assertTrue(isinstance(self.real_zero, numbers.Real))


class ComplexTests(_ComplexTests, ConjugateTests):

    def test_013_i_type(self):
        self.assertTrue(isinstance(self.i, numbers.Complex))

    def test_490_complex(self):
        self.assertEqual(complex(0), complex(self.zero))
        self.assertEqual(complex(1), complex(self.one))
        self.assertEqual(complex(0, 1), complex(self.i))

    def test_491_i_squared_is_minus_one(self):
        self.assertEqual(self.i * self.i, -self.one)


class _RealTests(_ComplexTests, FloorDivModTests, ExponentiationTests, TotalOrderingOverNumbersTests):

    def test_010_zero_type(self):
        self.assertTrue(isinstance(self.zero, numbers.Real))

    def test_011_one_type(self):
        self.assertTrue(isinstance(self.one, numbers.Real))


class RealTests(_RealTests, RoundingTests):

    def test_014_root_two_type(self):
        self.assertTrue(isinstance(self.root_two, numbers.Real))

    def test_490_float(self):
        self.assertEqual(0.0, float(self.zero))
        self.assertEqual(1.0, float(self.one))

    def test_491_root_two_squared_is_two(self):
        self.assertEqual(self.root_two * self.root_two, self.one + self.one)


class _RationalTests(_RealTests):
    pass


class RationalTests(_RationalTests, QuotientTests):

    def test_015_half_type(self):
        self.assertTrue(isinstance(self.half, numbers.Rational))

    def test_491_half_plus_half_is_one(self):
        self.assertEqual(self.half + self.half, self.one)


class IntegralTests(_RationalTests, BitwiseTests):

    def test_010_zero_type(self):
        self.assertTrue(isinstance(self.zero, numbers.Integral))

    def test_011_one_type(self):
        self.assertTrue(isinstance(self.one, numbers.Integral))

    def test_490_int(self):
        self.assertEqual(0, int(self.zero))
        self.assertEqual(1, int(self.one))


@base_test_modifier(st.integers())
class Test_int(IntegralTests):
    zero = 0
    one = 1
    real_zero = float(0)


FRACTIONS_RANGE = 10000000000


@base_test_modifier(st.fractions(min_value=fractions.Fraction(-FRACTIONS_RANGE),
                                 max_value=fractions.Fraction(FRACTIONS_RANGE),
                                 max_denominator=FRACTIONS_RANGE))
class Test_Fraction(RationalTests):
    zero = fractions.Fraction(0)
    one = fractions.Fraction(1)
    real_zero = float(fractions.Fraction(0))
    half = fractions.Fraction(1, 2)


FLOATS_RANGE = 1e30


@base_test_modifier(st.floats(min_value=-FLOATS_RANGE, max_value=FLOATS_RANGE))
class Test_float(RealTests):
    zero = 0.0
    one = 1.0
    real_zero = 0.0
    root_two = 2.0 ** 0.5

    def test_200_addition_associativity(self, a, b, c):
        if not self.isclose(a, b) and not self.isclose(b, c):
            super().test_200_addition_associativity(a, b, c)

    def test_220_multiplication_addition_left_distributivity(self, a, b, c):
        # :FUDGE: this consistently fails when b is close to -c due to the limitations of floating point numbers.
        # Therefore, continue the test only when the b is not close of -c
        if not IsClose.over_numbers(b, -c, rel_tol=self.isclose.rel_tol ** 0.5, abs_tol=self.isclose.abs_tol * 100.0):
            super().test_220_multiplication_addition_left_distributivity(a, b, c)

    def test_411_abs_is_subadditive(self, a, b):
        x = abs(a + b)
        y = abs(a) + abs(b)
        if not self.isclose(x, y):
            self.assertLessEqual(abs(a + b), abs(a) + abs(b))


COMPLEX_RANGE = 1e10


@base_test_modifier(complex_numbers(-COMPLEX_RANGE, COMPLEX_RANGE, -COMPLEX_RANGE, COMPLEX_RANGE, allow_nan=False, allow_infinity=False))
class Test_complex(ComplexTests):
    zero = complex(0)
    one = complex(1)
    real_zero = 0.0
    i = complex(0, 1)

    def test_220_multiplication_addition_left_distributivity(self, a, b, c):
        # :FUDGE: this consistently fails when b is close to -c due to the limitations of floating point numbers.
        # Therefore, continue the test only when the b is not close of -c
        if not IsClose.over_numbers(b, -c, rel_tol=self.isclose.rel_tol ** 0.5, abs_tol=self.isclose.abs_tol * 100.0):
            super().test_220_multiplication_addition_left_distributivity(a, b, c)

    def test_221_multiplication_addition_right_distributivity(self, a, b, c):
        # :FUDGE: this consistently fails when b is close to -c due to the limitations of floating point numbers.
        # Therefore, continue the test only when the b is not close of -c
        if not IsClose.over_numbers(b, -c, rel_tol=self.isclose.rel_tol ** 0.5, abs_tol=self.isclose.abs_tol * 100.0):
            super().test_221_multiplication_addition_right_distributivity(a, b, c)

    def test_411_abs_is_subadditive(self, a, b):
        x = abs(a + b)
        y = abs(a) + abs(b)
        if not self.isclose(x, y):
            self.assertLessEqual(abs(a + b), abs(a) + abs(b))


if __name__ == '__main__':

    SUITE = unittest.TestSuite()
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_int))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_Fraction))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_float))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_complex))
    TR = unittest.TextTestRunner(verbosity=2)
    TR.run(SUITE)

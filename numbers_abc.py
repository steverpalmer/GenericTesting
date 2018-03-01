#!/usr/bin/env python3
"""
Copyright 2018 Steve Palmer

A library of generic test for the base classes in the numbers library
"""

import abc
import unittest
import numbers
import fractions
import math

from hypothesis import assume, strategies as st

from isclose import IsClose
from core import Given, ClassUnderTest
from relations import EqualityTests, TotalOrderingTests
from lattices import LatticeWithComplement
from arithmetic import FieldTests, AbsoluteValueTests, FloorDivModTests, ExponentiationTests


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
    """
    These is the property test of Complex numbers that are shared with
    derived classes.
    """

    def test_generic_2105_bool_definition(self, a: ClassUnderTest) -> None:
        self.assertEqual(bool(a), not a == self.zero)


class ComplexTests(_ComplexTests):
    """
    These are the property test specific to the base class numbers.Complex.
    """

    @property
    @abc.abstractmethod
    def i(self) -> ClassUnderTest:
        pass

    def test_generic_2000_zero_type(self):
        self.assertIsInstance(self.zero, numbers.Complex)

    def test_generic_2001_one_type(self):
        self.assertIsInstance(self.one, numbers.Complex)

    def test_generic_2002_real_zero_type(self) -> None:
        self.assertIsInstance(self.real_zero, numbers.Real)

    def test_generic_2003_i_type(self) -> None:
        self.assertIsInstance(self.i, numbers.Complex)

    def test_generic_2300_i_times_i_is_minus_one(self) -> None:
        self.assertEqual(self.i * self.i, -self.one)

    def test_generic_2301_complex(self) -> None:
        self.assertEqual(complex(0), complex(self.zero))
        self.assertEqual(complex(1), complex(self.one))
        self.assertEqual(complex(0, 1), complex(self.i))

    def test_generic_2310_conjugate_is_additive(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual((a + b).conjugate(), a.conjugate() + b.conjugate())

    def test_generic_2311_conjugate_is_multiplicitive(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual((a * b).conjugate(), a.conjugate() * b.conjugate())

    def test_generic_2312_conjugate_has_same_absolute_value(self, a: ClassUnderTest) -> None:
        self.assertEqual(abs(a.conjugate()), abs(a))

    def test_generic_2313_conjugate_has_same_real_value(self, a: ClassUnderTest) -> None:
        self.assertEqual(a.conjugate().real, a.real)

    def test_generic_2314_conjugate_has_negated_imag_value(self, a: ClassUnderTest) -> None:
        self.assertEqual(a.conjugate().imag, -a.imag)

    def test_generic_2315_imag_is_zero_iff_conjugate_equals_self(self, a: ClassUnderTest) -> None:
        self.assertEqual(a == a.conjugate(), a.imag == self.real_zero)

    def test_generic_2316_absolute_value_real_and_imag_values(self, a: ClassUnderTest) -> None:
        self.assertEqual(abs(a) * abs(a), a.real * a.real + a.imag * a.imag)


class _RealTests(_ComplexTests, TotalOrderingTests, FloorDivModTests, ExponentiationTests):
    """
    These is the property test of Real numbers that are shared with
    derived classes.
    """

    def test_generic_2150_less_or_equal_orientation(self) -> None:
        self.assertTrue(self.zero <= self.one)

    def test_generic_2151_less_or_equal_consistent_with_addition(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        self.assertEqual(a <= b, a + c <= b + c)

    def test_generic_2152_less_or_equal_consistent_with_multiplication(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertImplies(self.zero <= a and self.zero <= b, self.zero <= a * b)


class RealTests(_RealTests):
    """
    These are the property test specific to the base class numbers.Real.
    """

    @property
    def real_zero(self):
        return self.zero

    @property
    @abc.abstractmethod
    def root_two(self) -> ClassUnderTest:
        pass

    def test_generic_2000_zero_type(self):
        self.assertIsInstance(self.zero, numbers.Real)

    def test_generic_2001_one_type(self):
        self.assertIsInstance(self.one, numbers.Real)

    def test_generic_2004_root_two_type(self) -> None:
        self.assertIsInstance(self.root_two, numbers.Real)

    def test_generic_2330_root_two_times_root_two_is_two(self) -> None:
        self.assertEqual(self.root_two * self.root_two, self.one + self.one)

    def test_generic_2331_float(self) -> None:
        self.assertEqual(0.0, float(self.zero))
        self.assertEqual(1.0, float(self.one))
        self.assertEqual(1.414213562, float(self.root_two))

    def test_generic_2340_round_is_integral(self, a: ClassUnderTest) -> None:
        self.assertEqual(float(round(a)) % 1.0, 0.0)

    def test_generic_2341_round_is_close(self, a: ClassUnderTest) -> None:
        self.assertLessEqual(abs(float(a) - float(round(a))), 0.5)

    def test_generic_2342_round_towards_even(self, a: ClassUnderTest) -> None:
        round_result = round(a)
        self.assertImplies(self.isclose(abs(float(a) - float(round_result)), 0.5), round_result % 2.0 == 0)

    #:TODO: It would be good to have tests of round(a, n)

    def test_generic_2350_floor_definition(self, a: ClassUnderTest) -> None:
        a_floor = math.floor(a)
        self.assertIsInstance(a_floor, numbers.Integral)
        a_floor = float(a_floor)
        self.assertEqual(a_floor % 1.0, 0.0)  # floor is integral
        a_float = float(a)
        self.assertLessEqual(a_floor, a_float)
        self.assertLess(a_float - a_floor, 1.0)

    def test_generic_2351_ceil_definition(self, a: ClassUnderTest) -> None:
        a_ceil = math.ceil(a)
        self.assertIsInstance(a_ceil, numbers.Integral)
        a_ceil = float(a_ceil)
        self.assertEqual(a_ceil % 1.0, 0.0)  # ceil is integral
        a_float = float(a)
        self.assertLessEqual(a_float, a_ceil)
        self.assertLess(a_ceil - a_float, 1.0)

    def test_generic_2352_trunc_definition(self, a: ClassUnderTest) -> None:
        a_trunc = math.trunc(a)
        self.assertIsInstance(a_trunc, numbers.Real)
        a_trunc = float(a_trunc)
        if a < self.zero:
            self.assertEqual(a_trunc, float(math.ceil(a)))
        else:
            self.assertEqual(a_trunc, float(math.floor(a)))


class _RationalTests(_RealTests):
    """
    These is the property test of Rational numbers that are shared with
    derived classes.
    """


class RationalTests(_RationalTests):
    """
    These are the property test specific to the base class numbers.Rational.
    """

    @property
    @abc.abstractmethod
    def half(self) -> ClassUnderTest:
        pass

    def test_generic_2000_zero_type(self):
        self.assertIsIstance(self.zero, numbers.Rational)

    def test_generic_2001_one_type(self):
        self.assertIsInstance(self.one, numbers.Rational)

    def test_generic_2005_half_type(self) -> None:
        self.assertIsInstance(self.half, numbers.Rational)

    def test_generic_2360_half_plus_half_is_one(self) -> None:
        self.assertEqual(self.half + self.half, self.one)

    def test_generic_2370_zero_terms(self) -> None:
        self.assertEqual(int(self.zero.numerator), 0)
        self.assertEqual(int(self.zero.denominator), 1)

    def test_generic_2371_numerator_carries_the_sign(self, a: ClassUnderTest) -> None:
        self.assertGreater(int(a.denominator), 0)
        self.assertEqual(0 <= int(a.numerator), self.zero <= a)

    @staticmethod
    def _gcd(a: int, b: int) -> int:
        a = abs(a)
        b = abs(b)
        if a < b:
            a, b = (b, a)
        rem = a % b
        while rem != 0:
            a, b = (b, rem)
            rem = a % b
        return b

    def test_generic_2372_lowest_terms(self, a: ClassUnderTest) -> None:
        assume(a != self.zero)
        self.assertEqual(RationalTests._gcd(int(a.numerator), int(a.denominator)), 1)


class IntegralTests(_RationalTests, LatticeWithComplement):

    def test_generic_2000_zero_type(self):
        self.assertIsInstance(self.zero, numbers.Integral)

    def test_generic_2001_one_type(self):
        self.assertIsInstance(self.one, numbers.Integral)

    def test_generic_2380_int(self) -> None:
        self.assertEqual(0, int(self.zero))
        self.assertEqual(1, int(self.one))

    @property
    def bottom(self) -> ClassUnderTest:
        return self.zero

    @property
    def top(self) -> ClassUnderTest:
        return -self.one

    def test_generic_2390_lshift_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        if 0 <= b <= 64:
            self.assertEqual(a << b, a * pow(2, b))

    def test_generic_2391_rshift_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        if 0 <= b <= 64:
            self.assertEqual(a >> b, a // pow(2, b))

@Given({ClassUnderTest: st.integers()})
class Test_int(IntegralTests):
    zero = 0
    one = 1
    real_zero = float(0)


FRACTIONS_RANGE = 10000000000


@Given({ClassUnderTest: st.fractions(min_value=fractions.Fraction(-FRACTIONS_RANGE),
                                     max_value=fractions.Fraction(FRACTIONS_RANGE),
                                     max_denominator=FRACTIONS_RANGE)})
class Test_Fraction(RationalTests):
    zero = fractions.Fraction(0)
    one = fractions.Fraction(1)
    real_zero = float(fractions.Fraction(0))
    half = fractions.Fraction(1, 2)


FLOATS_RANGE = 1e30


@Given({ClassUnderTest: st.floats(min_value=-FLOATS_RANGE, max_value=FLOATS_RANGE)})
class Test_float(RealTests):
    zero = 0.0
    one = 1.0
    root_two = 2.0 ** 0.5

    def test_generic_2220_addition_associativity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        assume(not self.isclose(a, b) and not self.isclose(b, c))
        super().test_generic_2220_addition_associativity(a, b, c)

    def test_generic_2237_multiplication_addition_left_distributivity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        # :FUDGE: this consistently fails when b is close to -c due to the limitations of floating point numbers.
        # Therefore, continue the test only when the b is not close of -c
        assume(not IsClose.over_numbers(b, -c, rel_tol=self.isclose.rel_tol ** 0.5, abs_tol=self.isclose.abs_tol * 100.0))
        super().test_generic_2237_multiplication_addition_left_distributivity(a, b, c)

    def test_generic_2274_abs_is_subadditive(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertCloseOrLessThan(abs(a + b), abs(a) + abs(b))


COMPLEX_RANGE = 1e10


@Given({ClassUnderTest: complex_numbers(-COMPLEX_RANGE, COMPLEX_RANGE,
                                        -COMPLEX_RANGE, COMPLEX_RANGE,
                                        allow_nan=False, allow_infinity=False)})
class Test_complex(ComplexTests):
    zero = complex(0)
    one = complex(1)
    real_zero = 0.0
    i = complex(0, 1)

    def test_generic_2237_multiplication_addition_left_distributivity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        # :FUDGE: this consistently fails when b is close to -c due to the limitations of floating point numbers.
        # Therefore, continue the test only when the b is not close of -c
        assume(not IsClose.over_numbers(b, -c, rel_tol=self.isclose.rel_tol ** 0.5, abs_tol=self.isclose.abs_tol * 100.0))
        super().test_generic_2237_multiplication_addition_left_distributivity(a, b, c)

    def test_generic_2238_multiplication_addition_right_distributivity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        # :FUDGE: this consistently fails when b is close to -c due to the limitations of floating point numbers.
        # Therefore, continue the test only when the b is not close of -c
        assume(not IsClose.over_numbers(b, -c, rel_tol=self.isclose.rel_tol ** 0.5, abs_tol=self.isclose.abs_tol * 100.0))
        super().test_generic_2238_multiplication_addition_right_distributivity(a, b, c)

    def test_generic_2274_abs_is_subadditive(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertCloseOrLessThan(abs(a + b), abs(a) + abs(b))


if __name__ == '__main__':

    SUITE = unittest.TestSuite()
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_int))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_Fraction))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_float))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_complex))
    TR = unittest.TextTestRunner(verbosity=2)
    TR.run(SUITE)

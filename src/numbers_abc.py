#!/usr/bin/env python3
"""
Copyright 2018 Steve Palmer

A library of generic test for the base classes in the numbers library
"""

import abc
import numbers
import math

from hypothesis import assume

from .core import ClassUnderTest
from .relations import EqualityTests, TotalOrderingTests
from .lattices import LatticeWithComplement
from .arithmetic import FieldTests, AbsoluteValueTests, FloorDivModTests, ExponentiationTests


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

    def test_generic_2301_complex_function(self) -> None:
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

    def test_generic_2330_less_or_equal_consistent_with_addition(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        self.assertEqual(a <= b, a + c <= b + c)

    def test_generic_2331_less_or_equal_consistent_with_multiplication(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
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

    def test_generic_2332_root_two_times_root_two_is_two(self) -> None:
        self.assertEqual(self.root_two * self.root_two, self.one + self.one)

    def test_generic_2333_float_function(self) -> None:
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

    # :TODO: It would be good to have tests of round(a, n)

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
        self.assertIsInstance(self.zero, numbers.Rational)

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

    def test_generic_2372_lowest_terms(self, a: ClassUnderTest) -> None:
        assume(a != self.zero)
        self.assertEqual(math.gcd(int(a.numerator), int(a.denominator)), 1)


class IntegralTests(_RationalTests, LatticeWithComplement):

    def test_generic_2000_zero_type(self):
        self.assertIsInstance(self.zero, numbers.Integral)

    def test_generic_2001_one_type(self):
        self.assertIsInstance(self.one, numbers.Integral)

    def test_generic_2380_int_function(self) -> None:
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


__all__ = ('ComplexTests', 'RealTests', 'RationalTests', 'IntegralTests')

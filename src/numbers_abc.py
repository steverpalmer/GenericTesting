# Copyright 2018 Steve Palmer

"""A library of generic test for the base classes in the numbers library."""

import abc
import numbers
import math
import unittest

from hypothesis import assume

from .core import ClassUnderTest
from .relations import EqualityTests, TotalOrderingTests
from .lattices import LatticeWithComplement
from .arithmetic import FieldTests, AbsoluteValueTests, FloorDivModTests, ExponentiationTests


class _ComplexTests(EqualityTests, FieldTests, AbsoluteValueTests):
    """The property tests of numbers.Complex that are shared with derived classes."""

    def test_generic_2800_bool_convention(self, a: ClassUnderTest) -> None:
        """bool(a) ⇔ not a == 0"""
        self.assertEqual(bool(a), not a == self.zero)


class ComplexTests(_ComplexTests):
    """The property tests specific to the base class numbers.Complex.

    I assume that the type of z.imag is the same as abs(z).
    """

    @property
    @abc.abstractmethod
    def i(self) -> ClassUnderTest:
        """√-1

        A defining characteristic of Complex numbers is that there should be a
        number "i" representing the square root of -1.
        """

    def test_generic_2300_i_times_i_is_minus_one(self) -> None:
        """i * i == -1"""
        self.assertEqual(self.i * self.i, -self.one)

    def test_generic_2301_complex_function(self) -> None:
        self.assertEqual(complex(0), complex(self.zero))
        self.assertEqual(complex(1), complex(self.one))
        self.assertEqual(complex(0, 1), complex(self.i))

    def test_generic_2310_conjugate_is_additive(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """(a + b).conjugate() == a.conjugate() + b.conjugate()"""
        self.assertEqual((a + b).conjugate(), a.conjugate() + b.conjugate())

    def test_generic_2311_conjugate_is_multiplicitive(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """(a * b).conjugate() == a.conjugate() * b.conjugate()"""
        self.assertEqual((a * b).conjugate(), a.conjugate() * b.conjugate())

    def test_generic_2312_conjugate_has_same_absolute_value(self, a: ClassUnderTest) -> None:
        """abs(a.conjugate()) == abs(a)"""
        self.assertEqual(abs(a.conjugate()), abs(a))

    def test_generic_2313_conjugate_has_same_real_value(self, a: ClassUnderTest) -> None:
        """a.conjugate().real == a.real"""
        self.assertEqual(a.conjugate().real, a.real)

    def test_generic_2314_conjugate_has_negated_imag_value(self, a: ClassUnderTest) -> None:
        """a.conjugate().imag == -a.imag"""
        self.assertEqual(a.conjugate().imag, -a.imag)

    def test_generic_2315_imag_is_zero_iff_conjugate_equals_self(self, a: ClassUnderTest) -> None:
        """a.conjugate() == a ⇒ a.imag == 0"""
        self.assertEqual(a == a.conjugate(), a.imag == self.abs_zero)

    def test_generic_2316_absolute_value_real_and_imag_values(self, a: ClassUnderTest) -> None:
        """abs(a) * abs(a) == a.real * a.real + a.imag * a.imag"""
        self.assertEqual(abs(a) * abs(a), a.real * a.real + a.imag * a.imag)


class _RealTests(_ComplexTests, TotalOrderingTests, FloorDivModTests, ExponentiationTests):
    """The property tests of numbers.Real that are shared with derived classes."""

    @property
    def abs_zero(self):
        return self.zero

    def test_generic_2152_less_or_equal_orientation(self) -> None:
        """0 <= 1"""
        self.assertTrue(self.zero <= self.one)

    def test_generic_2353_less_or_equal_consistent_with_addition(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        """a <= b ⇔ a + c <= b + c"""
        self.assertEqual(a <= b, a + c <= b + c)

    def test_generic_2354_less_or_equal_consistent_with_multiplication(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """0 <= a and 0 <= b ⇒ 0 <= a * b"""
        self.assertImplies(self.zero <= a and self.zero <= b, self.zero <= a * b)


class RealTests(_RealTests):
    """The property tests specific to the base class numbers.Real.

    Although not a strict requirement, I assume that abs() on a number.Real returns a numbers.Real,
    and not necessarilty a float.
    """

    @property
    @abc.abstractmethod
    def root_two(self) -> ClassUnderTest:
        """√2

        A defining characteristic of Real numbers is that there should be a
        number representing, for example, the square root of 2.
        """

    def test_generic_2330_root_two_times_root_two_is_two(self) -> None:
        """√2 * √2 == 2"""
        self.assertEqual(self.root_two * self.root_two, self.one + self.one)

    def test_generic_2331_float_function(self) -> None:
        self.assertEqual(0.0, float(self.zero))
        self.assertEqual(1.0, float(self.one))
        self.assertEqual(1.414213562, float(self.root_two))

    def test_generic_2340_round_is_integral(self, a: ClassUnderTest) -> None:
        """round(a) % 1 == 0"""
        self.assertEqual(float(round(a)) % 1.0, 0.0)

    def test_generic_2341_round_is_close(self, a: ClassUnderTest) -> None:
        """abs(a - round(a)) <= 0.5"""
        self.assertLessEqual(abs(float(a) - float(round(a))), 0.5)

    def test_generic_2342_round_towards_even(self, a: ClassUnderTest) -> None:
        """abs(a - round(a)) == 0.5 ⇒ round(a) % 2 == 0"""
        round_result = round(a)
        self.assertImplies(self.isclose(abs(float(a) - float(round_result)), 0.5), round_result % 2.0 == 0.0)

    # :TODO: It would be good to have tests of round(a, n)

    def test_generic_2350_floor_definition(self, a: ClassUnderTest) -> None:
        """(floor(a) % 1 == 0) and (floor(a) <= a) and (a - floor(a) < 1)"""
        a_floor = math.floor(a)
        self.assertIsInstance(a_floor, numbers.Integral)
        a_floor = float(a_floor)
        self.assertEqual(a_floor % 1.0, 0.0)  # floor is integral
        a_float = float(a)
        self.assertLessEqual(a_floor, a_float)
        self.assertLess(a_float - a_floor, 1.0)

    def test_generic_2351_ceil_definition(self, a: ClassUnderTest) -> None:
        """(ceil(a) % 1 == 0) and (a <= ceil(a)) and (ceil(a) - a < 1)"""
        a_ceil = math.ceil(a)
        self.assertIsInstance(a_ceil, numbers.Integral)
        a_ceil = float(a_ceil)
        self.assertEqual(a_ceil % 1.0, 0.0)  # ceil is integral
        a_float = float(a)
        self.assertLessEqual(a_float, a_ceil)
        self.assertLess(a_ceil - a_float, 1.0)

    def test_generic_2352_trunc_definition(self, a: ClassUnderTest) -> None:
        """trunc(a) == floor(a) if a >= 0 else ceil(a)"""
        a_trunc = math.trunc(a)
        self.assertIsInstance(a_trunc, numbers.Real)
        a_trunc = float(a_trunc)
        if a < self.zero:
            self.assertEqual(a_trunc, float(math.ceil(a)))
        else:
            self.assertEqual(a_trunc, float(math.floor(a)))


class _RationalTests(_RealTests):
    """The property tests of numbers.Rational that are shared with derived classes."""


class RationalTests(_RationalTests):
    """The property tests specific to the base class numbers.Rational."""

    @property
    @abc.abstractmethod
    def half(self) -> ClassUnderTest:
        pass

    def test_generic_2360_half_plus_half_is_one(self) -> None:
        """½ + ½ == 1"""
        self.assertEqual(self.half + self.half, self.one)

    def test_generic_2370_zero_terms(self) -> None:
        """0.numberator == 0 and 0.denominator == 0"""
        self.assertEqual(int(self.zero.numerator), 0)
        self.assertEqual(int(self.zero.denominator), 1)

    def test_generic_2371_numerator_carries_the_sign(self, a: ClassUnderTest) -> None:
        """a.numerator < 0 ⇔ a < 0"""
        self.assertGreater(int(a.denominator), 0)
        self.assertEqual(0 <= int(a.numerator), self.zero <= a)

    def test_generic_2372_lowest_terms(self, a: ClassUnderTest) -> None:
        """gcd(a.numberator, a.denominator) == 1"""
        assume(a != self.zero)
        self.assertEqual(math.gcd(int(a.numerator), int(a.denominator)), 1)


class IntegralTests(_RationalTests, LatticeWithComplement):
    """The property tests specific to the base class numbers.Integral."""

    @property
    def bottom(self) -> ClassUnderTest:
        return self.zero

    @property
    def top(self) -> ClassUnderTest:
        return -self.one

    def test_generic_2380_int_function(self) -> None:
        self.assertEqual(0, int(self.zero))
        self.assertEqual(1, int(self.one))

    def test_generic_2390_lshift_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """0 <= b ⇒ a << b == a * pow(2, b)"""
        assume(self.zero <= b)
        self.assertEqual(a << b, a * pow(2, b))

    def test_generic_2391_rshift_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """0 <= b ⇒ a >> b == a // pow(2, b)"""
        assume(self.zero <= b)
        self.assertEqual(a >> b, a // pow(2, b))


__all__ = ('ComplexTests', 'RealTests', 'RationalTests', 'IntegralTests',
           '_ComplexTests', '_RealTests', '_RationalTests')

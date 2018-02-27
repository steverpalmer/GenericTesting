"""
Copyright 2018 Steve Palmer
"""

import math
import numbers

from hypothesis import assume

from core import BaseTests


class AdditiveMonoid(BaseTests):

    def test_200_addition_associativity(self, a, b, c):
        self.assertEqual(a + (b + c), (a + b) + c)

    def test_201_additive_identity(self, a):
        self.assertEqual(a + self.zero, a)
        self.assertEqual(self.zero + a, a)


class FieldTests(AdditiveMonoid):

    def test_202_addition_inverse(self, a):
        self.assertEqual(a + (-a), self.zero)

    def test_203_addition_commutativity(self, a, b):
        self.assertEqual(a + b, b + a)

    def test_210_multiplication_associativity(self, a, b, c):
        self.assertEqual(a * (b * c), (a * b) * c)

    def test_211_multiplicative_identity(self, a):
        self.assertEqual(a * self.one, a)
        self.assertEqual(self.one * a, a)

    def test_212_multiplication_commutativity(self, a, b):
        self.assertEqual(a * b, b * a)

    def test_220_multiplication_addition_left_distributivity(self, a, b, c):
        self.assertEqual(a * (b + c), (a * b) + (a * c))

    def test_221_multiplication_addition_right_distributivity(self, a, b, c):
        # Oddly, this test seems to pass, for the fudge is not used.
        self.assertEqual((a + b) * c, (a * c) + (b * c))

    def test_230_pos_definition(self, a):
        self.assertEqual(+a, a)

    def test_240_sub_definition(self, a, b):
        self.assertEqual(a - b, a + (-b))

    def test_250_truediv_definition(self, a, b):
        assume(b != self.zero)
        calc = (a / b) * b
        self.assertEqual(calc, type(calc)(a))


class FloorDivModTests(BaseTests):

    def test_260_mod_range(self, a, b):
        assume(b != self.zero)
        rem = a % b
        if b <= self.zero:
            self.assertGreaterEqual(self.zero, rem)
            self.assertGreater(rem, b)
        else:
            self.assertLessEqual(self.zero, rem)
            self.assertLess(rem, b)

    def test_261_floordiv_definition(self, a, b):
        assume(b != self.zero)
        self.assertEqual((a // b) * b + a % b, a)

    def test_262_divmod_definition(self, a, b):
        assume(b != self.zero)
        self.assertEqual(divmod(a, b), (a // b, a % b))


class ExponentiationTests(BaseTests):
    """
    These tests are way incomplete.  It is tempting to include identities such as:
        1. a ** (b + c)  == a ** b * a ** c
        2. (a * b) ** c  == a ** c * b ** c
        3. (a ** b) ** c == a ** (b * c)

    However:
        1. these identities are only true for certain types.  E.g. items 3 is not true for Reals
        2. with ints (for which they are true), the full range maths kills the preformance.

    So, for now these are not tested.
    """

    def test_270_exponentiation_zero_by_zero(self):
        # By Python defintion (Standard Library §4.4 note 5)
        self.assertEqual(self.zero ** self.zero, self.one)

    def test_271_exponentiation_by_zero(self, a):
        assume(a != self.zero)
        self.assertEqual(a ** self.zero, self.one)

    def test_272_exponentiation_with_base_zero(self, a):
        assume(a > self.zero)
        self.assertEqual(self.zero ** a, self.zero)

    def test_273_exponentiation_with_base_one(self, a):
        assume(a != self.zero)
        self.assertEqual(self.one ** a, self.one)

    def test_274_exponentiation_by_one(self, a):
        assume(a != self.zero)
        self.assertEqual(a ** self.one, a)


class AbsoluteValueTests(BaseTests):

    def test_400_abs_not_negative(self, a):
        self.assertTrue(self.real_zero <= abs(a))

    def test_401_abs_positve_definite(self, a):
        self.assertEqual(abs(a) == self.real_zero, a == self.zero)

    def test_402_abs_one_is_one(self):
        self.assertEqual(abs(self.one), self.one)

    def test_410_abs_is_multiplicitive(self, a, b):
        self.assertEqual(abs(a * b), abs(a) * abs(b))

    def test_411_abs_is_subadditive(self, a, b):
        self.assertLessEqual(abs(a + b), abs(a) + abs(b))


class ConjugateTests(BaseTests):

    def test_420_conjugate_is_additive(self, a, b):
        self.assertEqual((a + b).conjugate(), a.conjugate() + b.conjugate())

    def test_421_conjugate_is_multiplicitive(self, a, b):
        self.assertEqual((a * b).conjugate(), a.conjugate() * b.conjugate())

    def test_422_conjugate_has_same_absolute_value(self, a):
        self.assertEqual(abs(a.conjugate()), abs(a))

    def test_423_conjugate_has_same_real_value(self, a):
        self.assertEqual(a.conjugate().real, a.real)

    def test_424_conjugate_has_negated_imag_value(self, a):
        self.assertEqual(a.conjugate().imag, -a.imag)

    def test_425_imag_is_zero_iff_conjugate_equals_self(self, a):
        self.assertEqual(a == a.conjugate(), a.imag == self.real_zero)

    def test_426_absolute_value_real_and_imag_values(self, a):
        self.assertEqual(abs(a) * abs(a), a.real * a.real + a.imag * a.imag)


class RoundingTests(BaseTests):

    def test_430_round_is_integral(self, a):
        self.assertEqual(float(round(a)) % 1.0, 0.0)

    def test_431_round_is_close(self, a):
        self.assertLessEqual(abs(float(a) - float(round(a))), 0.5)

    def test_432_round_towards_even(self, a):
        round_result = round(a)
        self.assertImplies(self.isclose(abs(float(a) - float(round_result)), 0.5), round_result % 2.0 == 0)

    # It would be good to have tests of round(a, n), but can't do that yet

    def test_435_floor_definition(self, a):
        a_floor = math.floor(a)
        self.assertTrue(isinstance(a_floor, numbers.Integral))
        a_floor = float(a_floor)
        self.assertEqual(a_floor % 1.0, 0.0)  # floor is integral
        a_float = float(a)
        self.assertLessEqual(a_floor, a_float)
        self.assertLess(a_float - a_floor, 1.0)

    def test_436_ceil_definition(self, a):
        a_ceil = math.ceil(a)
        self.assertTrue(isinstance(a_ceil, numbers.Integral))
        a_ceil = float(a_ceil)
        self.assertEqual(a_ceil % 1.0, 0.0)  # ceil is integral
        a_float = float(a)
        self.assertLessEqual(a_float, a_ceil)
        self.assertLess(a_ceil - a_float, 1.0)

    def test_437_trunc_definition(self, a):
        a_trunc = math.trunc(a)
        self.assertTrue(isinstance(a_trunc, numbers.Real))
        a_trunc = float(a_trunc)
        if a < self.zero:
            self.assertEqual(a_trunc, float(math.ceil(a)))
        else:
            self.assertEqual(a_trunc, float(math.floor(a)))


class QuotientTests(BaseTests):

    def test_440_zero_terms(self):
        self.assertEqual(int(self.zero.numerator), 0)
        self.assertEqual(int(self.zero.denominator), 1)

    def test_441_one_terms(self):
        self.assertEqual(int(self.one.numerator), 1)
        self.assertEqual(int(self.one.denominator), 1)

    def test_442_numerator_carries_the_sign(self, a):
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

    def test_443_lowest_terms(self, a):
        assume(a != self.zero)
        self.assertEqual(QuotientTests._gcd(int(a.numerator), int(a.denominator)), 1)


__all__ = ('AdditiveMonoid',
           'FieldTests',
           'FloorDivModTests',
           'ExponentiationTests',
           'AbsoluteValueTests',
           'ConjugateTests',
           'RoundingTests',
           'QuotientTests')

"""
Copyright 2018 Steve Palmer
"""

import math
import numbers

from hypothesis import assume

from core import GenericTests, ClassUnderTest


class AdditiveMonoid(GenericTests):

    def test_generic_200_addition_associativity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        self.assertEqual(a + (b + c), (a + b) + c)

    def test_generic_201_additive_identity(self, a: ClassUnderTest) -> None:
        self.assertEqual(a + self.zero, a)
        self.assertEqual(self.zero + a, a)


class FieldTests(AdditiveMonoid):

    def test_generic_202_addition_inverse(self, a: ClassUnderTest) -> None:
        self.assertEqual(a + (-a), self.zero)

    def test_generic_203_addition_commutativity(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a + b, b + a)

    def test_generic_210_multiplication_associativity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        self.assertEqual(a * (b * c), (a * b) * c)

    def test_generic_211_multiplicative_identity(self, a: ClassUnderTest) -> None:
        self.assertEqual(a * self.one, a)
        self.assertEqual(self.one * a, a)

    def test_generic_212_multiplication_commutativity(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a * b, b * a)

    def test_generic_220_multiplication_addition_left_distributivity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        self.assertEqual(a * (b + c), (a * b) + (a * c))

    def test_generic_221_multiplication_addition_right_distributivity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        self.assertEqual((a + b) * c, (a * c) + (b * c))

    def test_generic_230_pos_definition(self, a: ClassUnderTest) -> None:
        self.assertEqual(+a, a)

    def test_generic_240_sub_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a - b, a + (-b))

    def test_generic_250_truediv_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        assume(b != self.zero)
        calc = (a / b) * b
        self.assertEqual(calc, type(calc)(a))


class FloorDivModTests(GenericTests):

    def test_generic_260_mod_range(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        assume(b != self.zero)
        rem = a % b
        if b <= self.zero:
            self.assertGreaterEqual(self.zero, rem)
            self.assertGreater(rem, b)
        else:
            self.assertLessEqual(self.zero, rem)
            self.assertLess(rem, b)

    def test_generic_261_floordiv_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        assume(b != self.zero)
        self.assertEqual((a // b) * b + a % b, a)

    def test_generic_262_divmod_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        assume(b != self.zero)
        self.assertEqual(divmod(a, b), (a // b, a % b))


class ExponentiationTests(GenericTests):
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

    def test_generic_270_exponentiation_zero_by_zero(self) -> None:
        # By Python defintion (Standard Library §4.4 note 5)
        self.assertEqual(self.zero ** self.zero, self.one)

    def test_generic_271_exponentiation_by_zero(self, a: ClassUnderTest) -> None:
        assume(a != self.zero)
        self.assertEqual(a ** self.zero, self.one)

    def test_generic_272_exponentiation_with_base_zero(self, a: ClassUnderTest) -> None:
        assume(a > self.zero)
        self.assertEqual(self.zero ** a, self.zero)

    def test_generic_273_exponentiation_with_base_one(self, a: ClassUnderTest) -> None:
        assume(a != self.zero)
        self.assertEqual(self.one ** a, self.one)

    def test_generic_274_exponentiation_by_one(self, a: ClassUnderTest) -> None:
        assume(a != self.zero)
        self.assertEqual(a ** self.one, a)


class AbsoluteValueTests(GenericTests):

    def test_generic_400_abs_not_negative(self, a: ClassUnderTest) -> None:
        self.assertTrue(self.real_zero <= abs(a))

    def test_generic_401_abs_positve_definite(self, a: ClassUnderTest) -> None:
        self.assertEqual(abs(a) == self.real_zero, a == self.zero)

    def test_generic_402_abs_one_is_one(self) -> None:
        self.assertEqual(abs(self.one), self.one)

    def test_generic_410_abs_is_multiplicitive(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(abs(a * b), abs(a) * abs(b))

    def test_generic_411_abs_is_subadditive(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertLessEqual(abs(a + b), abs(a) + abs(b))


class ConjugateTests(GenericTests):

    def test_generic_420_conjugate_is_additive(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual((a + b).conjugate(), a.conjugate() + b.conjugate())

    def test_generic_421_conjugate_is_multiplicitive(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual((a * b).conjugate(), a.conjugate() * b.conjugate())

    def test_generic_422_conjugate_has_same_absolute_value(self, a: ClassUnderTest) -> None:
        self.assertEqual(abs(a.conjugate()), abs(a))

    def test_generic_423_conjugate_has_same_real_value(self, a: ClassUnderTest) -> None:
        self.assertEqual(a.conjugate().real, a.real)

    def test_generic_424_conjugate_has_negated_imag_value(self, a: ClassUnderTest) -> None:
        self.assertEqual(a.conjugate().imag, -a.imag)

    def test_generic_425_imag_is_zero_iff_conjugate_equals_self(self, a: ClassUnderTest) -> None:
        self.assertEqual(a == a.conjugate(), a.imag == self.real_zero)

    def test_generic_426_absolute_value_real_and_imag_values(self, a: ClassUnderTest) -> None:
        self.assertEqual(abs(a) * abs(a), a.real * a.real + a.imag * a.imag)


class RoundingTests(GenericTests):

    def test_generic_430_round_is_integral(self, a: ClassUnderTest) -> None:
        self.assertEqual(float(round(a)) % 1.0, 0.0)

    def test_generic_431_round_is_close(self, a: ClassUnderTest) -> None:
        self.assertLessEqual(abs(float(a) - float(round(a))), 0.5)

    def test_generic_432_round_towards_even(self, a: ClassUnderTest) -> None:
        round_result = round(a)
        self.assertImplies(self.isclose(abs(float(a) - float(round_result)), 0.5), round_result % 2.0 == 0)

    # It would be good to have tests of round(a, n), but can't do that yet

    def test_generic_435_floor_definition(self, a: ClassUnderTest) -> None:
        a_floor = math.floor(a)
        self.assertTrue(isinstance(a_floor, numbers.Integral))
        a_floor = float(a_floor)
        self.assertEqual(a_floor % 1.0, 0.0)  # floor is integral
        a_float = float(a)
        self.assertLessEqual(a_floor, a_float)
        self.assertLess(a_float - a_floor, 1.0)

    def test_generic_436_ceil_definition(self, a: ClassUnderTest) -> None:
        a_ceil = math.ceil(a)
        self.assertTrue(isinstance(a_ceil, numbers.Integral))
        a_ceil = float(a_ceil)
        self.assertEqual(a_ceil % 1.0, 0.0)  # ceil is integral
        a_float = float(a)
        self.assertLessEqual(a_float, a_ceil)
        self.assertLess(a_ceil - a_float, 1.0)

    def test_generic_437_trunc_definition(self, a: ClassUnderTest) -> None:
        a_trunc = math.trunc(a)
        self.assertTrue(isinstance(a_trunc, numbers.Real))
        a_trunc = float(a_trunc)
        if a < self.zero:
            self.assertEqual(a_trunc, float(math.ceil(a)))
        else:
            self.assertEqual(a_trunc, float(math.floor(a)))


class QuotientTests(GenericTests):

    def test_generic_440_zero_terms(self) -> None:
        self.assertEqual(int(self.zero.numerator), 0)
        self.assertEqual(int(self.zero.denominator), 1)

    def test_generic_441_one_terms(self) -> None:
        self.assertEqual(int(self.one.numerator), 1)
        self.assertEqual(int(self.one.denominator), 1)

    def test_generic_442_numerator_carries_the_sign(self, a: ClassUnderTest) -> None:
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

    def test_generic_443_lowest_terms(self, a: ClassUnderTest) -> None:
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

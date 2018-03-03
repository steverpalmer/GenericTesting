"""
Copyright 2018 Steve Palmer

A library of generic test for the elementary operators...
 * __add__
 * __neg__, __sub__, __pos__ and __mul__
 * __invert__, __xor__ (in terms of __or__ and __and__)
"""

import abc

from hypothesis import assume

from core import GenericTests, ClassUnderTest


class AdditiveMonoidTests(GenericTests):
    """
    Tests of the simplest semantics of the __add__ operator;
    essentially a list concatenation
    """

    @property
    @abc.abstractmethod
    def zero(self) -> ClassUnderTest:
        pass


    def test_generic_2220_addition_associativity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        self.assertEqual(a + (b + c), (a + b) + c)

    def test_generic_2221_additive_identity(self, a: ClassUnderTest) -> None:
        self.assertEqual(a + self.zero, a)
        self.assertEqual(self.zero + a, a)


class RingTests(AdditiveMonoidTests):
    """
    Extends AdditiveMonoid by:
    * adding operators __neg__ and __mul__
    * adding operators __sub__ and __pos__
    * extending the sematics to a Ring.
    """

    @property
    @abc.abstractmethod
    def one(self) -> ClassUnderTest:
        pass

    def test_generic_2230_addition_inverse(self, a: ClassUnderTest) -> None:
        self.assertEqual(a + (-a), self.zero)

    def test_generic_2231_addition_commutativity(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a + b, b + a)

    def test_generic_2232_pos_definition(self, a: ClassUnderTest) -> None:
        self.assertEqual(+a, a)

    def test_generic_2233_sub_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a - b, a + (-b))

    def test_generic_2234_multiplication_associativity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        self.assertEqual(a * (b * c), (a * b) * c)

    def test_generic_2235_multiplicative_identity(self, a: ClassUnderTest) -> None:
        self.assertEqual(a * self.one, a)
        self.assertEqual(self.one * a, a)

    def test_generic_2237_multiplication_addition_left_distributivity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        self.assertEqual(a * (b + c), (a * b) + (a * c))

    def test_generic_2238_multiplication_addition_right_distributivity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        self.assertEqual((a + b) * c, (a * c) + (b * c))


class CommutativeRingTests(RingTests):
    """
    Extends Ring to a Commutative Ring.
    """

    def test_generic_2236_multiplication_commutativity(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a * b, b * a)


class FieldTests(CommutativeRingTests):
    """
    Extends Commutative Ring to a Field.
    """

    def test_generic_2239_truediv_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        assume(not b == self.zero)
        calc = (a / b) * b
        self.assertEqual(calc, type(calc)(a))


class FloorDivModTests(GenericTests):
    """
    Discrete tests for __floordiv__, __mod__ and __divmod__

    It is assumed that these will be inherited along with
    one of the above test, so don't bother redefining zero and one
    """

    def test_generic_2240_mod_range(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        assume(not b == self.zero)
        rem = a % b
        if b <= self.zero:
            self.assertGreaterEqual(self.zero, rem)
            self.assertGreater(rem, b)
        else:
            self.assertLessEqual(self.zero, rem)
            self.assertLess(rem, b)

    def test_generic_2241_floordiv_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        assume(not b == self.zero)
        self.assertEqual((a // b) * b + a % b, a)

    def test_generic_2242_divmod_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        assume(not b == self.zero)
        self.assertEqual(divmod(a, b), (a // b, a % b))


class ExponentiationTests(GenericTests):
    """
    Discrete tests of __pow__

    It is assumed that these will be inherited along with
    one of the above test, so don't bother redefining zero and one

    These tests are very incomplete.  It is tempting to include identities such as:
        1. a ** (b + c)  == a ** b * a ** c
        2. (a * b) ** c  == a ** c * b ** c
        3. (a ** b) ** c == a ** (b * c)

    However:
        1. these identities are only true for certain types.  E.g. items 3 is not true for Reals
        2. with ints (for which they are true), the full range maths kills the preformance.

    So, for now these are not tested...
    """

    def test_generic_2250_exponentiation_zero_by_zero(self) -> None:
        # By Python defintion (Standard Library §4.4 note 5)
        self.assertEqual(self.zero ** self.zero, self.one)

    def test_generic_2251_exponentiation_by_zero(self, a: ClassUnderTest) -> None:
        assume(not a == self.zero)
        self.assertEqual(a ** self.zero, self.one)

    def test_generic_2252_exponentiation_with_base_zero(self, a: ClassUnderTest) -> None:
        assume(a > self.zero)
        self.assertEqual(self.zero ** a, self.zero)

    def test_generic_2253_exponentiation_with_base_one(self, a: ClassUnderTest) -> None:
        assume(not a == self.zero)
        self.assertEqual(self.one ** a, self.one)

    def test_generic_2254_exponentiation_by_one(self, a: ClassUnderTest) -> None:
        assume(not a == self.zero)
        self.assertEqual(a ** self.one, a)


class AbsoluteValueTests(GenericTests):
    """
    Discrete tests of __abs__

    It is assumed that these will be inherited along with
    one of the above test, so don't bother redefining zero and one
    
    However, since abs delivers a value of a different type,
    we need a real value for zero.
    """

    @property
    @abc.abstractmethod
    def real_zero(self) -> ClassUnderTest:
        pass

    def test_generic_2270_abs_not_negative(self, a: ClassUnderTest) -> None:
        self.assertTrue(self.real_zero <= abs(a))

    def test_generic_2271_abs_positve_definite(self, a: ClassUnderTest) -> None:
        self.assertEqual(abs(a) == self.real_zero, a == self.zero)

    def test_generic_2272_abs_one_is_one(self) -> None:
        self.assertEqual(abs(self.one), self.one)

    def test_generic_2273_abs_is_multiplicitive(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(abs(a * b), abs(a) * abs(b))

    def test_generic_2274_abs_is_subadditive(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertLessEqual(abs(a + b), abs(a) + abs(b))


__all__ = ('AdditiveMonoid', 'Ring', 'CommutatuveRing', 'FieldTests', 'FieldTests',
           'FloorDivModTests', 'ExponentiationTests', 'AbsoluteValueTests')

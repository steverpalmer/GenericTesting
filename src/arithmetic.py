# Copyright 2018 Steve Palmer

"""
A library of generic test for the elementary operators...
 * __add__
 * __neg__, __sub__, __pos__ and __mul__
 * __invert__, __xor__ (in terms of __or__ and __and__)
"""

import abc

from hypothesis import assume

from .core import GenericTests, ClassUnderTest


class AdditionMonoidTests(GenericTests):
    """
    Tests of the simplest (Monoid) semantics of the __add__ operator;
    essentially a list concatenation

    See https://en.wikipedia.org/wiki/Monoid
    """

    @property
    @abc.abstractmethod
    def zero(self) -> ClassUnderTest:
        pass

    @abc.abstractmethod
    def test_generic_2020_zero_type(self) -> None:
        self.fail("Need to define a test that the helper zero has the correct type")

    def test_generic_2220_addition_associativity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        "a + (b + c) == (a + b) + c"
        self.assertEqual(a + (b + c), (a + b) + c)

    def test_generic_2221_addition_identity(self, a: ClassUnderTest) -> None:
        "a + 0 == a == 0 + a"
        self.assertEqual(a + self.zero, a)
        self.assertEqual(self.zero + a, a)


class AdditionGroupTests(AdditionMonoidTests):
    """
    Tests of the Group semantics of the __add__ operator

    See https://en.wikipedia.org/wiki/Group_(mathematics)
    """

    def test_generic_2230_addition_inverse(self, a: ClassUnderTest) -> None:
        "a + (-a) == 0"
        self.assertEqual(a + (-a), self.zero)


class AdditionAbelianGroupTests(AdditionGroupTests):
    """
    See https://en.wikipedia.org/wiki/Abelian_group
    """

    def test_generic_2231_addition_commutativity(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        "a + b == b + a"
        self.assertEqual(a + b, b + a)


AdditionCommutativeGroupTests = AdditionAbelianGroupTests


class MultiplicationMonoidTests(GenericTests):
    """
    Tests of the simplest semantics of the __mul__ operator;
    essentially a list concatenation

    See https://en.wikipedia.org/wiki/Monoid
    """

    @property
    @abc.abstractmethod
    def one(self) -> ClassUnderTest:
        pass

    @abc.abstractmethod
    def test_generic_2021_one_type(self) -> None:
        self.fail("Need to define a test that the helper one has the correct type")

    def test_generic_2234_multiplication_associativity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        "a * (b * c) == (a * b) * c"
        self.assertEqual(a * (b * c), (a * b) * c)

    def test_generic_2235_multiplication_identity(self, a: ClassUnderTest) -> None:
        "a * 1 == 1 == 1 * a"
        self.assertEqual(a * self.one, a)
        self.assertEqual(self.one * a, a)


class RingTests(AdditionAbelianGroupTests, MultiplicationMonoidTests):
    """
    See https://en.wikipedia.org/wiki/Ring_(mathematics)
    """

    def test_generic_2105_not_zero_equal_one(self) -> None:
        "0 != 1"
        self.assertFalse(self.zero == self.one)

    def test_generic_2232_pos_definition(self, a: ClassUnderTest) -> None:
        "+a == a"
        self.assertEqual(+a, a)

    def test_generic_2233_sub_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        "a - b == a + (-b)"
        self.assertEqual(a - b, a + (-b))

    def test_generic_2237_multiplication_addition_left_distributivity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        "a * (b + c) == (a * b) + (a * c)"
        self.assertEqual(a * (b + c), (a * b) + (a * c))

    def test_generic_2238_multiplication_addition_right_distributivity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        "(a + b) * c = (a * c) + (b * c)"
        self.assertEqual((a + b) * c, (a * c) + (b * c))


class CommutativeRingTests(RingTests):
    """
    See https://en.wikipedia.org/wiki/Commutative_ring
    """

    def test_generic_2236_multiplication_commutativity(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        "a * b == b * a"
        self.assertEqual(a * b, b * a)


class FieldTests(CommutativeRingTests):
    """
    See https://en.wikipedia.org/wiki/Field_(mathematics)
    """

    def test_generic_2239_truediv_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        "b != 0 ⇒ (a / b) * b == a"
        assume(not b == self.zero)
        calc = (a / b) * b
        self.assertEqual(calc, type(calc)(a))


class FloorDivModTests(GenericTests):
    """
    Discrete tests for __floordiv__, __mod__ and __divmod__

    It is assumed that these will be inherited along with
    one of the above test, so don't bother redefining zero and one.

    I quietly assume that the result type of __floordiv__ can be used in mixed arithmetic
    with the ClassUnderTest.
    """

    def test_generic_2240_mod_range(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        "b != 0 ⇒ a % b ∈ [0 .. b)"
        assume(not b == self.zero)
        mod = a % b
        if b <= self.zero:
            self.assertGreaterEqual(self.zero, mod)
            self.assertGreater(mod, b)
        else:
            self.assertLessEqual(self.zero, mod)
            self.assertLess(mod, b)

    def test_generic_2241_floordiv_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        "b != 0 ⇒ (a // b) * b + (a % b) == a"
        assume(not b == self.zero)
        self.assertEqual((a // b) * b + a % b, a)

    def test_generic_2242_divmod_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        "b != 0 ⇒ divmod(a, b) == (a // b, a % b)"
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
        "0 ** 0 == 1"
        # By Python defintion (Standard Library §4.4 note 5)
        self.assertEqual(self.zero ** self.zero, self.one)

    def test_generic_2251_exponentiation_by_zero(self, a: ClassUnderTest) -> None:
        "not a == 0 ⇒ a ** 0 == 1"
        assume(not a == self.zero)
        self.assertEqual(a ** self.zero, self.one)

    def test_generic_2252_exponentiation_with_base_zero(self, a: ClassUnderTest) -> None:
        "a > 0 ⇒ 0 ** a == 0"
        assume(a > self.zero)
        self.assertEqual(self.zero ** a, self.zero)

    def test_generic_2253_exponentiation_with_base_one(self, a: ClassUnderTest) -> None:
        "not a == 0 ⇒ 1 ** a == 1"
        assume(not a == self.zero)
        self.assertEqual(self.one ** a, self.one)

    def test_generic_2254_exponentiation_by_one(self, a: ClassUnderTest) -> None:
        "not a == 0 ⇒ a ** 1 == a"
        assume(not a == self.zero)
        self.assertEqual(a ** self.one, a)


class AbsoluteValueTests(GenericTests):
    """
    Discrete tests of __abs__

    It is assumed that these will be inherited along with
    one of the above test, so I don't bother redefining zero and one

    However, since abs may deliver a value of a different type,
    we need a zero value in the abs() type.
    I define a default value "abs(zero)", but it can be overwritten in a derived class.
    """

    @property
    def abs_zero(self) -> ClassUnderTest:
        return abs(self.zero)

    def test_generic_2030_abs_zero_type(self) -> None:
        self.assertIsInstance(self.abs_zero, type(abs(self.zero)))

    def test_generic_2270_abs_not_negative(self, a: ClassUnderTest) -> None:
        "0 <= abs(a)"
        self.assertTrue(self.abs_zero <= abs(a))

    def test_generic_2271_abs_positve_definite(self, a: ClassUnderTest) -> None:
        "abs(a) == 0 ⇔ a == 0"
        self.assertEqual(abs(a) == self.abs_zero, a == self.zero)

    def test_generic_2273_abs_is_multiplicitive(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        "abs(a * b) == abs(a) * abs(b)"
        self.assertEqual(abs(a * b), abs(a) * abs(b))

    def test_generic_2274_abs_is_subadditive(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        "abs(a + b) <= abs(a) + abs(b)"
        self.assertLessEqual(abs(a + b), abs(a) + abs(b))


__all__ = ('AdditionMonoidTests', 'AdditionGroupTests', 'AdditionAbelianGroupTests', 'AdditionCommutativeGroupTests',
           'MultiplicationMonoidTests', 'RingTests', 'CommutativeRingTests', 'FieldTests',
           'FloorDivModTests', 'ExponentiationTests', 'AbsoluteValueTests')

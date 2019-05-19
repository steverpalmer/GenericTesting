# Copyright 2018 Steve Palmer

"""A library of generic test for the elementary arithmetic operators."""

import abc

from hypothesis import assume

from generic_testing.core import GenericTests, ClassUnderTest


class AdditionMonoidTests(GenericTests):
    """Tests of the simplest (Monoid) semantics of the __add__ operator.

    Essentially the arguments of __add_ form a list
    See https://en.wikipedia.org/wiki/Monoid
    """

    @property
    @abc.abstractmethod
    def zero(self) -> ClassUnderTest:
        """Addition Identity Value."""

    def test_generic_2220_addition_associativity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        """a + (b + c) == (a + b) + c"""
        self.assertEqual(a + (b + c), (a + b) + c)

    def test_generic_2221_addition_identity(self, a: ClassUnderTest) -> None:
        """a + 0 == a == 0 + a"""
        self.assertEqual(a + self.zero, a)
        self.assertEqual(self.zero + a, a)


class AdditionGroupTests(AdditionMonoidTests):
    """Tests of the Group semantics of the __add__ operator.

    See https://en.wikipedia.org/wiki/Group_(mathematics)
    """

    def test_generic_2230_addition_inverse(self, a: ClassUnderTest) -> None:
        """a + (-a) == 0"""
        self.assertEqual(a + (-a), self.zero)


class AdditionAbelianGroupTests(AdditionGroupTests):
    """Tests of the Abelian Group semantics of the __add__ operator.

    See https://en.wikipedia.org/wiki/Abelian_group
    """

    def test_generic_2231_addition_commutativity(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """a + b == b + a"""
        self.assertEqual(a + b, b + a)


AdditionCommutativeGroupTests = AdditionAbelianGroupTests


class MultiplicationMonoidTests(GenericTests):
    """Tests of the simplest (Monoid) semantics of the __mul__ operator.

    Essentially the arguments of __mul_ form a list
    See https://en.wikipedia.org/wiki/Monoid
    """

    @property
    @abc.abstractmethod
    def one(self) -> ClassUnderTest:
        """Multiplication Identity Value."""

    def test_generic_2234_multiplication_associativity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        """a * (b * c) == (a * b) * c"""
        self.assertEqual(a * (b * c), (a * b) * c)

    def test_generic_2235_multiplication_identity(self, a: ClassUnderTest) -> None:
        """a * 1 == 1 == 1 * a"""
        self.assertEqual(a * self.one, a)
        self.assertEqual(self.one * a, a)


class AdditionExtensionsTests:
    """Discrete tests of the __pos__ and __sub__ methods."""

    def test_generic_2232_pos_definition(self, a: ClassUnderTest) -> None:
        """+a == a"""
        self.assertEqual(+a, a)

    def test_generic_2233_sub_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """a - b == a + (-b)"""
        self.assertEqual(a - b, a + (-b))


class RingTests(AdditionAbelianGroupTests, AdditionExtensionsTests, MultiplicationMonoidTests):
    """Tests of the Ring semantics of the basic arithmetic operators.

    See https://en.wikipedia.org/wiki/Ring_(mathematics)
    """

    def test_generic_2105_not_zero_equal_one(self) -> None:
        """0 != 1"""
        self.assertFalse(self.zero == self.one)

    def test_generic_2237_multiplication_addition_left_distributivity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        """a * (b + c) == (a * b) + (a * c)"""
        self.assertEqual(a * (b + c), (a * b) + (a * c))

    def test_generic_2238_multiplication_addition_right_distributivity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        """(a + b) * c = (a * c) + (b * c)"""
        self.assertEqual((a + b) * c, (a * c) + (b * c))


class CommutativeRingTests(RingTests):
    """Tests of the Commutative Ring semantics of the basic arithmetic operators.

    See https://en.wikipedia.org/wiki/Commutative_ring
    """

    def test_generic_2239_multiplication_commutativity(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """a * b == b * a"""
        self.assertEqual(a * b, b * a)


class FieldTests(CommutativeRingTests):
    """Tests of the Field semantics of the basic arithmetic operators.

    See https://en.wikipedia.org/wiki/Field_(mathematics)
    """

    def test_generic_2245_truediv_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """b != 0 ⇒ (a / b) * b == a"""
        assume(not b == self.zero)
        calc = (a / b) * b
        self.assertEqual(calc, type(calc)(a))


class FloorDivModTests(GenericTests):
    """Discrete tests for __floordiv__, __mod__ and __divmod__ operators.

    It is assumed that these will be inherited along with
    one of the above test, so don't bother redefining zero and one.

    I quietly assume that the result type of __floordiv__ can be used in mixed arithmetic
    with the ClassUnderTest.
    """

    def test_generic_2246_mod_range(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """b != 0 ⇒ a % b ∈ [0 .. b)"""
        assume(not b == self.zero)
        mod = a % b
        if b <= self.zero:
            self.assertGreaterEqual(self.zero, mod)
            self.assertGreater(mod, b)
        else:
            self.assertLessEqual(self.zero, mod)
            self.assertLess(mod, b)

    def test_generic_2247_floordiv_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """b != 0 ⇒ (a // b) * b + (a % b) == a"""
        assume(not b == self.zero)
        self.assertEqual((a // b) * b + a % b, a)

    def test_generic_2248_divmod_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """b != 0 ⇒ divmod(a, b) == (a // b, a % b)"""
        assume(not b == self.zero)
        self.assertEqual(divmod(a, b), (a // b, a % b))


class ExponentiationTests(GenericTests):
    """Discrete tests of __pow__ operator.

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
        """0 ** 0 == 1"""
        # By Python defintion (Standard Library §4.4 note 5)
        self.assertEqual(self.zero ** self.zero, self.one)

    def test_generic_2251_exponentiation_by_zero(self, a: ClassUnderTest) -> None:
        """a != 0 ⇒ a ** 0 == 1"""
        assume(not a == self.zero)
        self.assertEqual(a ** self.zero, self.one)

    def test_generic_2252_exponentiation_with_base_zero(self, a: ClassUnderTest) -> None:
        """a > 0 ⇒ 0 ** a == 0"""
        assume(a > self.zero)
        self.assertEqual(self.zero ** a, self.zero)

    def test_generic_2253_exponentiation_with_base_one(self, a: ClassUnderTest) -> None:
        """a != 0 ⇒ 1 ** a == 1"""
        assume(not a == self.zero)
        self.assertEqual(self.one ** a, self.one)

    def test_generic_2254_exponentiation_by_one(self, a: ClassUnderTest) -> None:
        """a != 0 ⇒ a ** 1 == a"""
        assume(not a == self.zero)
        self.assertEqual(a ** self.one, a)


class AbsoluteValueTests(GenericTests):
    """Discrete tests of __abs__ operator.

    It is assumed that these will be inherited along with
    one of the above test, so I don't bother redefining zero and one

    However, since abs may deliver a value of a different type,
    we need a zero value in the abs() type.
    I define a default value "abs(zero)", but it can be overwritten in a derived class.
    """

    @property
    def abs_zero(self) -> ClassUnderTest:
        """abs(0)"""
        return abs(self.zero)

    def test_generic_2270_abs_not_negative(self, a: ClassUnderTest) -> None:
        """0 <= abs(a)"""
        self.assertTrue(self.abs_zero <= abs(a))

    def test_generic_2271_abs_positve_definite(self, a: ClassUnderTest) -> None:
        """abs(a) == 0 ⇔ a == 0"""
        self.assertEqual(abs(a) == self.abs_zero, a == self.zero)

    def test_generic_2273_abs_is_multiplicitive(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """abs(a * b) == abs(a) * abs(b)"""
        self.assertEqual(abs(a * b), abs(a) * abs(b))

    def test_generic_2274_abs_is_subadditive(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """abs(a + b) <= abs(a) + abs(b)"""
        self.assertLessEqual(abs(a + b), abs(a) + abs(b))


ScalarT = 'ScalarT'


class RModuleTests(AdditionAbelianGroupTests):
    """Test of the R-Module Semantics of the __add__ and __mul__ operators.

    A distinction in this case is the the __mul__ operator takes a scalar and a value
    This a generalization of a Vector Space used for types like timedelta.
    See https://en.wikipedia.org/wiki/Module_(mathematics)
    """

    @property
    @abc.abstractmethod
    def scalar_one(self) -> ScalarT:
        """Multiplication Identity Value."""

    def test_generic_2234_multiplication_associativity(self, r: ScalarT, s: ScalarT, a: ClassUnderTest) -> None:
        """(r * s) * a == (r * (s * a)"""
        self.assertEqual((r * s) * a, r * (s * a))

    def test_generic_2235_multiplication_identity(self, a: ClassUnderTest) -> None:
        """1 * a == a"""
        self.assertEqual(self.scalar_one * a, a)

    def test_generic_2237_multiplication_addition_left_distributivity(self, r: ScalarT, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """r * (a + b) == (r * a) + (r * b)"""
        self.assertEqual(r * (a + b), r * a + r * b)

    def test_generic_2239_multiplication_commutativity(self, r: ScalarT, a: ClassUnderTest) -> None:
        """r * a == a * r"""
        self.assertEqual(r * a, a * r)

    def test_generic_2240_r_module_multiplication_addition_left_distributivity(self, r: ScalarT, s: ScalarT, a: ClassUnderTest) -> None:
        """(r + s) * a == (r * a) + (s * a)"""
        self.assertEqual((r + s) * a, r * a + s * a)


class VectorSpaceTests(RModuleTests, AdditionExtensionsTests):
    """Tests of the Vector Space semantics of the basic arithmetic operators.

    See https://en.wikipedia.org/wiki/Vector_space

    Strictly, a vector space multiplication need not be commutative (r * a) == (a * r),
    but in the programming world, most examples are (e.g. timedelta).
    """

    @property
    def scalar_zero(self) -> ScalarT:
        """Zero in the scalar type."""
        return self.scalar_one - self.scalar_one

    def test_generic_2245_truediv_definition(self, r: ScalarT, a: ClassUnderTest) -> None:
        """r != 0 ⇒ (a / r) == (1 / r) * a"""
        assume(not r == self.scalar_zero)
        self.assertEqual(a / r, (self.scalar_one / r) * a)


VectorSpaceT = 'VectorSpaceT'


class AffineSpaceTests:
    """Tests of the Affine Space semantics of the basic operators.

    See https://en.wikipedia.org/wiki/Affine_space
    """

    @property
    @abc.abstractmethod
    def vector_space_zero(self) -> VectorSpaceT:
        """Addition Identity Value."""

    def test_generic_2220_addition_associativity(self, a: ClassUnderTest, b: VectorSpaceT, c: VectorSpaceT) -> None:
        """a + (b + c) == (a + b) + c"""
        self.assertEqual(a + (b + c), (a + b) + c)

    def test_generic_2221_addition_identity(self, a: ClassUnderTest) -> None:
        """a + 0 == a"""
        self.assertEqual(a + self.vector_space_zero, a)

    # This may be derivable from the others, but I don't see how
    def test_generic_2290_sub_distributivity(self, a: ClassUnderTest, b: ClassUnderTest, v: VectorSpaceT, w: VectorSpaceT) -> None:
        """(a + v) - (b + w) == (a - b) + (v - w)"""
        self.assertEqual((a + v) - (b + w), (a - b) + (v - w))

    # This may be derivable from the others, but I don't see how
    def test_generic_2291_sub_special_case_1(self, a: ClassUnderTest) -> None:
        """a - a == 0"""
        self.assertEqual(a - a, self.vector_space_zero)

    def test_generic_2292_sub_special_case_2(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """a + (b - a) == b"""
        self.assertEqual(a + (b - a), b)


__all__ = ('AdditionMonoidTests', 'AdditionGroupTests', 'AdditionAbelianGroupTests', 'AdditionCommutativeGroupTests',
           'MultiplicationMonoidTests', 'RingTests', 'CommutativeRingTests', 'FieldTests',
           'FloorDivModTests', 'ExponentiationTests', 'AbsoluteValueTests', 'AdditionExtensionsTests',
           'ScalarT', 'RModuleTests', 'VectorSpaceTests', 'VectorSpaceT', 'AffineSpaceTests')

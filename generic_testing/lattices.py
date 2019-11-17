# Copyright 2018 Steve Palmer

"""A library of generic test for the elementary bitwise operators."""

import abc

from hypothesis import assume

from .core import GenericTests, ClassUnderTest


class LatticeOrTests(GenericTests):
    """Tests of the __or__ operator."""

    def test_generic_2200_or_commutativity(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """a | b == b | a"""
        self.assertEqual(a | b, b | a)

    def test_generic_2201_or_associativity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        """a | (b | c) == (a | b) | c"""
        self.assertEqual(a | (b | c), (a | b) | c)


class LatticeAndTests(GenericTests):
    """Tests of the __or__ operator."""

    def test_generic_2205_and_commutativity(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """a & b == b & a"""
        self.assertEqual(a & b, b & a)

    def test_generic_2206_and_associativity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        """a & (b & c) == (a & b) & c"""
        self.assertEqual(a & (b & c), (a & b) & c)


class LatticeTests(LatticeOrTests, LatticeAndTests):
    """Tests of the __or__ and __and__ operators."""

    def test_generic_2203_or_and_absorption(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """a | (a & b) == a"""
        self.assertEqual(a | (a & b), a)

    def test_generic_2208_and_or_absorption(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """a & (a | b) == a"""
        self.assertEqual(a & (a | b), a)

    def test_generic_2209_and_or_distributive(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        """a & (b | c) == (a & b) | (a & c)"""
        self.assertEqual(a & (b | c), a & b | a & c)


class BoundedBelowLatticeTests(LatticeTests):
    """Extends the LatticeTests to include a (lowest bound) "bottom"."""

    @property
    @abc.abstractmethod
    def bottom(self) -> ClassUnderTest:
        """Lowest bound value."""

    def test_generic_2202_or_identity(self, a: ClassUnderTest) -> None:
        """a | ⊥ == a"""
        self.assertEqual(a | self.bottom, a)


class BoundedLatticeTests(BoundedBelowLatticeTests):
    """Extends the LatticeTests to include a (highest bound) "top"."""

    @property
    @abc.abstractmethod
    def top(self) -> ClassUnderTest:
        """Highest bound value."""

    def test_generic_2207_and_identity(self, a: ClassUnderTest) -> None:
        """a & ⊤ = a"""
        self.assertEqual(a & self.top, a)


class LatticeWithComplementTests(BoundedLatticeTests):
    """Tests of the __invert__ and __xor__ operators.

    Since these tests are defined in terms of a Bounded Lattice,
    it inherits the BoundedLatticeTests
    """

    def test_generic_2210_or_complementation(self, a: ClassUnderTest) -> None:
        """a | ~a == T"""
        self.assertEqual(a | ~a, self.top)

    def test_generic_2211_and_complementation(self, a: ClassUnderTest) -> None:
        """a & ~a == ⊥"""
        self.assertEqual(a & ~a, self.bottom)

    def test_generic_2215_xor_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """a ^ b == (a | b) & ~(a & b)"""
        self.assertEqual(a ^ b, (a | b) & ~(a & b))


class BitShiftTests(GenericTests):
    """Tests of the __lshift__ and __rshift__ operators.

    Arguably, these operators are more to do with numbers than "lattices", but they need to be put somewhere.
    """

    def test_generic_2390_lshift_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """0 <= b ⇒ a << b == a * pow(2, b)"""
        assume(self.zero <= b)
        self.assertEqual(a << b, a * pow(self.one + self.one, b))

    def test_generic_2391_rshift_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """0 <= b ⇒ a >> b == a // pow(2, b)"""
        assume(self.zero <= b)
        self.assertEqual(a >> b, a // pow(self.one + self.one, b))


__all__ = ('LatticeOrTests', 'LatticeAndTests', 'LatticeTests', 'BoundedBelowLatticeTests', 'BoundedLatticeTests', 'LatticeWithComplementTests',
           'BitShiftTests')

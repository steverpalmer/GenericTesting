"""
Copyright 2018 Steve Palmer

A library of generic test for the elementary operators...
 * __or__, __and__
 * __invert__, __xor__ (in terms of __or__ and __and__)
"""


import abc

from core import GenericTests, ClassUnderTest


class LatticeTests(GenericTests):
    """
    Tests of the __or__ and __and__ operators.
    """

    def test_generic_2200_or_commutativity(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a | b, b | a)

    def test_generic_2201_or_associativity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        self.assertEqual(a | (b | c), (a | b) | c)

    def test_generic_2203_or_and_absorption(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a | (a & b), a)

    def test_generic_2205_and_commutativity(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a & b, b & a)

    def test_generic_2206_and_associativity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        self.assertEqual(a & (b & c), (a & b) & c)

    def test_generic_2208_and_or_absorption(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a & (a | b), a)

    def test_generic_2209_and_or_distributive(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        self.assertEqual(a & (b | c), a & b | a & c)


class BoundedBelowLatticeTests(LatticeTests):
    """
    Extends the LatticeTests to include a (lowest bound) "bottom".
    """

    @property
    @abc.abstractmethod
    def bottom(self) -> ClassUnderTest:
        pass

    def test_generic_2202_or_identity(self, a: ClassUnderTest) -> None:
        self.assertEqual(a | self.bottom, a)


class BoundedLatticeTests(BoundedBelowLatticeTests):
    """
    Extends the LatticeTests to include a (highest bound) "top".
    """

    @property
    @abc.abstractmethod
    def top(self) -> ClassUnderTest:
        pass

    def test_generic_2207_and_identity(self, a: ClassUnderTest) -> None:
        self.assertEqual(a & self.top, a)


class LatticeWithComplement(BoundedLatticeTests):
    """
    Tests of the __invert__ and __xor__ operators.

    Since these tests are defined in terms of a Bounded Lattice,
    it inherits the BoundedLatticeTests
    """

    def test_generic_2210_or_complementation(self, a: ClassUnderTest) -> None:
        self.assertEqual(a | ~a, self.top)

    def test_generic_2211_and_complementation(self, a: ClassUnderTest) -> None:
        self.assertEqual(a & ~a, self.bottom)

    def test_generic_2215_xor_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a ^ b, (a | b) & ~(a & b))


__all__ = ('LatticeTests', 'BoundedBelowLatticeTests', 'BoundedLatticeTests', 'LatticeWithComplement')
"""
Copyright 2018 Steve Palmer
"""


import abc

from core import BaseTests, ClassUnderTest


class LatticeTests(BaseTests):

    def test_500_or_commutativity(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a | b, b | a)

    def test_501_or_associativity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        self.assertEqual(a | (b | c), (a | b) | c)

    def test_502_or_and_absorption(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a | (a & b), a)

    def test_510_and_commutativity(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a & b, b & a)

    def test_511_and_associativity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        self.assertEqual(a & (b & c), (a & b) & c)

    def test_512_and_or_absorption(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a & (a | b), a)

    def test_520_and_or_distributive(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        self.assertEqual(a & (b | c), a & b | a & c)


class BoundedBelowLatticeTests(LatticeTests):

    @property
    @abc.abstractmethod
    def bottom(self) -> ClassUnderTest:
        pass

    def test_530_or_identity(self, a: ClassUnderTest) -> None:
        self.assertEqual(a | self.bottom, a)


class BoundedLatticeTests(BoundedBelowLatticeTests):

    @property
    @abc.abstractmethod
    def top(self) -> ClassUnderTest:
        pass

    def test_531_and_identity(self, a: ClassUnderTest) -> None:
        self.assertEqual(a & self.top, a)


class LatticeWithComplement(BoundedLatticeTests):


    def test_540_or_complementation(self, a: ClassUnderTest) -> None:
        self.assertEqual(a | ~a, self.top)

    def test_541_and_complementation(self, a: ClassUnderTest) -> None:
        self.assertEqual(a & ~a, self.bottom)

    def test_550_xor_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a ^ b, (a | b) & ~(a & b))


class BitwiseTests(LatticeWithComplement):

    @property
    def bottom(self) -> ClassUnderTest:
        return self.zero

    @property
    def top(self) -> ClassUnderTest:
        return -self.one

    def test_560_lshift_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        if 0 <= b <= 64:
            self.assertEqual(a << b, a * pow(2, b))

    def test_570_rshift_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        if 0 <= b <= 64:
            self.assertEqual(a >> b, a // pow(2, b))


__all__ = ('LatticeTests', 'BoundedBelowLatticeTests', 'BoundedLatticeTests', 'LatticeWithComplement', 'BitwiseTests')

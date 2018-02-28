"""
Copyright 2018 Steve Palmer
"""


import abc

from core import GenericTests, ClassUnderTest


class LatticeTests(GenericTests):

    def test_generic_500_or_commutativity(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a | b, b | a)

    def test_generic_501_or_associativity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        self.assertEqual(a | (b | c), (a | b) | c)

    def test_generic_502_or_and_absorption(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a | (a & b), a)

    def test_generic_510_and_commutativity(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a & b, b & a)

    def test_generic_511_and_associativity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        self.assertEqual(a & (b & c), (a & b) & c)

    def test_generic_512_and_or_absorption(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a & (a | b), a)

    def test_generic_520_and_or_distributive(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        self.assertEqual(a & (b | c), a & b | a & c)


class BoundedBelowLatticeTests(LatticeTests):

    @property
    @abc.abstractmethod
    def bottom(self) -> ClassUnderTest:
        pass

    def test_generic_530_or_identity(self, a: ClassUnderTest) -> None:
        self.assertEqual(a | self.bottom, a)


class BoundedLatticeTests(BoundedBelowLatticeTests):

    @property
    @abc.abstractmethod
    def top(self) -> ClassUnderTest:
        pass

    def test_generic_531_and_identity(self, a: ClassUnderTest) -> None:
        self.assertEqual(a & self.top, a)


class LatticeWithComplement(BoundedLatticeTests):


    def test_generic_540_or_complementation(self, a: ClassUnderTest) -> None:
        self.assertEqual(a | ~a, self.top)

    def test_generic_541_and_complementation(self, a: ClassUnderTest) -> None:
        self.assertEqual(a & ~a, self.bottom)

    def test_generic_550_xor_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a ^ b, (a | b) & ~(a & b))


class BitwiseTests(LatticeWithComplement):

    @property
    def bottom(self) -> ClassUnderTest:
        return self.zero

    @property
    def top(self) -> ClassUnderTest:
        return -self.one

    def test_generic_560_lshift_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        if 0 <= b <= 64:
            self.assertEqual(a << b, a * pow(2, b))

    def test_generic_570_rshift_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        if 0 <= b <= 64:
            self.assertEqual(a >> b, a // pow(2, b))


__all__ = ('LatticeTests', 'BoundedBelowLatticeTests', 'BoundedLatticeTests', 'LatticeWithComplement', 'BitwiseTests')

"""
Copyright 2018 Steve Palmer
"""


import abc

from core import BaseTests


class LatticeTests(BaseTests):

    def test_500_or_commutativity(self, a, b):
        self.assertEqual(a | b, b | a)

    def test_501_or_associativity(self, a, b, c):
        self.assertEqual(a | (b | c), (a | b) | c)

    def test_502_or_and_absorption(self, a, b):
        self.assertEqual(a | (a & b), a)

    def test_510_and_commutativity(self, a, b):
        self.assertEqual(a & b, b & a)

    def test_511_and_associativity(self, a, b, c):
        self.assertEqual(a & (b & c), (a & b) & c)

    def test_512_and_or_absorption(self, a, b):
        self.assertEqual(a & (a | b), a)

    def test_520_and_or_distributive(self, a, b, c):
        self.assertEqual(a & (b | c), a & b | a & c)


class BoundedBelowLatticeTests(LatticeTests):

    @property
    @abc.abstractmethod
    def bottom(self):
        pass

    def test_530_or_identity(self, a):
        self.assertEqual(a | self.bottom, a)


class BoundedLatticeTests(BoundedBelowLatticeTests):

    @property
    @abc.abstractmethod
    def top(self):
        pass

    def test_531_and_identity(self, a):
        self.assertEqual(a & self.top, a)


class LatticeWithComplement(BoundedLatticeTests):


    def test_540_or_complementation(self, a):
        self.assertEqual(a | ~a, self.top)

    def test_541_and_complementation(self, a):
        self.assertEqual(a & ~a, self.bottom)

    def test_550_xor_definition(self, a, b):
        self.assertEqual(a ^ b, (a | b) & ~(a & b))


class BitwiseTests(LatticeWithComplement):

    @property
    def bottom(self):
        return self.zero

    @property
    def top(self):
        return -self.one

    def test_560_lshift_definition(self, a, b):
        if 0 <= b <= 64:
            self.assertEqual(a << b, a * pow(2, b))

    def test_570_rshift_definition(self, a, b):
        if 0 <= b <= 64:
            self.assertEqual(a >> b, a // pow(2, b))


__all__ = ('LatticeTests', 'BoundedBelowLatticeTests', 'BoundedLatticeTests', 'LatticeWithComplement', 'BitwiseTests')

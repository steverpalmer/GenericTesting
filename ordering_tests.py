"""
Copyright 2018 Steve Palmer
"""


import abc

from core import BaseTests


class PartialOrderingTests(BaseTests):

    def test_300_less_or_equal_reflexivity(self, a):
        self.assertTrue(a <= a)

    def test_301_less_or_equal_antisymmetry(self, a, b):
        self.assertImplies(a <= b and b <= a, a == b)

    def test_302_less_or_equal_transitivity(self, a, b, c):
        self.assertImplies(a <= b and b <= c, a <= c)

    def test_310_greater_or_equal_definition(self, a, b):
        self.assertEqual(a >= b, b <= a)

    def test_320_less_than_definition(self, a, b):
        self.assertEqual(a < b, a <= b and a != b)

    def test_330_greater_than_definition(self, a, b):
        self.assertEqual(a > b, b <= a and a != b)


class TotalOrderingTests(PartialOrderingTests):

    def test_303_less_or_equal_totality(self, a, b):
        self.assertTrue(a <= b or b <= a)


class TotalOrderingOverNumbersTests(TotalOrderingTests):

    @property
    @abc.abstractmethod
    def zero(self):
        pass

    @property
    @abc.abstractmethod
    def one(self):
        pass

    def test_304_less_or_equal_orientation(self):
        self.assertTrue(self.zero <= self.one)

    def test_340_less_or_equal_consistent_with_addition(self, a, b, c):
        self.assertEqual(a <= b, a + c <= b + c)

    def test_341_less_or_equal_consistent_with_multiplication(self, a, b):
        self.assertImplies(self.zero <= a and self.zero <= b, self.zero <= a * b)


__all__ = ('PartialOrderingTests', 'TotalOrderingTests', 'TotalOrderingOverNumbersTests')

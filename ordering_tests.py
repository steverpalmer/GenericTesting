"""
Copyright 2018 Steve Palmer
"""


import abc

from core import BaseTests, ClassUnderTest


class PartialOrderingTests(BaseTests):

    def test_300_less_or_equal_reflexivity(self, a: ClassUnderTest) -> None:
        self.assertTrue(a <= a)

    def test_301_less_or_equal_antisymmetry(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertImplies(a <= b and b <= a, a == b)

    def test_302_less_or_equal_transitivity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        self.assertImplies(a <= b and b <= c, a <= c)

    def test_310_greater_or_equal_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a >= b, b <= a)

    def test_320_less_than_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a < b, a <= b and a != b)

    def test_330_greater_than_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a > b, b <= a and a != b)


class TotalOrderingTests(PartialOrderingTests):

    def test_303_less_or_equal_totality(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertTrue(a <= b or b <= a)


class TotalOrderingOverNumbersTests(TotalOrderingTests):

    @property
    @abc.abstractmethod
    def zero(self) -> ClassUnderTest:
        pass

    @property
    @abc.abstractmethod
    def one(self) -> ClassUnderTest:
        pass

    def test_120_bool_definition(self, a: ClassUnderTest) -> None:
        self.assertEqual(bool(a), not a == self.zero)

    def test_304_less_or_equal_orientation(self) -> None:
        self.assertTrue(self.zero <= self.one)

    def test_340_less_or_equal_consistent_with_addition(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        self.assertEqual(a <= b, a + c <= b + c)

    def test_341_less_or_equal_consistent_with_multiplication(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertImplies(self.zero <= a and self.zero <= b, self.zero <= a * b)


__all__ = ('PartialOrderingTests', 'TotalOrderingTests', 'TotalOrderingOverNumbersTests')

"""
Copyright 2018 Steve Palmer
"""


from core import GenericTests, ClassUnderTest


class LessOrEqualTests(GenericTests):

    def test_generic_2140_less_or_equal_reflexivity(self, a: ClassUnderTest) -> None:
        self.assertTrue(a <= a)

    def test_generic_2141_less_or_equal_antisymmetry(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertImplies(a <= b and b <= a, a == b)

    def test_generic_2142_less_or_equal_transitivity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        self.assertImplies(a <= b and b <= c, a <= c)


class PartialOrderingTests(LessOrEqualTests):

    def test_generic_2160_greater_or_equal_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a >= b, b <= a)

    def test_generic_2161_less_than_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a < b, a <= b and a != b)

    def test_generic_2162_greater_than_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a > b, b <= a and a != b)


class TotalOrderingTests(PartialOrderingTests):

    def test_generic_2150_less_or_equal_totality(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertTrue(a <= b or b <= a)


__all__ = ('PartialOrderingTests', 'TotalOrderingTests')

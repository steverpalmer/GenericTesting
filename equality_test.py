"""
Copyright 2018 Steve Palmer
"""


from core import GenericTests, ClassUnderTest


class EqualsOnlyTests(GenericTests):

    def test_generic_2100_equality_reflexivity(self, a: ClassUnderTest) -> None:
        self.assertTrue(a == a)

    def test_generic_2101_equality_symmetry(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertImplies(a == b, b == a)

    def test_generic_2102_equality_transitivity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        self.assertImplies(a == b and b == c, a == c)


class EqualityTests(EqualsOnlyTests):

    def test_generic_2130_not_equal_defintion(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a != b, not a == b)


__all__ = ('EqualsOnlyTests', 'EqualityTests')

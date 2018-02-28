"""
Copyright 2018 Steve Palmer
"""


from core import GenericTests, ClassUnderTest


class EqualityTests(GenericTests):

    # § 1. Equality Relation (including Not Equal and bool())

    def test_generic_100_equality_reflexivity(self, a: ClassUnderTest) -> None:
        self.assertTrue(a == a)

    def test_generic_101_equality_symmetry(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertImplies(a == b, b == a)

    def test_generic_102_equality_transitivity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        self.assertImplies(a == b and b == c, a == c)

    def test_generic_110_not_equal_defintion(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a != b, not a == b)


__all__ = ('EqualityTests')

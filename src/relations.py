"""
Copyright 2018 Steve Palmer

A library of generic test for the elementary relationships...
 * __eq__
 * __ne__ (in terms of __eq__)
 * __le__
 * __ge__, __lt__, __gt__ (in terms of __le__)
"""


from .core import GenericTests, ClassUnderTest


class EqualsOnlyTests(GenericTests):
    """
    Tests of the __eq__ relation.
    """

    def test_generic_2100_equality_reflexivity(self, a: ClassUnderTest) -> None:
        self.assertTrue(a == a)

    def test_generic_2101_equality_symmetry(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertImplies(a == b, b == a)

    def test_generic_2102_equality_transitivity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        self.assertImplies(a == b and b == c, a == c)


class EqualityTests(EqualsOnlyTests):
    """
    Tests of the __ne__ relation.

    Since these tests are defined in terms of the __eq__ relation,
    it inherits the EqualsOnlyTests
    """

    def test_generic_2130_not_equal_defintion(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a != b, not a == b)


class LessOrEqualTests(GenericTests):
    """
    Tests of the __le__ relation.

    The antisymmetry test does use __eq__, but it does not inherit EqualsOnlyTests to allow better test management
    """

    def test_generic_2140_less_or_equal_reflexivity(self, a: ClassUnderTest) -> None:
        self.assertTrue(a <= a)

    def test_generic_2141_less_or_equal_antisymmetry(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertImplies(a <= b and b <= a, a == b)

    def test_generic_2142_less_or_equal_transitivity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        self.assertImplies(a <= b and b <= c, a <= c)


class PartialOrderingTests(LessOrEqualTests):
    """
    Tests of the __ge__, __lt__ and __gt__ relations.

    Since these tests are defined in terms of the __le__ relation,
    it inherits the LessOrEqualTests
    """

    def test_generic_2160_greater_or_equal_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a >= b, b <= a)

    def test_generic_2161_less_than_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a < b, a <= b and not a == b)

    def test_generic_2162_greater_than_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a > b, b <= a and not a == b)


class TotalOrderingTests(PartialOrderingTests):
    """
    Extends the PartialOrderingTests to a TotalOrdering.
    """

    def test_generic_2150_less_or_equal_totality(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertTrue(a <= b or b <= a)


__all__ = ('EqualsOnlyTests', 'EqualityTests', 'LessOrEqualTests', 'PartialOrderingTests', 'TotalOrderingTests')

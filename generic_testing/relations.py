# Copyright 2021 Steve Palmer

"""A library of generic test for the elementary relationships."""

from .core import GenericTests, ClassUnderTest


__all__ = (
    "EqualsOnlyTests",
    "EqualityTests",
    "LessOrEqualTests",
    "PartialOrderingTests",
    "TotalOrderingTests",
)


class EqualsOnlyTests(GenericTests):
    """Tests of the __eq__ relation."""

    def test_generic_2100_equality_reflexivity(self, a: ClassUnderTest) -> None:
        """a == a"""
        self.assertTrue(a == a)

    def test_generic_2101_equality_symmetry(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        """a == b ⇒ b == a"""
        self.assertImplies(a == b, b == a)

    def test_generic_2102_equality_transitivity(
        self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest
    ) -> None:
        """a == b and b == c ⇒ a == c"""
        self.assertImplies(a == b and b == c, a == c)


class EqualityTests(EqualsOnlyTests):
    """Tests of the __eq__ and __ne__ relation.

    Since these tests are defined in terms of the __eq__ relation,
    it inherits the EqualsOnlyTests
    """

    def test_generic_2130_not_equal_defintion(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        """a != b ⇔ not a == b"""
        self.assertEqual(a != b, not a == b)


class LessOrEqualTests(GenericTests):
    """Tests of the __le__ relation.

    The antisymmetry test does use __eq__, but it does not inherit EqualsOnlyTests to allow better test management
    """

    def test_generic_2140_less_or_equal_reflexivity(self, a: ClassUnderTest) -> None:
        """a <= a"""
        self.assertTrue(a <= a)

    def test_generic_2141_less_or_equal_antisymmetry(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        """a <= b and b <= a ⇒ a == b"""
        self.assertImplies(a <= b and b <= a, a == b)

    def test_generic_2142_less_or_equal_transitivity(
        self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest
    ) -> None:
        """a <= b and b <= c ⇒ a <= c"""
        self.assertImplies(a <= b and b <= c, a <= c)


class PartialOrderingTests(LessOrEqualTests):
    """Tests of the ordering relations assuming Partial Ordering.

    Since these tests are defined in terms of the __le__ relation,
    it inherits the LessOrEqualTests
    """

    def test_generic_2160_greater_or_equal_definition(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        """a >= b ⇔ b <= a"""
        self.assertEqual(a >= b, b <= a)

    def test_generic_2161_less_than_definition(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        """a < b ⇔ a <= b and not a == b"""
        self.assertEqual(a < b, a <= b and not a == b)

    def test_generic_2162_greater_than_definition(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        """a > b ⇔ b <= a and not a == b"""
        self.assertEqual(a > b, b <= a and not a == b)


class TotalOrderingTests(PartialOrderingTests):
    """Tests of the ordering relations assuming Total Ordering."""

    def test_generic_2150_less_or_equal_totality(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        """a <= b or b <= a"""
        self.assertTrue(a <= b or b <= a)

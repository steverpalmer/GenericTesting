# Copyright 2018 Steve Palmer

"""A library of generic test for the elementary function properties."""

from enum import Enum

from hypothesis import strategies as st

from .core import ClassUnderTest, GenericTests
from .relations import EqualityTests
from .collections_abc import HashableTests, IterableTests, KeyT
from .lattices import LatticeWithComplementTests
from .built_in_types import intTests


EnumUnderTest = "EnumUnderTest"


class _EnumTests(EqualityTests, HashableTests, IterableTests):
    """Tests of Enum class inheritable properties."""

    def test_generic_2110_equality_definition(
        self, a: ClassUnderTest, b: ClassUnderTest
    ):
        """a == b ⇔ a.value == b.value ⇔ a.name == b.name"""
        self.assertEqual(a == b, a.value == b.value)
        self.assertEqual(a == b, a.name == b.name)

    # For Enumerations, it is the class that is iterable, not the instances of the class...

    def test_generic_2400_iter_returns_an_iterator(self, E: EnumUnderTest) -> None:
        """Test __iter__ method."""
        IterableTests.test_generic_2400_iter_returns_an_iterator(self, E)

    def test_generic_2401_iterator_protocol_observed(self, E: EnumUnderTest) -> None:
        """Test iterator protocol."""
        IterableTests.test_generic_2401_iterator_protocol_observed(self, E)

    def test_generic_2420_contains_returns_a_boolean(
        self, E: EnumUnderTest, a: ClassUnderTest
    ) -> None:
        """isinstance(a in E, bool)"""
        self.assertIsInstance(a in E, bool)

    def test_generic_2421_contains_over_iterable_definition(
        self, E: EnumUnderTest, a: ClassUnderTest
    ) -> None:
        """a in E ⇔ any(a == x for x in E)"""
        contains = False
        for x in E:
            if x == a:
                contains = True
                break
        self.assertEqual(a in E, contains)

    def test_generic_2640_name_getitem_roundtrip(
        self, E: EnumUnderTest, a: ClassUnderTest
    ) -> None:
        """E[a.name] == a"""
        self.assertEqual(E[a.name], a)

    def test_generic_2641_value_call_roundtrip(
        self, E: EnumUnderTest, a: ClassUnderTest
    ) -> None:
        """E(a.value) == a"""
        self.assertEqual(E(a.value), a)

    def test_generic_2642_enum_attributes(self, E: EnumUnderTest, attr: KeyT) -> None:
        """E.n == E[n]"""
        self.assertEqual(getattr(E, attr), E[attr])


class EnumTests(_EnumTests):
    """Tests of Enum class properties."""

    def test_generic_2111_members_distinct_from_value(self, a: ClassUnderTest):
        """Enum members are not equal to their value."""
        self.assertFalse(a == a.value)

    def test_generic_2800_bool_convention(self, a: ClassUnderTest) -> None:
        """bool(a)"""
        self.assertTrue(bool(a))


class IntEnumTests(intTests, _EnumTests):
    """Tests of IntEnum class properties"""


class UniqueEnumMixinTests(GenericTests):
    """Tests of uniqueness of Enum class."""

    def test_generic_2645_enum_attributes_unique(
        self, E: EnumUnderTest, attr: KeyT
    ) -> None:
        """E[n].name == n"""
        self.assertEqual(E[attr].name, attr)


class FlagEnumMixinTests(LatticeWithComplementTests):
    """Test for Flag properties."""

    @property
    def top(self):
        return ~self.bottom

    def test_generic_2110_equality_definition(
        self, a: ClassUnderTest, b: ClassUnderTest
    ):
        """a == b ⇔ a.value == b.value"""
        self.assertEqual(a == b, a.value == b.value)

    def test_generic_2640_name_getitem_roundtrip(
        self, E: EnumUnderTest, a: ClassUnderTest
    ) -> None:
        """a.name is None or E[a.name] == a"""
        self.assertTrue(a.name is None or E[a.name] == a)

    def test_generic_2800_bool_convention(self, a: ClassUnderTest) -> None:
        """bool(a) ⇔ not a == ⊥"""
        self.assertEqual(bool(a), not a == self.bottom)


def enum_strategy_dict(cls: type, members=None, names=None):
    assert issubclass(cls, Enum)
    if members is None:
        members = st.sampled_from(cls)
    if names is None:
        names = st.sampled_from(list(cls.__members__))
    return {EnumUnderTest: st.just(cls), ClassUnderTest: members, KeyT: names}


__all__ = (
    "KeyT",
    "EnumUnderTest",
    "EnumTests",
    "IntEnumTests",
    "UniqueEnumMixinTests",
    "FlagEnumMixinTests",
    "enum_strategy_dict",
)

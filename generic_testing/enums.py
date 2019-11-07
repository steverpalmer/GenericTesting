# Copyright 2018 Steve Palmer

"""A library of generic test for the elementary function properties."""

from enum import Enum

from hypothesis import strategies as st

from generic_testing.core import ClassUnderTest
from generic_testing.relations import EqualityTests
from generic_testing.collections_abc import HashableTests, IterableTests, KeyT
from generic_testing.built_in_types import intTests


EnumUnderTest = 'EnumUnderTest'


class _EnumTests(EqualityTests, HashableTests, IterableTests):
    """Tests of Enum class inheritable properties."""

    def test_generic_2110_equality_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        self.assertEqual(a == b, a.value == b.value)
        self.assertEqual(a == b, a.name == b.name)

    # For Enumerations, it is the class that is iterable, not the instances of the class...

    def test_generic_2400_iter_returns_an_iterator(self, E: EnumUnderTest) -> None:
        """Test __iter__ method."""
        IterableTests.test_generic_2400_iter_returns_an_iterator(self, E)

    def test_generic_2401_iterator_protocol_observed(self, E: EnumUnderTest) -> None:
        IterableTests.test_generic_2401_iterator_protocol_observed(self, E)

    def test_generic_2640_name_getitem_roundtrip(self, E: EnumUnderTest, a: ClassUnderTest) -> None:
        """E[a.name] == a"""
        self.assertEqual(E[a.name], a)

    def test_generic_2641_value_call_roundtrip(self, E: EnumUnderTest, a: ClassUnderTest) -> None:
        """E(a.value) == a"""
        self.assertEqual(E(a.value), a)

    def test_generic_2642_enum_attributes(self, E: EnumUnderTest, attr: KeyT) -> None:
        """E.n == E[n]"""
        self.assertEqual(getattr(E, attr), E[attr])


class EnumTests(_EnumTests):
    """Tests of Enum class properties."""

    def test_generic_2800_bool_convention(self, a: ClassUnderTest) -> None:
        """bool(a)"""
        self.assertTrue(bool(a))


class UniqueEnumTests(EnumTests):
    """Tests of unique Enum class properties."""

    def test_generic_2643_enum_attributes_unique(self, E: EnumUnderTest, attr: KeyT) -> None:
        """E[n].name == n"""
        self.assertEqual(E[attr].name, attr)


class IntEnumTests(intTests, _EnumTests):
    """Tests od IntEnum class properties"""


def enum_strategy_dict(cls: type, members=None, names=None):
    assert issubclass(cls, Enum)
    if members is None:
        members = st.sampled_from(cls)
    if names is None:
        names = st.sampled_from(list(cls.__members__))
    return {EnumUnderTest: st.just(cls), ClassUnderTest: members, KeyT: names}


__all__ = ('KeyT', 'EnumUnderTest', 'EnumTests', 'UniqueEnumTests', 'IntEnumTests', 'enum_strategy_dict')

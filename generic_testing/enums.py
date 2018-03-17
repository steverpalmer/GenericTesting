# Copyright 2018 Steve Palmer

"""A library of generic test for the elementary function properties."""

from generic_testing.core import ClassUnderTest
from generic_testing.relations import EqualityTests
from generic_testing.collections_abc import HashableTests, IterableTests, KeyT
from generic_testing.built_in_types import intTests


class _EnumTests(EqualityTests, HashableTests, IterableTests):
    """Tests of Enum class inheritable properties."""

    def __init__(self, cls, methodName=None):
        super().__init__(methodName=methodName)
        self.cls = cls

    def test_generic_2110_equality_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        self.assertEqual(a == b, a.value == b.value)

    # For Enumerations, it is the class that is iterable, not the instances of the class...

    def test_generic_2400_iter_returns_an_iterator(self) -> None:
        """Test __iter__ method."""
        IterableTests.test_generic_2400_iter_returns_an_iterator(self, self.cls)

    def test_generic_2401_iterator_protocol_observed(self) -> None:
        IterableTests.test_generic_2401_iterator_protocol_observed(self, self.cls)

    def test_generic_2640_name_is_injective(self, a: ClassUnderTest, b: ClassUnderTest):
        """a != b ⇒ a.name != b.name"""
        self.assertImplies(not a == b, not a.name == b.name)

    def test_generic_2641_class_getitem_is_surjective(self, a: ClassUnderTest):
        """Enum[a.name] == a"""
        self.assertEqual(self.cls[a.name], a)


class EnumTests(_EnumTests):
    """Tests of Enum class properties."""

    def test_generic_2800_bool_convention(self, a: ClassUnderTest) -> None:
        """bool(a)"""
        self.assertTrue(bool(a))


class UniqueEnumTests(EnumTests):
    """Tests of unique Enum class properties."""

    def test_generic_2645_class_getitem_is_injective(self, a: KeyT, b: KeyT):
        """a != b ⇒ Enum[a] != Enum[b]"""
        self.assertImplies(not a == b, not self.cls[a] == self.cls[b])


class IntEnumTests(intTests, _EnumTests):
    """Tests od IntEnum class properties"""


__all__ = ('KeyT', 'EnumTests', 'UniqueEnumTests', 'IntEnumTests')

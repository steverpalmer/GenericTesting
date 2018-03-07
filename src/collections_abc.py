# Copyright 2018 Steve Palmer

"""A library of generic test for the base classes in the collections.abc library."""

import abc
import collections
import unittest

from hypothesis import assume, strategies as st

from .core import GenericTests, ClassUnderTest
from .relations import EqualityTests, PartialOrderingTests
from .lattices import BoundedBelowLatticeTests
from .augmented_assignment import LatticeWithComplementAugmentedTests


ElementT = 'ElementT'
ValueT = 'ValueT'


class IterableTests(GenericTests):
    """
    The property test of collections.abc.Iterables.
    """

    def test_generic_2400_iter_returns_an_iterator(self, a: ClassUnderTest) -> None:
        self.assertIsInstance(iter(a), collections.abc.Iterator)

    def test_generic_2401_iterator_protocol_observed(self, a: ClassUnderTest) -> None:
        a_iter = iter(a)
        try:
            next(a_iter)
            return  # next can return
        except StopIteration:
            # ... or rasie a StopIteration
            with self.assertRaises(StopIteration):  # ... and continues to do so
                next(a_iter)
            return
        self.fail()  # ... but nothing else


class SizedTests(GenericTests):
    """
    The property test of collections.abc.Sized.

    I assume that the len() function returns a value that can be compared to an int.
    """

    def test_generic_2410_len_returns_a_non_negative_int(self, a: ClassUnderTest) -> None:
        "0 <= len(a)"
        a_len = len(a)
        self.assertIsInstance(a_len, int)
        self.assertGreaterEqual(a_len, 0)

    def test_generic_2800_bool_convention(self, a: ClassUnderTest) -> None:
        "bool(a) ⇔ len(a) != 0"
        self.assertEqual(len(a) != 0, bool(a))


class ContainerTests(GenericTests):
    """
    The property test of collections.abc.Container.

    In fact, the standard does *not* say that the __contains__ method must return a bool.
    It only says that it returns a true or false (not even True or False).
    However, if this is property was not true, I think it would be a surprise, so it is included.
    If this is not true for your contained, then simply skip this test.
    """

    def test_generic_2420_contains_returns_a_boolean(self, a: ElementT, b: ClassUnderTest) -> None:
        self.assertIsInstance(a in b, bool)


class SizedOverIterableTests(SizedTests, IterableTests):
    """
    The property tests of an class that is both collections.abc.Sized and collections.abc.Iterable.

    In fact, this is *not* required, but it would be a surprise if it were not true.
    If this is not true for your contained, then simply skip this test.
    """

    def test_generic_2411_len_iterations(self, a: ClassUnderTest) -> None:
        a_len = len(a)
        iter_count = 0
        for _ in a:
            iter_count += 1
            if iter_count > a_len:
                break
        self.assertEqual(a_len, iter_count)


class ContainerOverIterableTests(IterableTests, ContainerTests):
    """
    The property tests of an class that is both collections.abc.Iterable and collections.abc.Container.

    See Language Reference Manual §3.3.6 "The membership test operators (in and not in) are normally
    implemented as an iteration ..."
    """

    def test_generic_2421_contains_over_iterable_definition(self, a: ElementT, b: ClassUnderTest) -> None:
        contains = False
        for x in b:
            if x == a:
                contains = True
                break
        self.assertEqual(a in b, contains)


class SizedIterableContainerWithEmpty(SizedOverIterableTests, ContainerOverIterableTests):
    """
    These test common properties of almost all containers.
    """

    @property
    @abc.abstractmethod
    def empty(self) -> ClassUnderTest:
        pass

    @abc.abstractmethod
    def test_generic_2010_empty_type(self) -> None:
        self.fail("Need to define a test that the helper empty has the correct type")

    def test_generic_2402_zero_iterations_over_empty(self) -> None:
        with self.assertRaises(StopIteration):
            next(iter(self.empty))

    def test_generic_2412_len_empty_is_zero(self) -> None:
        "len(∅) == 0"
        self.assertEqual(len(self.empty), 0)

    def test_generic_2422_empty_contains_nothing(self, a: ElementT) -> None:
        "a not in ∅"
        self.assertFalse(a in self.empty)


class SetTests(SizedIterableContainerWithEmpty, EqualityTests, PartialOrderingTests, BoundedBelowLatticeTests):
    """
    The property tests of collections.abc.Set.
    """

    @property
    def bottom(self) -> ClassUnderTest:
        return self.empty

    @unittest.skip("bottom is empty")
    def test_generic_2000_bottom_type(self) -> None:
        pass

    def test_generic_2151_ordering_consistent_with_lattice(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        "(a & b <= a <= a | b) and (a & b <= b <= a | b)"
        union = a | b
        intersection = a & b
        self.assertTrue(intersection <= a <= union)
        self.assertTrue(intersection <= b <= union)

    def test_generic_2152_less_or_equal_orientation(self, a: ClassUnderTest) -> None:
        "∅ <= a"
        self.assertLessEqual(self.empty, a)

    def test_generic_2430_disjoint_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        "a.isdisjoint(b) ⇔ a & b == ∅"
        self.assertEqual(a.isdisjoint(b), a & b == self.empty)

    def test_generic_2431_sub_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        "(a - b <= a) and (a - b) & b == ∅"
        c = a - b
        self.assertTrue(c <= a)
        self.assertTrue(c.isdisjoint(b))

    def test_generic_2432_xor_defintion(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        "a ^ b == (a | b) - (a & b)"
        self.assertEqual(a ^ b, (a | b) - (a & b))


class MappingViewTests(SizedTests):
    """
    The property tests of collections.abc.MappingView.

    :TODO: Maybe could try to test the dynamic nature of mapping views here.
    """
    pass


class KeysViewTests(MappingViewTests, SetTests):
    """
    The property tests of collections.abc.KeysView.
    """


class ItemsViewTests(MappingViewTests, SetTests):
    """
    The property tests of collections.abc.ItemsView.
    """


class ValuesViewTests(MappingViewTests, ContainerOverIterableTests):
    """
    The property tests of collections.abc.ValuesView.
    """


class MutableSetTests(SetTests, LatticeWithComplementAugmentedTests):
    """
    The property tests of collections.abc.MutableSet.
    """

    @abc.abstractmethod
    def copy(self, a: ClassUnderTest) -> ClassUnderTest:
        """
        To test Mutable containers, it is useful to have a helper that takes a copy
        of the container before it is mutated.
        """

    @abc.abstractmethod
    def singleton_constructor(self, a: ElementT) -> ClassUnderTest:
        """
        Since we have comprehensive test of set operations,
        it is useful to have a helper to construct a set from a single value.
        """

    def test_generic_2040_copy_helper_definition(self, a: ClassUnderTest) -> None:
        a_copy = self.copy(a)
        self.assertNotEqual(id(a), id(a_copy))
        self.assertEqual(a, a_copy)

    def test_generic_2041_singleton_constructor_helper_definition(self, a: ElementT) -> None:
        a_singleton = self.singleton_constructor(a)
        self.assertTrue(a in a_singleton)
        self.assertEqual(len(a_singleton), 1)

    def test_generic_2460_add_definition(self, a: ClassUnderTest, b: ElementT) -> None:
        a_copy = self.copy(a)
        b_singleton = self.singleton_constructor(b)
        a.add(b)
        self.assertEqual(a, a_copy | b_singleton)

    def test_generic_2461_discard_definition(self, a: ClassUnderTest, b: ElementT) -> None:
        a_copy = self.copy(a)
        b_singleton = self.singleton_constructor(b)
        a.discard(b)
        self.assertEqual(a, a_copy - b_singleton)


class MappingTests(SizedIterableContainerWithEmpty, EqualityTests):

    def test_generic_2110_equality_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        self.assertEqual(a == b, a.keys() == b.keys() and all(a[k] == b[k] for k in a))

    def test_generic_2480_getitem_on_empty_either_succeeds_or_raises_KeyError(self, a: ElementT) -> None:
        try:
            self.empty[a]
        except KeyError:
            pass
        except BaseException:
            self.fail()

    def test_generic_2481_getitem_over_all_keys_succeeds(self, a: ClassUnderTest) -> None:
        a_keys = a.keys()
        self.assertIsInstance(a_keys, collections.abc.KeysView)
        try:
            for k in a_keys:
                a[k]
        except KeyError:
            self.fail()

    def test_generic_2490_items_returns_an_ItemsView(self, a: ClassUnderTest) -> None:
        self.assertIsInstance(a.items(), collections.abc.ItemsView)

    def test_generic_2491_values_returns_an_ValuesView(self, a: ClassUnderTest) -> None:
        self.assertIsInstance(a.values(), collections.abc.ValuesView)

    def test_generic_2492_get_definition(self, a: ClassUnderTest, b: ElementT, c: ValueT) -> None:
        if b in a:
            expected = a[b]
        else:
            expected = c
        self.assertEqual(a.get(b, c), expected)


class MutableMappingTests(MappingTests):

    @abc.abstractmethod
    def copy(self, a: ClassUnderTest) -> ClassUnderTest:
        """
        To test Mutable containers, it is useful to have a helper that takes a copy
        of the container before it is mutated.
        """

    def test_generic_2040_copy_helper_definition(self, a: ClassUnderTest) -> None:
        a_copy = self.copy(a)
        self.assertNotEqual(id(a), id(a_copy))
        self.assertEqual(a, a_copy)

    def test_generic_2500_setitem_definition(self, a: ClassUnderTest, b: ElementT, c: ValueT) -> None:
        a_copy = self.copy(a)
        a[b] = c
        self.assertEqual(a[b], c)
        for key in a_copy:
            if key != b:
                self.assertEqual(a[key], a_copy[key])

    def test_generic_2501_delitem_definition(self, a: ClassUnderTest, data) -> None:
        assume(len(a) > 0)
        a_copy = self.copy(a)
        key_to_forget = data.draw(st.sampled_from(list(a.keys())))
        del a[key_to_forget]
        self.assertTrue(key_to_forget not in a)
        for other_key in a_copy:
            if other_key != key_to_forget:
                self.assertEqual(a[other_key], a_copy[other_key])

    def test_generic_2502_pop_definition(self, a: ClassUnderTest, b: ElementT) -> None:
        a_copy = self.copy(a)
        try:
            v = a.pop(b)
            self.assertEqual(v, a_copy[b])
            del a_copy[b]
        except KeyError:
            self.assertFalse(b in a)
        self.assertEqual(a, a_copy)

    def test_generic_2503_popitem_definition(self, a: ClassUnderTest) -> None:
        a_copy = self.copy(a)
        try:
            k, v = a.popitem()
            self.assertTrue(k in a_copy)
            self.assertEqual(a_copy[k], v)
            del a_copy[k]
            self.assertEqual(a, a_copy)
        except KeyError:
            self.assertFalse(bool(a_copy))

    def test_generic_2504_clear_definition(self, a: ClassUnderTest) -> None:
        a.clear()
        self.assertTrue(a == self.empty)

    def test_generic_2505_update_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        a_copy = self.copy(a)
        a.update(b)
        self.assertLessEqual(b.keys(), a.keys())
        for k in a:
            self.assertEqual(a[k], b[k] if k in b else a_copy[k])

    def test_generic_2506_setdefault_definition(self, a: ClassUnderTest, b: ElementT, c: ValueT) -> None:
        a_copy = self.copy(a)
        v = a.setdefault(b, c)
        self.assertTrue(b in a)
        self.assertEqual(a[b], v)
        if b not in a_copy:
            self.assertEqual(v, c)
            del a[b]
        self.assertEqual(a, a_copy)


__all__ = ('ElementT', 'ValueT',
           'IterableTests', 'SizedTests', 'ContainerTests',
           'SizedOverIterableTests', 'ContainerOverIterableTests', 'SizedIterableContainerWithEmpty',
           'SetTests', 'MappingViewTests', 'KeysViewTests', 'ItemsViewTests', 'ValuesViewTests', 'MutableSetTests',
           'MappingTests', 'MutableMappingTests')

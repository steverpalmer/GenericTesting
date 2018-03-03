"""
Copyright 2018 Steve Palmer

A library of generic test for the base classes in the collections.abc library
"""

import abc
import collections

from hypothesis import assume, strategies as st

from .core import GenericTests, ClassUnderTest
from .relations import EqualityTests, PartialOrderingTests
from .lattices import BoundedBelowLatticeTests


ElementT = 'ElementT'
ValueT = 'ValueT'

class IterableTests(GenericTests):
    """
    These is the property test of Iterables.
    """

    def test_generic_2400_iter_returns_an_iterator(self, a: ClassUnderTest) -> None:
        self.assertIsInstance(iter(a), collections.abc.Iterator)

    def test_generic_2401_iterator_protocol_observed(self, a: ClassUnderTest) -> None:
        a_iter = iter(a)
        try:
            _ = next(a_iter)
            return  # next can return
        except StopIteration:
            # ... or rasie a StopIteration
            with self.assertRaises(StopIteration):  # ... and continues to do so
                _ = next(a_iter)
            return
        self.fail()  # ... but nothing else


class SizedTests(GenericTests):
    """
    These is the property test of Sized.
    """

    def test_generic_2410_len_returns_a_non_negative_int(self, a: ClassUnderTest) -> None:
        a_len = len(a)
        self.assertIsInstance(a_len, int)
        self.assertGreaterEqual(a_len, 0)

    def test_generic_2419_bool_convention(self, a: ClassUnderTest) -> None:
        self.assertEqual(len(a) != 0, bool(a))


class ContainerTests(GenericTests):
    """
    These is the property test of Container.
    """

    def test_generic_2420_contains_returns_a_boolean(self, a: ElementT, b: ClassUnderTest) -> None:
        self.assertIsInstance(a in b, bool)


class SizedOverIterableTests(SizedTests, IterableTests):
    """
    :FIXME:
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
    :FIXME:
    """

    def test_generic_2421_contains_over_iterable_definition(self, a: ElementT, b: ClassUnderTest) -> None:
        contains = False
        for x in b:
            if x == a:
                contains = True
                break
        self.assertEqual(a in b, contains)


# class HashableTests(GenericTests):
# 
#     def test_generic_635_hash_returns_int(self, a: elementT) -> None:
#         self.assertTrue(isinstance(hash(a), int))
# 
#     def test_generic_636_equal_implies_equal_hash(self, a: elementT, b: elementT) -> None:
#         # Implicity checks that a.__eq__(b) is defined
#         self.assertImplies(a == b, hash(a) == hash(b))


class SetTests(SizedOverIterableTests, ContainerOverIterableTests, EqualityTests, PartialOrderingTests, BoundedBelowLatticeTests):
    """
    These is the property test of Container.
    """

    @property
    @abc.abstractmethod
    def empty(self) -> ClassUnderTest:
        pass

    @property
    def bottom(self) -> ClassUnderTest:
        return self.empty

    def test_generic_2000_empty_type(self) -> None:
        self.assertIsInstance(self.empty, collections.abc.Set)

    def test_generic_2150_less_or_equal_orientation(self, a: ClassUnderTest) -> None:
        self.assertLessEqual(self.empty, a)

    def test_generic_2151_ordering_consistent_with_lattice(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        union = a | b
        intersection = a & b
        self.assertTrue(intersection <= a <= union)
        self.assertTrue(intersection <= b <= union)

    def test_generic_2402_zero_iterations_over_empty(self) -> None:
        with self.assertRaises(StopIteration):
            next(iter(self.empty))

    def test_generic_2412_len_empty_is_zero(self) -> None:
        self.assertEqual(len(self.empty), 0)

    def test_generic_2422_empty_contains_nothing(self, a: ElementT) -> None:
        self.assertFalse(a in self.empty)

    def test_generic_2430_disjoint_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a.isdisjoint(b), a & b == self.empty)

    def test_generic_2431_sub_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        c = a - b
        self.assertTrue(c <= a)
        self.assertTrue(c.isdisjoint(b))

    def test_generic_2432_xor_defintion(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a ^ b, (a | b) - (a & b))


class MappingViewTests(SizedTests):
    pass


class KeysViewTests(MappingViewTests, SetTests):

    def test_generic_2000_empty_type(self) -> None:
        self.assertIsInstance(self.empty, collections.abc.KeysView)


class ItemsViewTests(MappingViewTests, SetTests):

    def test_generic_2000_empty_type(self) -> None:
        self.assertIsInstance(self.empty, collections.abc.ItemsView)


class ValuesViewTests(MappingViewTests, ContainerOverIterableTests):
    pass


class MutableSetTests(SetTests):

    @abc.abstractmethod
    def copy(self, a: ClassUnderTest) -> ClassUnderTest:
        pass

    @abc.abstractmethod
    def singleton_constructor(self, a: ElementT) -> ClassUnderTest:
        pass

    def test_generic_2000_empty_type(self) -> None:
        self.assertIsInstance(self.empty, collections.abc.MutableSet)

    def test_generic_2010_copy_helper_definition(self, a: ClassUnderTest) -> None:
        a_copy = self.copy(a)
        self.assertIsInstance(a_copy, collections.abc.MutableSet)
        self.assertNotEqual(id(a), id(a_copy))
        self.assertEqual(a, a_copy)

    def test_generic_2021_singleton_constructor_helper_definition(self, a: ElementT) -> None:
        a_singleton = self.singleton_constructor(a)
        self.assertIsInstance(a_singleton, collections.abc.MutableSet)
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


class MappingTests(SizedOverIterableTests, ContainerOverIterableTests, EqualityTests):

    @property
    @abc.abstractmethod
    def empty(self) -> ClassUnderTest:
        pass

    @abc.abstractmethod
    def singleton_constructor(self, a: ElementT, b: ValueT) -> ClassUnderTest:
        pass

    def test_generic_2000_empty_type(self) -> None:
        self.assertIsInstance(self.empty, collections.abc.Mapping)

    def test_generic_2021_singleton_constructor_helper_definition(self, a: ElementT, b: ValueT):
        map_singleton = self.singleton_constructor(a, b)
        self.assertIsInstance(map_singleton, collections.abc.Mapping)
        self.assertEqual(map_singleton[a], b)
        self.assertEqual(len(map_singleton), 1)

    def test_generic_2110_equality_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        self.assertEqual(a == b, a.keys() == b.keys() and all(a[k] == b[k] for k in a))

    def test_generic_2402_zero_iterations_over_empty(self) -> None:
        with self.assertRaises(StopIteration):
            next(iter(self.empty))

    def test_generic_2412_len_empty_is_zero(self) -> None:
        self.assertEqual(len(self.empty), 0)

    def test_generic_2480_getitem_on_empty_either_succeeds_or_raises_KeyError(self, a: ElementT) -> None:
        try:
            _ = self.empty[a]
        except KeyError:
            pass
        except:
            self.fail()

    def test_generic_2481_getitem_over_all_keys_succeeds(self, a: ClassUnderTest) -> None:
        a_keys = a.keys()
        self.assertIsInstance(a_keys, collections.abc.KeysView)
        try:
            for k in a_keys:
                _ = a[k]
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
        pass

    def test_generic_2010_copy_helper_definition(self, a: ClassUnderTest) -> None:
        a_copy = self.copy(a)
        self.assertIsInstance(a_copy, collections.abc.MutableMapping)
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
        self.assertFalse(bool(a))

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
           'SizedOverIterableTests', 'ContainerOverIterableTests',
           'SetTests', 'MappingViewTests', 'KeysViewTests', 'ItemsViewTests', 'ValuesViewTests', 'MutableSetTests',
           'MappingTests', 'MutableMappingTests')

if __name__ == '__main__':
    pass
"""
Copyright 2018 Steve Palmer
"""

import abc
import collections.abc
import unittest

from hypothesis import strategies as st

from core import BaseTests, base_test_modifier
from equality_test import EqualityTests
from ordering_tests import PartialOrderingTests
from lattice_tests import BoundedBelowLatticeTests


elementT = 'elementT'
keyT = 'keyT'
valueT = 'valueT'


class IterableTests(BaseTests):

    def test_610_iter_on_iterable_returns_an_iterator(self, a: collections.abc.Iterable) -> None:
        self.assertTrue(isinstance(iter(a), collections.abc.Iterator))

    def test_611_iterator_protocol_observed(self, a: collections.abc.Iterable) -> None:
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


class SizedTests(BaseTests):

    def test_620_len_returns_a_non_negative_int(self, a: collections.abc.Sized) -> None:
        a_len = len(a)
        self.assertTrue(isinstance(a_len, int))
        self.assertGreaterEqual(a_len, 0)

    def test_621_bool_convention(self, a: collections.abc.Sized) -> None:
        self.assertEqual(len(a) != 0, bool(a))


class ContainerTests(BaseTests):

    def test_625_contains_returns_a_boolean(self, a, b: collections.abc.Container) -> None:
        self.assertTrue(isinstance(a in b, bool))


class SizedIterable(collections.abc.Sized, collections.abc.Iterable):
    pass


class SizedOverIterableTests(SizedTests, IterableTests):

    def test_622_len_iterations(self, a: SizedIterable) -> None:
        a_len = len(a)
        iter_count = 0
        for _ in a:
            iter_count += 1
            if iter_count > a_len:
                break
        self.assertEqual(a_len, iter_count)


class IterableContainer(collections.abc.Iterable, collections.abc.Container):
    pass


class ContainerOverIterableTests(IterableTests, ContainerTests):

    def test_626_contains_over_iterable_definition(self, a, b: IterableContainer) -> None:
        contains = False
        for x in b:
            if x == a:
                contains = True
                break
        self.assertEqual(a in b, contains)


# class HashableTests(BaseTests):
# 
#     def test_635_hash_returns_int(self, a: elementT) -> None:
#         self.assertTrue(isinstance(hash(a), int))
# 
#     def test_636_equal_implies_equal_hash(self, a: elementT, b: elementT) -> None:
#         # Implicity checks that a.__eq__(b) is defined
#         self.assertImplies(a == b, hash(a) == hash(b))


class SetTests(SizedOverIterableTests, ContainerOverIterableTests, EqualityTests, PartialOrderingTests, BoundedBelowLatticeTests):

    @property
    @abc.abstractmethod
    def empty(self) -> collections.abc.Set:
        pass

    @property
    def bottom(self):
        return self.empty

    def test_306_less_or_equal_orientation(self, a: collections.abc.Set) -> None:
        self.assertTrue(self.empty <= a)

    def test_560_ordering_consistent_with_lattice(self, a: collections.abc.Set, b: collections.abc.Set) -> None:
        union = a | b
        intersection = a & b
        self.assertTrue(intersection <= a <= union)
        self.assertTrue(intersection <= b <= union)

    def test_612_zero_iterations_over_empty(self) -> None:
        with self.assertRaises(StopIteration):
            next(iter(self.empty))

    def test_623_len_empty_is_zero(self) -> None:
        self.assertEqual(len(self.empty), 0)

    def test_627_empty_contains_nothing(self, a: collections.abc.Hashable) -> None:
        self.assertFalse(a in self.empty)

    def test_630_disjoint_definition(self, a: collections.abc.Set, b: collections.abc.Set) -> None:
        self.assertEqual(a.isdisjoint(b), a & b == self.empty)

    def test_631_sub_definition(self, a: collections.abc.Set, b: collections.abc.Set) -> None:
        c = a - b
        self.assertTrue(c <= a)
        self.assertTrue(c.isdisjoint(b))

    def test_632_xor_defintion(self, a: collections.abc.Set, b: collections.abc.Set) -> None:
        self.assertEqual(a ^ b, (a | b) - (a & b))


class MutableSetTests(SetTests):

    def test_635_add_definition(self, a: collections.abc.MutableSet, b: collections.abc.Hashable) -> None:
        expected_len = len(a) if b in a else len(a) + 1
        a.add(b)
        self.assertEqual(len(a), expected_len)
        self.assertTrue(b in a)

    def test_636_discard_definition(self, a: collections.abc.MutableSet, b: collections.abc.Hashable) -> None:
        expected_len = len(a) - 1 if b in a else len(a)
        a.discard(b)
        self.assertEqual(len(a), expected_len)
        self.assertTrue(b not in a)


class MappingTests(SizedOverIterableTests, ContainerOverIterableTests, EqualityTests):

    @property
    @abc.abstractmethod
    def empty(self) -> collections.abc.Mapping:
        pass

    def test_612_zero_iterations_over_empty(self) -> None:
        with self.assertRaises(StopIteration):
            next(iter(self.empty))

    def test_623_len_empty_is_zero(self) -> None:
        self.assertEqual(len(self.empty), 0)

    def test_627_get_on_empty_raises_KeyError(self, a: collections.abc.Hashable) -> None:
        with self.assertRaises(KeyError):
            _ = self.empty[a]

#     def test_650_keys_view_type(self, a):
#         self.assertEqual(isinstance(a.keys(), collections.abc.KeysView))


class MutableMappingTests(MappingTests):
    pass


class frozensetExtensionTests(SetTests):

    def test_629_copy_definition(self, a: collections.abc.Set) -> None:
        b = a.copy()
        self.assertEqual(a, b)

    def test_640_issubset_defintion(self, a: collections.abc.Set, b: collections.abc.Set) -> None:
        self.assertEqual(a.issubset(b), a <= b)

    def test_641_isuperset_definition(self, a: collections.abc.Set, b: collections.abc.Set) -> None:
        self.assertEqual(a.issuperset(b), a >= b)

    def test_642_union_definition(self, a: collections.abc.Set, b: collections.abc.Set) -> None:
        self.assertEqual(a.union(b), a | b)

    def test_643_intersection_definition(self, a: collections.abc.Set, b: collections.abc.Set) -> None:
        self.assertEqual(a.intersection(b), a & b)

    def test_644_difference_definition(self, a: collections.abc.Set, b: collections.abc.Set) -> None:
        self.assertEqual(a.difference(b), a - b)

    def test_645_symmetric_difference_definition(self, a: collections.abc.Set, b: collections.abc.Set) -> None:
        self.assertEqual(a.symmetric_difference(b), a ^ b)


element_st = st.integers()
@base_test_modifier({None: st.frozensets(element_st), elementT: element_st})
class Test_frozenset(frozensetExtensionTests):

    @property
    def empty(self):
        return frozenset()

    def test_690_singleton_frozenset(self, a: collections.abc.Hashable) -> None:
        singleton = frozenset([a])
        self.assertEqual(len(singleton), 1)
        self.assertTrue(a in singleton)


element_st = st.integers()
@base_test_modifier({None: st.sets(element_st), elementT: element_st})
class Test_set(frozensetExtensionTests):

    @property
    def empty(self):
        return set()

    def test_629_copy_definition(self, a: set) -> None:
        b = a.copy()
        self.assertNotEqual(id(a), id(b))
        self.assertEqual(a, b)

    def test_646_add_definition(self, a: set, b: collections.abc.Hashable) -> None:
        a_copy = a.copy()
        a.add(b)
        self.assertTrue(a_copy <= a)
        self.assertTrue(b in a)

    def test_647_discard_definition(self, a: set, b: collections.abc.Hashable) -> None:
        a_copy = a.copy()
        a.discard(b)
        self.assertTrue(a <= a_copy)
        self.assertTrue(b not in a)

    def test_648_update_definition(self, a: set, b: collections.abc.Hashable) -> None:
        a_copy = a.copy()
        a_nother = a.copy()
        a |= b
        self.assertEqual(a, a_copy | b)
        a_nother.update(b)
        self.assertEqual(a, a_nother)

    def test_649_intersection_update_definition(self, a: set, b: set) -> None:
        a_copy = a.copy()
        a_nother = a.copy()
        a &= b
        self.assertEqual(a, a_copy & b)
        a_nother.intersection_update(b)
        self.assertEqual(a, a_nother)

    def test_650_difference_update_definition(self, a: set, b: set) -> None:
        a_copy = a.copy()
        a_nother = a.copy()
        a -= b
        self.assertEqual(a, a_copy - b)
        a_nother.difference_update(b)
        self.assertEqual(a, a_nother)

    def test_651_symmetric_difference_update_definition(self, a: set, b: set) -> None:
        a_copy = a.copy()
        a_nother = a.copy()
        a ^= b
        self.assertEqual(a, a_copy ^ b)
        a_nother.symmetric_difference_update(b)
        self.assertEqual(a, a_nother)

    def test_652_remove_definition(self, a: set, b: collections.abc.Hashable) -> None:
        a.add(b)
        a_copy = a.copy()
        a.remove(b)
        a_copy.discard(b)
        self.assertEqual(a, a_copy)
        with self.assertRaises(KeyError):
            a.remove(b)

    def test_653_pop_definition(self, a: set) -> None:
        if a:
            a_copy = a.copy()
            b = a.pop()
            self.assertTrue(b in a_copy)
            self.assertTrue(b not in a)
            a_copy.discard(b)
            self.assertEqual(a, a_copy)
        else:
            with self.assertRaises(KeyError):
                _ = a.pop()

    def test_654_clear_definition(self, a: set) -> None:
        a.clear()
        self.assertEqual(a, self.empty)


key_st = st.integers()
value_st = st.integers()
@base_test_modifier({None: st.dictionaries(key_st, value_st), elementT: key_st, keyT: key_st})
class Test_dict(MutableMappingTests):

    @property
    def empty(self):
        return dict()


if __name__ == '__main__':

    SUITE = unittest.TestSuite()
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_frozenset))
#    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_set))
#    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_dict))
    TR = unittest.TextTestRunner(verbosity=2)
    TR.run(SUITE)

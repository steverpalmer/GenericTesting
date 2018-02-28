"""
Copyright 2018 Steve Palmer
"""

import abc
import collections.abc
import unittest

from hypothesis import strategies as st

from core import GenericTests, Given, ClassUnderTest
from equality_test import EqualityTests
from ordering_tests import PartialOrderingTests
from lattice_tests import BoundedBelowLatticeTests


ElementT = 'ElementT'
ValueT = 'ValueT'

class IterableTests(GenericTests):

    def test_generic_610_iter_returns_an_iterator(self, a: ClassUnderTest) -> None:
        self.assertTrue(isinstance(iter(a), collections.abc.Iterator))

    def test_generic_611_iterator_protocol_observed(self, a: ClassUnderTest) -> None:
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

    def test_generic_620_len_returns_a_non_negative_int(self, a: ClassUnderTest) -> None:
        a_len = len(a)
        self.assertTrue(isinstance(a_len, int))
        self.assertGreaterEqual(a_len, 0)

    def test_generic_621_bool_convention(self, a: ClassUnderTest) -> None:
        self.assertEqual(len(a) != 0, bool(a))


class ContainerTests(GenericTests):

    def test_generic_625_contains_returns_a_boolean(self, a: ElementT, b: ClassUnderTest) -> None:
        self.assertTrue(isinstance(a in b, bool))


class SizedOverIterableTests(SizedTests, IterableTests):

    def test_generic_622_len_iterations(self, a: ClassUnderTest) -> None:
        a_len = len(a)
        iter_count = 0
        for _ in a:
            iter_count += 1
            if iter_count > a_len:
                break
        self.assertEqual(a_len, iter_count)


class ContainerOverIterableTests(IterableTests, ContainerTests):

    def test_generic_626_contains_over_iterable_definition(self, a: ElementT, b: ClassUnderTest) -> None:
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

    @property
    @abc.abstractmethod
    def empty(self) -> ClassUnderTest:
        pass

    @property
    def bottom(self) -> ClassUnderTest:
        return self.empty

    def test_generic_306_less_or_equal_orientation(self, a: ClassUnderTest) -> None:
        self.assertTrue(self.empty <= a)

    def test_generic_560_ordering_consistent_with_lattice(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        union = a | b
        intersection = a & b
        self.assertTrue(intersection <= a <= union)
        self.assertTrue(intersection <= b <= union)

    def test_generic_612_zero_iterations_over_empty(self) -> None:
        with self.assertRaises(StopIteration):
            next(iter(self.empty))

    def test_generic_623_len_empty_is_zero(self) -> None:
        self.assertEqual(len(self.empty), 0)

    def test_generic_627_empty_contains_nothing(self, a: ElementT) -> None:
        self.assertFalse(a in self.empty)

    def test_generic_630_disjoint_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a.isdisjoint(b), a & b == self.empty)

    def test_generic_631_sub_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        c = a - b
        self.assertTrue(c <= a)
        self.assertTrue(c.isdisjoint(b))

    def test_generic_632_xor_defintion(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a ^ b, (a | b) - (a & b))


class MutableSetTests(SetTests):

    def test_generic_635_add_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        expected_len = len(a) if b in a else len(a) + 1
        a.add(b)
        self.assertEqual(len(a), expected_len)
        self.assertTrue(b in a)

    def test_generic_636_discard_definition(self, a: ClassUnderTest, b: ElementT) -> None:
        expected_len = len(a) - 1 if b in a else len(a)
        a.discard(b)
        self.assertEqual(len(a), expected_len)
        self.assertTrue(b not in a)


class MappingTests(SizedOverIterableTests, ContainerOverIterableTests, EqualityTests):

    @property
    @abc.abstractmethod
    def empty(self) -> ClassUnderTest:
        pass

    def test_generic_612_zero_iterations_over_empty(self) -> None:
        with self.assertRaises(StopIteration):
            next(iter(self.empty))

    def test_generic_623_len_empty_is_zero(self) -> None:
        self.assertEqual(len(self.empty), 0)

    def test_generic_627_get_on_empty_raises_KeyError(self, a: ElementT) -> None:
        with self.assertRaises(KeyError):
            _ = self.empty[a]

#     def test_650_keys_view_type(self, a):
#         self.assertEqual(isinstance(a.keys(), collections.abc.KeysView))


class MutableMappingTests(MappingTests):
    pass


class frozensetExtensionTests(SetTests):

    def test_generic_629_copy_definition(self, a: ClassUnderTest) -> None:
        b = a.copy()
        self.assertEqual(a, b)

    def test_generic_640_issubset_defintion(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a.issubset(b), a <= b)

    def test_generic_641_isuperset_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a.issuperset(b), a >= b)

    def test_generic_642_union_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a.union(b), a | b)

    def test_generic_643_intersection_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a.intersection(b), a & b)

    def test_generic_644_difference_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a.difference(b), a - b)

    def test_generic_645_symmetric_difference_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a.symmetric_difference(b), a ^ b)


element_st = st.integers()
@Given({ClassUnderTest: st.frozensets(element_st), ElementT: element_st})
class Test_frozenset(frozensetExtensionTests):

    empty = frozenset()

    def test_generic_690_singleton_frozenset(self, a: ElementT) -> None:
        singleton = frozenset([a])
        self.assertEqual(len(singleton), 1)
        self.assertTrue(a in singleton)


element_st = st.integers()
@Given({ClassUnderTest: st.sets(element_st), ElementT: element_st})
class Test_set(frozensetExtensionTests):

    empty = set()

    def test_generic_629_copy_definition(self, a: ClassUnderTest) -> None:
        b = a.copy()
        self.assertNotEqual(id(a), id(b))
        self.assertEqual(a, b)

    def test_generic_646_add_definition(self, a: ClassUnderTest, b: ElementT) -> None:
        a_copy = a.copy()
        a.add(b)
        self.assertTrue(a_copy <= a)
        self.assertTrue(b in a)

    def test_generic_647_discard_definition(self, a: ClassUnderTest, b: ElementT) -> None:
        a_copy = a.copy()
        a.discard(b)
        self.assertTrue(a <= a_copy)
        self.assertTrue(b not in a)

    def test_generic_648_update_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        a_copy = a.copy()
        a_nother = a.copy()
        a |= b
        self.assertEqual(a, a_copy | b)
        a_nother.update(b)
        self.assertEqual(a, a_nother)

    def test_generic_649_intersection_update_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        a_copy = a.copy()
        a_nother = a.copy()
        a &= b
        self.assertEqual(a, a_copy & b)
        a_nother.intersection_update(b)
        self.assertEqual(a, a_nother)

    def test_generic_650_difference_update_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        a_copy = a.copy()
        a_nother = a.copy()
        a -= b
        self.assertEqual(a, a_copy - b)
        a_nother.difference_update(b)
        self.assertEqual(a, a_nother)

    def test_generic_651_symmetric_difference_update_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        a_copy = a.copy()
        a_nother = a.copy()
        a ^= b
        self.assertEqual(a, a_copy ^ b)
        a_nother.symmetric_difference_update(b)
        self.assertEqual(a, a_nother)

    def test_generic_652_remove_definition(self, a: ClassUnderTest, b: ElementT) -> None:
        a.add(b)
        a_copy = a.copy()
        a.remove(b)
        a_copy.discard(b)
        self.assertEqual(a, a_copy)
        with self.assertRaises(KeyError):
            a.remove(b)

    def test_generic_653_pop_definition(self, a: ClassUnderTest) -> None:
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

    def test_generic_654_clear_definition(self, a: ClassUnderTest) -> None:
        a.clear()
        self.assertEqual(a, self.empty)


key_st = st.integers()
value_st = st.integers()
@Given({ClassUnderTest: st.dictionaries(key_st, value_st), ElementT: key_st})
class Test_dict(MutableMappingTests):

    empty = dict()


if __name__ == '__main__':

    SUITE = unittest.TestSuite()
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_frozenset))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_set))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_dict))
    TR = unittest.TextTestRunner(verbosity=2)
    TR.run(SUITE)

"""
Copyright 2018 Steve Palmer
"""

import abc
import collections
import unittest

from hypothesis import assume, strategies as st

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

    def test_generic_020_empty_has_right_type(self) -> None:
        self.assertTrue(isinstance(self.empty), collections.abc.Set)

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

    @abc.abstractmethod
    def copy(self, a: ClassUnderTest) -> ClassUnderTest:
        pass

    @abc.abstractmethod
    def singleton_constructor(self, a: ElementT) -> ClassUnderTest:
        pass

    def test_generic_020_empty_has_right_type(self) -> None:
        self.assertTrue(isinstance(self.empty, collections.abc.MutableSet))

    def test_generic_021_copy_helper_definition(self, a: ClassUnderTest) -> None:
        a_copy = self.copy(a)
        self.assertTrue(isinstance(a_copy, collections.abc.MutableSet))
        self.assertNotEqual(id(a), id(a_copy))
        self.assertEqual(a, a_copy)

    def test_generic_022_singleton_constructor_helper_definition(self, a: ElementT) -> None:
        a_singleton = self.singleton_constructor(a)
        self.assertTrue(isinstance(a_singleton, collections.abc.MutableSet))
        self.assertTrue(a in a_singleton)
        self.assertEqual(len(a_singleton), 1)

    def test_generic_635_add_definition(self, a: ClassUnderTest, b: ElementT) -> None:
        a_copy = self.copy(a)
        b_singleton = self.singleton_constructor(b)
        a.add(b)
        self.assertEqual(a, a_copy | b_singleton)

    def test_generic_636_discard_definition(self, a: ClassUnderTest, b: ElementT) -> None:
        a_copy = self.copy(a)
        b_singleton = self.singleton_constructor(b)
        a.discard(b)
        self.assertEqual(a, a_copy - b_singleton)


class MappingViewTests(SizedTests):
    pass


class KeysViewTests(MappingViewTests, SetTests):
    pass


class ItemsViewTests(MappingViewTests, SetTests):
    pass


class ValuesViewTests(MappingViewTests, ContainerOverIterableTests):
    pass


class MappingTests(SizedOverIterableTests, ContainerOverIterableTests, EqualityTests):

    @property
    @abc.abstractmethod
    def empty(self) -> ClassUnderTest:
        pass

    @abc.abstractmethod
    def singleton_constructor(self, a: ElementT, b: ValueT) -> ClassUnderTest:
        pass

    def test_generic_020_empty_has_the_right_type(self) -> None:
        self.assertTrue(isinstance(self.empty, collections.abc.Mapping))

    def test_generic_021_singleton_constructor_helper_definition(self, a: ElementT, b: ValueT):
        map_singleton = self.singleton_constructor(a, b)
        self.assertTrue(isinstance(map_singleton, collections.abc.Mapping))
        self.assertEqual(map_singleton[a], b)
        self.assertEqual(len(map_singleton), 1)

    def test_generic_105_equality_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        self.assertEqual(a == b, a.keys() == b.keys() and all(a[k] == b[k] for k in a))

    def test_generic_612_zero_iterations_over_empty(self) -> None:
        with self.assertRaises(StopIteration):
            next(iter(self.empty))

    def test_generic_623_len_empty_is_zero(self) -> None:
        self.assertEqual(len(self.empty), 0)

    def test_generic_627_getitem_on_empty_either_succeeds_or_raises_KeyError(self, a: ElementT) -> None:
        try:
            _ = self.empty[a]
        except KeyError:
            pass
        except:
            self.fail()

    def test_generic_628_getitem_over_all_keys_succeeds(self, a: ClassUnderTest) -> None:
        a_keys = a.keys()
        self.assertTrue(isinstance(a_keys, collections.abc.KeysView))
        try:
            for k in a_keys:
                _ = a[k]
        except KeyError:
            self.fail()

    def test_generic_650_items_returns_an_ItemsView(self, a: ClassUnderTest) -> None:
        self.assertTrue(isinstance(a.items(), collections.abc.ItemsView))

    def test_generic_651_values_returns_an_ValuesView(self, a: ClassUnderTest) -> None:
        self.assertTrue(isinstance(a.values(), collections.abc.ValuesView))

    def test_generic_652_get_on_empty_returns_default(self, a: ElementT, b: ValueT) -> None:
        self.assertEqual(self.empty.get(a, b), b)


class MutableMappingTests(MappingTests):

    @abc.abstractmethod
    def copy(self, a: ClassUnderTest) -> ClassUnderTest:
        pass

    def test_generic_022_copy_helper_definition(self, a: ClassUnderTest) -> None:
        a_copy = self.copy(a)
        self.assertTrue(isinstance(a_copy, collections.abc.MutableMapping))
        self.assertNotEqual(id(a), id(a_copy))
        self.assertEqual(a, a_copy)

    def test_generic_630_setitem_definition(self, a: ClassUnderTest, b: ElementT, c: ValueT) -> None:
        a_copy = self.copy(a)
        a[b] = c
        self.assertEqual(a[b], c)
        for key in a_copy:
            if key != b:
                self.assertEqual(a[key], a_copy[key])

    def test_generic_631_delitem_definition(self, a: ClassUnderTest, data) -> None:
        assume(len(a) > 0)
        a_copy = self.copy(a)
        key_to_forget = data.draw(st.sampled_from(list(a.keys())))
        del a[key_to_forget]
        self.assertTrue(key_to_forget not in a)
        for other_key in a_copy:
            if other_key != key_to_forget:
                self.assertEqual(a[other_key], a_copy[other_key])


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


class dictExtensionTests(MutableMappingTests):

    def copy(self, a: ClassUnderTest) -> ClassUnderTest:
        return a.copy()


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
class Test_set(MutableSetTests, frozensetExtensionTests):

    empty = set()

    def copy(self, s: ClassUnderTest) -> ClassUnderTest:
        return s.copy()

    def singleton_constructor(self, a: ElementT) -> ClassUnderTest:
        return set([a])

    def test_generic_629_copy_definition(self, a: ClassUnderTest) -> None:
        b = a.copy()
        self.assertNotEqual(id(a), id(b))
        self.assertEqual(a, b)

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
@Given({ClassUnderTest: st.builds(lambda m: m.keys(), st.dictionaries(key_st, value_st)), ElementT: key_st})
class Test_dict_KeysView(KeysViewTests):

    empty = dict().keys()


key_st = st.integers()
value_st = st.integers()
@Given({ClassUnderTest: st.builds(lambda m: m.items(), st.dictionaries(key_st, value_st)), ElementT: key_st})
class Test_dict_ItemsView(ItemsViewTests):

    empty = dict().items()


key_st = st.integers()
value_st = st.integers()
@Given({ClassUnderTest: st.builds(lambda m: m.values(), st.dictionaries(key_st, value_st)), ElementT: key_st})
class Test_dict_ValuesView(ValuesViewTests):

    empty = dict().values()


key_st = st.integers()
value_st = st.integers()
@Given({ClassUnderTest: st.dictionaries(key_st, value_st), ElementT: key_st, ValueT: value_st})
class Test_dict(dictExtensionTests):

    empty = dict()

    def singleton_constructor(self, a: ElementT, b: ValueT) -> ClassUnderTest:
        return {a: b}


key_st = st.characters()
value_st = st.integers(min_value=0)
@Given({ClassUnderTest: st.builds(collections.Counter, st.text(key_st)), ElementT: key_st, ValueT: value_st})
class Test_Counter(dictExtensionTests):

    empty = collections.Counter()

    def singleton_constructor(self, a: ElementT, b: ValueT) -> ClassUnderTest:
        return collections.Counter({a: b})


key_st = st.integers()
value_st = st.integers()
@Given({ClassUnderTest: st.builds(collections.OrderedDict, st.lists(st.tuples(key_st, value_st))), ElementT: key_st, ValueT: value_st})
class Test_OrderedDict(dictExtensionTests):

    empty = collections.OrderedDict()

    def singleton_constructor(self, a: ElementT, b: ValueT) -> ClassUnderTest:
        return collections.OrderedDict([(a, b)])


if __name__ == '__main__':

    SUITE = unittest.TestSuite()
#     SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_frozenset))
#     SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_set))
#     SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_dict_KeysView))
#     SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_dict_ItemsView))
#     SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_dict_ValuesView))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_dict))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_Counter))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_OrderedDict))
    TR = unittest.TextTestRunner(verbosity=2)
    TR.run(SUITE)

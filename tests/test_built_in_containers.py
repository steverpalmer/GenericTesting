#!/usr/bin/env python3
# Copyright 2021 Steve Palmer

"""A test of the generic_test.built_in_tests using the built-in container types."""

import unittest
import collections
import types

from hypothesis import strategies as st

from generic_testing_test_context import generic_testing


element_st = st.integers()


@generic_testing.Given(
    {
        generic_testing.ClassUnderTest: st.frozensets(element_st),
        generic_testing.ElementT: element_st,
    }
)
class Test_frozenset(generic_testing.frozensetTests):
    pass


element_st = st.integers()


@generic_testing.Given(
    {
        generic_testing.ClassUnderTest: st.sets(element_st),
        generic_testing.ElementT: element_st,
    }
)
class Test_set(generic_testing.setTests):
    pass


key_st = st.integers()
value_st = st.integers()


@generic_testing.Given(
    {
        generic_testing.ClassUnderTest: st.builds(
            lambda m: m.keys(), st.dictionaries(key_st, value_st)
        ),
        generic_testing.ElementT: key_st,
    }
)
class Test_dict_KeysView(generic_testing.dictKeysViewTests):
    pass


key_st = st.integers()
value_st = st.integers()


@generic_testing.Given(
    {
        generic_testing.ClassUnderTest: st.builds(
            lambda m: m.items(), st.dictionaries(key_st, value_st)
        ),
        generic_testing.ElementT: key_st,
    }
)
class Test_dict_ItemsView(generic_testing.dictItemsViewTests):
    pass


key_st = st.integers()
value_st = st.integers()


@generic_testing.Given(
    {
        generic_testing.ClassUnderTest: st.builds(
            lambda m: m.values(), st.dictionaries(key_st, value_st)
        ),
        generic_testing.ElementT: key_st,
    }
)
class Test_dict_ValuesView(generic_testing.dictValuesViewTests):
    pass


key_st = st.integers()
value_st = st.integers()


@generic_testing.Given(
    {
        generic_testing.ClassUnderTest: st.builds(
            (lambda d: types.MappingProxyType(d)), st.dictionaries(key_st, value_st)
        ),
        generic_testing.KeyT: key_st,
        generic_testing.ValueT: value_st,
    }
)
class Test_MappingProxyType(generic_testing.MappingProxyTypeTests):
    pass


key_st = st.integers()
value_st = st.integers()


@generic_testing.Given(
    {
        generic_testing.ClassUnderTest: st.dictionaries(key_st, value_st),
        generic_testing.KeyT: key_st,
        generic_testing.ValueT: value_st,
    }
)
class Test_dict(generic_testing.dictTests):
    pass


key_st = st.characters()
value_st = st.integers(min_value=0)


@generic_testing.Given(
    {
        generic_testing.ClassUnderTest: st.builds(collections.Counter, st.text(key_st)),
        generic_testing.KeyT: key_st,
        generic_testing.ValueT: value_st,
    }
)
class Test_Counter(generic_testing.CounterTests):
    pass


key_st = st.integers()
value_st = st.integers()


@generic_testing.Given(
    {
        generic_testing.ClassUnderTest: st.builds(
            collections.OrderedDict, st.lists(st.tuples(key_st, value_st))
        ),
        generic_testing.KeyT: key_st,
        generic_testing.ValueT: value_st,
    }
)
class Test_OrderedDict(generic_testing.OrderedDictTests):
    pass


class factory:
    def __init__(self):
        self.count = 0

    def __call__(self):
        self.count += 1
        return self.count


key_st = st.integers()
value_st = st.integers()


@generic_testing.Given(
    {
        generic_testing.ClassUnderTest: st.builds(
            (lambda items: collections.defaultdict(factory(), items)),
            st.lists(st.tuples(key_st, value_st)),
        ),
        generic_testing.KeyT: key_st,
        generic_testing.ValueT: value_st,
    }
)
class Test_defaultdict(generic_testing.defaultdictTests):
    def __init__(self, methodName=None):
        super().__init__(factory(), methodName)


values_st = st.integers()


@generic_testing.Given(
    {
        generic_testing.ClassUnderTest: st.lists(values_st).map(lambda l: tuple(l)),
        generic_testing.KeyT: st.integers(min_value=-(2 ** 30), max_value=2 ** 30),
        generic_testing.ValueT: values_st,
        generic_testing.ScalarT: st.integers(min_value=-1, max_value=10),
    }
)
class Test_tuple(generic_testing.tupleTests):
    pass


alphabet_st = st.characters()


@generic_testing.Given(
    {
        generic_testing.ClassUnderTest: st.text(alphabet_st),
        generic_testing.KeyT: st.integers(min_value=-(2 ** 30), max_value=2 ** 30),
        generic_testing.ValueT: alphabet_st,
        generic_testing.ScalarT: st.integers(min_value=-1, max_value=10),
    }
)
class Test_str(generic_testing.tupleTests):

    empty = ""


values_st = st.integers()


@generic_testing.Given(
    {
        generic_testing.ClassUnderTest: st.lists(values_st),
        generic_testing.KeyT: st.integers(min_value=-(2 ** 30), max_value=2 ** 30),
        generic_testing.ValueT: values_st,
        generic_testing.ScalarT: st.integers(min_value=-1, max_value=10),
    }
)
class Test_list(generic_testing.listTests):
    pass


__all__ = (
    "Test_frozenset",
    "Test_set",
    "Test_dict_KeysView",
    "Test_dict_ItemsView",
    "Test_dict_ValuesView",
    "Test_MappingProxyType",
    "Test_dict",
    "Test_Counter",
    "Test_OrderedDict",
    "Test_defaultdict",
    "Test_tuple",
    "Test_list",
)


if __name__ == "__main__":
    SUITE = unittest.TestSuite()
    #  name = None  # :TRICK: need to introdcue 'name' before iterating through locals
    #  value = None  # :TRICK: need to introdcue 'value' before iterating through locals
    #  for name, value in locals().items():
    #      if name.startswith('Test_'):
    #          SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(value))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_frozenset))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_set))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_dict_KeysView))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_dict_ItemsView))
    SUITE.addTest(
        unittest.defaultTestLoader.loadTestsFromTestCase(Test_dict_ValuesView)
    )
    SUITE.addTest(
        unittest.defaultTestLoader.loadTestsFromTestCase(Test_MappingProxyType)
    )
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_dict))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_Counter))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_OrderedDict))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_defaultdict))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_tuple))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_str))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_list))
    TR = unittest.TextTestRunner(verbosity=2)
    TR.run(SUITE)

#!/usr/bin/env python3
# Copyright 2018 Steve Palmer

"""A test of the generic_test.built_in_tests using the built-in container types."""

import unittest
import collections
import types

from hypothesis import strategies as st

from src import *


element_st = st.integers()


@Given({ClassUnderTest: st.frozensets(element_st),
        ElementT: element_st})
class Test_frozenset(frozensetTests):
    pass


element_st = st.integers()


@Given({ClassUnderTest: st.sets(element_st),
        ElementT: element_st})
class Test_set(setTests):
    pass


key_st = st.integers()
value_st = st.integers()


@Given({ClassUnderTest: st.builds(lambda m: m.keys(), st.dictionaries(key_st, value_st)),
        ElementT: key_st})
class Test_dict_KeysView(dictKeysViewTests):
    pass


key_st = st.integers()
value_st = st.integers()


@Given({ClassUnderTest: st.builds(lambda m: m.items(), st.dictionaries(key_st, value_st)),
        ElementT: key_st})
class Test_dict_ItemsView(dictItemsViewTests):
    pass


key_st = st.integers()
value_st = st.integers()


@Given({ClassUnderTest: st.builds(lambda m: m.values(), st.dictionaries(key_st, value_st)),
        ElementT: key_st})
class Test_dict_ValuesView(dictValuesViewTests):
    pass


key_st = st.integers()
value_st = st.integers()


@Given({ClassUnderTest: st.builds((lambda d: types.MappingProxyType(d)), st.dictionaries(key_st, value_st)),
        KeyT: key_st,
        ValueT: value_st})
class Test_MappingProxyType(MappingProxyTypeTests):
    pass


key_st = st.integers()
value_st = st.integers()


@Given({ClassUnderTest: st.dictionaries(key_st, value_st),
        KeyT: key_st,
        ValueT: value_st})
class Test_dict(dictTests):
    pass


key_st = st.characters()
value_st = st.integers(min_value=0)


@Given({ClassUnderTest: st.builds(collections.Counter, st.text(key_st)),
        KeyT: key_st,
        ValueT: value_st})
class Test_Counter(CounterTests):
    pass


key_st = st.integers()
value_st = st.integers()


@Given({ClassUnderTest: st.builds(collections.OrderedDict, st.lists(st.tuples(key_st, value_st))),
        KeyT: key_st,
        ValueT: value_st})
class Test_OrderedDict(OrderedDictTests):
    pass


class factory:

    def __init__(self):
        self.count = 0

    def __call__(self):
        self.count += 1
        return self.count


key_st = st.integers()
value_st = st.integers()


@Given({ClassUnderTest: st.builds((lambda items: collections.defaultdict(factory(), items)), st.lists(st.tuples(key_st, value_st))),
        KeyT: key_st,
        ValueT: value_st})
class Test_defaultdict(defaultdictTests):

    def __init__(self, methodName=None):
        super().__init__(factory(), methodName)


values_st = st.integers()


@Given({ClassUnderTest: st.lists(values_st).map(lambda l: tuple(l)),
        KeyT: st.integers(min_value=-(2**30), max_value=2**30),
        ValueT: values_st,
        ScalarT: st.integers(min_value=-1, max_value=10)})
class Test_tuple(tupleTests):
    pass


alphabet_st = st.characters()


@Given({ClassUnderTest: st.text(alphabet_st),
        KeyT: st.integers(min_value=-(2**30), max_value=2**30),
        ValueT: alphabet_st,
        ScalarT: st.integers(min_value=-1, max_value=10)})
class Test_str(tupleTests):

    empty = ''


values_st = st.integers()


@Given({ClassUnderTest: st.lists(values_st),
        KeyT: st.integers(min_value=-(2**30), max_value=2**30),
        ValueT: values_st,
        ScalarT: st.integers(min_value=-1, max_value=10)})
class Test_list(listTests):
    pass


__all__ = ('Test_frozenset', 'Test_set',
           'Test_dict_KeysView', 'Test_dict_ItemsView', 'Test_dict_ValuesView',
           'Test_MappingProxyType', 'Test_dict',
           'Test_Counter', 'Test_OrderedDict', 'Test_defaultdict', 'Test_tuple', 'Test_list')


if __name__ == '__main__':
    SUITE = unittest.TestSuite()
    name = None  # :TRICK: need to introdcue 'name' before iterating through locals
    value = None  # :TRICK: need to introdcue 'value' before iterating through locals
    for name, value in locals().items():
        if name.startswith('Test_'):
            SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(value))
#     SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_str))
    TR = unittest.TextTestRunner(verbosity=2)
    TR.run(SUITE)

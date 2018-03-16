#!/usr/bin/env python3
# Copyright 2018 Steve Palmer

"""A test of the generic_test.enums using the standard library enum module types."""

import unittest
import enum

from hypothesis import strategies as st

from generic_testing.core import ClassUnderTest, Given
from generic_testing.enums import KeyT, EnumTests, UniqueEnumTests, IntEnumTests


class E1(enum.Enum):
    red = 0
    blue = 1
    green = 1


@Given({ClassUnderTest: st.sampled_from(E1),
        KeyT: st.sampled_from(list(E1.__members__))})
class Test_E1(EnumTests):

    def __init__(self, methodName=None):
        super().__init__(E1, methodName=methodName)


class E2(enum.Enum):
    red = 0
    blue = 1
    green = 2


@Given({ClassUnderTest: st.sampled_from(E2),
        KeyT: st.sampled_from(list(E2.__members__))})
class Test_E2(UniqueEnumTests):

    def __init__(self, methodName=None):
        super().__init__(E2, methodName=methodName)


class E3(enum.IntEnum):
    red = 0
    blue = 1
    green = 1


@Given({ClassUnderTest: st.sampled_from(E3),
        KeyT: st.sampled_from(list(E3.__members__))})
class Test_E3(IntEnumTests):

    def __init__(self, methodName=None):
        super().__init__(E3, methodName=methodName)


if __name__ == '__main__':
    SUITE = unittest.TestSuite()
    name = None  # :TRICK: need to introdcue 'name' before iterating through locals
    value = None  # :TRICK: need to introdcue 'value' before iterating through locals
    for name, value in locals().items():
        if name.startswith('Test_'):
            SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(value))
    TR = unittest.TextTestRunner(verbosity=2)
    TR.run(SUITE)

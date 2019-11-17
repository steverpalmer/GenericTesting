#!/usr/bin/env python3
# Copyright 2018 Steve Palmer

"""A test of the generic_test.enums using the standard library enum module types."""

import unittest
import enum

from generic_testing_test_context import generic_testing


class E1(enum.Enum):
    red = 0
    blue = 1
    green = 1


@generic_testing.Given(generic_testing.enum_strategy_dict(E1))
class Test_E1(generic_testing.EnumTests):
    pass


@enum.unique
class E2(enum.Enum):
    red = 0
    blue = 1
    green = 2


@generic_testing.Given(generic_testing.enum_strategy_dict(E2))
class Test_E2(generic_testing.UniqueEnumMixinTests, generic_testing.EnumTests):
    pass


class E3(enum.IntEnum):
    red = 0
    blue = 1
    green = 1


@generic_testing.Given(generic_testing.enum_strategy_dict(E3))
class Test_E3(generic_testing.IntEnumTests):
    pass


class E4(enum.Flag):
    black = 0
    red = 1
    blue = 2
    green = 4
    white = 7


@generic_testing.Given(generic_testing.enum_strategy_dict(E4))
class Test_E4(generic_testing.UniqueEnumMixinTests, generic_testing.FlagEnumMixinTests, generic_testing.EnumTests):

    @property
    def bottom(self):
        return E4.black


if __name__ == '__main__':
    SUITE = unittest.TestSuite()
    name = None  # :TRICK: need to introdcue 'name' before iterating through locals
    value = None  # :TRICK: need to introdcue 'value' before iterating through locals
    for name, value in locals().items():
        if name.startswith('Test_'):
            SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(value))
    TR = unittest.TextTestRunner(verbosity=2)
    TR.run(SUITE)

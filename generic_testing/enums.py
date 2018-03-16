# Copyright 2018 Steve Palmer

"""A library of generic test for the elementary function properties."""

from hypothesis import strategies as st

from generic_testing.core import ClassUnderTest, Given
from generic_testing.relations import EqualityTests
from generic_testing.collections_abc import ValueT


class EnumTests(EqualityTests):

    def __init__(self, cls, methodName=None):
        super().__init__(methodName=methodName)
        self.right_inverse = cls.__call__

    def test_generic_2110_equality_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        self.assertEqual(a == b, a.value == b.value)

    def test_generic_xxxx_value_is_injective(self, a: ClassUnderTest, b: ClassUnderTest):
        """a != b ⇒ a.value != b.value"""
        self.assertImplies(not a == b, not a.value == b.value)

    def test_generic_xxxx_value_is_surjective(self, a: ValueT):
        """Enum(a).value == a"""
        self.assertEqual(self.right_inverse(a).value, a)


import enum


class E(enum.Enum):
    red = 1
    blue = 2
    green = 3


@Given({ClassUnderTest: st.sampled_from(E),
        ValueT: st.sampled_from([e.value for e in E])})
class Test_E(EnumTests):

    def __init__(self, methodName=None):
        super().__init__(E, methodName=methodName)


if __name__ == '__main__':
    import unittest
    SUITE = unittest.TestSuite()
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_E))
    TR = unittest.TextTestRunner(verbosity=2)
    TR.run(SUITE)

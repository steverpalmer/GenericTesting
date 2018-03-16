# Copyright 2018 Steve Palmer

"""A library of generic test for the elementary function properties."""

from hypothesis import strategies as st

from generic_testing.core import GenericTests, ClassUnderTest, Given
from generic_testing.relations import EqualityTests


DomainT = 'DomainT'
CodomainT = 'CodomainT'


class FunctionTests(GenericTests):

    def __init__(self, function, right_inverse=None, methodName=None):
        super().__init__(methodName)
        self.function = function
        self.right_inverse = right_inverse

    @staticmethod
    def relabel(annotation):
        if annotation == ClassUnderTest:
            return DomainT
        return GenericTests.relabel(annotation)


class InjectiveTests(FunctionTests):

    def test_generic_xxxx_is_injective(self, a: DomainT, b: DomainT) -> None:
        self.assertImplies(not a == b, not self.function(a) == self.function(b))


class SurjectiveTests(FunctionTests):

    def test_generic_xxxx_is_surjective(self, a: CodomainT) -> None:
        self.assertEqual(self.function(self.right_inverse(a)), a)


class BijectiveTests(InjectiveTests, SurjectiveTests):
    pass


class EnumTests(SurjectiveTests, EqualityTests):

    def __init__(self, cls, methodName=None):
        super().__init__(lambda e: e.value, cls.__call__, methodName=methodName)


import enum


class E(enum.Enum):
    red = 1
    blue = 2
    green = 2


@Given({DomainT: st.sampled_from(E), CodomainT: st.sampled_from([e.value for e in E])})
class Test_E(EnumTests):

    def __init__(self, methodName=None):
        super().__init__(E, methodName=methodName)


if __name__ == '__main__':
    import unittest
    SUITE = unittest.TestSuite()
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_E))
    TR = unittest.TextTestRunner(verbosity=2)
    TR.run(SUITE)

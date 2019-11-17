# Copyright 2018 Steve Palmer

"""A library of generic test for the datetime classes."""

import datetime
import unittest

from hypothesis import strategies as st

from .core import ClassUnderTest, Given
from .relations import EqualityTests, TotalOrderingTests, VectorSpaceTests, VectorSpaceT, ScalarT, AffineSpaceTests


class timedeltaTests(EqualityTests, TotalOrderingTests, VectorSpaceTests):
    """Tests of timedelta class properties."""

    zero = datetime.timedelta()
    abs_zero = zero
    scalar_one = 1.0

    def test_generic_2353_less_or_equal_consistent_with_addition(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        """a <= b ⇔ a + c <= b + c"""
        self.assertEqual(a <= b, a + c <= b + c)

    def test_generic_2354_less_or_equal_consistent_with_multiplication(self, a: ScalarT, b: ClassUnderTest) -> None:
        """0 <= a and 0 <= b ⇒ 0 <= a * b"""
        self.assertImplies((self.scalar_one - self.scalar_one) <= a and self.zero <= b, self.zero <= a * b)


class datetimeTests(EqualityTests, TotalOrderingTests, AffineSpaceTests):
    """Tests of datetime class properties."""

    vector_space_zero = datetime.timedelta()


class dateTests(EqualityTests, TotalOrderingTests, AffineSpaceTests):
    """Tests of date class properties."""

    vector_space_zero = datetime.timedelta()


@Given({ClassUnderTest: st.integers(min_value=-864000000000, max_value=864000000000).map(lambda i: datetime.timedelta(milliseconds=i)),
        ScalarT: st.integers(min_value=-100, max_value=100).map(lambda i: i / 10.0)})
class Test_timedelta(timedeltaTests):
    pass


@Given({ClassUnderTest: st.datetimes(min_value=datetime.datetime(1900, 1, 1), max_value=datetime.datetime(2100, 1, 1)),
        VectorSpaceT: st.timedeltas(min_value=datetime.timedelta(-3650), max_value=datetime.timedelta(3650))})
class Test_datetime(datetimeTests):
    pass


@Given({ClassUnderTest: st.dates(min_value=datetime.date(1900, 1, 1), max_value=datetime.date(2100, 1, 1)),
        VectorSpaceT: st.integers(min_value=-3650, max_value=3650).map(lambda i: datetime.timedelta(i))})
class Test_date(dateTests):
    pass


SUITE = unittest.TestSuite()
SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_timedelta))
SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_datetime))
SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_date))
TR = unittest.TextTestRunner(verbosity=2)
TR.run(SUITE)

#!/usr/bin/env python3
"""
Copyright 2018 Steve Palmer
"""


import unittest
import inspect

from hypothesis import given

from isclose import IsClose


class BaseTests(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.isclose = IsClose()
        self.addTypeEqualityFunc(float, self.assertIsClose)
        self.addTypeEqualityFunc(complex, self.assertIsClose)

    def assertImplies(self, antecedent, consequent, msg: str=None):
        """
        I like implies as an operator ... so shoot me.
        """
        if antecedent and not consequent:
            if msg is None:
                msg = "Consquent is False even though Antecedent is True"
            raise self.failureException(msg)

    def assertIsClose(self, a, b, msg: str=None):
        """
        Sort of like assertAlmostEqual, but defined in terms of IsClose.
        """
        if not self.isclose(a, b):
            if msg is None:
                msg = "{a} is not close enough to {b}".format(a=a, b=b)
            raise self.failureException(msg)

    def assertNotIsClose(self, a, b, msg: str=None):
        """
        assertNotIsClose is to assertIsClose as assertNotAlmostEqual is to assertAlmostEqual - completeness
        """
        if not self.isclose(a, b):
            if msg is None:
                msg = "{a} is not close enough to {b}".format(a=a, b=b)
            raise self.failureException(msg)

    def assertCloseOrLessThan(self, a, b, msg: str=None):
        if not (a < b or self.isclose(a, b)):
            if msg is None:
                msg = "{a} is not sufficiently less than {b}".format(a=a, b=b)
            raise self.failureException(msg)

    def assertCloseOrGreaterThan(self, a, b, msg: str=None):
        if not (a > b or self.isclose(a, b)):
            if msg is None:
                msg = "{a} is not sufficiently less than {b}".format(a=a, b=b)
            raise self.failureException(msg)


def Given(strategy=None, *, testMethodPrefix='test'):
    """
    Decorator for BaseTest derived test cases
    """
    if strategy is None:
        strategy = dict()
    elif not isinstance(strategy, dict):
        strategy = {None: strategy}
#    apply_given = all(isinstance(value, strategies) for value in strategy.values())
    def result(cls):
        if not issubclass(cls, BaseTests):
            raise TypeError("should operate on classes inheriting from BaseTest")
        for name, method in inspect.getmembers(cls):
            if name.startswith(testMethodPrefix) and callable(method):
#                 args = {arg: strategy[value.annotation if value.annotation != inspect.Parameter.empty else None]
#                         for arg, value in inspect.signature(method).parameters.items() if arg != 'self'}
                signature = inspect.signature(method)
                parameters = signature.parameters
                args = {arg: param for arg, param in parameters.items() if arg != 'self'}
                if len(args) > 0:
                    attr = given(**{arg: strategy.get(param.annotation if param.annotation != inspect.Parameter.empty else None, None) for arg, param in args.items()})(method)
                    setattr(cls, name, attr)
        return cls
    return result


ClassUnderTest = 'ClassUnderTest'


__all__ = ('BaseTests', 'Given', 'ClassUnderTest')

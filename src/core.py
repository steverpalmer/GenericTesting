#!/usr/bin/env python3
"""
Copyright 2018 Steve Palmer
"""

import abc
import unittest
import inspect

from hypothesis import given, strategies as st

from .isclose import IsClose


class GenericTests(unittest.TestCase, metaclass=abc.ABCMeta):

    def __init__(self, methodName=None):
        """
        unittest.TestCase defines the default methodName to be 'runtest'.
        Rather than repeat this through the code,
        GenericTests default the value to None, and then substitute 'runTest' here.
        """
        if methodName is None:
            methodName = 'runTest'
        super().__init__(methodName)
        self.isclose = IsClose()
        self.addTypeEqualityFunc(float, self.assertIsClose)
        self.addTypeEqualityFunc(complex, self.assertIsClose)

    def assertIsInstance(self, obj, type_, msg: str=None):
        """
        I kept writing self.assertTrue(isinstance(obj, type_)),
        and getting little useful information back on failure!
        """
        if not isinstance(obj, type_):
            if msg is None:
                msg = "{obj} has type {obj_type}, not {type} as expected".format(obj=obj, obj_type=type(obj), type=type_)
            raise self.failureException(msg)

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


ClassUnderTest = 'ClassUnderTest'


def Given(strategy=None, *, testMethodPrefix='test_generic', data_arg='data'):
    """
    Decorator for BaseTest derived test cases
    """
    if strategy is None:
        strategy = dict()
    elif not isinstance(strategy, dict):
        strategy = {ClassUnderTest: strategy}

#    apply_given = all(isinstance(value, strategies) for value in strategy.values())
    def result(cls):
        if not issubclass(cls, GenericTests):
            raise TypeError("should operate on classes inheriting from BaseTest")
        for name, method in inspect.getmembers(cls):
            if name.startswith(testMethodPrefix) and callable(method):
                signature = inspect.signature(method)
                parameters = signature.parameters
                args = {arg: param for arg, param in parameters.items() if arg != 'self'}
                if len(args) > 0:
                    given_args = dict()
                    for arg, param in args.items():
                        annotation = None if param.annotation == inspect.Parameter.empty else param.annotation
                        if annotation in strategy:
                            strat = strategy[annotation]
                        elif arg == data_arg:
                            strat = st.data()
                        else:
                            strat = None
                        given_args[arg] = strat
                    attr = given(**given_args)(method)
                    setattr(cls, name, attr)
        return cls
    return result


__all__ = ('GenericTests', 'Given', 'ClassUnderTest')

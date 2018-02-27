#!/usr/bin/env python3
"""
Copyright 2018 Steve Palmer
"""


import unittest
import inspect

from hypothesis import given, strategies

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


def base_test_modifier(strategy=None, *, testMethodPrefix='test'):
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
                    attr = given(**{arg: strategy[param.annotation if param.annotation != inspect.Parameter.empty else None] for arg, param in args.items()})(method)
#                     else:
#                         for arg, param in args.items():
#                             if param.annotation != inspect.Parameter.empty and param.annotation in strategy:
#                                 parameters[arg] = param.replace(annotation=strategy[param.annotation])
#                         signature = signature.replace(parameters=parameters)
#                         
                    setattr(cls, name, attr)
        return cls
    return result


"""
To get a handle on the unittest.TestCase assert checks,
I've been considering something like the following...

class Wrapper():

    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def __repr__(self) -> str:
        return "NumberWrapper({0.value!r})".format(self)

    def __str__(self) -> str:
        return str(self._value)

    def __getattr__(self, name):
        return getattr(self._value, name)
"""


__all__ = ('BaseTests', 'base_test_modifier')

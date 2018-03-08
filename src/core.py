# Copyright 2018 Steve Palmer

"""Fundemental tools in the GenericTesting library."""

import abc
import unittest
import inspect

from hypothesis import given, strategies as st

from .isclose import IsClose


class GenericTests(unittest.TestCase, metaclass=abc.ABCMeta):
    """Base class for all Generic Tests.

    This extends the self.assert* methods on unittest.TestCase,
    including an isclose tool for use on floating point types.
    """

    def __init__(self, methodName=None):
        """Constructor.

        unittest.TestCase defines the default methodName to be 'runtest'.
        Rather than repeat this through the code,
        GenericTests default the value to None, and then substitute 'runTest' here.
        """
        if methodName is None:
            methodName = 'runTest'
        super().__init__(methodName)

        # some types are based on floating point approximations,
        # so equality on these types need to be IsClose.
        self.isclose = IsClose()
        self.addTypeEqualityFunc(float, self.assertIsClose)
        self.addTypeEqualityFunc(complex, self.assertIsClose)

    def assertIsInstance(self, obj, type_, msg: str=None):
        """Confirm type of object.

        I kept writing self.assertTrue(isinstance(obj, type_)),
        and getting little useful information back on failure!
        """
        if not isinstance(obj, type_):
            if msg is None:
                msg = "{obj} has type {obj_type}, not a subclass of {type} as expected".format(obj=obj, obj_type=type(obj), type=type_)
            raise self.failureException(msg)

    def assertImplies(self, antecedent, consequent, msg: str=None):
        """Confirm implication.

        I like implies as an operator ... so shoot me.
        """
        if antecedent and not consequent:
            if msg is None:
                msg = "Consquent is False even though Antecedent is True"
            raise self.failureException(msg)

    def assertIsClose(self, a, b, msg: str=None):
        """Confirm one number is close to another.

        Sort of like assertAlmostEqual, but defined in terms of IsClose.
        """
        if not self.isclose(a, b):
            if msg is None:
                msg = "{a} is not close enough to {b}".format(a=a, b=b)
            raise self.failureException(msg)

    def assertNotIsClose(self, a, b, msg: str=None):
        """Confirm one number is not close to another.

        assertNotIsClose is to assertIsClose as assertNotAlmostEqual is to assertAlmostEqual - completeness
        """
        if self.isclose(a, b):
            if msg is None:
                msg = "{a} is not close enough to {b}".format(a=a, b=b)
            raise self.failureException(msg)

    def assertCloseOrLessThan(self, a, b, msg: str=None):
        """Confirm one number is close or less than another."""
        if not (a < b or self.isclose(a, b)):
            if msg is None:
                msg = "{a} is not sufficiently less than {b}".format(a=a, b=b)
            raise self.failureException(msg)

    def assertCloseOrGreaterThan(self, a, b, msg: str=None):
        """Confirm one number is close or greater than another."""
        if not (a > b or self.isclose(a, b)):
            if msg is None:
                msg = "{a} is not sufficiently less than {b}".format(a=a, b=b)
            raise self.failureException(msg)


ClassUnderTest = 'ClassUnderTest'


def Given(strategy_dict=None, *, testMethodPrefix='test_generic', data_arg='data'):
    """Bind GenericTests to hypothesis strategies.

    It binds hypothesis strategies to the test_generic methods using the strategy_dict.
    """
    if strategy_dict is None:
        strategy_dict = dict()
    elif not isinstance(strategy_dict, dict):
        strategy_dict = {ClassUnderTest: strategy_dict}

    def result(cls: type) -> type:
        if not issubclass(cls, GenericTests):
            raise TypeError("should operate on classes inheriting from GenericTests")
        for name, method in inspect.getmembers(cls):
            if name.startswith(testMethodPrefix) and callable(method):
                parameters = inspect.signature(method).parameters
                args = {arg: param for arg, param in parameters.items() if arg != 'self'}
                if len(args) > 0:
                    given_args = dict()
                    for arg, param in args.items():
                        annotation = None if param.annotation == inspect.Parameter.empty else param.annotation
                        if annotation in strategy_dict:
                            strat = strategy_dict[annotation]
                        elif arg == data_arg:
                            strat = st.data()
                        else:
                            strat = None
                        given_args[arg] = strat
                    setattr(cls, name, given(**given_args)(method))
        return cls
    return result


__all__ = ('GenericTests', 'Given', 'ClassUnderTest')

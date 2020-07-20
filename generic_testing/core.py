# Copyright 2018 Steve Palmer

"""Fundemental tools in the GenericTesting library."""

import abc
import unittest
import inspect
import datetime

from hypothesis import given, strategies as st

from isclose import IsClose


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
            methodName = "runTest"
        super().__init__(methodName)

        # some types are based on floating point approximations,
        # so equality on these types need to be IsClose.
        self.isclose = IsClose()
        self.addTypeEqualityFunc(float, self.assertIsClose)
        self.addTypeEqualityFunc(complex, self.assertIsClose)
        self.addTypeEqualityFunc(datetime.timedelta, self.assertIsClose)

    @staticmethod
    def relabel(annotation):
        """Change the annotation on base class methods to another value.

        This function is used by the Given class decorator below
        to allow the class under test to relabel a type_hint.
        An example of this is that ContainerTests uses the label ElementT
        for the argument of its test_generic_2420_contains_returns_a_boolean
        test.  When this is inherited by MappingTests, it relabels ElementT to
        be KeyT, as appropriate for mappings.
        On the other hand, when ContainerTests is inherited by SequenceTests,
        it relabels ElementT to ValueT, as appropriate for sequences.
        By default, no relabelling is applied.
        """
        return annotation

    def _pass(self) -> None:
        pass

    def _skip(self) -> None:
        raise unittest.SkipTest("")

    def assertIsInstance(self, obj, type_, msg: str = None):
        """Confirm type of object.

        I kept writing self.assertTrue(isinstance(obj, type_)),
        and getting little useful information back on failure!
        """
        if not isinstance(obj, type_):
            if msg is None:
                msg = f"{obj!r} has type {type(obj).__name__}, not a subclass of {type_.__name__} as expected"
            raise self.failureException(msg)

    def assertImplies(self, antecedent, consequent, msg: str = None):
        """Confirm implication.

        I like implies as an operator ... so shoot me.
        """
        if antecedent and not consequent:
            if msg is None:
                msg = "Consquent is False even though Antecedent is True"
            raise self.failureException(msg)

    def assertIsClose(self, a, b, msg: str = None):
        """Confirm one number is close to another.

        Sort of like assertAlmostEqual, but defined in terms of IsClose.
        """
        if not self.isclose(a, b):
            if msg is None:
                msg = f"{a} is not close enough to {b}"
            raise self.failureException(msg)

    def assertNotIsClose(self, a, b, msg: str = None):
        """Confirm one number is not close to another.

        assertNotIsClose is to assertIsClose as assertNotAlmostEqual is to assertAlmostEqual - completeness
        """
        if self.isclose(a, b):
            if msg is None:
                msg = f"{a} is not close enough to {b}"
            raise self.failureException(msg)

    def assertCloseOrLessThan(self, a, b, msg: str = None):
        """Confirm one number is close or less than another."""
        if not (a < b or self.isclose(a, b)):
            if msg is None:
                msg = f"{a} is not sufficiently less than {b}"
            raise self.failureException(msg)

    def assertCloseOrGreaterThan(self, a, b, msg: str = None):
        """Confirm one number is close or greater than another."""
        if not (a > b or self.isclose(a, b)):
            if msg is None:
                msg = f"{a} is not sufficiently less than {b}"
            raise self.failureException(msg)


ClassUnderTest = "ClassUnderTest"


def Given(strategy_dict=None, *, testMethodPrefix="test_generic", data_arg="data"):
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
                args = {
                    arg: param for arg, param in parameters.items() if arg != "self"
                }
                if len(args) > 0:
                    given_args = dict()
                    for arg, param in args.items():
                        annotation = cls.relabel(
                            None
                            if param.annotation == inspect.Parameter.empty
                            else param.annotation
                        )
                        if annotation in strategy_dict:
                            strat = strategy_dict[annotation]
                        elif arg == data_arg:
                            strat = st.data()
                        elif isinstance(annotation, st.SearchStrategy):
                            strat = annotation
                        else:
                            raise TypeError(
                                f"Cannot bind {cls.__name__}.{name}.{arg} with annotation {annotation} to strategy"
                            )
                        given_args[arg] = strat
                    setattr(cls, name, given(**given_args)(method))
        return cls

    return result


__all__ = ("GenericTests", "Given", "ClassUnderTest")

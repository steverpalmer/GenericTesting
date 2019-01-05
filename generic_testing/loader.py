# Copyright 2018 Steve Palmer

"""Determine the generic test base class for a given class_under_test."""

import enum
import collections
import numbers
import fractions
import types
import inspect

import yaml

from generic_testing.core import *
from generic_testing.relations import *
from generic_testing.lattices import *
from generic_testing.arithmetic import *
from generic_testing.collections_abc import *
from generic_testing.numbers_abc import *
from generic_testing.built_in_types import *


class ClassDescription(types.SimpleNamespace, yaml.YAMLObject):
    """Class to act as a marker in the class docstring for a yaml segment."""

    yaml_tag = u'!ClassDescription'

    struct = collections.namedtuple('ClassDescriptionStruct', 'has skipping excluding')

    def in_full(self):
        return self.struct(*(getattr(self, field, None) for field in self.struct._fields))


@enum.unique
class _ContainerLikeFlags(enum.IntEnum):
    Init = 0
    Container = 1
    Iterable = 2
    Sized = 4

    @staticmethod
    def discover(T: type):
        result = _ContainerLikeFlags.Init
        if issubclass(T, collections.abc.Container):
            result |= _ContainerLikeFlags.Container
        if issubclass(T, collections.abc.Iterable):
            result |= _ContainerLikeFlags.Iterable
        if issubclass(T, collections.abc.Sized):
            result |= _ContainerLikeFlags.Sized
        return result


class GenericTestLoader:
    """Generates Base Class for Property Test Class."""

    def __init__(self):
        """Constructor."""
        self._superclass_mapping = collections.OrderedDict([(type(object), EqualityTests)])

    def register(self, T: type, T_Tests: GenericTests):
        """Register a base class to test mapping."""
        self._superclass_mapping[T] = T_Tests

    @staticmethod
    def _is_user_defined(obj, mthd) -> bool:
        """Is method on class not default."""
        attr = getattr(obj, mthd, None)
        return attr is not None and attr is not getattr(object, mthd, None)

    collection_like_list = ([],  # Init
                            [ContainerTests],  # Container
                            [IterableTests],  # Iterable
                            [ContainerOverIterableTests],  # Container and Iterable
                            [SizedTests],  # Sized
                            [SizedTests, ContainerTests],  # Sized and Container
                            [SizedOverIterableTests],  # Sized and Iterable
                            [ContainerOverIterableTests, SizedOverIterableTests])  # Sized, Iterable and Container

    def discover(self, T: type, *, use_docstring_yaml: bool = False) -> GenericTests:
        """Generate Base Case based on supplied class."""
        result = None
        if isinstance(T.__doc__, str) and use_docstring_yaml:
            for class_description in yaml.load_all(T.__doc__):
                if isinstance(class_description, ClassDescription):
                    class_description = class_description.in_full()
                    result = GenericTests
                    if class_description.has:
                        base_class_list = []
                        for model in class_description.has:
                            model += 'Tests'
                            if model in globals():
                                base_class_list.append(globals()[model])
                        if base_class_list:
                            class result(*base_class_list):
                                pass
                            if class_description.excluding:
                                for name, _ in inspect.getmembers(result):
                                    for excld in class_description.excluding:
                                        if name.find(excld) >= 0:
                                            setattr(result, name, GenericTests._pass)
                                            break
                            if class_description.skipping:
                                for name, _ in inspect.getmembers(result):
                                    for excld in class_description.skipping:
                                        if name.find(excld) >= 0:
                                            setattr(result, name, GenericTests._skip)
                                            break
#                             if class_description.where:
#                                 for name, val in class_description.where.items():
#                                     setattr(result, name, getattr(result, val, None))
                    return result
        for known_T in reversed(self._superclass_mapping):
            if issubclass(T, known_T):
                result = self._superclass_mapping[known_T]
                break
        if result is None:
            # Need to work a bit harder
            base_class_list = list(self.collection_like_list[_ContainerLikeFlags.discover(T)])
            if GenericTestLoader._is_user_defined(T, '__eq__'):
                if GenericTestLoader._is_user_defined(T, '__ne__'):
                    base_class_list.append(EqualityTests)
                else:
                    base_class_list.append(EqualsOnlyTests)
            if GenericTestLoader._is_user_defined(T, '__le__'):
                if GenericTestLoader._is_user_defined(T, '__ge__') and \
                   GenericTestLoader._is_user_defined(T, '__lt__') and \
                   GenericTestLoader._is_user_defined(T, '__gt__'):
                    # :TODO: determine if Total or Partial Order somehow
                    base_class_list.append(PartialOrderingTests)
                else:
                    base_class_list.append(LessOrEqualTests)
            if base_class_list:
                class result(*base_class_list):
                    pass
        if result is None:
            raise TypeError()
        return result


defaultGenericTestLoader = GenericTestLoader()

# The following should be ordered from the most abstract to the most specific.
# They are searched in the reverse order.

# Abstract Base Clases
defaultGenericTestLoader.register(collections.abc.Set, SetTests)
defaultGenericTestLoader.register(collections.abc.MutableSet, MutableSetTests)
defaultGenericTestLoader.register(collections.abc.KeysView, KeysViewTests)
defaultGenericTestLoader.register(collections.abc.ItemsView, ItemsViewTests)
defaultGenericTestLoader.register(collections.abc.ValuesView, ValuesViewTests)
defaultGenericTestLoader.register(collections.abc.Mapping, MappingTests)
defaultGenericTestLoader.register(collections.abc.MutableMapping, MutableMappingTests)
defaultGenericTestLoader.register(collections.abc.Sequence, SequenceTests)
defaultGenericTestLoader.register(collections.abc.MutableSequence, MutableSequenceTests)
defaultGenericTestLoader.register(numbers.Complex, ComplexTests)
defaultGenericTestLoader.register(numbers.Real, RealTests)
defaultGenericTestLoader.register(numbers.Rational, RationalTests)
defaultGenericTestLoader.register(numbers.Integral, IntegralTests)

# Concrete classes
defaultGenericTestLoader.register(set, setTests)
defaultGenericTestLoader.register(frozenset, frozensetTests)
defaultGenericTestLoader.register(dict, dictTests)
defaultGenericTestLoader.register(collections.Counter, CounterTests)
defaultGenericTestLoader.register(collections.OrderedDict, OrderedDictTests)
defaultGenericTestLoader.register(collections.defaultdict, defaultdictTests)
defaultGenericTestLoader.register(tuple, tupleTests)
defaultGenericTestLoader.register(str, tupleTests)
defaultGenericTestLoader.register(list, listTests)

defaultGenericTestLoader.register(complex, complexTests)
defaultGenericTestLoader.register(float, floatTests)
defaultGenericTestLoader.register(fractions.Fraction, FractionTests)
defaultGenericTestLoader.register(int, intTests)


__all__ = ('ClassDescription', 'GenericTestLoader', 'defaultGenericTestLoader')

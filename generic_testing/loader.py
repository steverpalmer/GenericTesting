# Copyright 2018 Steve Palmer

"""Determine the generic test base class for a given class_under_test."""

import enum
import collections
import numbers
import fractions
import inspect
import io

import yaml

from generic_testing.core import *
from generic_testing.relations import *
from generic_testing.lattices import *
from generic_testing.arithmetic import *
from generic_testing.collections_abc import *
from generic_testing.numbers_abc import *
from generic_testing.built_in_types import *
from generic_testing.file_likes import *
from generic_testing.enums import *


class _ClassDescription(yaml.YAMLObject):

    yaml_tag = '!ClassDescription'
    yaml_loader = yaml.SafeLoader

    @staticmethod
    def _is_none_or_list_of_str(l) -> bool:
        return l is None or (isinstance(l, list) and all(isinstance(s, str) for s in l))

    def __new__(cls, *, has=None, excluding=None, skipping=None):
        assert cls._is_none_or_list_of_str(has)
        assert cls._is_none_or_list_of_str(excluding)
        assert cls._is_none_or_list_of_str(skipping)
        result = super().__new__(cls)
        result.has = has
        result.excluding = excluding
        result.skipping = skipping
        return result

    def __repr__(self) -> str:
        return f"{type(self).__name__}(has={self.has!r}, excluding={self.excluding!r}, skipping={self.skipping!r})"


@enum.unique
class _ContainerLikeFlags(enum.IntFlag):
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

            for class_description in yaml.safe_load_all(T.__doc__):
                if isinstance(class_description, _ClassDescription):
                    if class_description.has:
                        base_class_list = []
                        for model in class_description.has:
                            model = str(model) + 'Tests'
                            if model in globals():
                                base_class_list.append(globals()[model])
                            else:
                                print(f"ERROR: Model {model} not in globals")
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
                    break  # accept only one ClassDescription per docstring
        if result is None:
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
                    base_class_list.append(TotalOrderingTests if GenericTestLoader._is_user_defined(T, 'cmp') else PartialOrderingTests)
                else:
                    base_class_list.append(LessOrEqualTests)
            if base_class_list:
                class result(*base_class_list):
                    pass
        if result is None:
            raise TypeError()
        assert issubclass(result, GenericTests)
        return result


defaultGenericTestLoader = GenericTestLoader()

# The following should be ordered from the most abstract to the most specific.
# They are searched in the reverse order.

# Abstract Base Clases
defaultGenericTestLoader.register(io.RawIOBase, RawIOBaseTests)
defaultGenericTestLoader.register(io.BufferedIOBase, BufferedIOBaseTests)
defaultGenericTestLoader.register(io.TextIOBase, TextIOBaseTests)
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

defaultGenericTestLoader.register(enum.Enum, EnumTests)
defaultGenericTestLoader.register(enum.IntEnum, IntEnumTests)

__all__ = ('GenericTestLoader', 'defaultGenericTestLoader')

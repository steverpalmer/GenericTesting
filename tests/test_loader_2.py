#!/usr/bin/env python3
# Copyright 2018 Steve Palmer

"""A test of the generic_test.loader using the defined methods."""

import unittest
import collections
import functools

from hypothesis import strategies as st

from generic_testing_test_context import generic_testing


class C_Iterable:
    def __init__(self, data) -> None:
        assert isinstance(data, collections.abc.Iterable)
        super().__init__()
        self.data = data

    def __iter__(self):
        return iter(self.data)


@generic_testing.Given(st.lists(st.integers()))
class Test_01_Iterable(generic_testing.defaultGenericTestLoader.discover(C_Iterable)):
    pass


class C_Sized:
    def __init__(self, data) -> None:
        assert isinstance(data, collections.abc.Iterable)
        super().__init__()
        self.data = data

    def __len__(self):
        return len(self.data)


@generic_testing.Given(st.lists(st.integers()))
class Test_02_Sized(generic_testing.defaultGenericTestLoader.discover(C_Sized)):
    pass


class C_Container:
    def __init__(self, data) -> None:
        assert isinstance(data, collections.abc.Iterable)
        super().__init__()
        self.data = data

    def __contains__(self, key):
        return key in self.data


@generic_testing.Given(
    {
        generic_testing.ClassUnderTest: st.lists(st.integers()),
        generic_testing.ElementT: st.integers(),
    }
)
class Test_03_Container(generic_testing.defaultGenericTestLoader.discover(C_Container)):
    pass


class C_SizedIterable:
    def __init__(self, data) -> None:
        assert isinstance(data, collections.abc.Iterable)
        super().__init__()
        self.data = data

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)


@generic_testing.Given(st.lists(st.integers()))
class Test_04_SizedIterable(
    generic_testing.defaultGenericTestLoader.discover(C_SizedIterable)
):
    pass


class C_IterableContainer:
    def __init__(self, data) -> None:
        assert isinstance(data, collections.abc.Iterable)
        super().__init__()
        self.data = data

    def __iter__(self):
        return iter(self.data)

    def __contains__(self, key):
        return key in self.data


@generic_testing.Given(
    {
        generic_testing.ClassUnderTest: st.lists(st.integers()),
        generic_testing.ElementT: st.integers(),
    }
)
class Test_05_IterableContainer(
    generic_testing.defaultGenericTestLoader.discover(C_IterableContainer)
):
    pass


class C_SizedContainer:
    def __init__(self, data) -> None:
        assert isinstance(data, collections.abc.Iterable)
        super().__init__()
        self.data = data

    def __len__(self):
        return len(self.data)

    def __contains__(self, key):
        return key in self.data


@generic_testing.Given(
    {
        generic_testing.ClassUnderTest: st.lists(st.integers()),
        generic_testing.ElementT: st.integers(),
    }
)
class Test_06_SizedContainer(
    generic_testing.defaultGenericTestLoader.discover(C_SizedContainer)
):
    pass


class C_SizedIterableContainer:
    def __init__(self, data) -> None:
        assert isinstance(data, collections.abc.Iterable)
        super().__init__()
        self.data = data

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __contains__(self, key):
        return key in self.data


@generic_testing.Given(
    {
        generic_testing.ClassUnderTest: st.lists(st.integers()),
        generic_testing.ElementT: st.integers(),
    }
)
class Test_07_SizedIterableContainer(
    generic_testing.defaultGenericTestLoader.discover(C_SizedIterableContainer)
):
    pass


class C_Equals:
    def __init__(self, data: int):
        self.data = data

    def __eq__(self, other):
        return self.data == other.data


@generic_testing.Given(st.builds(C_Equals))
class Test_08_Equals(generic_testing.defaultGenericTestLoader.discover(C_Equals)):
    pass


class C_Equals_and_NotEquals:
    def __init__(self, data: int):
        self.data = data

    def __eq__(self, other):
        return self.data == other.data

    def __ne__(self, other):
        return self.data != other.data


@generic_testing.Given(st.builds(C_Equals_and_NotEquals))
class Test_09_Equals_and_NotEquals(
    generic_testing.defaultGenericTestLoader.discover(C_Equals_and_NotEquals)
):
    pass


class C_LessEquals:
    def __init__(self, data: int):
        self.data = data

    def __eq__(self, other):
        return self.data == other.data

    def __le__(self, other):
        return self.data <= other.data


@generic_testing.Given(st.builds(C_LessEquals))
class Test_10_LessEquals(
    generic_testing.defaultGenericTestLoader.discover(C_LessEquals)
):
    pass


@functools.total_ordering
class C_Ordered:
    def __init__(self, data: int):
        self.data = data

    def __eq__(self, other):
        return self.data == other.data

    def __le__(self, other):
        return self.data <= other.data


@generic_testing.Given(st.builds(C_Ordered))
class Test_10_Ordered(generic_testing.defaultGenericTestLoader.discover(C_Ordered)):
    pass


@functools.total_ordering
class C_FullHouse:
    def __init__(self, data: str):
        self.data = data.upper()

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __contains__(self, key):
        return key.upper() in self.data

    def __eq__(self, other):
        return self.data == other.data

    def __ne__(self, other):
        return self.data != other.data

    def __le__(self, other):
        return self.data <= other.data


@generic_testing.Given(
    {
        generic_testing.ClassUnderTest: st.builds(C_FullHouse),
        generic_testing.ElementT: st.characters(),
    }
)
class Test_11_FullHouse(generic_testing.defaultGenericTestLoader.discover(C_FullHouse)):
    pass


class Main:
    def __init__(self) -> None:
        suite = unittest.TestSuite()
        names = [
            name
            for name, cls in globals().items()
            if name.startswith("Test_")
            and issubclass(cls, generic_testing.GenericTests)  # noqa W503
        ]
        for name in sorted(names):
            suite.addTest(
                unittest.defaultTestLoader.loadTestsFromTestCase(globals()[name])
            )
        tr = unittest.TextTestRunner(verbosity=2)
        tr.run(suite)


Main()

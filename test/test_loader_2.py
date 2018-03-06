import unittest
import collections
import functools

from hypothesis import strategies as st

from src import *


class C_Iterable:

    def __init__(self, data) -> None:
        assert isinstance(data, collections.abc.Iterable)
        super().__init__()
        self.data = data

    def __iter__(self):
        return iter(self.data)


@Given(st.lists(st.integers()))
class Test_01_Iterable(defaultGenericTestLoader.discover(C_Iterable)):
    pass


class C_Sized:

    def __init__(self, data) -> None:
        assert isinstance(data, collections.abc.Iterable)
        super().__init__()
        self.data = data

    def __len__(self):
        return len(self.data)


@Given(st.lists(st.integers()))
class Test_02_Sized(defaultGenericTestLoader.discover(C_Sized)):
    pass


class C_Container:

    def __init__(self, data) -> None:
        assert isinstance(data, collections.abc.Iterable)
        super().__init__()
        self.data = data

    def __contains__(self, key):
        return key in self.data


@Given({ClassUnderTest: st.lists(st.integers()), ElementT: st.integers()})
class Test_03_Container(defaultGenericTestLoader.discover(C_Container)):
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


@Given(st.lists(st.integers()))
class Test_04_SizedIterable(defaultGenericTestLoader.discover(C_SizedIterable)):
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


@Given({ClassUnderTest: st.lists(st.integers()), ElementT: st.integers()})
class Test_05_IterableContainer(defaultGenericTestLoader.discover(C_IterableContainer)):
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


@Given({ClassUnderTest: st.lists(st.integers()), ElementT: st.integers()})
class Test_06_SizedContainer(defaultGenericTestLoader.discover(C_SizedContainer)):
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


@Given({ClassUnderTest: st.lists(st.integers()), ElementT: st.integers()})
class Test_07_SizedIterableContainer(defaultGenericTestLoader.discover(C_SizedIterableContainer)):
    pass


class C_Equals:

    def __init__(self, data: int):
        self.data = data

    def __eq__(self, other):
        return self.data == other.data


@Given(st.builds(C_Equals))
class Test_08_Equals(defaultGenericTestLoader.discover(C_Equals)):
    pass


class C_Equals_and_NotEquals:

    def __init__(self, data: int):
        self.data = data

    def __eq__(self, other):
        return self.data == other.data

    def __ne__(self, other):
        return self.data != other.data


@Given(st.builds(C_Equals_and_NotEquals))
class Test_09_Equals_and_NotEquals(defaultGenericTestLoader.discover(C_Equals_and_NotEquals)):
    pass


class C_LessEquals:

    def __init__(self, data: int):
        self.data = data

    def __eq__(self, other):
        return self.data == other.data

    def __le__(self, other):
        return self.data <= other.data


@Given(st.builds(C_LessEquals))
class Test_10_LessEquals(defaultGenericTestLoader.discover(C_LessEquals)):
    pass


@functools.total_ordering
class C_Ordered:

    def __init__(self, data: int):
        self.data = data

    def __eq__(self, other):
        return self.data == other.data

    def __le__(self, other):
        return self.data <= other.data


@Given(st.builds(C_Ordered))
class Test_10_Ordered(defaultGenericTestLoader.discover(C_Ordered)):
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


@Given({ClassUnderTest: st.builds(C_FullHouse), ElementT: st.characters()})
class Test_11_FullHouse(defaultGenericTestLoader.discover(C_FullHouse)):
    pass


class Main:

    def __init__(self) -> None:
        suite = unittest.TestSuite()
        names = [name for name, cls in globals().items() if name.startswith('Test_') and issubclass(cls, GenericTests)]
        for name in sorted(names):
            suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(globals()[name]))
        tr = unittest.TextTestRunner(verbosity=2)
        tr.run(suite)

Main()


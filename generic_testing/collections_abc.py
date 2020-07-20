# Copyright 2018 Steve Palmer

"""A library of generic test for the base classes in the collections.abc library."""

import abc
import collections

from hypothesis import assume, strategies as st

from .core import GenericTests, ClassUnderTest
from .relations import EqualityTests, PartialOrderingTests
from .lattices import BoundedBelowLatticeTests
from .augmented_assignment import LatticeWithComplementAugmentedTests


ElementT = "ElementT"
KeyT = "KeyT"
ValueT = "ValueT"


class HashableTests(GenericTests):
    """The property tests of collections.abc.Hashable."""

    def test_generic_2135_hash_returns_an_int(self, a: ClassUnderTest):
        """isinstance(hash(a), int)"""
        self.assertIsInstance(hash(a), int)

    def test_generic_2136_hash_equal_on_equal_inputs(
        self, a: ClassUnderTest, b: ClassUnderTest
    ):
        """a == b ⇒ hash(a) == hash(b)"""
        self.assertImplies(a == b, hash(a) == hash(b))


class IterableTests(GenericTests):
    """The property test of collections.abc.Iterables."""

    def test_generic_2400_iter_returns_an_iterator(self, a: ClassUnderTest) -> None:
        """Test __iter__ method."""
        self.assertIsInstance(iter(a), collections.abc.Iterator)

    def test_generic_2401_iterator_protocol_observed(self, a: ClassUnderTest) -> None:
        """Test iterator protocol."""
        a_iter = iter(a)
        try:
            next(a_iter)
            return  # next can return
        except StopIteration:
            # ... or rasie a StopIteration
            with self.assertRaises(StopIteration):  # ... and continues to do so
                next(a_iter)
            return
        self.fail()  # ... but nothing else


class SizedTests(GenericTests):
    """The property test of collections.abc.Sized.

    I assume that the len() function returns a value that can be compared to an int.
    """

    def test_generic_2410_len_returns_a_non_negative_int(
        self, a: ClassUnderTest
    ) -> None:
        """0 <= len(a)"""
        a_len = len(a)
        self.assertIsInstance(a_len, int)
        self.assertGreaterEqual(a_len, 0)

    def test_generic_2800_bool_convention(self, a: ClassUnderTest) -> None:
        """bool(a) ⇔ len(a) != 0"""
        self.assertEqual(len(a) != 0, bool(a))


class ContainerTests(GenericTests):
    """The property test of collections.abc.Container.

    In fact, the standard does *not* say that the __contains__ method must return a bool.
    It only says that it returns a true or false (not even True or False).
    However, if this is property was not true, I think it would be a surprise, so it is included.
    If this is not true for your contained, then simply skip this test.
    """

    def test_generic_2420_contains_returns_a_boolean(
        self, a: ElementT, b: ClassUnderTest
    ) -> None:
        """isinstance(a in b, bool)"""
        self.assertIsInstance(a in b, bool)


class SizedOverIterableTests(SizedTests, IterableTests):
    """The property tests of an class that is both collections.abc.Sized and collections.abc.Iterable.

    In fact, this is *not* required, but it would be a surprise if it were not true.
    If this is not true for your contained, then simply skip this test.
    """

    def test_generic_2411_len_iterations(self, a: ClassUnderTest) -> None:
        a_len = len(a)
        iter_count = 0
        for _ in a:
            iter_count += 1
            if iter_count > a_len:
                break
        self.assertEqual(a_len, iter_count)


class ContainerOverIterableTests(IterableTests, ContainerTests):
    """The property tests of an class that is both collections.abc.Iterable and collections.abc.Container.

    See Language Reference Manual §3.3.6 "The membership test operators (in and not in) are normally
    implemented as an iteration ..."
    """

    def test_generic_2421_contains_over_iterable_definition(
        self, a: ElementT, b: ClassUnderTest
    ) -> None:
        """a in b ⇔ any(a == x for x in b)"""
        contains = False
        for x in b:
            if x == a:
                contains = True
                break
        self.assertEqual(a in b, contains)


class SizedIterableContainerWithEmptyTests(
    SizedOverIterableTests, ContainerOverIterableTests
):
    """These test common properties of almost all containers."""

    @property
    @abc.abstractmethod
    def empty(self) -> ClassUnderTest:
        """The Empty container"""

    def test_generic_2402_zero_iterations_over_empty(self) -> None:
        with self.assertRaises(StopIteration):
            next(iter(self.empty))

    def test_generic_2412_len_empty_is_zero(self) -> None:
        """len(∅) == 0"""
        self.assertEqual(len(self.empty), 0)

    def test_generic_2422_empty_contains_nothing(self, a: ElementT) -> None:
        """a not in ∅"""
        self.assertFalse(a in self.empty)


class SetTests(
    SizedIterableContainerWithEmptyTests,
    EqualityTests,
    PartialOrderingTests,
    BoundedBelowLatticeTests,
):
    """The property tests of collections.abc.Set."""

    @property
    def bottom(self) -> ClassUnderTest:
        return self.empty

    def test_generic_2110_equality_definition(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        """a == b ⇔ (x in a ⇔ x in b)"""
        expected = True
        universe = a | b
        for x in universe:
            if (x in a) != (x in b):
                expected = False
                break
        self.assertEqual(a == b, expected)

    def test_generic_2145_less_or_equal_definition(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        """a <= b ⇔ (x in a ⇒ x in b)"""
        expected = True
        for x in a:
            if x not in b:
                expected = False
                break
        self.assertEqual(a <= b, expected)

    def test_generic_2151_ordering_consistent_with_lattice(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        """(a & b <= a <= a | b) and (a & b <= b <= a | b)"""
        union = a | b
        intersection = a & b
        self.assertTrue(intersection <= a <= union)
        self.assertTrue(intersection <= b <= union)

    def test_generic_2430_disjoint_definition(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        """a.isdisjoint(b) ⇔ a & b == ∅"""
        self.assertEqual(a.isdisjoint(b), a & b == self.empty)

    def test_generic_2431_sub_definition(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        """x in a - b ⇔ x in a and x not in b"""
        c = a - b
        universe = a | b
        self.assertLessEqual(c, universe)
        for x in universe:
            self.assertEqual(
                x in c, x in a and x not in b, f"fails for a={a!r}, b={b!r}, x={x!r}"
            )

    def test_generic_2432_xor_defintion(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        """x in a ^ b ⇔ x in a and x not in b or x not in a and x in b"""
        c = a ^ b
        universe = a | b
        self.assertLessEqual(c, universe)
        for x in universe:
            self.assertEqual(
                x in c,
                x in a and x not in b or x not in a and x in b,
                f"fails for a={a!r}, b={b!r}, x={x!r}",
            )


class MappingViewTests(SizedTests):
    """The property tests of collections.abc.MappingView.

    :TODO: Maybe could try to test the dynamic nature of mapping views here.
    """


class KeysViewTests(MappingViewTests, SetTests):
    """The property tests of collections.abc.KeysView."""


class ItemsViewTests(MappingViewTests, SetTests):
    """The property tests of collections.abc.ItemsView."""


class ValuesViewTests(MappingViewTests, ContainerOverIterableTests):
    """The property tests of collections.abc.ValuesView."""


class MutableSetTests(SetTests, LatticeWithComplementAugmentedTests):
    """The property tests of collections.abc.MutableSet."""

    @abc.abstractmethod
    def copy(self, a: ClassUnderTest) -> ClassUnderTest:
        """Copy Helper function.

        To test Mutable containers, it is useful to have a helper that takes
        a copy of the container before it is mutated.
        """

    def test_generic_2040_copy_helper_definition(self, a: ClassUnderTest) -> None:
        a_copy = self.copy(a)
        self.assertNotEqual(id(a), id(a_copy))
        self.assertEqual(a, a_copy)

    def test_generic_2460_add_definition(self, a: ClassUnderTest, b: ElementT) -> None:
        """a.add(b); x in a ⇔ x in a₀ or x == b"""
        a_copy = self.copy(a)
        a.add(b)
        universe = a | a_copy
        for x in universe:
            self.assertEqual(x in a, x in a_copy or x == b)

    def test_generic_2461_discard_definition(
        self, a: ClassUnderTest, b: ElementT
    ) -> None:
        """a.discard(b); x in a ⇔ x in a₀ and not x == b"""
        a_copy = self.copy(a)
        a.discard(b)
        universe = a | a_copy
        for x in universe:
            self.assertEqual(x in a, x in a_copy and not x == b)


class MappingTests(SizedIterableContainerWithEmptyTests, EqualityTests):
    """The property tests of collections.abc.Mapping."""

    @staticmethod
    def relabel(annotation):
        if annotation == ElementT:
            return KeyT
        return annotation

    def test_generic_2110_equality_definition(
        self, a: ClassUnderTest, b: ClassUnderTest
    ):
        self.assertEqual(a == b, a.keys() == b.keys() and all(a[k] == b[k] for k in a))

    def test_generic_2480_getitem_on_empty_either_succeeds_or_raises_KeyError(
        self, a: KeyT
    ) -> None:
        try:
            self.empty[a]
        except KeyError:
            pass
        except BaseException:
            self.fail()

    def test_generic_2481_getitem_over_all_keys_succeeds(
        self, a: ClassUnderTest
    ) -> None:
        a_keys = a.keys()
        self.assertIsInstance(a_keys, collections.abc.KeysView)
        try:
            for k in a_keys:
                a[k]
        except KeyError:
            self.fail()

    def test_generic_2490_items_returns_an_ItemsView(self, a: ClassUnderTest) -> None:
        """Test items method."""
        self.assertIsInstance(a.items(), collections.abc.ItemsView)

    def test_generic_2491_values_returns_an_ValuesView(self, a: ClassUnderTest) -> None:
        """Test values method."""
        self.assertIsInstance(a.values(), collections.abc.ValuesView)

    def test_generic_2492_get_definition(
        self, a: ClassUnderTest, b: KeyT, c: ValueT
    ) -> None:
        """Test get method."""
        if b in a:
            expected = a[b]
        else:
            expected = c
        self.assertEqual(a.get(b, c), expected)


class MutableMappingTests(MappingTests):
    """The property tests of collections.abc.MutableMapping."""

    @abc.abstractmethod
    def copy(self, a: ClassUnderTest) -> ClassUnderTest:
        """Copy helper.

        To test Mutable containers, it is useful to have a helper that takes a copy
        of the container before it is mutated.
        """

    def test_generic_2040_copy_helper_definition(self, a: ClassUnderTest) -> None:
        a_copy = self.copy(a)
        self.assertNotEqual(id(a), id(a_copy))
        self.assertEqual(a, a_copy)

    def test_generic_2500_setitem_definition(
        self, a: ClassUnderTest, b: KeyT, c: ValueT
    ) -> None:
        """a[b] = c; a[k] == c if k == b else a₀[k]"""
        a_copy = self.copy(a)
        a[b] = c
        universe = a_copy.keys() | a.keys()
        for key in universe:
            self.assertEqual(a[key], c if key == b else a_copy[key])

    def test_generic_2501_delitem_definition(self, a: ClassUnderTest, data) -> None:
        """Test __delitem__ method."""
        assume(len(a) > 0)
        a_copy = self.copy(a)
        key_to_forget = data.draw(st.sampled_from(list(a.keys())))
        del a[key_to_forget]
        self.assertTrue(key_to_forget not in a)
        universe = a_copy.keys() | a.keys()
        universe.remove(key_to_forget)
        for key in universe:
            self.assertEqual(a[key], a_copy[key])

    def test_generic_2502_pop_definition(self, a: ClassUnderTest, b: KeyT) -> None:
        """Test pop method."""
        a_copy = self.copy(a)
        try:
            v = a.pop(b)
            self.assertEqual(v, a_copy[b])
            del a_copy[b]
        except KeyError:
            self.assertFalse(b in a)
        self.assertEqual(a, a_copy)

    def test_generic_2503_popitem_definition(self, a: ClassUnderTest) -> None:
        """Test popitem method."""
        a_copy = self.copy(a)
        try:
            k, v = a.popitem()
            self.assertTrue(k in a_copy)
            self.assertEqual(a_copy[k], v)
            del a_copy[k]
            self.assertEqual(a, a_copy)
        except KeyError:
            self.assertFalse(bool(a_copy))

    def test_generic_2504_clear_definition(self, a: ClassUnderTest) -> None:
        """Test clear method."""
        a.clear()
        self.assertTrue(a == self.empty)

    def test_generic_2505_update_definition(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        """Test update method."""
        a_copy = self.copy(a)
        a.update(b)
        self.assertLessEqual(b.keys(), a.keys())
        for k in a:
            self.assertEqual(a[k], b[k] if k in b else a_copy[k])

    def test_generic_2506_setdefault_definition(
        self, a: ClassUnderTest, b: KeyT, c: ValueT
    ) -> None:
        """Test setdefault method."""
        a_copy = self.copy(a)
        v = a.setdefault(b, c)
        self.assertTrue(b in a)
        self.assertEqual(a[b], v)
        if b not in a_copy:
            self.assertEqual(v, c)
            del a[b]
        self.assertEqual(a, a_copy)


class SequenceTests(SizedIterableContainerWithEmptyTests):
    """The property tests of collections.abc.Sequence."""

    @staticmethod
    def relabel(annotation):
        if annotation == ElementT:
            return ValueT
        return annotation

    def test_generic_2530_getitem_on_empty_raises_IndexError(self, i: KeyT) -> None:
        """Ø[i] raises IndexError"""
        with self.assertRaises(IndexError):
            self.empty[i]

    def test_generic_2531_getitem_has_same_order_as_iterator(
        self, a: ClassUnderTest
    ) -> None:
        i = 0
        for x in a:
            self.assertEqual(x, a[i])
            i += 1
        with self.assertRaises(IndexError):
            a[i]

    def test_generic_2532_getitem_over_negative_indices_definition(
        self, a: ClassUnderTest
    ) -> None:
        """a[-i] == a[len(a) - i]"""
        a_len = len(a)
        i = 1
        while i <= a_len:
            self.assertEqual(a[-i], a[a_len - i])
            i += 1
        with self.assertRaises(IndexError):
            a[-a_len - 1]

    def test_generic_2533_getitem_slice_definition(
        self, a: ClassUnderTest, data
    ) -> None:
        """a[start:stop:step][i] = a[start + i * step]"""
        a_len = len(a)
        if a_len > 0:
            start = data.draw(st.integers(min_value=0, max_value=a_len - 1))
            stop = data.draw(st.integers(min_value=0, max_value=a_len - 1))
            step = data.draw(st.integers(min_value=1, max_value=a_len))
            if start > stop:
                step = -step
            a_slice = a[start:stop:step]
            i = 0
            j = start
            while j < stop if step >= 0 else j > stop:
                self.assertEqual(a_slice[i], a[j])
                i += 1
                j += step

    def test_generic_2535_reversed_definition(self, a: ClassUnderTest) -> None:
        i = -1
        for x in reversed(a):
            self.assertEqual(x, a[i])
            i -= 1
        with self.assertRaises(IndexError):
            a[i]

    def test_generic_2536_index_definition(self, a: ClassUnderTest, b: ValueT) -> None:
        # :TODO: index extra parameters
        try:
            i = a.index(b)
            self.assertEqual(a[i], b)
            j = 0
            while j < i:
                self.assertNotEqual(a[j], b)
                j += 1
        except ValueError:
            self.assertFalse(b in a)

    def test_generic_2537_index_definition_extra_tests(
        self, a: ClassUnderTest, data
    ) -> None:
        assume(len(a) > 0)
        b = data.draw(st.sampled_from(a))
        self.assertTrue(b in a)
        SequenceTests.test_generic_2536_index_definition(self, a, b)

    def test_generic_2538_count_definition(self, a: ClassUnderTest, b: ValueT) -> None:
        count = 0
        for x in a:
            if x == b:
                count += 1
        self.assertEqual(count, a.count(b))

    def test_generic_2539_count_definition_extra_tests(
        self, a: ClassUnderTest, data
    ) -> None:
        assume(len(a) > 0)
        b = data.draw(st.sampled_from(a))
        SequenceTests.test_generic_2538_count_definition(self, a, b)


class MutableSequenceTests(SequenceTests):
    """The property tests of collections.abc.MutableSequence."""

    @abc.abstractmethod
    def copy(self, a: ClassUnderTest) -> ClassUnderTest:
        """
        To test Mutable containers, it is useful to have a helper that takes a copy
        of the container before it is mutated.
        """

    def test_generic_2040_copy_helper_definition(self, a: ClassUnderTest) -> None:
        a_copy = self.copy(a)
        self.assertNotEqual(id(a), id(a_copy))
        self.assertEqual(a, a_copy)

    def test_generic_2550_setitem_definition(
        self, a: ClassUnderTest, b: KeyT, c: ValueT
    ) -> None:
        """a[b] = c; a[i] == c if i == b else a₀[i]"""
        a_len = len(a)
        if -a_len <= b < a_len:
            a_copy = self.copy(a)
            a[b] = c
            self.assertEqual(len(a), a_len)
            if b < 0:
                b += a_len
            i = 0
            for x in a:
                self.assertEqual(x, c if i == b else a_copy[i])
                i += 1
        else:
            with self.assertRaises(IndexError):
                a[b] = c

    def test_generic_2552_delitem_definition(self, a: ClassUnderTest, b: KeyT) -> None:
        """del a[b]; a[i] == a₀[i + int(b <= i)]"""
        a_len = len(a)
        if -a_len <= b < a_len:
            a_copy = self.copy(a)
            del a[b]
            self.assertEqual(len(a), a_len - 1)
            if b < 0:
                b += a_len
            i = 0
            for x in a:
                self.assertEqual(x, a_copy[i + int(b <= i)])
                i += 1
        else:
            with self.assertRaises(IndexError):
                del a[b]

    def test_generic_2554_insert_definition(
        self, a: ClassUnderTest, b: KeyT, c: ValueT
    ) -> None:
        """a.insert(b, c); a[i] == c if i == b else a₀[i - int(i > b)]"""
        a_len = len(a)
        a_copy = self.copy(a)
        a.insert(b, c)
        self.assertEqual(len(a), a_len + 1)
        if b < 0:
            b += a_len
        b = max(0, min(a_len, b))  # clip b
        i = 0
        for x in a:
            self.assertEqual(x, c if i == b else a_copy[i - int(i > b)])
            i += 1

    def test_generic_2560_append_definition(self, a: ClassUnderTest, b: ValueT) -> None:
        """a.append(b); a[i] == a₀[i]; a[-1] == b"""
        a_len = len(a)
        a_copy = self.copy(a)
        a.append(b)
        self.assertEqual(len(a), a_len + 1)
        i = 0
        for x in a:
            self.assertEqual(x, b if i == a_len else a_copy[i])
            i += 1

    def test_generic_2561_reverse_definition(self, a: ClassUnderTest) -> None:
        """a.reverse(); a[i] == a₀[-i-1]"""
        a_len = len(a)
        a_copy = self.copy(a)
        a.reverse()
        self.assertEqual(len(a), a_len)
        i = 0
        for x in a:
            self.assertEqual(x, a_copy[-i - 1])
            i += 1

    def test_generic_2562_extend_definition(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        """a.extend(b); a[i] == a₀[i] if i < len(a₀) else b[i - len(a₀)]"""
        a_len = len(a)
        a_copy = self.copy(a)
        a.extend(b)
        self.assertEqual(len(a), a_len + len(b))
        i = 0
        for x in a:
            self.assertEqual(x, a_copy[i] if i < a_len else b[i - a_len])
            i += 1

    def test_generic_2563_pop_definition(self, a: ClassUnderTest, b: KeyT) -> None:
        """v = a.pop(b); v == a₀[b] and (a[i] == a₀[i + int(b <= i)])"""
        a_len = len(a)
        if -a_len <= b < a_len:
            a_copy = self.copy(a)
            v = a.pop(b)
            self.assertEqual(v, a_copy[b])
            self.assertEqual(len(a), a_len - 1)
            if b < 0:
                b += a_len
            i = 0
            for x in a:
                self.assertEqual(x, a_copy[i + int(b <= i)])
                i += 1
        else:
            with self.assertRaises(IndexError):
                a.pop(b)

    def test_generic_2564_remove_defintion(self, a: ClassUnderTest, b: ValueT) -> None:
        """a.remove(b); a[j] == a₀[j + int(a₀.index(b) < j]"""
        if b in a:
            a_len = len(a)
            a_copy = self.copy(a)
            i = a.index(b)
            a.remove(b)
            self.assertEqual(len(a), a_len - 1)
            j = 0
            for x in a:
                self.assertEqual(x, a_copy[j + int(i <= j)])
                j += 1
        else:
            with self.assertRaises(ValueError):
                a.remove(b)

    def test_generic_2565_iadd_definition(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        """a += b; a[i] == a₀[i] if i < len(a₀) else b[i - len(a₀)]"""
        a_len = len(a)
        a_copy = self.copy(a)
        a += b
        self.assertEqual(len(a), a_len + len(b))
        i = 0
        for x in a:
            self.assertEqual(x, a_copy[i] if i < a_len else b[i - a_len])
            i += 1


__all__ = (
    "ElementT",
    "KeyT",
    "ValueT",
    "HashableTests",
    "IterableTests",
    "SizedTests",
    "ContainerTests",
    "SizedOverIterableTests",
    "ContainerOverIterableTests",
    "SizedIterableContainerWithEmptyTests",
    "SetTests",
    "MappingViewTests",
    "KeysViewTests",
    "ItemsViewTests",
    "ValuesViewTests",
    "MutableSetTests",
    "MappingTests",
    "MutableMappingTests",
    "SequenceTests",
    "MutableSequenceTests",
)

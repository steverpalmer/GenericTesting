#!/usr/bin/env python3
# Copyright 2019 Steve Palmer

"""Extension to math.isclose and cmath.isclose."""

import typing
import numbers
import math
import cmath
import dataclasses

try:
    from .version import Version, version
    if not version.is_backwards_compatible_with('1.0.0'):
        raise ImportError
except ImportError:
    def Version(s): return s  # noqa

__all__ = ('version', 'IsClose')
version = Version('1.0.0')

T = typing.TypeVar('T')  # should support basic operator (+, -) and relations (<, >)

T_abs_tol = typing.TypeVar('T_abs_tol')
T_rel_tol = typing.TypeVar('T_rel_tol')
Relation = typing.Callable[[T, T], bool]


@dataclasses.dataclass(frozen=True)
class IsClose(typing.Generic[T, T_abs_tol, T_rel_tol]):
    """Make the IsClose of math and cmath a little more convenient."""

    rel_tol: T_rel_tol = None
    abs_tol: T_abs_tol = None

    default_rel_tol: T_rel_tol = dataclasses.field(default=1e-9, init=False, repr=False, compare=False)
    default_abs_tol: T_abs_tol = dataclasses.field(default=0.0, init=False, repr=False, compare=False)

    @staticmethod
    def polymorphic(a: T, b: T, *, rel_tol: T_rel_tol = None, abs_tol: T_abs_tol = None) -> bool:
        """Polymorphic isclose.

        >>> IsClose.polymorphic(complex(1), float(1))
        True
        >>> IsClose.polymorphic(float(1), complex(2))
        False
        >>> IsClose.polymorphic(float(2), float(1))
        False
        >>> IsClose.polymorphic(1, float(1))
        True
        >>> IsClose.polymorphic(datetime.timedelta(1), datetime.timedelta(1), \
                                rel_tol=0.0, abs_tol=datetime.timedelta(0))
        True
        >>> IsClose.polymorphic(datetime.timedelta(1, microseconds=1), datetime.timedelta(1), \
                                rel_tol=0.0, abs_tol=datetime.timedelta(0))
        False
        >>> IsClose.polymorphic(datetime.timedelta(1, microseconds=1), datetime.timedelta(1), \
                                rel_tol=1e-9, abs_tol=datetime.timedelta(0))
        True
        >>> IsClose.polymorphic(datetime.datetime.now(), datetime.datetime.now(), \
                                abs_tol=datetime.timedelta(seconds=1))
        True
        """
        if not isinstance(a, numbers.Number) or not isinstance(b, numbers.Number):
            # try and do something reasonable
            result = False
            try:
                if a is b or a == b:
                    result = True
                else:
                    difference: T_abs_tol = abs(a - b)
                    abs_result = abs_tol is not None and difference <= abs_tol
                    rel_result = rel_tol is not None and difference <= rel_tol * max(abs(a), abs(b))
                    result = abs_result or rel_result
            except Exception:
                raise TypeError
        else:
            if rel_tol is None:
                rel_tol = IsClose.default_rel_tol
            if abs_tol is None:
                abs_tol = IsClose.default_abs_tol
            if isinstance(a, numbers.Complex) or isinstance(b, numbers.Complex):
                result = cmath.isclose(complex(a), complex(b), rel_tol=rel_tol, abs_tol=abs_tol)
            else:
                result = math.isclose(float(a), float(b), rel_tol=rel_tol, abs_tol=abs_tol)
        return result

    def __call__(self, a: T, b: T) -> bool:
        """Apply IsClose().

        >>> myisclose = IsClose()
        >>> myisclose(1.0, 1.0)
        True
        """
        return IsClose.polymorphic(a, b, rel_tol=self.rel_tol, abs_tol=self.abs_tol)

    def close(self) -> Relation:
        """close function.

        >>> myisclose = IsClose()
        >>> callable(myisclose.close)
        True
        """
        return self

    def notclose(self) -> Relation:
        """not close function.

        >>> myisclose = IsClose()
        >>> callable(myisclose.notclose)
        True
        """
        return lambda a, b: not self(a, b)

    def much_less_than(self) -> Relation:
        """definitely less function."""
        return lambda a, b: a < b and not self(a, b)

    def less_than_or_close(self) -> Relation:
        """less or close function."""
        return lambda a, b: a < b or self(a, b)

    def much_greater_than(self) -> Relation:
        """definitely greater function."""
        return lambda a, b: a > b and not self(a, b)

    def greater_than_or_close(self) -> Relation:
        """greater or close function."""
        return lambda a, b: a > b or self(a, b)


if __name__ == '__main__':
    import datetime  # noqa F401
    import doctest
    doctest.testmod()

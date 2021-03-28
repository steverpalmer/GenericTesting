#!/usr/bin/env python3
# Copyright 2021 Steve Palmer

"""Extension to math.isclose and cmath.isclose."""

import cmath
import logging
import math
import numbers

LOG = logging.getLogger("isclose")

try:
    import version as _version

    if not _version.version.is_backwards_compatible_with("1.0.0"):
        raise ImportError
except ImportError:
    _version = type("_version", (object,), {"Version": lambda self, s: s})()

__all__ = ("version", "isclose", "IsClose")
version = _version.Version("1.1.0")


def isclose(a, b, **kwargs) -> bool:
    """polymorphic, parameterized isclose.
    >>> isclose(1.0, 1.0)
    True
    >>> isclose(0.0, 1.0)
    False
    >>> isclose(1.0j, 1.0j)
    True
    >>> isclose(-1.0j, 1.0j)
    False
    """

    type_a = type(a)
    type_b = type(b)

    if type_a != type_b and issubclass(type_b, type_a):
        x, y = b, a
    else:
        x, y = a, b

    result = NotImplemented
    try:
        result = x.isclose(y, **kwargs)
    except Exception:
        pass
    if result is NotImplemented:
        try:
            result = y.isclose(x, **kwargs)
        except Exception:
            pass
    if result is NotImplemented:
        rel_tol = kwargs.get("rel_tol", None)
        abs_tol = kwargs.get("abs_tol", None)
        try:
            if isinstance(a, numbers.Real) and isinstance(b, numbers.Real):
                result = math.isclose(
                    float(a),
                    float(b),
                    rel_tol=isclose.default_rel_tol
                    if rel_tol is None
                    else float(rel_tol),
                    abs_tol=isclose.default_abs_tol
                    if abs_tol is None
                    else float(abs_tol),
                )
            elif isinstance(a, numbers.Complex) and isinstance(b, numbers.Complex):
                result = cmath.isclose(
                    complex(a),
                    complex(b),
                    rel_tol=isclose.default_rel_tol
                    if rel_tol is None
                    else float(rel_tol),
                    abs_tol=isclose.default_abs_tol
                    if abs_tol is None
                    else float(abs_tol),
                )
            elif a is b or a == b:
                result = True
            else:
                difference = abs(a - b)
                abs_result = abs_tol is not None and difference <= abs_tol
                rel_result = rel_tol is not None and difference <= rel_tol * max(
                    abs(a), abs(b)
                )
                result = abs_result or rel_result
        except Exception:
            pass

    if result is NotImplemented and not kwargs.get("return_NotImplemented", None):
        raise TypeError(f"cannot compare {a!r} and {b!r}")

    return result


isclose.default_rel_tol = 1e-9
isclose.default_abs_tol = 0.0


class IsClose:
    """Allows pre-defined closeness on polymorphic isclose."""

    def __init__(self, **kwargs) -> None:
        self._kwargs = kwargs

    @property
    def kwargs(self):
        return self._kwargs

    def __call__(self, a, b) -> bool:
        """Apply IsClose().

        >>> myisclose = IsClose()
        >>> myisclose(1.0, 1.0)
        True
        """
        return isclose(a, b, **self._kwargs)

    def close(self):
        """close function.

        >>> myisclose = IsClose()
        >>> callable(myisclose.close)
        True
        """
        return self

    def notclose(self):
        """not close function.

        >>> myisclose = IsClose()
        >>> callable(myisclose.notclose)
        True
        """
        return lambda a, b: not self(a, b)

    def much_less_than(self):
        """definitely less function."""
        return lambda a, b: a < b and not self(a, b)

    def less_than_or_close(self):
        """less or close function."""
        return lambda a, b: a < b or self(a, b)

    def much_greater_than(self):
        """definitely greater function."""
        return lambda a, b: a > b and not self(a, b)

    def greater_than_or_close(self):
        """greater or close function."""
        return lambda a, b: a > b or self(a, b)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

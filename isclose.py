#!/usr/bin/env python3
"""
Copyright 2018 Steve Palmer
"""


import numbers
import math
import cmath


class IsClose:
    """
    make the IsClose of math and cmath a little more convenient...
    """

    @staticmethod
    def _rel_tol(rel_tol):
        """
        Exposes the default value of rel_tol to the library IsClose function
        >>> IsClose._rel_tol("fred")
        Traceback (most recent call last):
            ...
        TypeError: rel_tol must be a real number
        >>> IsClose._rel_tol(-1.0)
        Traceback (most recent call last):
            ...
        ValueError: rel_tol must be non-negative
        >>> IsClose._rel_tol(0.001)
        0.001
        >>> IsClose._rel_tol(None)
        1e-09
        """
        if rel_tol is None:
            result = 1e-09  # §9.2.1  math.IsClose rel_tol default value (and cmath.IsClose)
        elif not isinstance(rel_tol, numbers.Real):
            raise TypeError("rel_tol must be a real number")
        else:
            result = float(rel_tol)
            if result < 0.0:
                raise ValueError("rel_tol must be non-negative")
        return result

    @staticmethod
    def _abs_tol(abs_tol):
        """
        Exposes the default value of abs_tol to the library IsClose function
        >>> IsClose._abs_tol("fred")
        Traceback (most recent call last):
            ...
        TypeError: abs_tol must be a real number
        >>> IsClose._abs_tol(-1.0)
        Traceback (most recent call last):
            ...
        ValueError: abs_tol must be non-negative
        >>> IsClose._abs_tol(1e-30)
        1e-30
        >>> IsClose._abs_tol(None)
        0.0
        """
        if abs_tol is None:
            result = 0.0  # §9.2.1  math.IsClose abs_tol default value (and cmath.IsClose)
        elif not isinstance(abs_tol, numbers.Real):
            raise TypeError("abs_tol must be a real number")
        else:
            result = float(abs_tol)
            if result < 0.0:
                raise ValueError("abs_tol must be non-negative")
        return result

    @staticmethod
    def _over_numbers(a, b, rel_tol, abs_tol):
        """
        a polymorphic version of the IsClose library.
        >>> IsClose._over_numbers("fred", 0, 0.0, 0.0)
        Traceback (most recent call last):
            ...
        TypeError: IsClose should be used on numbers only
        >>> IsClose._over_numbers(complex(1), float(1), 0.0, 0.0)
        True
        >>> IsClose._over_numbers(float(1), complex(2), 0.0, 0.0)
        False
        >>> IsClose._over_numbers(float(2), float(1), 0.0, 0.0)
        False
        >>> IsClose._over_numbers(1, float(1), 0.0, 0.0)
        True
        """
        if not isinstance(a, numbers.Number) or not isinstance(b, numbers.Number):
            raise TypeError("IsClose should be used on numbers only")
        elif isinstance(a, numbers.Complex) or isinstance(b, numbers.Complex):
            result = cmath.isclose(complex(a), complex(b), rel_tol=rel_tol, abs_tol=abs_tol)
        else:
            result = math.isclose(float(a), float(b), rel_tol=rel_tol, abs_tol=abs_tol)
        return result

    @staticmethod
    def over_numbers(a, b, *, rel_tol=None, abs_tol=None):
        """
        uses the polymorphic version of the IsClose library, with the usual defaults
        >>> IsClose.over_numbers(complex(1/3, 1/3), complex(0.3333333333333333333333, 0.33333333333333333333))
        True
        >>> IsClose.over_numbers(float(2), float(1))
        False
        """
        rel_tol = IsClose._rel_tol(rel_tol)
        abs_tol = IsClose._abs_tol(abs_tol)
        return IsClose._over_numbers(a, b, rel_tol=rel_tol, abs_tol=abs_tol)

    def __init__(self, rel_tol=None, abs_tol=None):
        self._rel_tol = IsClose._rel_tol(rel_tol)
        self._abs_tol = IsClose._abs_tol(abs_tol)

    @property
    def rel_tol(self):
        """
        >>> ic = IsClose(0.01, 0.001)
        >>> ic.rel_tol
        0.01
        """
        return self._rel_tol

    @property
    def abs_tol(self):
        """
        >>> ic = IsClose(0.01, 0.001)
        >>> ic.abs_tol
        0.001
        """
        return self._abs_tol

    def __call__(self, a, b) -> bool:
        """
        >>> myisclose = IsClose()
        >>> myisclose(1.0, 1.0)
        True
        """
        return IsClose._over_numbers(a, b, rel_tol=self._rel_tol, abs_tol=self._abs_tol)

    def close(self):
        """
        >>> myisclose = IsClose()
        >>> callable(myisclose.close)
        True
        """
        return self

    def notclose(self):
        """
        >>> myisclose = IsClose()
        >>> callable(myisclose.notclose)
        True
        """
        def result(a, b):
            return not self(a, b)
        return result

    # the following only make sense to floats

    def much_less_than(self):
        def result(a: float, b: float) -> bool:
            return a < b and not self(a, b)
        return result

    def less_than_or_close(self):
        def result(a: float, b: float) -> bool:
            return a < b or self(a, b)

    def much_greater_than(self):
        def result(a: float, b: float) -> bool:
            return a > b and not self(a, b)
        return result

    def greater_than_or_close(self):
        def result(a: float, b: float) -> bool:
            return a > b or self(a, b)
        return result


__all__ = ('IsClose')


if __name__ == '__main__':
    import doctest
    doctest.testmod()

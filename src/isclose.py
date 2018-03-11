# Copyright 2018 Steve Palmer

"""Extension to math.isclose and cmath.isclose."""

import numbers
import math
import cmath

import networkx as nx

# def _most_specific_single_supertype(*args) -> type:
#     """Determine the most specific (least abstract) supertype of the args.
# 
#     This is akin to the Lowest common ancestor problem,
#     but since it is a relatively small scale,
#     I don't try for an optimized algorithm.
# 
#     Can be awkward if the args have more than one common superclass.
#     """
#     types = tuple(o if isinstance(o, type) else type(o) for o in args)
#     superclasses = nx.DiGraph()
#     common_superclasses = [set(T.__mro__) for T in types]
#     common_superclasses = common_superclasses[0].intersection(*common_superclasses[1:])
#     for T in common_superclasses:
#         for parent in T.__mro__:
#             if parent != T:
#                 superclasses.add_edge(T, parent)
#     superclasses = nx.transitive_closure(superclasses)
#     while True:
#         sorted_superclasses = list(nx.topological_sort(superclasses))
#         result = sorted_superclasses[0]
#         if all(superclasses.has_edge(result, T) for T in sorted_superclasses[1:]):
#             break
#         common_superclasses &= set(superclasses.successors(result))
#         superclasses = superclasses.subgraph(common_superclasses)
#     return result


class IsClose:
    """Make the IsClose of math and cmath a little more convenient."""

    @staticmethod
    def _rel_tol(rel_tol) -> float:
        """Exposes the default value of rel_tol to the library IsClose function.

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
    def _abs_tol(abs_tol) -> float:
        """Exposes the default value of abs_tol to the library IsClose function.

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
    def _polymorphic(a: numbers.Number, b: numbers.Number, rel_tol: float, abs_tol: float) -> bool:
        """Polymorphic isclose.

        >>> IsClose._polymorphic(complex(1), float(1), 0.0, 0.0)
        True
        >>> IsClose._polymorphic(float(1), complex(2), 0.0, 0.0)
        False
        >>> IsClose._polymorphic(float(2), float(1), 0.0, 0.0)
        False
        >>> IsClose._polymorphic(1, float(1), 0.0, 0.0)
        True
        >>> IsClose._polymorphic(datetime.timedelta(1), datetime.timedelta(1), 0.0, 0.0)
        True
        >>> IsClose._polymorphic(datetime.timedelta(1, microseconds=1), datetime.timedelta(1), 0.0, 0.0)
        False
        >>> IsClose._polymorphic(datetime.timedelta(1, microseconds=1), datetime.timedelta(1), 1e-9, 0.0)
        True
        """
        if not isinstance(a, numbers.Number) or not isinstance(b, numbers.Number):
            # try and do something reasonable
            result = False
            if a == b:
                result = True
            else:
                try:
                    difference = abs(a - b)
                except BaseException:
                    pass
                else:
                    try:
                        if difference < rel_tol * max(abs(a), abs(b)):
                            result = True
                    except BaseException:
                        pass
                    if not result:
                        if type(a) == type(b):
                            try:
                                abs_tol = type(a)(abs_tol)
                            except BaseException:
                                pass
                        try:
                            if difference <= abs_tol:
                                result = True
                        except BaseException:
                            pass
        elif isinstance(a, numbers.Complex) or isinstance(b, numbers.Complex):
            result = cmath.isclose(complex(a), complex(b), rel_tol=rel_tol, abs_tol=abs_tol)
        else:
            result = math.isclose(float(a), float(b), rel_tol=rel_tol, abs_tol=abs_tol)
        return result

    @staticmethod
    def polymorphic(a: numbers.Number, b: numbers.Number, *, rel_tol: float=None, abs_tol: float=None) -> bool:
        """Polymorphic isclose.

        >>> IsClose.polymorphic(complex(1/3, 1/3), complex(0.3333333333333333333333, 0.33333333333333333333))
        True
        >>> IsClose.polymorphic(float(2), float(1))
        False
        """
        rel_tol = IsClose._rel_tol(rel_tol)
        abs_tol = IsClose._abs_tol(abs_tol)
        return IsClose._polymorphic(a, b, rel_tol=rel_tol, abs_tol=abs_tol)

    def __init__(self, rel_tol: numbers.Real=None, abs_tol: numbers.Real=None) -> None:
        """Define rel_tol and abs_tol default values."""
        self._rel_tol = IsClose._rel_tol(rel_tol)
        self._abs_tol = IsClose._abs_tol(abs_tol)

    @property
    def rel_tol(self) -> float:
        """rel_tol value.

        >>> ic = IsClose(0.01, 0.001)
        >>> ic.rel_tol
        0.01
        """
        return self._rel_tol

    @property
    def abs_tol(self) -> float:
        """abs_tol value.

        >>> ic = IsClose(0.01, 0.001)
        >>> ic.abs_tol
        0.001
        """
        return self._abs_tol

    def __call__(self, a: numbers.Number, b: numbers.Number) -> bool:
        """Apply IsClose().

        >>> myisclose = IsClose()
        >>> myisclose(1.0, 1.0)
        True
        """
        return IsClose._polymorphic(a, b, rel_tol=self._rel_tol, abs_tol=self._abs_tol)

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
        def result(a: numbers.Number, b: numbers.Number):
            return not self(a, b)
        return result

    # the following only make sense to floats

    def much_less_than(self):
        """definitely less function."""
        def result(a: float, b: float) -> bool:
            return a < b and not self(a, b)
        return result

    def less_than_or_close(self):
        """less or close function."""
        def result(a: float, b: float) -> bool:
            return a < b or self(a, b)

    def much_greater_than(self):
        """definitely greater function."""
        def result(a: float, b: float) -> bool:
            return a > b and not self(a, b)
        return result

    def greater_than_or_close(self):
        """greater or close function."""
        def result(a: float, b: float) -> bool:
            return a > b or self(a, b)
        return result


__all__ = ('IsClose')


if __name__ == '__main__':
    import doctest
    doctest.testmod()

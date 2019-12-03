#!/usr/bin/env python3
# Copyright 2018 Steve Palmer

"""A simplistic ModuloN class to help test the generic_test library."""

import math
import numbers
import operator

try:
    from version import Version, version
    if not version.is_backwards_compatible_with('1.0.0'):
        raise ImportError
except ImportError:
    def Version(s): return s

__all__ = ('version', 'ModuloN', 'ModuloPow2')
version = Version('0.1.0')


def _operator_fallbacks(fallback_operator, doc=""):
    """Returns tuple of polymorphic binary operators.

    Based on the pattern shown in Python Standard Library numbers module.
    """
    if fallback_operator is None:
        return (None, None)

    def forward(a, b):
        if type(a) == type(b):
            if a._modulus == b._modulus:
                return type(a)(a._modulus, fallback_operator(a._value, b._value), is_trusted=True)
            else:
                return fallback_operator(int(a), int(b))
#                 raise ValueError("inconsistent modulus values")
        elif isinstance(b, int):
            return fallback_operator(int(a), b)
        elif isinstance(b, float):
            return fallback_operator(float(a), b)
        elif isinstance(b, complex):
            return fallback_operator(complex(a), b)
        else:
            return NotImplemented
    forward.__name__ = '__' + fallback_operator.__name__ + '__'
    forward.__doc__ = doc

    def reverse(b, a):
        if type(a) == type(b):
            if a._modulus == b._modulus:
                return type(a)(a._modulus, fallback_operator(a._value, b._value), is_trusted=True)
            else:
                return fallback_operator(int(a), int(b))
#                 raise ValueError("inconsistent modulus values")
        elif isinstance(a, numbers.Integral):
            return fallback_operator(int(a), int(b))
        elif isinstance(a, numbers.Real):
            return fallback_operator(float(a), float(b))
        elif isinstance(a, numbers.Complex):
            return fallback_operator(complex(a), complex(b))
        else:
            return NotImplemented
    reverse.__name__ = '__r' + fallback_operator.__name__ + '__'
    reverse.__doc__ = doc

    return forward, reverse


def _pow(a: 'ModuloN', b: 'ModuloN') -> 'ModuloN':
    return type(a)(a._modulus, pow(a._value, int(b), a._modulus), is_trusted=True)


class ModuloN(numbers.Integral):
    """Modular Arithmetic.

    ModuloN provides a class for modular arithmetic in Python.
    See https://en.wikipedia.org/wiki/Modular_arithmetic.

    Each instance includes the modulus as well as the value.
    Calculations involving the same modulus values wrap around.
    Otherwise, the values are promoted to ints and normal arithmetic rules apply.

    Common modulus values are captured by a series of specialized constructors,
    such as bit and digit.

--- !ClassDescription
    has:
      - Equality
      - TotalOrdering
      - Field
      - FloorDivMod
      - Exponentiation
      - AbsoluteValue
    excluding:
      - abs_is_multiplicitive
    """

    __slots__ = ('_modulus', '__value')

    def __init__(self, modulus: int, value: int = None, *, is_trusted: bool = False) -> None:
        """
        >>> _ = ModuloN(8, 3)
        >>> ModuloN(-2)
        Traceback (most recent call last):
            ...
        ValueError: Modulus must be positive
        >>> ModuloN(8, 10)
        ModuloN(8, 2)
        """
        if not is_trusted:
            if modulus <= 0:
                raise ValueError("Modulus must be positive")
        self._modulus = modulus
        self._value = value

    @property
    def modulus(self) -> int:
        return self._modulus

    @property
    def _value(self):
        return self.__value

    @_value.setter
    def _value(self, value: int):
        if value is None:
            value = 0
        self.__value = value % self._modulus

    @classmethod
    def bit(cls, value=None):
        return cls(2, value, is_trusted=True)

    @classmethod
    def decimal_digit(cls, value=None):
        return cls(10, value, is_trusted=True)

    @classmethod
    def nibble(cls, value=None):
        return cls(16, value, is_trusted=True)

    @classmethod
    def u8(cls, value=None):
        return cls(256, value, is_trusted=True)

    @classmethod
    def u16(cls, value=None):
        return cls(65536, value, is_trusted=True)

    @classmethod
    def u32(cls, value=None):
        return cls(4294967296, value, is_trusted=True)

    def __repr__(self) -> str:
        default = "{self.__class__.__name__}({self._modulus}, {self._value})"
        specials = {2: "{self.__class__.__name__}.bit({self._value})",
                    10: "{self.__class__.__name__}.digit({self._value})",
                    16: "{self.__class__.__name__}.nibble({self._value})",
                    256: "{self.__class__.__name__}.u8({self._value})",
                    65536: "{self.__class__.__name__}.u16({self._value})",
                    4294967296: "{self.__class__.__name__}.u32({self._value})"}
        return specials.get(self._modulus, default).format(self=self)

    def __str__(self) -> str:
        return f"{self._value}(mod {self._modulus})"

    def __bytes__(self) -> bytes:
        return bytes(self._value)

    def __format__(self, format_spec) -> str:
        return format(self._value, format_spec)

    def __eq__(self, other) -> bool:
        if isinstance(other, ModuloN):
            result = self._modulus == other._modulus and self._value == other._value
        else:
            result = int(self) == other
        return result

    def __le__(self, other) -> bool:
        """Partial Ordering on ModulusN, but Total Ordering on ModulusN with a fixed modulus."""
        if isinstance(other, ModuloN):
            result = self._modulus == other._modulus and self._value <= other._value
        else:
            result = int(self) <= other
        return result

    def __ge__(self, other) -> bool:
        return other.__le__(self)

    def __lt__(self, other) -> bool:
        if isinstance(other, ModuloN):
            result = self._modulus == other._modulus and self._value < other._value
        else:
            result = int(self) <= other
        return result

    def __gt__(self, other) -> bool:
        return other.__lt__(self)

    def __hash__(self) -> int:
        # Since __eq__ above allows ModuloN values to be equal to the open integers,
        # we can only rely on the _value field for the hash.
        return hash(self._value)

    def __bool__(self) -> bool:
        return self._value != 0

    __add__, __radd__ = _operator_fallbacks(operator.add, "a + b")

    __sub__, __rsub__ = _operator_fallbacks(operator.sub, "a - b")

    __mul__, __rmul__ = _operator_fallbacks(operator.mul, "a * b")

    def __truediv__(self, other) -> float:
        if isinstance(other, ModuloN):
            result = self._value / other._value
        else:
            result = self._value / other
        return result

    def __rtruediv__(self, other) -> 'ModuloN':
        return other / self._value

    # FIXME: The following two could be better if modulus is prime!
    __floordiv__, __rfloordiv__ = _operator_fallbacks(operator.floordiv, "a // b")

    __mod__, __rmod__ = _operator_fallbacks(operator.mod, "a % b")

    def __pow__(self, other):
        if type(self) == type(other):
            if self._modulus == other._modulus:
                return type(self)(self._modulus, pow(self._value, int(other), self._modulus), is_trusted=True)
            else:
                return int(self) ** int(other)
#                 raise ValueError("inconsistent modulus values")
        else:
            return int(self) ** other

    def __rpow__(self, other):
        return other ** int(self)

    __lshift__, __rlshift__ = _operator_fallbacks(None)

    __rshift__, __rrshift__ = _operator_fallbacks(None)

    __and__, __rand__ = _operator_fallbacks(None)

    __xor__, __rxor__ = _operator_fallbacks(None)

    __or__, __ror__ = _operator_fallbacks(None)

    def __neg__(self) -> 'ModuloN':
        return type(self)(self._modulus, -self._value, is_trusted=True)

    def __pos__(self) -> 'ModuloN':
        return type(self)(self._modulus, self._value, is_trusted=True)

    __invert__ = None

    def __abs__(self) -> int:
        return self._value

    def __int__(self) -> int:
        return self._value

    def __index__(self) -> int:
        return self._value

    def __round__(self, n: int) -> 'ModuloN':
        return self

    def __floor__(self) -> 'ModuloN':
        return self

    def __ceil__(self) -> 'ModuloN':
        return self

    def __trunc__(self) -> 'ModuloN':
        return self


class ModuloPow2(ModuloN):
    """Modular Arithmetic with modulus a power of 2.

    ModuloPow2 is a ModuloN, optimised with a modulus that is a power of 2.
    This means that instead of an expensive mod operation, we can simply use
    bitwise and operation.

--- !ClassDescription
    has:
      - Integral
    skipping:
      - rshift_definition
    excluding:
      - abs_is_multiplicitive
      - less_or_equal_consistent_with_addition
    """

    def __init__(self, modulus: int, value: int = None, *, is_trusted: bool = False) -> None:
        """
        >>> _ = ModuloPow2(8, 3)
        >>> ModuloPow2(-2)
        Traceback (most recent call last):
            ...
        ValueError: Modulus must be positive
        >>> ModuloPow2(3)
        Traceback (most recent call last):
            ...
        ValueError: Modulus must be positive power of two
        >>> ModuloPow2(0.5)
        Traceback (most recent call last):
            ...
        ValueError: Modulus must be positive power of two
        >>> ModuloPow2(8, 10)
        ModuloPow2(8, 2)
        """
        if not is_trusted:
            if modulus <= 0:
                raise ValueError("Modulus must be positive")
            bits = math.log2(modulus)
            if not bits.is_integer() or bits < 0.0:
                raise ValueError("Modulus must be positive power of two")
        super().__init__(modulus, value, is_trusted=True)

    @property
    def _value(self):
        return self.__value

    @_value.setter
    def _value(self, value: int):
        if value is None:
            value = 0
        self.__value = value & (self._modulus - 1)

    @classmethod
    def decimal_digit(cls, value=None):
        raise ValueError("Modulus must be positive power of two")

    __lshift__, __rlshift__ = _operator_fallbacks(operator.lshift)

    __rshift__, __rrshift__ = _operator_fallbacks(operator.rshift)

    __and__, __rand__ = _operator_fallbacks(operator.and_)

    __xor__, __rxor__ = _operator_fallbacks(operator.xor)

    __or__, __ror__ = _operator_fallbacks(operator.or_)

    def __invert__(self) -> 'ModuloN':
        return type(self)(self._modulus, ~self._value, is_trusted=True)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

#!/usr/bin/env python3
# Copyright 2019 Steve Palmer

import typing
import re
import itertools


_non_negative_integers_regex = re.compile(r'(0|([1-9][0-9]*))')

_non_numeric_identifer_regex = re.compile(r'([0-9A-Za-z\-]*[A-Za-z\-][0-9A-Za-z\-]*)')

_identifier_regex = re.compile(f'({_non_negative_integers_regex.pattern}|{_non_numeric_identifer_regex.pattern})')

_dot_separated_identifiers_regex = re.compile(f'{_identifier_regex.pattern}(\\.{_identifier_regex.pattern})*')

_version_regex = re.compile(f'(?P<major>{_non_negative_integers_regex.pattern})'
                            f'\\.(?P<minor>{_non_negative_integers_regex.pattern})'
                            f'\\.(?P<patch>{_non_negative_integers_regex.pattern})'
                            f'(-(?P<pre_release>{_dot_separated_identifiers_regex.pattern}))?'
                            f'(\\+(?P<build>{_dot_separated_identifiers_regex.pattern}))?')


class Version:
    """A class to represent a Semantic Version number.

    See See https://semver.org/
--- !ClassDescription
    has:
      - Equality
      - TotalOrdering
      - Hashable
      - Iterable
    """

################################################################################
# Helpers
################################################################################

    yaml_tag = 'Version'

    @staticmethod
    def _is_identifier(ident) -> bool:
        return isinstance(ident, int) or (isinstance(ident, str) and _non_numeric_identifer_regex.fullmatch(ident))

    @staticmethod
    def _maybe_int(ident) -> typing.Union[int, str]:
        if _non_negative_integers_regex.fullmatch(ident):
            result = int(ident)
        else:
            result = ident
        return result

    @staticmethod
    def _maybe_version(s: str) -> typing.Union[str, 'Version']:
        try:
            result = Version(s)
        except Exception:
            result = s
        return result

    def _check(self) -> None:
        if not __debug__:
            return
        if not isinstance(self._major, int):  # Rule 2
            raise TypeError(f"major attribute must be an integer, got: {self._major!r}")
        if self._major < 0:  # Rule 2
            raise ValueError(f"major attribute must be non-negative, got: {self._major}")
        if not isinstance(self._minor, int):  # Rule 2
            raise TypeError(f"minor attribute must be an integer, got: {self._minor!r}")
        if self._minor < 0:  # Rule 2
            raise ValueError(f"minor attribute must be non-negative, got: {self._minor}")
        if not isinstance(self._patch, int):  # Rule 2
            raise TypeError(f"major attribute must be an integer, got: {self._patch!r}")
        if self._patch < 0:  # Rule 2
            raise ValueError(f"patch attribute must be non-negative, got: {self._patch}")
        if not isinstance(self._pre_release, tuple):
            raise TypeError(f"expected pre_release to be a tuple, got: {self._pre_release!r}")
        for n, ident in enumerate(self._pre_release):
            if not Version._is_identifier(ident):
                raise TypeError(f"bad identifer in pre_release attribute #{n}: {ident!r}")
        if not isinstance(self._build, tuple):
            raise TypeError(f"expected pre_release to be a tuple, got: {self._build!r}")
        for n, ident in enumerate(self._build):
            if not Version._is_identifier(ident):
                raise TypeError(f"bad identifer in build attribute #{n}: {ident!r}")

################################################################################
# Construction, Properties and Conversions
################################################################################

    def __init__(self,
                 major: int = None,
                 minor: int = None,
                 patch: int = None,
                 pre_release: typing.Iterable = None,
                 build: typing.Iterable = None) -> None:
        if major is None:
            major = 0
        elif minor is None and patch is None and pre_release is None and build is None:
            if isinstance(major, str):
                match = _version_regex.fullmatch(major)
                if match is None:
                    raise ValueError(f"Incompatible version string: {major!r}")
                dct = match.groupdict()
                major = int(dct['major'])
                minor = int(dct['minor'])
                patch = int(dct['patch'])
                if dct['pre_release']:
                    pre_release = tuple(map(Version._maybe_int, dct['pre_release'].split('.')))
                else:
                    pre_release = tuple()
                if dct['build']:
                    build = tuple(map(Version._maybe_int, dct['build'].split('.')))
                else:
                    build = tuple()
            elif isinstance(major, Version):
                major, minor, patch, pre_release, build = tuple(Version)
            elif not isinstance(major, int):
                raise TypeError
        if minor is None:
            minor = 1 if major == 0 else 0
        if patch is None:
            patch = 0
        if pre_release is None:
            pre_release = tuple()
        else:
            pre_release = tuple(pre_release)
        if build is None:
            build = tuple()
        else:
            build = tuple(build)
        self._major = major
        self._minor = minor
        self._patch = patch
        self._pre_release = pre_release
        self._build = build
        self._check()

    @property
    def major(self) -> int:
        self._check()
        return self._major

    @property
    def minor(self) -> int:
        self._check()
        return self._minor

    @property
    def patch(self) -> int:
        self._check()
        return self._patch

    @property
    def pre_release(self) -> tuple:
        self._check()
        return self._pre_release

    @property
    def build(self) -> tuple:
        self._check()
        return self._build

    @property
    def has_stable_api(self) -> bool:
        self._check()
        return self._major != 0

    def to_str(self) -> str:
        result = ''
        try:
            result = f'{self._major!r}.{self._minor!r}.{self._patch!r}'
            if self._pre_release:
                result += '-' + '.'.join(str(ident) for ident in self._pre_release)
            if self._build:
                result += '+' + '.'.join(str(ident) for ident in self._build)
            self._check()
        except Exception as exc:
            result += f'!{exc!r}'
        return result

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self.to_str()!r})'

    def __str__(self) -> str:
        return self.to_str()

    def __iter__(self):
        self._check()
        yield self._major
        yield self._minor
        yield self._patch
        yield self._pre_release
        yield self._build

    def __hash__(self) -> int:
        return hash(str(Version(self.major, self.minor, self.patch, self.pre_release)))

################################################################################
# Relations
################################################################################

    def cmp(self, other) -> int:
        """Total Ordering over Versions.

        Reurns:
        -1   if self < other
         0   if self == other
         1   if self > other
        None if self is not comparable with other
        """
        self._check()
        other = Version._maybe_version(other)
        if not isinstance(other, Version):
            result = None
        else:
            other._check()
            self_mmp = (self._major, self._minor, self._patch)
            other_mmp = (other._major, other._minor, other._patch)
            result = int(self_mmp > other_mmp) - int(self_mmp < other_mmp)
            if result == 0:
                result = int(bool(other._pre_release)) - int(bool(self._pre_release))
                if result == 0:
                    for self_pr, other_pr in itertools.zip_longest(self._pre_release, other._pre_release):
                        if self_pr == other_pr:
                            continue
                        elif self_pr is None:
                            result = -1
                        elif other_pr is None:
                            result = 1
                        elif type(self_pr) == type(other_pr):
                            result = int(self_pr > other_pr) - int(self_pr < other_pr)
                        elif isinstance(self_pr, int):
                            result = -1
                        else:
                            result = 1
                        break
        return result

    def __eq__(self, other) -> bool:
        cmp_ = self.cmp(other)
        return NotImplemented if cmp_ is None else cmp_ == 0

    def __le__(self, other) -> bool:
        cmp_ = self.cmp(other)
        return NotImplemented if cmp_ is None else cmp_ <= 0

    def __ge__(self, other) -> bool:
        cmp_ = self.cmp(other)
        return NotImplemented if cmp_ is None else cmp_ >= 0

    def __lt__(self, other) -> bool:
        cmp_ = self.cmp(other)
        return NotImplemented if cmp_ is None else cmp_ < 0

    def __gt__(self, other) -> bool:
        cmp_ = self.cmp(other)
        return NotImplemented if cmp_ is None else cmp_ > 0

    def is_backwards_compatible_with(self, other) -> bool:
        self._check()
        other = Version._maybe_version(other)
        if not isinstance(other, Version):
            raise TypeError
        return self._major == other._major and other <= self

################################################################################
# 'Arithmetic'
################################################################################

    def next_major(self, pre_release: tuple = None, build: tuple = None) -> 'Version':
        self._check()
        result = Version(self._major + 1, pre_release=pre_release, build=build)
        assert self < result
        assert not result.is_backwards_compatible_with(self)
        return result

    def next_minor(self, pre_release: tuple = None, build: tuple = None) -> 'Version':
        self._check()
        result = Version(self._major, self._minor + 1, pre_release=pre_release, build=build)
        assert self < result
        assert result.is_backwards_compatible_with(self)
        return result

    def next_patch(self, pre_release: tuple = None, build: tuple = None) -> 'Version':
        self._check()
        result = Version(self._major, self._minor, self._patch + 1, pre_release=pre_release, build=build)
        assert self < result
        assert result.is_backwards_compatible_with(self)
        return result

    def release(self, build: tuple = None) -> 'Version':
        self._check()
        result = Version(self._major, self._minor, self._patch, build=build)
        assert self <= result
        assert result.is_release_version
        return result


version = Version('1.0.0')


__all__ = ('version', 'Version')


if __name__ == '__main__':
    import doctest
    doctest.testmod()

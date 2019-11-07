# Copyright 2018 Steve Palmer

"""Merge generic_testing into a single namespace."""

from generic_testing.version import Version, version
assert version.is_backwards_compatible_with('1.0.0')
version = Version('0.1.1')

from generic_testing.timeout import Timeout, version as _timeout_version
assert _timeout_version.is_backwards_compatible_with('1.0.0')

from generic_testing.isclose import IsClose, version as _isclose_version
assert _isclose_version.is_backwards_compatible_with('1.0.0')

from generic_testing.core import *
from generic_testing.relations import *
from generic_testing.arithmetic import *
from generic_testing.lattices import *
from generic_testing.numbers_abc import *
from generic_testing.collections_abc import *
from generic_testing.augmented_assignment import *
from generic_testing.built_in_types import *
from generic_testing.enums import *
from generic_testing.file_likes import *

from generic_testing.loader import *

# Copyright 2018 Steve Palmer

"""Merge generic_testing into a single namespace."""

__version__ = "0.1"

from generic_testing.isclose import IsClose

from generic_testing.core import *
from generic_testing.relations import *
from generic_testing.arithmetic import *
from generic_testing.lattices import *
from generic_testing.numbers_abc import *
from generic_testing.collections_abc import *
from generic_testing.augmented_assignment import *
from generic_testing.built_in_types import *
from generic_testing.loader import *

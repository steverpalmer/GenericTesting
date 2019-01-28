# Copyright 2018 Steve Palmer

"""An unittest extension to stop testing after too many failures or errors found."""

import unittest


class LimitedTextTestResult(unittest.TextTestResult):
    """Stop after a certain number of failures or errors."""

    def __init__(self, stream, descriptions, verbosity, max_failures: int = None, max_errors: int = None):
        """Define maximum allowable failures and errors."""
        super().__init__(stream, descriptions, verbosity)
        self._max_failures = max_failures
        self._max_errors = max_errors

    def stopTest(self, test):
        """Override the sope method."""
        super().stopTest(test)
        if self._max_failures is not None and len(self.failures) >= self._max_failures:
            self.stop()
        elif self._max_errors is not None and len(self.errors) >= self._max_errors:
            self.stop()


__all__ = ('LimitedTextTestResult')

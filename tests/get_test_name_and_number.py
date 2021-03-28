#!/usr/bin/env python3
# Copyright 2021 Steve Palmer

"""Generate a complete list of test numbers and names."""

import collections
import inspect

import generic_testing

TestRecord = collections.namedtuple("TestRecord", ["class_", "testname", "test_number"])


class Main:
    def __init__(self):
        alltests = []
        for name, cls in inspect.getmembers(generic_testing):
            if name.endswith("Tests") and inspect.isclass(cls):
                for name2, fun in inspect.getmembers(cls):
                    if name2.startswith("test_generic_") and inspect.isfunction(fun):
                        try:
                            test_num = int(name2[13:17])
                        except ValueError:
                            test_num = 0
                        alltests.append(TestRecord(name, name2, test_num))
        alltests.sort(key=lambda tr: f"{tr.test_number:04d}{tr.testname}{tr.class_}")
        for tr in alltests:
            print(
                f"TestRecord(test_number={tr.test_number:04d}, class_={tr.class_:30s}, testname={tr.testname})"
            )


if __name__ == "__main__":
    Main()

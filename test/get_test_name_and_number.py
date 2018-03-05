#!/usr/bin/env python3
"""
Copyright 2018 Steve Palmer

Generate a complete list of test numbers and names
"""

import collections
from pprint import pprint

import src

TestRecord = collections.namedtuple('TestRecord', ['class_', 'testname', 'test_number'])

class Main:

    def __init__(self):
        alltests = []
        for name, cls in vars(src).items():
            if name.endswith('Tests') and issubclass(cls, src.GenericTests):
                for name2 in vars(cls):
                    if name2.startswith('test_generic_'):
                        test_num = int(name2[13:17])
                        alltests.append(TestRecord(name, name2, test_num))
        alltests.sort(key=lambda tr: "{tr.test_number:04d}{tr.testname}{tr.class_}".format(tr=tr))
        pprint(alltests)

if __name__ == '__main__':
    Main()

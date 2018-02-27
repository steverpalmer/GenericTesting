"""
Copyright 2018 Steve Palmer
"""


from core import BaseTests


class EqualityTests(BaseTests):

    # § 1. Equality Relation (including Not Equal and bool())

    def test_100_equality_reflexivity(self, a):
        self.assertTrue(a == a)

    def test_101_equality_symmetry(self, a, b):
        self.assertImplies(a == b, b == a)

    def test_102_equality_transitivity(self, a, b, c):
        self.assertImplies(a == b and b == c, a == c)

    def test_110_not_equal_defintion(self, a, b):
        self.assertEqual(a != b, not a == b)

#     def test_120_bool_definition(self, a):
#         self.assertEqual(bool(a), not a == self.zero)


__all__ = ('EqualityTests')

GenericTesting
==============

29 March 2021
-------------

A scheme for generating python unittest tests based on an algebraic
definitions of the properties.

For example, if a method \_\_eq\_\_ is defined, then a user of the class
might expect:

 * Reflexivity [a == a]
 * Symmetry [a == b implies b == a]
 * Transitivity [a == b and b == c implies a == c]

These properties are (largely) independent of the type or specific
functionality of the equality being defined. For example, the equality
may be between objects representing people or objects representing
addresses. Similarly, it could be checking if addresses are identical
(letter by letter), or whether they are the same building, or even
just in the same postal district. The details of the comparison are
important, but the properties above are likely to be expected by any
one using the comparison, and are independent of the type and hence
Generic. Similar lists of properties can be identified for many of the
special methods in the Python Data Model.

I believe that by testing the generic properties above, and some
examples exercising the specific behaviour, you could build a fairly
comprehensive test suite quite quickly.

I've been trying to build the process using the excellent
[hypothesis](https://hypothesis.readthedocs.io/en/latest/index.html) library.

Note: This is still very much a ''Work-In-Progress''. I am testing my
generic tests using the Python built-in types.

For example, to perform a test of the built-in int class, use:

    @Given(st.integers())
    class Test_int(defaultGenericTestLoader.discover(int)):
        pass

    SUITE = unittest.defaultTestLoader.loadTestsFromTestCase(Test_int)

The `defaultGenericTestLoader.discover(int)` looks for the best set of
generic tests for the specified class. This can be inherrited by your
own class where you can add any special tests you want in the normal
`unittest.TestCase` style. The `Given` class decorator will bind the
generic tests to the production strategy. The standard library
`unittest.defaultTestLoader.loadTestsFromTestCase` can be used to
generate a normal `unittest.TestSuite` collecting all the tests
together ready to be run. As of 29 March, the above ran 66 tests, each
exercised against the hypothesis default 100 examples ints, taking 3.3
seconds. The output was:

    test_generic_2100_equality_reflexivity (__main__.Test_int)
    a == a ... ok
    test_generic_2101_equality_symmetry (__main__.Test_int)
    a == b ⇒ b == a ... ok
    test_generic_2102_equality_transitivity (__main__.Test_int)
    a == b and b == c ⇒ a == c ... ok
    test_generic_2105_not_zero_equal_one (__main__.Test_int)
    0 != 1 ... ok
    test_generic_2130_not_equal_defintion (__main__.Test_int)
    a != b ⇔ not a == b ... ok
    test_generic_2140_less_or_equal_reflexivity (__main__.Test_int)
    a <= a ... ok
    test_generic_2141_less_or_equal_antisymmetry (__main__.Test_int)
    a <= b and b <= a ⇒ a == b ... ok
    test_generic_2142_less_or_equal_transitivity (__main__.Test_int)
    a <= b and b <= c ⇒ a <= c ... ok
    test_generic_2150_less_or_equal_totality (__main__.Test_int)
    a <= b or b <= a ... ok
    test_generic_2152_less_or_equal_orientation (__main__.Test_int)
    0 <= 1 ... ok
    test_generic_2160_greater_or_equal_definition (__main__.Test_int)
    a >= b ⇔ b <= a ... ok
    test_generic_2161_less_than_definition (__main__.Test_int)
    a < b ⇔ a <= b and not a == b ... ok
    test_generic_2162_greater_than_definition (__main__.Test_int)
    a > b ⇔ b <= a and not a == b ... ok
    test_generic_2200_or_commutativity (__main__.Test_int)
    a | b == b | a ... ok
    test_generic_2201_or_associativity (__main__.Test_int)
    a | (b | c) == (a | b) | c ... ok
    test_generic_2202_or_identity (__main__.Test_int)
    a | ⊥ == a ... ok
    test_generic_2203_or_and_absorption (__main__.Test_int)
    a | (a & b) == a ... ok
    test_generic_2205_and_commutativity (__main__.Test_int)
    a & b == b & a ... ok
    test_generic_2206_and_associativity (__main__.Test_int)
    a & (b & c) == (a & b) & c ... ok
    test_generic_2207_and_identity (__main__.Test_int)
    a & ⊤ = a ... ok
    test_generic_2208_and_or_absorption (__main__.Test_int)
    a & (a | b) == a ... ok
    test_generic_2209_and_or_distributive (__main__.Test_int)
    a & (b | c) == (a & b) | (a & c) ... ok
    test_generic_2210_or_complementation (__main__.Test_int)
    a | ~a == T ... ok
    test_generic_2211_and_complementation (__main__.Test_int)
    a & ~a == ⊥ ... ok
    test_generic_2215_xor_definition (__main__.Test_int)
    a ^ b == (a | b) & ~(a & b) ... ok
    test_generic_2220_addition_associativity (__main__.Test_int)
    a + (b + c) == (a + b) + c ... ok
    test_generic_2221_addition_identity (__main__.Test_int)
    a + 0 == a == 0 + a ... ok
    test_generic_2230_addition_inverse (__main__.Test_int)
    a + (-a) == 0 ... ok
    test_generic_2231_addition_commutativity (__main__.Test_int)
    a + b == b + a ... ok
    test_generic_2232_pos_definition (__main__.Test_int)
    +a == a ... ok
    test_generic_2233_sub_definition (__main__.Test_int)
    a - b == a + (-b) ... ok
    test_generic_2234_multiplication_associativity (__main__.Test_int)
    a * (b * c) == (a * b) * c ... ok
    test_generic_2235_multiplication_identity (__main__.Test_int)
    a * 1 == a == 1 * a ... ok
    test_generic_2237_multiplication_addition_left_distributivity (__main__.Test_int)
    a * (b + c) == (a * b) + (a * c) ... ok
    test_generic_2238_multiplication_addition_right_distributivity (__main__.Test_int)
    (a + b) * c = (a * c) + (b * c) ... ok
    test_generic_2239_multiplication_commutativity (__main__.Test_int)
    a * b == b * a ... ok
    test_generic_2245_truediv_definition (__main__.Test_int)
    b != 0 ⇒ (a / b) * b == a ... ok
    test_generic_2246_mod_range (__main__.Test_int)
    b != 0 ⇒ a % b ∈ [0 .. b) ... ok
    test_generic_2247_floordiv_definition (__main__.Test_int)
    b != 0 ⇒ (a // b) * b + (a % b) == a ... ok
    test_generic_2248_divmod_definition (__main__.Test_int)
    b != 0 ⇒ divmod(a, b) == (a // b, a % b) ... ok
    test_generic_2250_exponentiation_zero_by_zero (__main__.Test_int)
    0 ** 0 == 1 ... ok
    test_generic_2251_exponentiation_by_zero (__main__.Test_int)
    a != 0 ⇒ a ** 0 == 1 ... ok
    test_generic_2252_exponentiation_with_base_zero (__main__.Test_int)
    a > 0 ⇒ 0 ** a == 0 ... ok
    test_generic_2253_exponentiation_with_base_one (__main__.Test_int)
    a != 0 ⇒ 1 ** a == 1 ... ok
    test_generic_2254_exponentiation_by_one (__main__.Test_int)
    a != 0 ⇒ a ** 1 == a ... ok
    test_generic_2270_abs_not_negative (__main__.Test_int)
    0 <= abs(a) ... ok
    test_generic_2271_abs_positve_definite (__main__.Test_int)
    abs(a) == 0 ⇔ a == 0 ... ok
    test_generic_2273_abs_is_multiplicitive (__main__.Test_int)
    abs(a * b) == abs(a) * abs(b) ... ok
    test_generic_2274_abs_is_subadditive (__main__.Test_int)
    abs(a + b) <= abs(a) + abs(b) ... ok
    test_generic_2280_ior_definition (__main__.Test_int)
    a |= b; a == a₀ | b ... ok
    test_generic_2281_iand_definition (__main__.Test_int)
    a &= b; a == a₀ & b ... ok
    test_generic_2282_isub_definition (__main__.Test_int)
    a -= b; a == a₀ - b ... ok
    test_generic_2283_ixor_definition (__main__.Test_int)
    a ^= b; a == a₀ ^ b ... ok
    test_generic_2284_iadd_definition (__main__.Test_int)
    a += b; a == a₀ + b ... ok
    test_generic_2285_imul_definition (__main__.Test_int)
    a *= b; a == a₀ * b ... ok
    test_generic_2286_itruediv_definition (__main__.Test_int)
    a /= b; a == a₀ / b ... ok
    test_generic_2287_ifloordiv_definition (__main__.Test_int)
    a //= b; a == a₀ // b ... ok
    test_generic_2288_imod_definition (__main__.Test_int)
    a %= b; a == a₀ % b ... ok
    test_generic_2353_less_or_equal_consistent_with_addition (__main__.Test_int)
    a <= b ⇔ a + c <= b + c ... ok
    test_generic_2354_less_or_equal_consistent_with_multiplication (__main__.Test_int)
    0 <= a and 0 <= b ⇒ 0 <= a * b ... ok
    test_generic_2380_int_function (__main__.Test_int) ... ok
    test_generic_2390_lshift_definition (__main__.Test_int)
    0 <= b ⇒ a << b == a * pow(2, b) ... ok
    test_generic_2391_rshift_definition (__main__.Test_int)
    0 <= b ⇒ a >> b == a // pow(2, b) ... ok
    test_generic_2392_ilshift_definition (__main__.Test_int)
    0 <= b ⇒ a <<= b; a == a₀ << b ... ok
    test_generic_2393_irshift_definition (__main__.Test_int)
    0 <= b ⇒ a >>= b; a == a₀ >> b ... ok
    test_generic_2800_bool_convention (__main__.Test_int)
    bool(a) ⇔ not a == 0 ... ok
    ----------------------------------------------------------------------
    Ran 66 tests in 3.295s
    OK

A more interesting example is defined in the `test` directory in
module `modulo_n.py`. It defines a new class `ModuloN` and a
specialization `ModuloPow2`. Included in the docstring for the classes
is a description of the class properties. The test module
`test_modulo_n.py` has:

    @Given(st.builds(ModuloN.decimal_digit, st.integers()))
    class Test_ModuloN_decimal_digit(defaultGenericTestLoader.discover(ModuloN, use_doctring_yaml=True)):
        zero = ModuloN.decimal_digit(0)
        one = ModuloN.decimal_digit(1)

Again `defaultGenericTestLoader.discover(ModuloN)` uses the class
description to build a base clase with a corresponding set of
properties. In this case. the tests need a definition of the special
values `zero` (the additive identity) and `one` (the multiplicative
identity), given in the body of the test class. Finally, the `Given`
class decorator, binds the tests to values drawn from the set of
ModuleN.decimal_digits based on the set of integers. As of 29 March,
this runs 134 tests against ModuloN in 8 seconds.

Cheers,
Steve Palmer

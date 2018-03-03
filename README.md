GenericTesting
==============

27 February 2018

A scheme for generating python unittest tests based on an algebraic
definitions of the properties.

For example, if a method \_\_eq\_\_ is defined, then a user of the class
might expect:

 * Reflexivity [a == a]
 * Symmetry [a == b implies b == a]
 * Transitivity [a == b and b == c implies a == c]

These properties are (largely) independent of the type or specific
functionality of the equality being defined.  For example, the
equality may be between objects representing people or objects
representing addresses.  Similarly, it could be checking if
addresses are identical (letter by letter), or whether they are the
same building, or even just in the same postal district.  The details
of the comparison are important, but the properties above are likely
to be expected by any one using the comparison, and are independent of
the type and hence Generic.  Similar lists of
properties can be identified for many of the special methods in the
Python Data Model.

I believe that by testing the generic properties above, and some
examples exercising the specific behaviour, you could build a fairly
comprehensive test suite quite quickly.

I've been trying to build the process using the excellent
[hypothesis](https://hypothesis.readthedocs.io/en/latest/index.html) library.

Note: This is still very much a ''Work-In-Progress''.  I am testing my generic
tests using the Python built-in types.

For example, to perform a test of the built-in int class, use:

    @Given(st.integers())
    class Test_int(defaultGenericTestLoader.discover(int)):
        pass

    SUITE = unittest.defaultTestLoader.loadTestsFromTestCase(Test_int)

The `defaultGenericTestLoader.discover(int)` looks for the best set of generic
tests for the specified class.  This can be inherrited by your own class where you
can add any special tests you want in the normal `unittest.TestCase` style.
The `Given` class decorator will bind the generic tests to the production strategy.
The standard library `unittest.defaultTestLoader.loadTestsFromTestCase` can be
used to generate a normal `unittest.TestSuite` collecting all the tests together
ready to be run.  In this case, in excess of 57 properties of ints will be run against
the hypothesis default 100 example ints.

Cheers,
Steve Palmer

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
[https://hypothesis.readthedocs.io/en/latest/index.html hypothesis] library.

Note: This is still very much a ''Work-In-Progress''.  I am testing my generic
tests using the Python built-in types.

Cheers,
Steve Palmer

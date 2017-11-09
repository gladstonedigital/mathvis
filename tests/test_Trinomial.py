from mathvis.polynomials import Trinomial
from fractions import Fraction

def test_constructor():
    pass

def test_find_roots():
    assert Trinomial(1, 4, 4).roots == [-2]
    assert Trinomial(1, 1, -6).roots == [2, -3]
    assert Trinomial(4, -17, -50).roots == [Fraction(25,4), -2]
    assert Trinomial(1, 4, -32).roots == [4, -8]
    assert Trinomial(12, 5, -2).roots == [Fraction(1,4), Fraction(-2,3)]


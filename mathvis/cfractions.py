#!/usr/bin/env python3

import math
from fractions import Fraction
from numbers import Complex
from numbers import Rational

class CFraction(Complex):
    """Store complex number of the form a + bj, where a and b
    are Fraction instances
    """
    def __init__(self, real, imag=Fraction(0)):
        self._real = Fraction(real)
        self._imag = Fraction(imag)

    def __abs__(self):
        return Fraction(math.sqrt(self.real**2 + self.imag**2))

    def __complex__(self):
        return complex(self.real, self.imag)

    @property
    def real(self):
        return self._real

    @property
    def imag(self):
        return self._imag

    def __eq__(self, other):
        if isinstance(other, Real):
            return self.imag == 0 and self.real == other
        return self.imag == other.imag and self.real == other.real

    def __add__(self, other):
        return CFraction(self.real+other.real, self.imag+other.imag)

    def __radd__(self, other):
        return self.__add__(other)

    def __neg__(self):
        return CFraction(Fraction(-1*self.real), Fraction(-1*self.imag))

    def __pos__(a):
        return CFraction(Fraction(a.real), Fraction(a.imag))

    def conjugate(self):
        return CFraction(self.real, -1*self.imag)

    def __mul__(self, other):
        return CFraction(self.real*other.real - self.imag*other.imag, self.real*other.imag + self.imag*other.real)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(a, power):
        if isinstance(power, Rational):
            if power.denominator == 1:
                power = power.numerator
                if power == 0:
                    return CFraction(1)
                elif power > 0:
                    zn = CFraction(1)
                    while power > 0:
                        zn *= a
                        power -= 1
                    return zn
                elif power < 0:
                    new_denominator = a.real.numerator**2*a.imag.denominator**2 + a.real.denominator**2*a.imag.numerator**2
                    print(a)
                    return CFraction(Fraction((a.real.denominator*a.real.numerator*a.imag.denominator**2), new_denominator),
                        -1 * Fraction((a.real.denominator**2*a.imag.numerator*a.imag.denominator), new_denominator)) ** abs(power)
            else:
                theta = math.atan(Fraction(a.imag, a.real))
                return CFraction(abs(a)**power * math.cos(power*theta), abs(a)**power * math.sin(power*theta))
        else:
            return complex(a) ** power

    def __rpow__(power, a):
        return a.__pow__(power)

    def __truediv__(self, other):
        return self.__mul__(other ** -1)

    def __rtruediv__(self, other):
        return other.__mul__(self ** -1)

    def __str__(self):
        return str(self.real) + ("+" if self.imag >= 0 else "-") + str(abs(self.imag)) + "j"

    def __repr__(self):
        return self.__str__()

def main():
    z = CFraction(2,3)
    print(z**2)
    print(z**-2)

if __name__ == "__main__":
    main()


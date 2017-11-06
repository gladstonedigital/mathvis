#!/usr/bin/env python3

from fractions import Fraction
from numbers import Complex, Rational, Real
from math import sqrt, atan, cos, sin

"""
Implementation of complex numbers (a+b*j) where the real and imaginary components \
are represented as Fraction instances to preserve accuracy during most mathematical \
operations.

When accuracy is lost due to conversion to float in order to perform an operation, \
the result is converted back into a CFraction instance before returning. Of course \
this doesn't recovery any accuracy but the type stays the same.

Accuracy is not preserved during the following computations:
    - __abs__(), magnitude implemented as sqrt(a**2 + b**2)
    - __complex__(), converting to a built-in complex type
    - math operations involving a CFraction and an irrational number
        (becomes float during calculation)
    - math operations involving a CFraction and most floating point numbers
        certain floats are able to be converted to Fractions correctly but most aren't
    - CFraction raised to a fractional power
"""

class CFraction(Complex):
    """Store complex number of the form (a+b*j), where a and b are Fraction instances."""

    def __init__(self, real, imag=0):
        self._real = Fraction(real)
        self._imag = Fraction(imag)

    @property
    def real(self):
        """Real component of complex number"""
        return self._real

    @property
    def imag(self):
        """Imaginary component of complex number"""
        return self._imag

    def conjugate(self):
        """Return complex conjugate (negated imaginary component)"""
        return CFraction(self.real, -1*self.imag)

    def limit_denominator(self, max_denominator=1000000):
        """Limit length of fraction at the cost of some accuracy"""
        return CFraction(self.real.limit_denominator(max_denominator),
                         self.imag.limit_denominator(max_denominator))

    def __abs__(self):
        """Return magnitude of complex number sqrt(a**2 + b**2)"""
        return Fraction(sqrt(self.real**2 + self.imag**2))

    def __complex__(self):
        """Convert to built-in complex type"""
        return complex(self.real, self.imag)

    def __eq__(self, other):
        """Check equality with other CFractions or other types"""
        if isinstance(other, Real):
            return self.imag == 0 and self.real == other
        return self.imag == other.imag and self.real == other.real

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        return CFraction(self.real+Fraction(other.real), self.imag+Fraction(other.imag))

    def __radd__(self, other):
        return self.__add__(other)

    def __neg__(self):
        return CFraction(Fraction(-1*self.real), Fraction(-1*self.imag))

    def __pos__(a):
        return CFraction(Fraction(a.real), Fraction(a.imag))

    def __mul__(self, other):
        return CFraction(self.real*other.real - self.imag*other.imag, self.real*other.imag + self.imag*other.real)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(a, power):
        """Raise CFraction to power 'power'. 'power' can be Rational, CFraction, or other"""
        if isinstance(power, Rational):
            if power.denominator == 1:
                power = power.numerator
                if power >= 0:
                    zn = CFraction(1)
                    while power > 0:
                        zn *= a
                        power -= 1
                    return zn
                elif power < 0:
                    new_denominator = a.real.numerator**2*a.imag.denominator**2 + a.real.denominator**2*a.imag.numerator**2
                    return CFraction(Fraction((a.real.denominator*a.real.numerator*a.imag.denominator**2), new_denominator),
                        -1 * Fraction((a.real.denominator**2*a.imag.numerator*a.imag.denominator), new_denominator)) ** abs(power)
            else:
                theta = atan(Fraction(a.imag, a.real))
                return CFraction(abs(a)**power * cos(power*theta), abs(a)**power * sin(power*theta))
        elif isinstance(power, CFraction):
            if power.imag == 0:
                return a**power.real
            z = complex(a)**complex(power)
            return CFraction(z.real, z.imag)
        else:
            z = complex(a)**power
            return CFraction(z.real, z.imag)

    def __rpow__(power, a):
        return a.__pow__(power)

    def __truediv__(self, other):
        if isinstance(other, CFraction):
            return CFraction(Fraction((self.real*other.real + self.imag*other.imag), other.real**2 + other.imag**2),
                             Fraction((self.imag*other.real - self.real*other.imag), other.real**2 + other.imag**2))
        return CFraction(self.real / other, self.imag / other)

    def __rtruediv__(self, other):
        return CFraction(other).__truediv__(self)

    def __div__(self, other):
        return self.__truediv__(other)

    def __rdiv__(self, other):
        return CFraction(other).__truediv__(self)

    def __str__(self):
        return "(" + str(self.real) + ("+" if self.imag >= 0 else "-") + str(abs(self.imag)) + "j)"

    def __repr__(self):
        return self.__str__()

def main():
    z = CFraction(2,3)
    print(z**2)
    print(z**-2)

if __name__ == "__main__":
    main()


#!/usr/bin/env python3

import argparse
import math
import numpy
import matplotlib.pyplot as plt
from fractions import Fraction
from cfractions import CFraction

description = """
Factors trinomials from (ax^2 + bx + c) to (px + q)(rx + s)
"""

display_max_denominator = 9999
display_max_precision = 4
display_force_exact = False

class Line():
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.a == other.a and self.b == other.b

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        if not isinstance(self.a, CFraction) and not isinstance(self.b, CFraction):
            a_disp = (self.a if display_force_exact or self.a.denominator <= display_max_denominator else round(float(self.a), display_max_precision))
            prefix = ("(%sx" % ("" if self.a == 1 else ("-" if self.a == -1 else a_disp)))
            b_disp = (self.b if display_force_exact or self.b.denominator <= display_max_denominator else round(float(self.b), display_max_precision))
            suffix = (")" if self.b == 0 else ((" + %s)" % b_disp) if b_disp > 0 else " - %s)" % (-1 * b_disp)))
            return prefix + suffix
        else:
            return "({}x + {})".format("" if self.a == 1 else ("-" if self.a == -1 else (self.a if display_force_exact or self.a.denominator <= display_max_denominator else round(float(self.a), display_max_precision))),
                                       format_cfraction(self.b))

    def evaluate(self, x):
        return self.a*x + self.b

class FactorPair():
    def __init__(self, p=0, q=0, r=0, s=0, b1=None, b2=None):
        if b1 != None and b2 != None:
            self.binomials = [b1, b2]
            self.p = b1.a
            self.q = b1.b
            self.r = b2.a
            self.s = b2.b
        else:
            self.binomials = []
            self.binomials.append(Line(p, q))
            self.binomials.append(Line(r, s))
            self.p = p
            self.q = q
            self.r = r
            self.s = s

    def __iter__(self):
        return iter(self.binomials)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.binomials[0] == other.binomials[0] and self.binomials[1] == other.binomials[1] \
                or self.binomials[0] == other.binomials[1] and self.binomials[1] == other.binomials[0]
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "%s · %s" % tuple(self)

    def expand(self):
        return Quadratic(self.p*self.r, self.p*self.s + self.q*self.r, self.q*self.s)

class Quadratic():
    def __init__(self, a, b, c):
        self.factor_pairs = {}
        self.a = Fraction(a)
        self.b = Fraction(b)
        self.c = Fraction(c)
        self.roots = self.find_roots()

    def __str__(self):
        a_disp = (self.a if display_force_exact or self.a.denominator <= display_max_denominator else round(float(self.a), display_max_precision))
        term1 = ("%sx^2" % ("" if self.a == 1 else ("-" if self.a == -1 else a_disp)))
        b_disp = (self.b if display_force_exact or self.b.denominator <= display_max_denominator else round(float(self.b), display_max_precision))
        term2 = ("" if self.b == 0 else ((" + %sx" % b_disp) if b_disp > 0 else " - %sx" % (-1 * b_disp)))
        c_disp = (self.c if display_force_exact or self.c.denominator <= display_max_denominator else round(float(self.c), display_max_precision))
        term3 = ("" if self.c == 0 else ((" + %s" % c_disp) if c_disp > 0 else " - %s" % (-1 * c_disp)))
        return term1 + term2 + term3

    def evaluate(self, x):
        return self.a*(x**2) + self.b*x + self.c

    def find_roots(self):
        roots = []
        discriminant = Fraction(self.b**2 - (4 * self.a * self.c))
        if discriminant < 0: # complex solutions
            self.radical = CFraction(0, math.sqrt(-1 * discriminant))
            roots.append((-1 * self.b + self.radical) / (2 * self.a))
            roots.append((-1 * self.b - self.radical) / (2 * self.a))
        else:
            self.radical = Fraction(math.sqrt(discriminant))
            if self.a == 0: # linear function
                roots.append(-1 * self.c / self.b)
            else: # quadratic function
                roots.append((-1 * self.b + self.radical) / (2 * self.a))
                roots.append((-1 * self.b - self.radical) / (2 * self.a))

        return roots

    def factor(self, p=1, verbose=False):
        if p == 0:
            return None

        if self.radical == None:
            return None

        if p in self.factor_pairs:
            return self.factor_pairs[p]

        if self.a == 0: # linear function
            p = Fraction(p)
            r = self.c * p / self.b
            q = 0
            s = self.b / p
        else: # quadratic function
            p = Fraction(p)
            r = self.a / p
            q = (self.b - self.radical) / (2 * r)
            s = (self.b + self.radical) / (2 * p)

        if verbose:
            print("a=pr:      %s" % (self.a == p*r))
            print("b=(qr+ps): %s" % (self.b == (q*r + p*s)))
            print("c=qs:      %s" % (self.c == q*s))

        self.factor_pairs[p] = FactorPair(p, q, r, s)
        return self.factor_pairs[p]

    def plot_all(self, low, high):
        x = numpy.linspace(low, high, (high - low) * 10)
        y = self.evaluate(x)
        fig, ax = plt.subplots()
        ax.plot(x, y)

        for pair in self.factor_pairs.values():
            for line in pair.binomials:
                y = line.evaluate(x)
                ax.plot(x, y)

        plt.show()

def format_cfraction(c):
    return "({} {} {}j)".format(c.real if display_force_exact or c.real.denominator <= display_max_denominator else round(float(c.real), display_max_precision),
                                "+" if c.imag >= 0 else "-",
                                abs(c.imag) if display_force_exact or c.imag.denominator <= display_max_denominator else round(float(abs(c.imag)), display_max_precision))

def main():
    global display_force_exact, display_max_precision

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("a", help="ax^2")
    parser.add_argument("b", help="bx")
    parser.add_argument("c", help="c")
    parser.add_argument("factor", nargs="?", help="Coefficient p in (px + q) of factored solution")
    parser.add_argument("--exact", "-e", action="store_true", help="Always display exact coefficients")
    parser.add_argument("--precision", "-c", type=int, help="Precision of floating point coefficients")
    parser.add_argument("--plot", "-p", action="store_true", help="Show plot of polynomial and factors")
    parser.add_argument("--factor-range", "-r", nargs=2, help="Range of p in (px + q) factored solutions")
    parser.add_argument("--factor-step", "-s", help="Increment between factors in factor range")
    parser.add_argument("--view-xrange", "-v", nargs=2, help="Segment of x-axis to display when plotting")
    args = parser.parse_args()

    if args.exact:
        display_force_exact = True
    if args.precision is not None:
        display_max_precision = args.precision
    if args.factor_range is None:
        args.factor_range = [1, 8]
    if args.factor_step is None:
        args.factor_step = 1
    if args.view_xrange is None:
        args.view_xrange = [-10, 10]

    try:
        f = Quadratic(args.a, args.b, args.c)
    except Exception as e:
        print("{}: {}".format(type(e).__name__, e))
        return

    print("%s has %d root%s at:" % (f, len(f.roots), "" if len(f.roots) == 1 else "s"))
    for root in f.roots:
        if isinstance(root, CFraction):
            print("    x = %s" % format_cfraction(root))
        else:
            print("    x = %s" % (str(root) if display_force_exact or root.denominator <= display_max_denominator else str(round(float(root), display_max_precision))))

    factors = []
    if args.factor is not None:
        factors.append(args.factor)
    else:
        for p in numpy.arange(Fraction(args.factor_range[0]), Fraction(args.factor_range[1]) + 1, Fraction(args.factor_step)):
            factors.append(p)

    print("")
    if f.radical is None:
        print("%s has no factor pairs in the real space" % f)
    else:
        print("Some of the possible factorizations of %s:" % f)
        for p in factors:
            print(f.factor(p))

    if args.plot:
        f.plot_all(Fraction(args.view_xrange[0]), Fraction(args.view_xrange[1]))

if __name__ == "__main__":
    main()


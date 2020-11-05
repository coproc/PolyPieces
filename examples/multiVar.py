'''
Multivariate polynomials can be represented as nested UniVarPoly (i.e. the coefficients are of type UniVarPoly).
The lexicographic ordering of the variables is assumed to be ascending when going from the inner most polynomials
to the outer levels.
'''
import os
import sys

SCRIPT_DIR = os.path.split(os.path.abspath(__file__))[0]
SRC_DIR = os.path.realpath(os.path.join(SCRIPT_DIR,'../src'))
sys.path.append(SRC_DIR)
from UniVarPoly import UniVarPoly as UP, symbol, symbols

def dbgPoly(poly):
	print(poly.format(termOrderAsc=True), ', coeffs:', poly.coeffs)

x,y = symbols('x,y')

p1 = 1-x
p2 = 1-y
print('p1:', p1,', p2:', p2)
# degree
print('deg(p1):',      p1.deg(),   ', deg(p2):',      p2.deg())
print('deg(p1, "x"):', p1.deg("x"),', deg(p1, "y"):', p1.deg("y"))
print('deg(p2, "x"):', p2.deg("x"),', deg(p2, "y"):', p2.deg("y"))
# derivative
print('der(p1):',      p1.der(),   ', der(p2):',      p2.der())
print('der(p1, "x"):', p1.der("x"),', der(p1, "y"):', p1.der("y"))
print('der(p2, "x"):', p2.der("x"),', der(p2, "y"):', p2.der("y"))

p1p2 = p1+p2
dbgPoly(p1p2)
print('p1:', p1,', p2:', p2)

p2d1 = p2-p1
dbgPoly(p2d1)
print('p1:', p1,', p2:', p2)

p1d2 = p1-p2
dbgPoly(p1d2)
print('p1:', p1,', p2:', p2)

p0 = p1d2+p2d1
dbgPoly(p0)
print('equals 0:', p0 == 0)
print('p1:', p1,', p2:', p2)

p1m2 = p1*p2
dbgPoly(p1m2)
print('p1:', p1,', p2:', p2)

z = symbol('z')
ps = x+y+z
dbgPoly(ps)
ps2 = ps**2
dbgPoly(ps2)
print(ps2(3))
print(ps2(3)(2))
print(ps2(3)(2)(1))

pxyz = UP.fromString('x*y*z')
dbgPoly(pxyz)

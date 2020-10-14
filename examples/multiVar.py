'''
Multivariate polynomials can be represented as nested UniVarPoly (i.e. the coefficients are of type UniVarPoly).
The lexicographic ordering of the variables is assumed to be ascending when going from the inner most polynomials
to the outer levels.
'''
import sys
sys.path.append('../src')
from UniVarPoly import UniVarPoly as UP, symbol, symbols

def dbgPoly(poly):
	print(poly.format(termOrderAsc=True), ', coeffs:', poly.coeffs)

x,y = symbols('x,y')

p1 = 1-x
p2 = 1-y
print('p1:', p1,', p2:',p2)

p1p2 = p1+p2
dbgPoly(p1p2)
print('p1:', p1,', p2:',p2)

p2d1 = p2-p1
dbgPoly(p2d1)
print('p1:', p1,', p2:',p2)

p1d2 = p1-p2
dbgPoly(p1d2)
print('p1:', p1,', p2:',p2)

p0 = p1d2+p2d1
dbgPoly(p0)
print('equals 0:', p0 == 0)
print('p1:', p1,', p2:',p2)

p1m2 = p1*p2
dbgPoly(p1m2)
print('p1:', p1,', p2:',p2)

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

'''generate a series of piecewise polynomial functions converging to a bell-shaped
   function with rare properties:
   - it has non-zero values only in ]-2,2[, but is arbitrarily often differentiable over R
   - its derivative consists of two copies of itself
   We do exact computations by using coefficients of type fractions.Fraction.
'''
import os
import sys
sys.path.append('../src')

import math
from fractions import Fraction
from UniVarPoly import UniVarPoly, symbol
from PolyPieces import PolyPiece, PolyPieceFunc
import TextPlot

p_x = symbol()
p_x2 = p_x**2

# m_h is a piecewise constant function (1/(2*h) for |x| < h,  0 otherwise)
# m_h is symmetric and the area under it is 1.
def m_h(h):
	return PolyPieceFunc(PolyPiece(Fraction(1,2*h), [-h,h]))


# m_n is the convolution of the functions m_1, m_(1/2), ... m_(1/2^n)
def m_n(n):
	if n == 0: return m_h(1),1
	m_n1,_2n1 = m_n(n-1)
	print(m_n1)
	_2n = 2*_2n1
	return m_n1^m_h(Fraction(1,_2n)),_2n


TextPlot.adjustConsoleEncodingForUnicode()

m_6,_ = m_n(6)
print(m_6)
print(TextPlot.plotFpp(m_6))

# derivates show a fractal structure
m_d = m_6
derFuncs = []
for i in range(3):
	m_d = m_d.der() 
	derFuncs.append(m_d)
	print(TextPlot.plotFpp(m_d))

for f in derFuncs:
	print(f)

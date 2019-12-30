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
from UniVarPoly import UniVarPoly, p_x, p_x2
from PolyPieces import PolyPiece, PolyPieceFunc
import TextPlot

# m_h is a piecewise constant function (1/(2*h) for |x| < h,  0 otherwise)
# m_h is symmetric and the area under it is 1.
def m_h(h):
	return PolyPieceFunc(PolyPiece(Fraction(1,2*h), [-h,h]))


# m_n is the convolution of the functions m_1, m_(1/2), ... m_(1/2^n)
def m_n(n):
	if n == 0: return m_h(1),1
	m_n1,_2n1 = m_n(n-1)
	_2n = 2*_2n1
	return m_n1^m_h(Fraction(1,_2n)),_2n


TextPlot.adjustConsoleEncodingForUnicode()

m_4,_ = m_n(4)
print(m_4)
print(TextPlot.plotFpp(m_4))

# derivates show a fractal structure
m_4d = m_4
for i in range(2):
	m_4d = m_4d.der() 
	print(TextPlot.plotFpp(m_4d))

'''
This series of converging functions was presented by Univ.Prof. Dr. Roman Schnabl
as a 30-years anniversary lecture at TU Wien on October 1st, 2019.
The audience were the students starting their studies of Technical Mathematics at TU Wien in October 1989.
The presented series of functions and the surprising properties of the limit function have probably
been discovered by Prof. Schnabl himself.

generate a series of piecewise polynomial functions converging to a bell-shaped
function with surprising and rare properties:
   - it has non-zero values only in ]-2,2[, but is arbitrarily often differentiable over R
   - its derivative consists of two copies of itself
'''
from pathlib import Path
SRC_DIR = Path(__file__).parent.parent / 'src'
import sys
sys.path.append(str(SRC_DIR.resolve()))

import math
from fractions import Fraction
from PolyPieces import PolyPiece, PolyPieceFunc
import TextPlot


# m_h is a piecewise constant function (1/(2*h) for |x| < h,  0 otherwise)
# m_h is non-negative, symmetric and the area under it is 1.
# We do exact computations by using coefficients of type fractions.Fraction.
def m_h(h):
	return PolyPieceFunc(PolyPiece(Fraction(1,2*h), [-h,h]))


# m_n is the convolution of the functions m_1, m_(1/2), ... m_(1/2^n)
def m_n(n, showIntermediateResults=False):
	m_i = m_h(1)
	_2i = 1 # powers of 2
	for _ in range(n):
		if showIntermediateResults: print(m_i)
		_2i *= 2
		m_i = m_i ^ m_h(Fraction(1,_2i))
	return m_i


if __name__ == '__main__':
	TextPlot.adjustConsoleEncodingForUnicode()

	# since the series of functions is converging quickly, m_6 is already very close to the limit function.
	m_6 = m_n(6, True)
	print(m_6)
	print(TextPlot.plotFpp(m_6))

	# derivates show a fractal structure
	m_d = m_6
	derFuncs = []
	for i in range(3):
		m_d = m_d.der() 
		derFuncs.append(m_d)
		print(TextPlot.plotFpp(m_d))

	#for f in derFuncs:
	#	print(f)

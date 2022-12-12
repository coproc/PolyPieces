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
print(__file__)
SRC_DIR = Path(__file__).resolve().parent.parent / 'src'
print(SRC_DIR)
import sys
sys.path.append(str(SRC_DIR.resolve()))

import math
from fractions import Fraction
from PolyPieces import PolyPiece, PolyPieceFunc
import TextPlot
from Polynomial import poly


# r_w is an even rectangular function of width w with area 1 under its curve
# We try to do exact computations by using coefficients of type fractions.Fraction.
def r_w(w):
	if isinstance(w, int):
		w = Fraction(w)
	return PolyPieceFunc(PolyPiece(1/w, [-w/2,w/2]))


# s_n is the convolution of the functions r_1, r_(1/2), ... r_(1/2^n)
def s_n(n, showIntermediateResults=False):
	s_i = r_w(1)
	_2i = 1 # powers of 2
	for _ in range(n):
		if showIntermediateResults: print(m_i)
		_2i *= 2
		s_i = s_i ^ r_w(Fraction(1,_2i))
	return s_i


def s_n_series(n:int):
	series = [r_w(1)]
	_2i = 1 # powers of 2
	for _ in range(n):
		_2i *= 2
		series.append(series[-1] ^ r_w(Fraction(1,_2i)))
	return series


if __name__ == '__main__':
	TextPlot.adjustConsoleEncodingForUnicode()

	# since the series of functions is converging quickly, s_6 is already very close to the limit function.
	k = 6
	s_k1,s_k = s_n_series(k)[-2:]
	print(s_k1)
	print(s_k)
	
	# these 3 functions are all equal
	print(s_k.der())
	print(s_k1.der() ^ r_w(Fraction(1,2**k)))
	s_k1_delta = 2**k*(s_k1(poly('x+1/2**%d' % (k+1))) - s_k1(poly('x-1/2**%d' % (k+1))))
	print(s_k1_delta)
	
	# so this function is identical to zero
	print(s_k.der() - s_k1_delta)

	# this function is equal to s_k.der() for x < 0
	print(2*s_k1(poly('2x+1')))

	# this function is equal to s_k.der() for x > 0
	print(-2*s_k1(poly('2x-1')))

	#print(TextPlot.plotFpp(s_k.der()))
	#print(TextPlot.plotFpp(s_k1_delta))

	# derivates show a fractal structure
	ds_k = s_k
	derFuncs = []
	for i in range(3):
		derFuncs.append(ds_k)
		print(TextPlot.plotFpp(ds_k))
		ds_k = ds_k.der() 
    
	#for f in derFuncs:
	#	print(f)

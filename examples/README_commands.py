
#------------ CODE INIT ------------
# make sure imports from ../src work
import os, sys
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(FILE_DIR, os.pardir, 'src'))
# simulate console output of expressions
_p_ = None
# print result of last expression
def _p():
	global _p_
	if _p_ is not None:
		print(_p_.__repr__())
		_p_ = None
#------------ CODE INIT ------------

from UniVarPoly import UniVarPoly, symbol
x = symbol()
poly = 3*x - 1
_p_= poly*poly
_p()
poly_3 = poly**3; print(poly_3)
_p_= poly_3(1)
_p()
from PolyPieces import PolyPieceFunc
# define density for uniform distribution over the interval [0,1]
uniformDensity = PolyPieceFunc((1, [0,1]))
# this is the Irwin-Hall distribution for n=1
print(uniformDensity)
_p()
_p()
# compute density of the sum of two uniformly distributed random variables (by convolution)
uniformDensitySum2 = uniformDensity.conv(uniformDensity)
# this is the Irwin-Hall distribution for n=2
print(uniformDensitySum2)
_p()
_p()
_p()
# compute density of the sum of two uniformly distributed random variables (by convolution)
uniformDensitySum2 = uniformDensity.conv(uniformDensity)
# and now the Irwin-Hall distributions for n=3,4
print(uniformDensitySum2.conv(uniformDensity))
_p()
_p()
_p()
print(uniformDensitySum2.conv(uniformDensity).conv(uniformDensity))
_p()
_p()
_p()
from fractions import Fraction
from UniVarPoly import symbol
x = symbol()
poly_rat = 5*x - Fraction(1,4)
print(poly_rat)
# indefinite integral
_p_= poly_rat.int()
_p()
# exponentiation
_p_= poly_rat**4
_p()

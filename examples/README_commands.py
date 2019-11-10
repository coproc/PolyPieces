
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

from UniVarPoly import UniVarPoly, p_x as x
poly = 3*x - 1
_p_= poly*poly
_p()
from PolyPieces import PolyPiece, PolyPieceFunc
# define density for uniform distribution over the interval [0,1]
uniformDensity = PolyPieceFunc(PolyPiece(1, [0,1]))
print(uniformDensity)
# compute density of the sum of two uniformly distributed random variables (by convolution)
uniformDensitySum2 = uniformDensity.conv(uniformDensity)
print(uniformDensitySum2)
from UniVarPoly import p_1, p_x
poly_rat = 5*p_x - p_1/4
print(poly_rat)
# indefinite integral
_p_= poly_rat.int()
_p()
# exponentiation
_p_= poly_rat**4
_p()

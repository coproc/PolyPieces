import sys
sys.path.append("../src")
_ = None
from UniVarPoly import UniVarPoly, p_x as x
_ = None
if _ is not None: print(_.__repr__())
_ = poly = 3*x - 1
_ = poly*poly
if _ is not None: print(_.__repr__())
from PolyPieces import PolyPiece, PolyPieceFunc
_ = None
if _ is not None: print(_.__repr__())
# define density for uniform distribution over the interval [0,1]
_ = uniformDensity = PolyPieceFunc(PolyPiece(1, [0,1]))
_ = print(uniformDensity)
# compute density of the sum of two uniformly distributed random variables (by convolution)
_ = uniformDensitySum2 = uniformDensity.conv(uniformDensity)
_ = print(uniformDensitySum2)
from fractions import Fraction
_ = None
_ = poly_rat = Fraction(5)*x - Fraction(1,4)
_ = print(poly_rat)
_ = print(poly_rat.int())

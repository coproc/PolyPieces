# PolyPieces README
from UniVarPoly import UniVarPoly, p_x as x
poly = 3*x - 1
poly*poly
from PolyPieces import PolyPiece, PolyPieceFunc
# define density for uniform distribution over the interval [0,1]
uniformDensity = PolyPieceFunc(PolyPiece(1, [0,1]))
print(uniformDensity)
# compute density of the sum of two uniformly distributed random variables (by convolution)
uniformDensitySum2 = uniformDensity.conv(uniformDensity)
print(uniformDensitySum2)
from fractions import Fraction
poly_rat = Fraction(5)*x - Fraction(1,4)
print(poly_rat)
print(poly_rat.int())

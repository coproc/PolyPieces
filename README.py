from UniVarPoly import UniVarPoly, p_x as x
poly = 3*x - 1
poly*poly
from PolyPieces import PolyPiece, PolyPieceFunc
uniformRandomDensity = PolyPieceFunc(PolyPiece([0,1], 1))
print(uniformRandomDensity)
uniformRandomDensitySum2 = uniformRandomDensity.conv(uniformRandomDensity)
print(uniformRandomDensitySum2)
uniformRandomDensitySum3 = uniformRandomDensitySum2.conv(uniformRandomDensity)
print(uniformRandomDensitySum3)

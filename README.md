# PolyPieces README

Basic arithmetic with univariate polynomials und piecewise polynomial functions.

## Installation

Simply copy the files from `src/`.



## Examples

Basic usage. For more elaborate examples see the files in `examples/`.

### UniVarPoly
```python
from UniVarPoly import UniVarPoly, p_x as x

poly = 3*x - 1
poly*poly
```

### PolyPieceFunc
from PolyPieces import PolyPiece, PolyPieceFunc

uniformRandomDensity = PolyPieceFunc([PolyPiece([0,1], UniVarPoly(1))])
print(uniformRandomDensity)
uniformRandomDensitySum2 = uniformRandomDensity.conv(uniformRandomDensity)
print(uniformRandomDensitySum2)
uniformRandomDensitySum3 = uniformRandomDensitySum2.conv(uniformRandomDensity)
print(uniformRandomDensitySum2)

## Tests
See the doctests in the implementation files.
# PolyPieces README

Basic arithmetic with univariate polynomials und piecewise polynomial functions.

## Installation

Simply copy the files from `src/`.



## Examples

Basic usage. For more elaborate examples see the files in `examples/`.

### UniVarPoly
```python
>>> from UniVarPoly import UniVarPoly, p_x as x

>>> poly = 3*x - 1
>>> poly*poly
<poly '9x^2 - 6x + 1'>
```

### PolyPieceFunc
```python
>>> from PolyPieces import PolyPiece, PolyPieceFunc

>>> uniformRandomDensity = PolyPieceFunc([PolyPiece([0,1], UniVarPoly(1))])
>>> print(uniformRandomDensity)
```
```
  1, x in [0,1]
```
```python
>>> uniformRandomDensitySum2 = uniformRandomDensity.conv(uniformRandomDensity)
>>> print(uniformRandomDensitySum2)
```
```
  x, x in [0,1]
  -x + 2, x in [1,2]
```
```python
>>> uniformRandomDensitySum3 = uniformRandomDensitySum2.conv(uniformRandomDensity)
>>> print(uniformRandomDensitySum2)
```
```
  0.5x^2, x in [0,1]
  -x^2 + 3x - 1.5, x in [1,2]
  0.5x^2 - 3x + 4.5, x in [2,3]
```

## Tests
See the doctests in the implementation files.
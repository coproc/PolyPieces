# PolyPieces README

Basic arithmetic with univariate polynomials und piecewise polynomial functions.

The main intent of this library is to compute the convolution of piecewise polynomial functions
for getting the density functions of sums of random variables.

The coefficient domain used for computing with the polynomials is defined by the types of the coefficients 
of the input polynomials. 
If the original coefficients are integers, the computations will be carried out with integers as long
as no divisions occur.
If the original coefficients are fractions (`fractions.Fraction`), the computations will be carried out
with full precision and printed with fractions.


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

# define density for uniform distribution over the interval [0,1]
>>> uniformDensity = PolyPieceFunc(PolyPiece(1, [0,1]))
>>> print(uniformDensity)
```
```
f(x) =
  1, x in [0,1]
  0, else
```
```python
# compute density of the sum of two uniformly distributed random variables (by convolution)
>>> uniformDensitySum2 = uniformDensity.conv(uniformDensity)
>>> print(uniformDensitySum2)
```
```
f(x) =
  x,      x in [0,1]
  -x + 2, x in [1,2]
  0, else
```
```python
# compute density of the sum of three uniformly distributed random variables
>>> uniformDensitySum3 = uniformDensitySum2.conv(uniformDensity)
>>> print(uniformDensitySum3)
```
```
f(x) =
  0.5x^2,            x in [0,1]
  -x^2 + 3x - 1.5,   x in [1,2]
  0.5x^2 - 3x + 4.5, x in [2,3]
  0, else
```

## Tests
See the doctests in the implementation files.

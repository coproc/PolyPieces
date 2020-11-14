# PolyPieces README

The main intent of this package is to compute the exact convolution of piecewise polynomial functions
(for getting the density functions of sums of random variables).
Therefor it provides 
* the class `UniVarPoly` for basic symbolic computation with univariate polynomials and 
* the class `PolyPieceFunc` for basic symbolic computation with piecewise polynomial functions.

The coefficient domain used for computing with the polynomials is defined by the types of the coefficients 
of the input polynomials. Any number type, including complex and rational numbers (via type `fractions.Fraction`), can be used.
If the original coefficients are integers, the computations will be carried out with exact arithmetic over the integers or rationals.
To convert a polynomial's (or a piecewise polynomial function's) integer or rational coefficients to type `float`, multiply it with the float value `1.0`.


## Installation

Simply copy the files from `src/`.


## Examples

Basic usage. For more elaborate examples see the files in `examples/`.

### Simple example with UniVarPoly
```python
>>> from UniVarPoly import UniVarPoly, symbol

>>> x = symbol()
>>> poly = 3*x - 1
>>> poly*poly
<UniVarPoly '9x^2 - 6x + 1'>
>>> poly_3 = poly**3; print(poly_3)
27x^3 - 27x^2 + 9x - 1
>>> poly_3(1)
8
```

### Simple example with PolyPieceFunc
Let us compute the [Irwin-Hall distribution](https://en.wikipedia.org/wiki/Irwin%E2%80%93Hall_distribution) for `n = 2,3,4`:
```python
>>> from PolyPieces import PolyPieceFunc

# define density for uniform distribution over the interval [0,1]
>>> uniformDensity = PolyPieceFunc((1, [0,1]))
# this is the Irwin-Hall distribution for n=1
>>> print(uniformDensity)
f(x) =
  1, x in [0,1]
  0, else
```
```python
# compute density of the sum of two uniformly distributed random variables (by convolution)
>>> uniformDensitySum2 = uniformDensity.conv(uniformDensity)
# this is the Irwin-Hall distribution for n=2
>>> print(uniformDensitySum2)
f(x) =
  x,      x in [0,1]
  -x + 2, x in [1,2]
  0, else
```
```python
# compute density of the sum of two uniformly distributed random variables (by convolution)
>>> uniformDensitySum2 = uniformDensity.conv(uniformDensity)
# and now the Irwin-Hall distributions for n=3,4
>>> print(uniformDensitySum2.conv(uniformDensity))
f(x) =
  1/2x^2,            x in [0,1]
  -x^2 + 3x - 3/2,   x in [1,2]
  1/2x^2 - 3x + 9/2, x in [2,3]
  0, else
>>> print(uniformDensitySum2.conv(uniformDensity).conv(uniformDensity))
f(x) =
  1/6x^3,                     x in [0,1]
  -1/2x^3 + 2x^2 - 2x + 2/3,  x in [1,2]
  1/2x^3 - 4x^2 + 10x - 22/3, x in [2,3]
  -1/6x^3 + 2x^2 - 8x + 32/3, x in [3,4]
  0, else
```

## Tests
See the doctests in the implementation files.

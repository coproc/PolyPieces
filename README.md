# PolyPieces README

The main intent of this package is to compute the convolution of piecewise polynomial functions
(for getting the density functions of sums of random variables).
Therefor it provides 
* the class `UniVarPoly` for basic arithmetic with univariate polynomials and 
* the class `PolyPieceFunc` for basic arithmetic with piecewise polynomial functions.

The coefficient domain used for computing with the polynomials is defined by the types of the coefficients 
of the input polynomials. Any number type, including complex and rational numbers (via type `fractions.Fraction`), can be used.
If the original coefficients are integers, the computations will be carried out with exact arithmetic:
the computations stick with integers as long as possible, 
a division with an integer divisor results in fractions (type `fractions.Fraction`).
To convert a polynomial with integer or rational coefficients to a polynomial with coefficients of type `float` multiply it with the float value `1.0`.


## Installation

Simply copy the files from `src/`.


## Examples

Basic usage. For more elaborate examples see the files in `examples/`.

### Simple example with UniVarPoly
```python
>>> from UniVarPoly import UniVarPoly, p_x as x

>>> poly = 3*x - 1
>>> poly*poly
<UniVarPoly '9x^2 - 6x + 1'>
```

### Simple example with PolyPieceFunc
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

### Exact computations
```python
>>> from UniVarPoly import p_1, p_x
>>> poly_rat = 5*p_x - p_1/4
>>> print(poly_rat)
```
```
5x - 1/4
```
```python
# indefinite integral
>>> poly_rat.int()
```
```
<UniVarPoly '5/2x^2 - 1/4x'>
```
```python
# exponentiation
>>> poly_rat**4
```
```
<UniVarPoly '625x^4 - 125x^3 + 75/8x^2 - 5/16x + 1/256'>
```

## Tests
See the doctests in the implementation files.

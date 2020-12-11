"""
operations on univariate polynomials.
A polynomial is represented as an iterable over the monomial coefficients,
e.g. as a list [c0, c1, ..., cn] representing the polynomial c0 + c1*x + ... + cn*x^n.
("dense representation")
"""

from itertools import islice, zip_longest


# islice does not allow a negative step
def _rev_islice(cont, start, stop):
	for i in range(start, stop, -1):
		yield cont[i]


def degree(coeffs):
	"""highest power among monomials with non-zero coefficient; zero polynomial has degree -1"""
	deg = len(coeffs) - 1
	for c in reversed(coeffs):
		if c != 0: break
		deg -= 1
	return deg


def normalize(coeffs):
	"""return input with (zero) coefficients of monomials with powers above degree removed"""
	maxLen = degree(coeffs)+1
	return coeffs[:maxLen] if maxLen < len(coeffs) else coeffs


def inormalize(coeffs):
	"""remove (zero) coefficients of monomials with power above degree from input"""
	maxLen = degree(coeffs)+1
	del coeffs[maxLen:]


def evaluate(coeffs, x0):
	"""evaluate polynomial represented by 'coeffs' at x = x0"""
	p_x0 = 0
	for c_k in reversed(coeffs):
		p_x0 = p_x0*x0 + c_k
	return p_x0


def add(coeffs1, coeffs2):
	s = [c1+c2 for c1,c2 in zip_longest(coeffs1, coeffs2, fillvalue=0)]
	return normalize(s)


def iadd(coeffs, coeffs2):
	for i in range(min(len(coeffs), len(coeffs2))):
		coeffs[i] += coeffs2[i]
	if len(coeffs2) > len(coeffs):
		coeffs += coeffs2[len(coeffs):]
	else:
		inormalize(coeffs)


def sub(coeffs1, coeffs2):
	s = [c1-c2 for c1,c2 in zip_longest(coeffs1, coeffs2, fillvalue=0)]
	return normalize(s)


def isub(coeffs, coeffs2):
	for i in range(min(len(coeffs), len(coeffs2))):
		coeffs[i] -= coeffs2[i]
	if len(coeffs2) > len(coeffs):
		coeffs += [-c for c in coeffs2[len(coeffs):]]
	else:
		inormalize(coeffs)


def scale(coeffs, s):
	res = [s*coeff for coeff in coeffs]
	return normalize(res)


def iscale(coeffs, c):
	for i in range(len(coeffs)):
		coeffs[i] *= c
	inormalize(coeffs)


def multiply(coeffs1, coeffs2):
	deg1,deg2 = degree(coeffs1), degree(coeffs2)
	_scal_prod = lambda v1,v2: sum(c1*c2 for c1,c2 in zip(v1,v2))
	return [_scal_prod(
		islice     (coeffs1, max(0, deg-deg2), min(deg1, deg)+1),
		_rev_islice(coeffs2, min(deg2, deg), max(0, deg-deg1)-1))
		for deg in range(deg1+deg2+1)]


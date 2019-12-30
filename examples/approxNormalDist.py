'''generate a piecewise polynomial function approximating Gauss' bell curve
   by convoluting the density of a uniform random variable with itself several times.
   We do exact computations by using coefficients of type fractions.Fraction.
'''
import sys
sys.path.append('../src')

import math
from fractions import Fraction
from UniVarPoly import UniVarPoly, p_x, p_x2
from PolyPieces import PolyPiece, PolyPieceFunc
import TextPlot


def normalDistDensity(expVal=0, sigma=1):
	normFac = 1/math.sqrt(2*math.pi)/sigma
	return lambda x: normFac*math.exp(-0.5*((x-expVal)/sigma)**2)


# compute expectation value
# Note: E(X) = integral(-inf,inf) xd(x)dx,
#   where d(x) is the density function of random variable X.
# @param fpp density function as piecewise polynomial function
def expectation(fpp):
	fpp_x = p_x * fpp
	return fpp_x.int()


# compute variance
# Note: V(X) = E(X^2) - E(X)^2, 
#   where E(g(X)) = integral(-inf,inf) g(x)d(x)dx and
#   d(x) is the density function of random variable X.
# @param fpp density function as piecewise polynomial function
def variance(fpp, expVal=None):
	if expVal is None: expVal = expectation(fpp)
	fpp_x2 = p_x2 * fpp
	return fpp_x2.int() - expVal*expVal


TextPlot.adjustConsoleEncodingForUnicode()

d_deg0 = PolyPieceFunc(PolyPiece(Fraction(1), [0,1]))
d_deg1 = d_deg0^d_deg0 # polynomials in d_deg1 have degree 1
d_deg3 = d_deg1^d_deg1 # polynomials in d_deg3 have degree 3

print("approximation of normal distribution of degree 3:")
print(d_deg3)
print()
print(TextPlot.plotFpp(d_deg3))
expVal = expectation(d_deg3)
var = variance(d_deg3)
d_deg3_max = d_deg3.eval(2)
print("area=%s, expectation value=%s, variance=%s, f_max=f(2)=%s=%f" % (d_deg3.int(), expVal, var, d_deg3_max, d_deg3_max))

ndd = normalDistDensity(expVal, math.sqrt(var))
#print(TextPlot.plot(ndd, [0,4]))
ndd_dev = lambda x: d_deg3.eval(x) - ndd(x)
print("\ndeviation from corresponding normal distribution:")
print(TextPlot.plot(ndd_dev, [0,4]))
devVals = [ndd_dev(4*i/100) for i in range(100)]
print("min=%f, max=%f, dev at 2=%.1f%%" % (min(devVals),max(devVals),100*ndd_dev(2)/d_deg3_max))


d_deg7 = d_deg3^d_deg3
d_deg11 = d_deg7^d_deg3
d_deg11_s = d_deg11.comp(p_x+Fraction(6))
print("\napproximation of standard normal distribution of degree 11:")
print(d_deg11_s)
print()
#print(TextPlot.plotFpp(d_deg3))
expVal_s = expectation(d_deg11_s)
var_s = variance(d_deg11_s)
d_deg11_max = d_deg11_s.eval(0)
print("area=%s, expectation value=%s, variance=%s, f_max=f(0)=%s=%f" % (d_deg11_s.int(), expVal_s, var_s, d_deg11_max, d_deg11_max))

ndd_s = normalDistDensity()
ndd_s_dev = lambda x: d_deg11_s.eval(x) - ndd_s(x)
print("\ndeviation from standard normal distribution:")
print(TextPlot.plot(ndd_s_dev, [-6,6]))
devsVals = [ndd_s_dev(12*i/100-6) for i in range(100)]
print("min=%f, max=%f, dev at 0=%.1f%%" % (min(devsVals),max(devsVals),100*ndd_s_dev(0)/d_deg11_max))

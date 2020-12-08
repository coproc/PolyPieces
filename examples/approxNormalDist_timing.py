'''generate a piecewise polynomial function approximating Gauss' bell curve
   by convoluting the density of a uniform random variable with itself several times.
   We do exact computations by using coefficients of type fractions.Fraction.
'''
from fractions import Fraction
import math
import os
import sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(THIS_DIR, os.pardir, 'src'))

from PolyPieces import PolyPiece, PolyPieceFunc

d_deg0 = PolyPieceFunc(PolyPiece(Fraction(1), [0,1]))

def fold_lin(fl):
	fc = fl[0]
	for i in range(1,len(fl)):
		fc = fc^fl[i]
	return fc

def fold_pairs(fl):
	if len(fl) == 1: return fl[0]
	fcl = []
	for i in range(0,len(fl),2):
		if i+1 < len(fl):
			fcl.append(fl[i]^fl[i+1])
		else:
			fcl.append(fl[i])
	return fold_pairs(fcl)

fl = 13*[d_deg0]

#print(fold_lin(fl))
#print(fold_pairs(fl))

from timeit import timeit
print('timing fold_lin(fl)  : ', end='', flush=True)
print(timeit("fold_lin(fl)", number=10, globals=globals()))
print('timing fold_pairs(fl): ', end='', flush=True)
print(timeit("fold_pairs(fl)", number=10, globals=globals()))
'''simulate 3-point estimatimon from random data
'''
import os
import sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(THIS_DIR, os.pardir, 'src'))

from Polynomial import symbol
from PolyPieces import PolyPiece, PolyPieceFunc

x = symbol()

# generate density function of triangular distribution
def triangDistDensity(a,b,c):
	pp1 = PolyPiece((x-a)/(c-a), [a,c])
	pp2 = PolyPiece((b-x)/(b-c), [c,b])
	return PolyPieceFunc([pp1,pp2])*2/(b-a)


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


# generate some random triangular distributions
from random import randint
triangleDists = []
for i in range(6):
	a = randint(1,10)
	c = a + randint(1,30)
	b = c + randint(1,50)
	triangleDists.append(triangDistDensity(a,b,c))

print('fold_lin and fold_pairs should give same result; diff:', fold_lin(triangleDists) - fold_pairs(triangleDists))

from timeit import timeit
print('timing fold_lin  :', end='', flush=True)
print(' %5.2f' % timeit("fold_lin  (triangleDists)", number=3, globals=globals()))
print('timing fold_pairs:', end='', flush=True)
print(' %5.2f' % timeit("fold_pairs(triangleDists)", number=3, globals=globals()))

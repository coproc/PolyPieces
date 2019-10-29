'''simulate 3-point estimatimon from random data
'''
import sys
sys.path.append('../src')

from UniVarPoly import UniVarPoly, p_x as x
from PolyPieces import PolyPiece, PolyPieceFunc
import AsciiPlot

# generate density function of triangular distribution
def triangDistDensity(a,b,c):
	pp1 = PolyPiece((x-a)/(c-a), [a,c])
	pp2 = PolyPiece((b-x)/(b-c), [c,b])
	return PolyPieceFunc([pp1,pp2])*2/(b-a)


# generate ascii plot (as string) for piecewise polynomial function
def plotFpp(fpp, xRange=None, yRange=None, xRes=80, yRes=20, unicodeOutput=True):
	polyPieces = fpp.polyPieces
	if xRange is None: xRange = [polyPieces[0].interval[0],polyPieces[-1].interval[1]]
	return AsciiPlot.plot(lambda x: fpp.eval(x), xRange, yRange, xRes, yRes, unicodeOutput)
	

# generate some random triangular distributions
from random import randint
triangleDists = []
for i in range(4):
	a = randint(1,10)
	c = a + randint(1,3)
	b = c + randint(1,7)
	triangleDists.append(triangDistDensity(a,b,c))

for td in triangleDists:
	print(plotFpp(td, [0,20], [0,1], yRes=8))

from functools import reduce
densityOfSum = reduce(lambda x,y: x^y, triangleDists)

print('\ndensity of sum of random variables with triangular distribution')
print(densityOfSum)
print()
print(plotFpp(densityOfSum))

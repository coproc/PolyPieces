'''simulate 3-point estimatimon from random data
'''
import math
import os
import sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(THIS_DIR, os.pardir, 'src'))

from approxNormalDist import normalDistDensity
from Polynomial import symbol
from PolyPieces import PolyPiece, PolyPieceFunc
import TextPlot

x = symbol()

# generate density function of triangular distribution
def triangDistDensity(a,b,c):
	pp1 = PolyPiece((x-a)/(c-a), [a,c])
	pp2 = PolyPiece((b-x)/(b-c), [c,b])
	return PolyPieceFunc([pp1,pp2])*2/(b-a)


# generate some random triangular distributions
from random import randint
triangleDists = []
expValTotal = 0
varianceTotal = 0
for i in range(6):
	a = randint(1,10)
	c = a + randint(1,3)
	b = c + randint(1,7)
	triangleDists.append(triangDistDensity(a,b,c))
	expValTotal += (a+b+c)/3.
	varianceTotal += sum([v*v for v in (a-b,b-c,c-a)])/36.

TextPlot.adjustConsoleEncodingForUnicode()

for td in triangleDists:
	print(TextPlot.plotFpp(td, [0,20], [0,1], yRes=8))

from functools import reduce
densityOfSum = reduce(lambda x,y: x^y, triangleDists)

print('\ndensity of sum of random variables with triangular distribution')
print(densityOfSum)
print()
print(TextPlot.plotFpp(densityOfSum))


sigmaTotal = math.sqrt(varianceTotal)
normalApproxDensity = normalDistDensity(expValTotal,sigmaTotal)
diffFunc = lambda x: densityOfSum(x)-normalApproxDensity(x)
polyPieces = densityOfSum.polyPieces
xRange = polyPieces[0].interval[0], polyPieces[-1].interval[1]
print('\ndifference to normal approx')
print(TextPlot.plot(diffFunc, xRange=xRange))

xRes = 1000
xStep = (xRange[1]-xRange[0])/xRes
densSumMax = max((densityOfSum(xRange[0]+i*xStep),xRange[0]+i*xStep) for i in range(0,xRes+1))
normalMax = normalApproxDensity(expValTotal)
absDiffMax = max(abs(diffFunc(xRange[0]+i*xStep)) for i in range(0,xRes+1))
print('\ndensity of sum max: %.3f (x=%.2f), normal max. %.3f (x=%.2f)' % (*densSumMax, normalMax, expValTotal))
print('max abs diff: %.3f (%.2f%%)' % (absDiffMax, 100.*absDiffMax/densSumMax[0]))

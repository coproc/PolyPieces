'''simulate 3-point estimatimon from random data
'''
import sys
sys.path.append('../src')

from UniVarPoly import UniVarPoly, p_x as x
from PolyPieces import PolyPiece, PolyPieceFunc


# generate density function of triangular distribution
def triangDistDensity(a,b,c):
	pp1 = PolyPiece((x-a)/(c-a), [a,c])
	pp2 = PolyPiece((b-x)/(b-c), [c,b])
	return PolyPieceFunc([pp1,pp2])*2/(b-a)


PLOT_DOTS = ('\N{COMBINING DOT BELOW}', '.', '\N{MIDDLE DOT}', '\N{DOT ABOVE}')
# print((len(PLOT_DOTS)+1)*' '+PLOT_DOTS[0])
# print('_'+''.join(PLOT_DOTS)+'+')
# print(PLOT_DOTS[-1])

def asciiPlot(f, xRange, yRange=None, xRes=80, yRes=20, unicodeOutput=True):
	dx = (xRange[1]-xRange[0])/xRes
	xVals = [xRange[0]+i*dx for i in range(xRes+1)]
	yVals = [f(x) for x in xVals]
	yMin,yMax = (min(yVals),max(yVals)) if yRange is None else yRange
	print(yMin,yMax)
	dy = (yMax-yMin)/(yRes-1)
	plotArea = [len(xVals)*' ' for _ in range(yRes+1)]
	for xIdx,y in enumerate(yVals):
		yScaled = (yMax-y)/dy+0.4
		yIdx = int(yScaled)
		line = plotArea[yIdx]
		dotChar = PLOT_DOTS[3-int(3.98*(yScaled-yIdx)+0.01)] if unicodeOutput else '.'
		plotArea[yIdx] = line[0:xIdx] + dotChar + line[xIdx+1:]
	return '\n'.join(plotArea)

def plotFpp(fpp, xRange=None, yRange=None, xRes=80, yRes=20, unicodeOutput=True):
	polyPieces = fpp.polyPieces
	if xRange is None: xRange = [polyPieces[0].interval[0],polyPieces[-1].interval[1]]
	return asciiPlot(lambda x: fpp.eval(x), xRange, yRange, xRes, yRes, unicodeOutput)
	

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

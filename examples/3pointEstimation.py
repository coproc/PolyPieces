'''simulate 3-point estimatimon from random data
'''
import sys
sys.path.append('../src')

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
for i in range(4):
	a = randint(1,10)
	c = a + randint(1,3)
	b = c + randint(1,7)
	triangleDists.append(triangDistDensity(a,b,c))

TextPlot.adjustConsoleEncodingForUnicode()

for td in triangleDists:
	print(TextPlot.plotFpp(td, [0,20], [0,1], yRes=8))

from functools import reduce
densityOfSum = reduce(lambda x,y: x^y, triangleDists)

print('\ndensity of sum of random variables with triangular distribution')
print(densityOfSum)
print()
print(TextPlot.plotFpp(densityOfSum))

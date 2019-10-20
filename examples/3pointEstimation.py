'''simulate 3-point estimatimon from random data
'''
import sys
sys.path.append('../src')

from UniVarPoly import UniVarPoly
from PolyPieces import PolyPiece, PolyPieceFunc

# generate density function of triangular distribution
def triangDistDensity(a,b,c):
	pp1 = PolyPiece([a,c], UniVarPoly([0, 2./(b-a)/(c-a)]).comp([-a,1]))
	pp2 = PolyPiece([c,b], UniVarPoly([0,-2./(b-a)/(b-c)]).comp([-b,1]))
	return PolyPieceFunc([pp1,pp2])


from random import randint

for i in range(10):
	# 
	a = randint(1,10)
	c = a + randint(1,3)
	b = c + randint(1,5)
	density3point = triangDistDensity(a,b,c)

	if i == 0:
		densityOfSum = density3point
	else:
		densityOfSum %= density3point
	print('.', end = '') # show progress

print()
print('density of sum of random variables with triangular distribution')
print(densityOfSum)

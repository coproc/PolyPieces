'''generate a piecewise polynomial function approximating Gauss' bell curve
   by convoluting the density of a uniform random variable with itself several times
'''
import sys
sys.path.append('../src')

import math
from UniVarPoly import UniVarPoly, p_x, p_x2
from PolyPieces import PolyPiece, PolyPieceFunc


# compute variance of a symmetric density function (i.e. expectation value is 0)
def varSym(fpp):
	fpp_x2 = p_x2 * fpp
	return fpp_x2.int()


def normedDist(fDist):
	area, var = fDist.int(), varSym(fDist)
	print("area", area, "var", var)
	fDistNormed1 = fDist.comp(UniVarPoly([0, math.sqrt(var)]))
	area1, var1 = fDistNormed1.int(), varSym(fDistNormed1)
	print("area1", area1, "var1", var1)
	fDistNormed2 = 1./area1 * fDistNormed1
	area2, var2 = fDistNormed2.int(), varSym(fDistNormed2)
	print("area2", area2, "var2", var2)
	return fDistNormed2

	
rg = 1 # 2*math.sqrt(3)
fDist_deg0 = PolyPieceFunc([PolyPiece([-rg/2.,rg/2.], UniVarPoly(1./rg))])
print(fDist_deg0)
print(fDist_deg0.int(), varSym(fDist_deg0))

fDist_deg1 = fDist_deg0.conv(fDist_deg0)
fDist_deg2 = convUnitVar(fDist_deg1, fDist_deg0)
fDist_deg4 = convUnitVar(fDist_deg2, fDist_deg1)

#print('fDist_deg1:')
#print(fpp1)
#print(fpp1.int(), varSym(fpp1))
#print('fppConv2:')
#print(fpp2)
#print(fpp2.int(), varSym(fpp2))
#print('fppConv4:')
#print(fpp4)
#print(fpp4.int(), varSym(fpp4))
#print(list(map(varSym, [fpp0, fpp1, fpp2, fpp4])))
#print(fpp4._isContinuous(prec=1e-5, printFailReason=True))

fDist_deg4_normed = normedDist(fDist_deg4)
print('approximation of normal density of degree 4')
print(fDist_deg4_normed)

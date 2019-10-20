import math
from UniVarPoly import UniVarPoly, p_x, p_x2
from PolyPieces import PolyPiece, PolyPieceFunc

SQRT2 = math.sqrt(2)
P_SQRT2x = SQRT2 * p_x

def convPow(fpp, n):
	fppConv = fpp
	print('fppConv0:')
	print(fppConv)
	for i in range(n):
		fppConv = fppConv. conv(fppConv)
		print('fppConv%d:' % (i+1))
		print(fppConv)
	return fppConv

def varSym(fpp):
	fpp_x2 = p_x2 * fpp
	return fpp_x2.int()


def convUnitVar(fpp1, fpp2):
	fppConv = fpp1.conv(fpp2)
	return fppConv
	#print("fppConv\n", fppConv)
	#fppConvNormed = SQRT2 * fppConv.comp(P_SQRT2x)
	#print("fppConvNormed\n", fppConvNormed)
	#return fppConvNormed
	#return SQRT2 * fppConv.comp(P_SQRT2x)
	#print(fppConv)
	#v1, v2, v = varSym(fpp1), varSym(fpp2), varSym(fppConv)
	#print(v1, v2, v)
	#fppConvNormed = fppConv.comp(UniVarPoly([0, 2**(1./3.)]))
	#print(fppConvNormed)
	#vn = varSym(fppConvNormed)
	#print("var normed:", v, vn, v/vn)
	#fppConvNormed2 = fppConv.comp(UniVarPoly([0, v**(1./3.)]))
	#fppConvNormed2 = SQRT2 * fppConv.comp(UniVarPoly([0, SQRT2]))
	#fppArea = fppConvNormed2.int()
	#print("area", fppArea)
	#fppConvNormed3 = 1./fppArea * fppConvNormed2
	#print(fppConvNormed)
	#vn2 = varSym(fppConvNormed2)
	#print("var normed2:", v, vn2, v/vn2)
	#return fppConvNormed2 #.comp(UniVarPoly([0, math.sqrt(2)]))


def fppNorm(fpp):
	area, var = fpp.int(), varSym(fpp)
	print("area", area, "var", var)
	fppNormed1 = fpp.comp(UniVarPoly([0, math.sqrt(var)]))
	area1, var1 = fppNormed1.int(), varSym(fppNormed1)
	print("area1", area1, "var1", var1)
	fppNormed2 = 1./area1 * fppNormed1
	area2, var2 = fppNormed2.int(), varSym(fppNormed2)
	print("area2", area2, "var2", var2)
	return fppNormed2

	
rg = 1 # 2*math.sqrt(3)
fpp0 = PolyPieceFunc([PolyPiece([-rg/2.,rg/2.], UniVarPoly(1./rg))])
print(fpp0)
print(fpp0.int(), varSym(fpp0))

fpp1 = convUnitVar(fpp0, fpp0)
fpp2 = convUnitVar(fpp1, fpp0)
fpp4 = convUnitVar(fpp2, fpp1)

print('fppConv1:')
print(fpp1)
print(fpp1.int(), varSym(fpp1))
print('fppConv2:')
print(fpp2)
print(fpp2.int(), varSym(fpp2))
print('fppConv4:')
print(fpp4)
print(fpp4.int(), varSym(fpp4))
print(list(map(varSym, [fpp0, fpp1, fpp2, fpp4])))
print(fpp4._isContinuous(prec=1e-5, printFailReason=True))

fpp4Normed = fppNorm(fpp4)
print(fpp4Normed)

#fppConvN = convPow(fpp2, 2)
#print(fppConvN.int())
#print(fppConvN)
#print(fppConvN._isContinuous(prec=1e-5, printFailReason=True))

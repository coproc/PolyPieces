'''piecewise polynomial functions
'''
import sys
import numbers
from fractions import Fraction
from UniVarPoly import UniVarPoly


class PolyPiece:
	'''polynomial over interval'''
	def __init__(self, poly, interval=None):
		if interval is None:
			if isinstance(poly, PolyPiece):
				self.poly = poly.poly
				self.interval = poly.interval
			else:
				try:
					poly,self.interval = poly
					self.poly = poly if isinstance(poly,UniVarPoly) else UniVarPoly(poly)
				except Exception:
					raise TypeError("PolyPiece cannot be constructed from '%s'" % [poly])
		else:
			self.poly = poly if isinstance(poly, UniVarPoly) else UniVarPoly(poly)
			self.interval = interval
			if len(self.interval) != 2 or not all([isinstance(n, numbers.Real) for n in self.interval]):
				raise TypeError("cannot create PolyPiece: invalid interval '%s'" % interval)
			if  self.interval[0] > self.interval[1]:
				raise ValueError("cannot create PolyPiece: invalid interval '%s'" % interval)


	def conv(self, pp):
		if self.poly.deg() < pp.poly.deg():
			return pp.conv(self)

		a1, b1 = self.interval
		a2, b2 = pp.interval
		#    a1  b1
		#     ---- 
		#	 ------
		#   a2    b2
		#
		# a1+a2 < b1+a2 <= a1+b2 < b1+b2:
		#	a1+a2 < x < b1+a2: a1 < t < x-a2
		#	b1+a2 < x < a1+b2: a1 < t < b1
		#	a1+b2 < x < b1+b2: x-b2 < t < b1

		#   a1    b1
		#	 ------
		#     ---- 
		#    a2  b2
		#
		# a1+a2 < a1+b2 <= b1+a2 < b1+b2:
		#	a1+a2 < x < a1+b2: a1 < t < x-a2
		#	a1+b2 < x < b1+a2: x-b2 < t < x-a2
		#	b1+a2 < x < b1+b2: x-b2 < t < b1
		xLimits = [a1+a2]
		tIntervals = [[a1,[-a2,1]]]
		if a1+b2 < b1+a2:
			tIntervals.append([[-b2,1],[-a2,1]])
			xLimits.extend([a1+b2,b1+a2])
		elif a1+b2 > b1+a2:
			tIntervals.append([a1,b1])
			xLimits.extend([b1+a2,a1+b2])
		else:
			xLimits.append(a1+b2)
		tIntervals.append([[-b2,1], b1])
		xLimits.append(b1+b2)
		#print(xLimits)

		# (f*g)(x) = int f(t)*g(x-t) dt = F(t)*g(x-t)_a1_x-a2 + int F(t)*g'(x-t) 
		#         = F(t)*g(x-t) + F2(t)*g'(x-t) + int F2(t)*g''(x-t) | a1 .. x-a2 =
		#		 = F(x-a2)*g(a2) + ... - (F(a1)*g(x-a1) + ...)
		p2_dk = pp.poly
		if p2_dk == 0: return PolyPieceFunc()
		p1int_k = self.poly.int()
		ppl_conv = [PolyPiece(UniVarPoly(), xLimits[i:i+2]) for i in range(len(tIntervals))]
		while True:
			for j,tLimits in enumerate(tIntervals):
				for i,t in enumerate(tLimits):
					s = 1 if i%2 else -1
					if type(t) == list:
						pt = (s*p2_dk.eval(-t[0])) * p1int_k.comp(t)
					else:
						pt = (s*p1int_k.eval(t))   * p2_dk.comp([-t,1])
					ppl_conv[j].poly += pt
			p2_dk = p2_dk.der()
			if p2_dk == 0: break
			p1int_k = p1int_k.int()
		return PolyPieceFunc(ppl_conv)


	def __mul__(self, pp):
		return self.conv(pp)


	def __str__(self, prec=None):
		aRepr = UniVarPoly._coeffRepr(self.interval[0], prec)
		bRepr = UniVarPoly._coeffRepr(self.interval[1], prec)
		return "%s, x in [%s,%s]" % (self.poly, aRepr, bRepr)


class PolyPieceFunc:
	'''create piecewise polynomial function
	
	   >>> fpp = PolyPieceFunc(PolyPiece(1,[0,1]))
	   >>> print(fpp)
	   f(x) =
	     1, x in [0,1]
	     0, else
	   >>> from UniVarPoly import p_x as x
	   >>> fpp = PolyPieceFunc(((x,[0,1]), (1-x,[1,2])))
	   >>> print(fpp)
	   f(x) =
	     x,      x in [0,1]
	     -x + 1, x in [1,2]
	     0, else
	'''
	def __init__(self, polyPieces=None):
		if polyPieces is None:
			self.polyPieces = []
		elif isinstance(polyPieces, PolyPiece):
			self.polyPieces = [polyPieces]
		elif isinstance(polyPieces, list) and all([isinstance(pp, PolyPiece) for pp in polyPieces]):
			self.polyPieces = polyPieces
		else:
			try:
				self.polyPieces = [PolyPiece(pp) for pp in polyPieces]
			except TypeError:
				raise TypeError("piecewise polynomial function cannot be created from '%s'" % [polyPieces])
			except Exception:
				raise ValueError("piecewise polynomial function cannot be created from '%s'" % polyPieces)
		if not self._isConsistent():
			raise ValueError("invalid poly pieces in '%s'" % polyPieces)


	def _isConsistent(self, prec=1e-10, printFailReason=False):
		if len(self.polyPieces) == 0: return True
		for i,pp in enumerate(self.polyPieces):
			intv_i = pp.interval
			if intv_i[0] > intv_i[1] + prec:
				if printFailReason:
					print("poly %d: invalid interval %s" % (i,intv_i), file=sys.stderr)
				return False
			if abs(intv_i[0] - intv_i[1]) < prec:
				if printFailReason:
					print("poly %d: 0-length interval %s (warning)" % (i,intv_i), file=sys.stderr)
			if i>0 and intv_i[0] < intvPrev[1]-prec:
				if printFailReason:
					print("poly %d overlaps with previous poly (%f - %f)" %(i, intvPrev[1], intv_i[0]), file=sys.stderr)
				return False
			intvPrev = intv_i
		return True


	def _isContinuous(self, prec=1e-10, printFailReason=False):
		'''check if piecewise function is continuous.
		
		   >>> fpp = PolyPieceFunc()
		   >>> fpp._isContinuous()
		   True
		   >>> fpp1 = PolyPieceFunc([PolyPiece(1, [0,1])])
		   >>> fpp1._isContinuous()
		   False
		   >>> fpp2 = PolyPieceFunc([PolyPiece(UniVarPoly([0,1]),[0,1]), PolyPiece(UniVarPoly([2,-1]),[1,2])])
		   >>> fpp2._isContinuous()
		   True
		'''
		assert(self._isConsistent(printFailReason=printFailReason))
		if len(self.polyPieces) == 0: return True
		ppPrev = PolyPiece(UniVarPoly(), [-float('inf'),self.polyPieces[0].interval[0]])
		for i,pp in enumerate(self.polyPieces):
			x0 = pp.interval[0]
			valPrev = ppPrev.poly.eval(x0) if abs(x0 - ppPrev.interval[1]) < prec else 0
			val_x0 = pp.poly.eval(x0)
			if abs(val_x0 - valPrev) >= prec:
				if printFailReason:
					print("poly %d does not start at previous value %f, but at %f" % (i, valPrev, val_x0), file=sys.stderr)
				return False
			ppPrev = pp
		return True


	def _selectPP(self, x0, idxStart=0):
		'''return (first) polynomial piece containing x0 in its definition range
		
		   >>> pp1 = PolyPiece(UniVarPoly([0,1]), [-1,1])
		   >>> pp2 = PolyPiece(UniVarPoly([0,2]), [ 1,2])
		   >>> fpp = PolyPieceFunc([pp1, pp2])
		   >>> fpp._isConsistent()
		   True
		   >>> fpp._selectPP(-2)
		   (<UniVarPoly '0'>, 0)
		   >>> fpp._selectPP(-1)
		   (<UniVarPoly 'x'>, 0)
		   >>> fpp._selectPP(1)
		   (<UniVarPoly 'x'>, 0)
		   >>> fpp._selectPP(2)
		   (<UniVarPoly '2x'>, 1)
		'''
		if idxStart >= len(self.polyPieces):          return UniVarPoly(),idxStart
		if x0 < self.polyPieces[idxStart].interval[0]: return UniVarPoly(),idxStart
		for i,pp in enumerate(self.polyPieces[idxStart:]):
			intv,pi = pp.interval, pp.poly
			if intv[0] > x0:
				return UniVarPoly(), idxStart+i
			if x0 <= intv[1]:
				return pi, idxStart+i
		return UniVarPoly(), idxStart+len(self.polyPieces)


	def eval(self, x0):
		'''evaluate at x=x0
		
		   >>> pp1 = PolyPiece(UniVarPoly([0,1]), [-1,1])
		   >>> pp2 = PolyPiece(UniVarPoly([0,2]), [ 1,2])
		   >>> fpp = PolyPieceFunc([pp1, pp2])
		   >>> fpp.eval(-2)
		   0
		   >>> fpp.eval(-1)
		   -1
		   >>> fpp.eval(-0.5)
		   -0.5
		   >>> fpp.eval(1)
		   1
		   >>> fpp.eval(1.5)
		   3.0
		   >>> fpp.eval(2)
		   4
		   >>> fpp.eval(2.1)
		   0
		'''
		poly, _ = self._selectPP(x0)
		return poly.eval(x0)


	def comp(self, p):
		'''compute polynomial composition self o poly.
		   Only implemented for numbers and linear polynomials.
		
		   >>> fpp = PolyPieceFunc([PolyPiece(1, [0,1])])
		   >>> p1 = UniVarPoly([-1,1])
		   >>> fpp2 = fpp.comp(p1)
		   >>> x0Vals = [-1, -0.5, 0, 0.5, 1, 1.5, 2]
		   >>> all(map(lambda x0: fpp2.eval(x0) == fpp.eval(p1.eval(x0)), x0Vals))
		   True
		'''
		if isinstance(p, numbers.Number):
			return self.eval(p)
		if not isinstance(p, UniVarPoly):
			raise ValueError("unexpected type '%s' for composition" % type(p))
		if p.deg() == 0:
			return self.eval(p.coeffs[0])
		if p.deg() > 1:
			raise ValueError("composition only implemented for polynomials up to degree 1, degree %d received" % p.deg())

		d,k = p.coeffs
		try:
			scaleFacIntv = Fraction(1,k)
		except TypeError:
			scaleFacIntv = 1/k
		fppComp = PolyPieceFunc()
		for pp in self.polyPieces:
			a,b = pp.interval
			fppComp.polyPieces.append(PolyPiece(pp.poly.comp(p), [(a-d)*scaleFacIntv,(b-d)*scaleFacIntv]))
			
		return fppComp


	def _binArithOp(self, op2, opFunc):
		'''implement a binary arithmetic operation with a number, a polynomial or another piecewise polynomial function.
		'''
		allowedOpTypes = [numbers.Number, UniVarPoly, PolyPieceFunc]
		if not any(map(lambda t: isinstance(op2, t), allowedOpTypes)):
			raise ValueError("arithmetic operator of invalid type '%s'" % type(op2))
		xl = []
		for pp in self.polyPieces:
			xl += pp.interval
		if isinstance(op2, PolyPieceFunc):
			for pp in op2.polyPieces:
				xl += pp.interval
		xl = list(set(xl))
		xl.sort()
		
		ppl_res = []
		i1,i2 = 0,0
		for i,xi in enumerate(xl[:-1]):
			xi_1 = xl[i+1]
			x = 0.5*(xi+xi_1)
			p1,i1 = self._selectPP(x, i1)
			if isinstance(op2, PolyPieceFunc):
				p2,i2 = op2._selectPP(x, i2)
			else:
				p2 = op2
			ppl_res.append(PolyPiece(opFunc(p1,p2), [xi,xi_1]))
		return PolyPieceFunc(ppl_res)


	def __add__(self, op2):
		'''overload operator +
		
		   >>> fpp = PolyPieceFunc([PolyPiece(UniVarPoly([0,1]), [0,1])])
		   >>> print(fpp + 1)
		   f(x) =
		     x + 1, x in [0,1]
		     0, else
		   >>> print(fpp + fpp)
		   f(x) =
		     2x, x in [0,1]
		     0, else
		'''
		return self._binArithOp(op2, lambda x,y: x+y)


	def __iadd__(self, op2):
		'''overload operator +=
		'''
		self.polyPieces = (self + op2).polyPieces
		return self


	def __radd__(self, op1):
		'''overload operator + for right hand side
		'''
		return self.__add__(op1)


	def __pos__(self):
		'''overload unary operator +
		
		   >>> fpp = PolyPieceFunc([PolyPiece(UniVarPoly([0,1]), [0,1])])
		   >>> print(+fpp)
		   f(x) =
		     x, x in [0,1]
		     0, else
		'''
		return 1*self


	def __neg__(self):
		'''overload unary operator -
		
		   >>> fpp = PolyPieceFunc([PolyPiece(UniVarPoly([0,1]), [0,1])])
		   >>> print(-fpp)
		   f(x) =
		     -x, x in [0,1]
		     0, else
		'''
		return (-1)*self


	def __sub__(self, op2):
		'''overload operator -
		
		   >>> fpp = PolyPieceFunc([PolyPiece(UniVarPoly([0,1]), [0,1])])
		   >>> print(fpp - 1)
		   f(x) =
		     x - 1, x in [0,1]
		     0, else
		   >>> print(2*fpp - fpp)
		   f(x) =
		     x, x in [0,1]
		     0, else
		'''
		return self._binArithOp(op2, lambda x,y: x-y)


	def __isub__(self, op2):
		'''overload operator -=
		'''
		self.polyPieces = (self - op2).polyPieces
		return self


	def __rsub__(self, op1):
		'''overload operator + for right hand side
		
		   >>> fpp = PolyPieceFunc([PolyPiece(UniVarPoly([0,1]), [0,1])])
		   >>> print(1 - fpp)
		   f(x) =
		     -x + 1, x in [0,1]
		     0, else
		'''
		return -(self.__sub__(op1))


	def __mul__(self, op2):
		'''overload operator *
		
		   >>> fpp = PolyPieceFunc([PolyPiece(UniVarPoly([0,1]), [0,1])])
		   >>> print(fpp * 2)
		   f(x) =
		     2x, x in [0,1]
		     0, else
		   >>> print(fpp * fpp)
		   f(x) =
		     x^2, x in [0,1]
		     0, else
		'''
		return self._binArithOp(op2, lambda x,y: x*y)


	def __imul__(self, op2):
		'''overload operator *=
		'''
		self.polyPieces = (self * op2).polyPieces
		return self


	def __rmul__(self, op1):
		'''overload operator * for right hand side
		'''
		return self.__mul__(op1)


	def __truediv__(self, op2):
		'''overload operators /, /=
		   (divisor must be number)
		
		   >>> fpp = PolyPieceFunc([PolyPiece(UniVarPoly([0,1]), [0,1])])
		   >>> print(fpp / 2)
		   f(x) =
		     1/2x, x in [0,1]
		     0, else
		   >>> fpp /= 2
		   >>> print(fpp)
		   f(x) =
		     1/2x, x in [0,1]
		     0, else
		'''
		if isinstance(op2, numbers.Number):
			return self._binArithOp(op2, lambda x,y: x/y)
		raise TypeError("divisor of invalid type %s (must be number)" % type(op2))


	def der(self):
		'''derivative function
		
		   >>> p_1 = UniVarPoly([1])
		   >>> p_x2 = UniVarPoly([0,0,1])
		   >>> p_x_2 = UniVarPoly([2,1])
		   >>> p_x__2 = UniVarPoly([-2,1])
		   >>> fpp = PolyPieceFunc([PolyPiece(p_x2.comp(p_x_2),  [-2,-1]), 
		   ...                      PolyPiece(2*p_1 - p_x2,      [-1, 1]), 
		   ...                      PolyPiece(p_x2.comp(p_x__2), [ 1, 2])]) 
		   >>> fppDer = fpp.der()
		   >>> fppDer._isContinuous()
		   True
		   >>> list(map(lambda x: fppDer.eval(x), [-2,-1,0,1,2]))
		   [0, 2, 0, -2, 0]
		   >>> fppDer.int()
		   0
		'''
		# derivative of constant polynomial is the zero polynomial
		fDer = PolyPieceFunc()
		for pp in self.polyPieces:
			fDer.polyPieces.append(PolyPiece(pp.poly.der(), pp.interval))
		return fDer


	def int(self, interval=[-float('inf'),float('inf')]):
		'''definite integral over given interval
		
		   >>> fpp = PolyPieceFunc()
		   >>> fpp.int()
		   0
		   >>> fpp1 = PolyPieceFunc([PolyPiece(1, [0,1])])
		   >>> fpp1.int()
		   1
		   >>> fpp2 = PolyPieceFunc([PolyPiece(UniVarPoly([0,1]),[0,1]), PolyPiece(UniVarPoly([2,-1]),[1,2])])
		   >>> fpp2.int([-1,3])
		   1
		   >>> fpp2.int([0.5,3])
		   0.875
		   >>> fpp2.int([-1,1.5])
		   0.875
		   >>> fpp2.int([0.5,1.5])
		   0.75
		'''
		intVal = 0
		for pp in self.polyPieces:
			if pp.interval[0] > interval[1]: break
			if pp.interval[1] < interval[0]: continue
			intVal += pp.poly.intDef([max(interval[0], pp.interval[0]),
			                          min(interval[1], pp.interval[1])])
		if isinstance(intVal, Fraction) and intVal.denominator == 1: intVal = intVal.numerator
		return intVal


	def conv(self, fpp):
		# (Sum_i fi) * (Sum_i gi) = Sum_i Sum_j fi * gj
		fpp_conv = PolyPieceFunc()
		for pp1 in self.polyPieces:
			for pp2 in fpp.polyPieces:
				fpp_conv += pp1 * pp2
		return fpp_conv


	def __xor__(self, fpp):
		return self.conv(fpp)


	def __ixor__(self, fpp):
		self.polyPieces = (self ^ fpp).polyPieces
		return self
		

	@staticmethod
	def _align(key, strings):
		keyPos = max([s.find(key) for s in strings])
		return [((keyPos-len(s1))*' ' + key).join([s1,s2]) for s1,s2 in [s.split(key) for s in strings]]


	def __str__(self):
		pieceReprs = [str(pp) for pp in self.polyPieces]
		pieceReprs = PolyPieceFunc._align('x in', pieceReprs)
		indent = '  '
		return 'f(x) =\n' + indent + ('\n'+indent).join(pieceReprs) + '\n' + indent + '0, else'


if __name__ == "__main__":
	import doctest
	doctest.testmod()
	#fpp = PolyPieceFunc(PolyPiece(1,[0,1]))
	#print(fpp)
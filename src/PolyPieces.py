'''piecewise polynomial functions
'''
import sys
import numbers
from fractions import Fraction
from Polynomial import Polynomial


class PolyPiece:
	'''polynomial over interval'''
	def __init__(self, poly, interval=None):
		if interval is None:
			if isinstance(poly, PolyPiece):
				self.poly = poly.poly
				self.interval = poly.interval
			else:
				try:
					poly,interval = poly
					PolyPiece(poly, interval) # check if arguments are valid
					self.poly = poly if isinstance(poly,Polynomial) else Polynomial(poly)
					self.interval = interval
				except Exception:
					raise TypeError("PolyPiece cannot be constructed from '%s'" % [poly])
		elif len(interval) == 2 and all([isinstance(n, numbers.Real) for n in interval]):
			if  interval[1] < interval[0]:
				raise ValueError("cannot create PolyPiece: invalid interval '%s'" % interval)
			self.poly = poly if isinstance(poly, Polynomial) else Polynomial(poly)
			self.interval = interval
		else:
			raise TypeError("cannot create PolyPiece, this is not an interval of reals: '%s'" % interval)


	def conv(self, pp):
		'''compute convolution
		   >>> pp0 = PolyPiece(1, [0,1])
		   >>> print(pp0.conv(pp0))
		   f(x) =
		     x,      x in [0,1]
		     -x + 2, x in [1,2]
		     0, else
		   >>> p_x = Polynomial([0, 1])
		   >>> pp1 = PolyPiece(p_x, [0,1])
		   >>> print(pp1.conv(pp1))
		   f(x) =
		     1/6x^3,            x in [0,1]
		     -1/6x^3 + x - 2/3, x in [1,2]
		     0, else
		'''
		if self.poly.deg() < pp.poly.deg():
			return pp.conv(self)

		xName = self.poly.varName
		def xPoly(coeffs): return Polynomial(coeffs, xName)
		xIdPoly = xPoly([0,1])
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
		tIntervals = [[a1, xPoly([-a2,1])]]
		if a1+b2 < b1+a2:
			tIntervals.append([xPoly([-b2,1]), xPoly([-a2,1])])
			xLimits.extend([a1+b2,b1+a2])
		elif a1+b2 > b1+a2:
			tIntervals.append([a1,b1])
			xLimits.extend([b1+a2,a1+b2])
		else:
			xLimits.append(a1+b2)
		tIntervals.append([xPoly([-b2,1]), b1])
		xLimits.append(b1+b2)

		# integration of a polynomial with two variables is reduced to computations with univariate polynomial
		# by using the multiplication rule until the second polynomial reduces to zero:
		# (f*g)(x) = int f(t)*g(x-t) dt = F(t)*g(x-t)_a1_x-a2 + int F(t)*g'(x-t) 
		#          = F(t)*g(x-t) + F2(t)*g'(x-t) + int F2(t)*g''(x-t) | a1 .. x-a2 =
		#          = F(x-a2)*g(a2) + ... - (F(a1)*g(x-a1) + ...)
		p2_dk = pp.poly
		if p2_dk == 0: return PolyPieceFunc()
		p1int_k = self.poly.int()
		ppl_conv = [PolyPiece(0, xLimits[i:i+2]) for i in range(len(tIntervals))]
		while True:
			for j,tLimits in enumerate(tIntervals):
				for s,t in zip((-1,1), tLimits):
					pt = s * p1int_k.comp(t) * p2_dk.comp(xIdPoly - t)
					ppl_conv[j].poly += pt
			p2_dk = p2_dk.der()
			if p2_dk == 0: break
			p1int_k = p1int_k.int()
		return PolyPieceFunc(ppl_conv)


	def __xor__(self, pp):
		return self.conv(pp)


	def __str__(self, prec=None):
		aRepr = Polynomial._coeffRepr(self.interval[0], prec)
		bRepr = Polynomial._coeffRepr(self.interval[1], prec)
		return "%s, x in [%s,%s]" % (self.poly, aRepr, bRepr)


class PolyPieceFunc:
	'''create piecewise polynomial function
	
	   >>> fpp = PolyPieceFunc(PolyPiece(1,[0,1]))
	   >>> print(fpp)
	   f(x) =
	     1, x in [0,1]
	     0, else
	   >>> from Polynomial import symbol
	   >>> x = symbol()
	   >>> fpp = PolyPieceFunc(((x,[0,1]), (1-x,[1,2])))
	   >>> print(fpp)
	   f(x) =
	     x,      x in [0,1]
	     -x + 1, x in [1,2]
	     0, else
	   >>> fpp = PolyPieceFunc(((x,[0,1]), (0,[1,2])))
	   >>> print(fpp)
	   f(x) =
	     x, x in [0,1]
	     0, else
	   >>> fpp = PolyPieceFunc(((0,0), (x,1), (1,2)))
	   >>> print(fpp)
	   f(x) =
	     x, x in [0,1]
	     1, x in [1,2]
	     0, else
	   >>> fpp = PolyPieceFunc((0,0), (x,1), (1,2))
	   >>> print(fpp)
	   f(x) =
	     x, x in [0,1]
	     1, x in [1,2]
	     0, else
	'''
	def __init__(self, *polyPieces):
		self.polyPieces = PolyPieceFunc._constructPolyPieces(*polyPieces)
		self._normalize()
		if not self._isConsistent():
			raise ValueError("inconsistent poly pieces in '%s'" % polyPieces)

	@staticmethod
	def _constructPolyPieces(*polyPieces):
		if len(polyPieces) == 0:
			return []
		elif len(polyPieces) == 1:
			if isinstance(polyPieces[0], PolyPiece):
				return polyPieces
			else:
				for constrFunc in [PolyPieceFunc._constructPP_fromPPs, PolyPieceFunc._constructPP_fromPPConvertibles,
					PolyPieceFunc._constructPP_fromPolyLimitPairs]:
					try:
						#print('trying', constrFunc, file=sys.stderr)
						return constrFunc(polyPieces[0])
					except: pass
		for constrFunc in [PolyPieceFunc._constructPP_fromPPs, PolyPieceFunc._constructPP_fromPPConvertibles,
			PolyPieceFunc._constructPP_fromPolyLimitPairs]:
			try:
				#print('trying', constrFunc, file=sys.stderr)
				return constrFunc(polyPieces)
			except: pass
		raise TypeError("piecewise polynomial function cannot be created from '%s'" % (polyPieces,))

	@staticmethod
	def _constructPP_fromPPs(polyPieces):
		if all([isinstance(pp, PolyPiece) for pp in ret]):
			return list(polyPieces)
		raise InvalidArgument("poly pieces cannot be constructed by mere copying")
		
	@staticmethod
	def _constructPP_fromPPConvertibles(polyPieces):
		return [PolyPiece(pp) for pp in polyPieces]

	@staticmethod
	def _constructPP_fromPolyLimitPairs(polyPieces):
		lowerLimit = -float('inf')
		ret = []
		for poly,upperLimit in polyPieces:
			interval = (lowerLimit, upperLimit)
			lowerLimit = upperLimit
			if interval[0] == -float('inf') and poly == 0: continue
			ret.append(PolyPiece(poly, interval))
		return ret


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


	def _isContinuous(self, prec=None, printFailReason=False):
		'''check if piecewise function is continuous.
		
		   >>> fpp = PolyPieceFunc()
		   >>> fpp._isContinuous()
		   True
		   >>> fpp1 = PolyPieceFunc([PolyPiece(1, [0,1])])
		   >>> fpp1._isContinuous()
		   False
		   >>> fpp2 = PolyPieceFunc([PolyPiece(Polynomial([0,1]),[0,1]), PolyPiece(Polynomial([2,-1]),[1,2])])
		   >>> fpp2._isContinuous()
		   True
		'''
		assert(self._isConsistent(printFailReason=printFailReason))
		def _precDef(prec, val):
			if prec is not None: return prec
			if isinstance(val, (int, Fraction)): return 0 # exact computation with ints and fractions
			return 1e-10 # approximate calculations with floats

		if len(self.polyPieces) == 0: return True
		ppPrev = PolyPiece(Polynomial(), [-float('inf'),self.polyPieces[0].interval[0]])
		for i,pp in enumerate(self.polyPieces):
			x0 = pp.interval[0]
			absDiffX = abs(x0 - ppPrev.interval[1])
			valPrev = ppPrev.poly.eval(x0) if absDiffX <= _precDef(prec, absDiffX) else 0
			val_x0 = pp.poly.eval(x0)
			absDiffY = abs(val_x0 - valPrev)
			if absDiffY > _precDef(prec, absDiffY):
				if printFailReason:
					print("poly %d does not start at previous value %f, but at %f" % (i, valPrev, val_x0), file=sys.stderr)
				return False
			ppPrev = pp
		return True


	def _selectPP(self, x0, idxStart=0):
		'''return (first) polynomial piece containing x0 in its definition range
		
		   >>> pp1 = PolyPiece(Polynomial([0,1]), [-1,1])
		   >>> pp2 = PolyPiece(Polynomial([0,2]), [ 1,2])
		   >>> fpp = PolyPieceFunc([pp1, pp2])
		   >>> fpp._isConsistent()
		   True
		   >>> fpp._selectPP(-2)
		   (<Polynomial '0'>, 0)
		   >>> fpp._selectPP(-1)
		   (<Polynomial 'x'>, 0)
		   >>> fpp._selectPP(1)
		   (<Polynomial 'x'>, 0)
		   >>> fpp._selectPP(2)
		   (<Polynomial '2x'>, 1)
		'''
		if idxStart >= len(self.polyPieces):          return Polynomial(),idxStart
		if x0 < self.polyPieces[idxStart].interval[0]: return Polynomial(),idxStart
		for i,pp in enumerate(self.polyPieces[idxStart:]):
			intv,pi = pp.interval, pp.poly
			if intv[0] > x0:
				return Polynomial(), idxStart+i
			if x0 <= intv[1]:
				return pi, idxStart+i
		return Polynomial(), idxStart+len(self.polyPieces)


	def eval(self, x0):
		'''evaluate at x=x0
		
		   >>> pp1 = PolyPiece(Polynomial([0,1]), [-1,1])
		   >>> pp2 = PolyPiece(Polynomial([0,2]), [ 1,2])
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
		   >>> p1 = Polynomial([-1,1])
		   >>> fpp2 = fpp.comp(p1)
		   >>> x0Vals = [-1, -0.5, 0, 0.5, 1, 1.5, 2]
		   >>> all(map(lambda x0: fpp2.eval(x0) == fpp.eval(p1.eval(x0)), x0Vals))
		   True
		'''
		if isinstance(p, numbers.Number):
			return self.eval(p)
		if not isinstance(p, Polynomial):
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


	def __call__(self, poly):
		'''overload call operator (composition/substitution/evaluation)
		'''
		return self.comp(poly)


	# for debugging purposes
	def _log(self, msg):
		with open('debug.log','a') as f:
			f.write('%s:\n%s\n' % (msg, self))


	# remove intervals with 0-polynomials
	def _normalize(self):
		self.polyPieces = [pp for pp in self.polyPieces if pp.poly != 0 and pp.interval[0] != pp.interval[1]]


	def _binArithOp(self, op2, opFunc):
		'''implement a binary arithmetic operation with a number, a polynomial or another piecewise polynomial function.
		'''
		allowedOpTypes = [numbers.Number, Polynomial, PolyPieceFunc]
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
		
		   >>> fpp = PolyPieceFunc([PolyPiece(Polynomial([0,1]), [0,1])])
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
		
		   >>> fpp = PolyPieceFunc([PolyPiece(Polynomial([0,1]), [0,1])])
		   >>> print(+fpp)
		   f(x) =
		     x, x in [0,1]
		     0, else
		'''
		return 1*self


	def __neg__(self):
		'''overload unary operator -
		
		   >>> fpp = PolyPieceFunc([PolyPiece(Polynomial([0,1]), [0,1])])
		   >>> print(-fpp)
		   f(x) =
		     -x, x in [0,1]
		     0, else
		'''
		return (-1)*self


	def __sub__(self, op2):
		'''overload operator -
		
		   >>> fpp = PolyPieceFunc([PolyPiece(Polynomial([0,1]), [0,1])])
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
		
		   >>> fpp = PolyPieceFunc([PolyPiece(Polynomial([0,1]), [0,1])])
		   >>> print(1 - fpp)
		   f(x) =
		     -x + 1, x in [0,1]
		     0, else
		'''
		return -(self.__sub__(op1))


	def __mul__(self, op2):
		'''overload operator *
		
		   >>> fpp = PolyPieceFunc([PolyPiece(Polynomial([0,1]), [0,1])])
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
		
		   >>> fpp = PolyPieceFunc([PolyPiece(Polynomial([0,1]), [0,1])])
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
		
		   >>> p_1 = Polynomial([1])
		   >>> p_x2 = Polynomial([0,0,1])
		   >>> p_x_2 = Polynomial([2,1])
		   >>> p_x__2 = Polynomial([-2,1])
		   >>> fpp = PolyPieceFunc([PolyPiece(p_x2.comp(p_x_2),  [-2,-1]), 
		   ...                      PolyPiece(2*p_1 - p_x2,      [-1, 1]), 
		   ...                      PolyPiece(p_x2.comp(p_x__2), [ 1, 2])]) 
		   >>> fppDer = fpp.der()
		   >>> fppDer._isContinuous()
		   True
		   >>> list(map(lambda x: fppDer.eval(x), [-2,-1,0,1,2]))
		   [0, 2, 0, -2, 0]
		   >>> fppDer.intDef()
		   0
		'''
		# derivative of constant polynomial is the zero polynomial
		fDer = PolyPieceFunc()
		for pp in self.polyPieces:
			fDer.polyPieces.append(PolyPiece(pp.poly.der(), pp.interval))
		return fDer


	def intDef(self, interval=[-float('inf'),float('inf')]):
		'''definite integral over given interval
		
		   >>> fpp = PolyPieceFunc()
		   >>> fpp.intDef()
		   0
		   >>> fpp1 = PolyPieceFunc([PolyPiece(1, [0,1])])
		   >>> fpp1.intDef()
		   1
		   >>> fpp2 = PolyPieceFunc([PolyPiece(Polynomial([0,1]),[0,1]), PolyPiece(Polynomial([2,-1]),[1,2])])
		   >>> fpp2.intDef([-1,3])
		   1
		   >>> fpp2.intDef([0.5,3])
		   0.875
		   >>> fpp2.intDef([-1,1.5])
		   0.875
		   >>> fpp2.intDef([0.5,1.5])
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
		'''compute convolution int(-inf,inf) f(t)g(x-t)dt

		   >>> pdf0 = PolyPieceFunc(PolyPiece(1,[0,1]))
		   >>> pdf1 = pdf0.conv(pdf0)
		   >>> print(pdf1)
		   f(x) =
		     x,      x in [0,1]
		     -x + 2, x in [1,2]
		     0, else
		   >>> pdf2 = pdf1.conv(pdf0)
		   >>> print(pdf2)
		   f(x) =
		     1/2x^2,            x in [0,1]
		     -x^2 + 3x - 3/2,   x in [1,2]
		     1/2x^2 - 3x + 9/2, x in [2,3]
		     0, else
		   >>> ', '.join([str(pdf2(x)) for x in [0,1,2,3]])
		   '0, 1/2, 1/2, 0'
		   >>> pdf2.intDef([0,4])
		   1
		   >>> pdf3 = pdf1.conv(pdf1)
		   >>> print(pdf3)
		   f(x) =
		     1/6x^3,                     x in [0,1]
		     -1/2x^3 + 2x^2 - 2x + 2/3,  x in [1,2]
		     1/2x^3 - 4x^2 + 10x - 22/3, x in [2,3]
		     -1/6x^3 + 2x^2 - 8x + 32/3, x in [3,4]
		     0, else
		   >>> pdf3.intDef([0,4])
		   1

		   >> [pdf3(x) for x in [0,1,2,3,4]]
		'''
		# (Sum_i fi) * (Sum_i gi) = Sum_i Sum_j fi * gj
		fpp_conv = PolyPieceFunc()
		for pp1 in self.polyPieces:
			for pp2 in fpp.polyPieces:
				fpp_conv += pp1.conv(pp2)
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
		if not self.polyPieces:
			return 'f(x) = 0'
		pieceReprs = [str(pp) for pp in self.polyPieces]
		pieceReprs = PolyPieceFunc._align('x in', pieceReprs)
		indent = '  '
		return 'f(x) =\n' + indent + ('\n'+indent).join(pieceReprs) + '\n' + indent + '0, else'


if __name__ == "__main__":
	import doctest
	print('running doc tests ...')
	doctest.testmod()

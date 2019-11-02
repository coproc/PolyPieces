'''Basic arithmetic for univariate polynomials encoded as list of coefficients
'''
from __future__ import division
import copy
import numbers
from fractions import Fraction


class UniVarPoly:
	def __init__(self, coeffs = [0]):
		'''create univariate polynomial.

		   The coefficients must be given in ascending order.
		   If no coefficients are given [0] (the 0 polynomial) is assumed.
		   If a polynomial is given, its coefficents are (deeply) copied.
		   >>> p_0 = UniVarPoly()
		   >>> p_0.coeffs
		   [0]
		   >>> p_1 = UniVarPoly(1)
		   >>> p_1.coeffs
		   [1]
		   >>> p_x2 = UniVarPoly([0,0,1]) # x^2
		   >>> p_x2.coeffs
		   [0, 0, 1]
		   >>> p = UniVarPoly('(x-1)*(x+1)')
		   >>> p.coeffs
		   [-1, 0, 1]
		   >>> p2 = UniVarPoly(p)
		   >>> p.coeffs.append(1)
		   >>> p2.coeffs
		   [-1, 0, 1]
		   >>> p.coeffs
		   [-1, 0, 1, 1]
		'''
		if type(coeffs) == list:
			self.coeffs = copy.deepcopy(coeffs)
		elif isinstance(coeffs, UniVarPoly):
			self.coeffs = copy.deepcopy(coeffs.coeffs)
		elif isinstance(coeffs, numbers.Number):
			self.coeffs = [coeffs]
		elif isinstance(coeffs, str):
			p = eval(coeffs, None, {'x': p_x})
			self.coeffs = p.coeffs
		else:
			raise ValueError("unexpected type '%s' when constructing polynomial" % type(coeffs))


	def deg(self):
		'''degree of polynomial
		
		   >>> UniVarPoly([0, 1, 1]).deg()
		   2
		'''
		return len(self.coeffs) - 1


	def eval(self, x0):
		'''evaluate polynomial at given x0, i.e. compute poly(x0)
		
		   >>> p = UniVarPoly([1, 2, 1])
		   >>> p.eval(0)
		   1
		   >>> p.eval(1)
		   4
		'''
		x0_k = 1
		p_x0 = 0
		for k in range(len(self.coeffs)):
			p_x0 += self.coeffs[k]*x0_k
			x0_k *= x0
		return p_x0

		
	def _iaddCoeffs(self, coeffs):
		for i in range(min(len(self.coeffs), len(coeffs))):
			self.coeffs[i] += coeffs[i]
		if len(coeffs) > len(self.coeffs):
			self.coeffs += coeffs[len(self.coeffs):]
		while len(self.coeffs) > 1 and self.coeffs[-1] == 0:
			self.coeffs = self.coeffs[:-1]


	def _isubCoeffs(self, coeffs):
		coeffsInv = [-c for c in coeffs]
		self._iaddCoeffs(coeffsInv)

	
	def iadd(self, poly):
		'''add another polynomial.
		   poly can be a number, a coefficient list or another univariate polynomial
		   
		   >>> p = UniVarPoly([0,1]) # x
		   >>> p.iadd(-1)
		   >>> p.coeffs
		   [-1, 1]
		   >>> p.iadd([0,0,1])
		   >>> p.coeffs
		   [-1, 1, 1]
		   >>> p.iadd(UniVarPoly([0,0,-1]))
		   >>> p.coeffs
		   [-1, 1]
		'''
		if isinstance(poly, numbers.Number):
			self.coeffs[0] += poly
		elif isinstance(poly, list):
			self._iaddCoeffs(poly)
		elif isinstance(poly, UniVarPoly):
			self._iaddCoeffs(poly.coeffs)
		else:
			raise ValueError("unexpected argument type " + type(poly))


	def isub(self, poly):
		'''subtract another polynomial.
		   poly can be a number, a coefficient list or another univariate polynomial
		   
		   >>> p = UniVarPoly([0,1]) # x
		   >>> p.isub(1)
		   >>> p.coeffs
		   [-1, 1]
		   >>> p.isub([1,1])
		   >>> p.coeffs
		   [-2]
		   >>> p.isub(UniVarPoly([0,-1]))
		   >>> p.coeffs
		   [-2, 1]
		'''
		if isinstance(poly, numbers.Number):
			self.coeffs[0] -= poly
		elif isinstance(poly, list):
			self._isubCoeffs(poly)
		elif isinstance(poly, UniVarPoly):
			self._isubCoeffs(poly.coeffs)
		else:
			raise ValueError("unexpected argument type " + type(poly))


	def __add__(self, poly):
		'''overload operator +
		
		   >>> p1 = UniVarPoly([0,1,1])
		   >>> p2 = UniVarPoly([0,0,-1])
		   >>> p = p1 + 1 + [0,-1] + p2
		   >>> p.coeffs
		   [1]
		'''
		try:
			pSum = UniVarPoly(self.coeffs)
			pSum.iadd(poly)
			return pSum
		except ValueError:
			return NotImplemented # ValueError("unexpected argument type '%s'" % type(poly))



	def __iadd__(self, poly):
		'''overload operator +=
		
		   >>> p = UniVarPoly([0,1])
		   >>> p += 1
		   >>> p.coeffs
		   [1, 1]
		'''
		self.iadd(poly)
		return self


	def __radd__(self, poly):
		'''overload operator + for right hand side
		   >>> p = UniVarPoly([0,1])
		   >>> p = -1 + p
		   >>> p.coeffs
		   [-1, 1]
		'''
		return self.__add__(poly)


	def __sub__(self, poly):
		'''overload operator -
		
		   >>> p1 = UniVarPoly([0,1,1])
		   >>> p2 = UniVarPoly([1,0,1])
		   >>> p = p1 - p2
		   >>> p.coeffs
		   [-1, 1]
		'''
		try:
			pDiff = UniVarPoly(self.coeffs)
			pDiff.isub(poly)
			return pDiff
		except ValueError:
			return NotImplemented # ValueError("unexpected argument type '%s'" % type(poly))


	def __isub__(self, poly):
		'''overload operator -=
		
		   >>> p = UniVarPoly([0,1])
		   >>> p -= 1
		   >>> p.coeffs
		   [-1, 1]
		'''
		self.isub(poly)
		return self


	def __rsub__(self, poly):
		'''overload operator - for right hand side
		   >>> p = UniVarPoly([0,1])
		   >>> (1 - p).coeffs
		   [1, -1]
		'''
		p = UniVarPoly(poly)
		return p.__sub__(self)


	def scale(self, s):
		'''multiply each coefficient with given scale s
		
		   >>> p = UniVarPoly([2,1])
		   >>> p.scale(2)
		   >>> p.coeffs
		   [4, 2]
		'''
		for i in range(len(self.coeffs)):
			self.coeffs[i] *= s


	def scaled(self, s):
		'''return polynomial scaled by given scale s
		
		   >>> p1 = UniVarPoly([2,1])
		   >>> p2 = p1.scaled(2)
		   >>> p2.coeffs
		   [4, 2]
		'''
		polyScaled = UniVarPoly(self)
		polyScaled.scale(s)
		return polyScaled


	def _mulCoeffs(self, coeffs):
		coeffsMul = []
		for i in range(len(self.coeffs) + len(coeffs) - 1):
			ci = 0
			for j in range(i+1):
				if i-j >= len(coeffs): continue
				if j   >= len(self.coeffs): break
				ci += self.coeffs[j] * coeffs[i-j]
			coeffsMul.append(ci)
		return coeffsMul



	def __pos__(self):
		'''override unary operator +

		   >>> p = UniVarPoly([1,-1])
		   >>> (+p).coeffs
		   [1, -1]
		'''
		return self
		

	def __neg__(self):
		'''override unary operator -

		   >>> p = UniVarPoly([1,-1])
		   >>> (-p).coeffs
		   [-1, 1]
		'''
		return self.scaled(-1)

		
	def __mul__(self, poly):
		'''overload operator *
		
		   >>> p1 = UniVarPoly([0,1])
		   >>> p2 = UniVarPoly([1,1])
		   >>> p = p1 * p2
		   >>> p.coeffs
		   [0, 1, 1]
		'''
		if isinstance(poly, numbers.Number):
			return self.scaled(poly)
		if isinstance(poly, list):
			coeffs = poly
		elif isinstance(poly, UniVarPoly):
			coeffs = poly.coeffs
		else:
			return NotImplemented
		return UniVarPoly(self._mulCoeffs(coeffs))


	def imul(self, poly):
		'''multiply polynomial with coefficient, coefficient list or polynomial
		
		   >>> p = UniVarPoly([0,1])
		   >>> p.imul(2)
		   >>> p.coeffs
		   [0, 2]
		   >>> p.imul([1,1])
		   >>> p.coeffs
		   [0, 2, 2]
		   >>> p.imul(p)
		   >>> p.coeffs
		   [0, 0, 4, 8, 4]
		'''
		polyMul = self.__mul__(poly)
		self.coeffs = polyMul.coeffs

		
	def __imul__(self, poly):
		'''overload operator *=
		
		   >>> p = UniVarPoly([0,1])
		   >>> p *= 2
		   >>> p.coeffs
		   [0, 2]
		'''
		self.imul(poly)
		return self


	def __rmul__(self, poly):
		'''overload operator * for right hand side
		   >>> p1 = UniVarPoly([0,1])
		   >>> p2 = 2 * p1
		   >>> p2.coeffs
		   [0, 2]
		'''
		return self.__mul__(poly)


	def __truediv__(self, d):
		'''overload operator /
		   (divisor must be number, polynomial division not implemented)
		
		   >>> p1 = UniVarPoly([-1,2])
		   >>> p = p1 / 5
		   >>> p.coeffs
		   [-0.2, 0.4]
		'''
		if isinstance(d, numbers.Number):
			return self.scaled(1/d)
		else:
			return NotImplemented


	def __idiv__(self, d):
		'''overload operator /=
		   (divisor must be number, polynomial division not implemented)
		
		   >>> p = UniVarPoly([-1,1])
		   >>> p /= 2
		   >>> p.coeffs
		   [-0.5, 0.5]
		'''
		self.imul(1/d)
		return self


	def __pow__(self, e):
		'''overlaod operator ** (exponentiation)

		   >>> p = UniVarPoly([-1,1])
		   >>> p2 = p**2
		   >>> p2.coeffs
		   [1, -2, 1]
		   >>> p3 = p**3
		   >>> p3.coeffs
		   [-1, 3, -3, 1]
		'''
		res = UniVarPoly(1)
		p_2 = UniVarPoly(self)
		while (e>0):
			if e % 2: res *= p_2
			e >>= 1
			p_2 *= p_2
		return res
		

	def comp(self, poly):
		'''compute polynomial composition self o poly
		
		   >>> p1 = UniVarPoly([0,0,1])
		   >>> p2 = UniVarPoly([-1,1])
		   >>> p = p1.comp(p2)
		   >>> p.coeffs
		   [1, -2, 1]
		'''
		if isinstance(poly, numbers.Number):
			return self.eval(poly)
		poly_k = UniVarPoly(poly)
		polyComp = UniVarPoly([self.coeffs[0]])
		for k in range(1, len(self.coeffs)):
			if k > 1: poly_k *= poly
			polyComp += self.coeffs[k] * poly_k
			
		return polyComp


	def der(self):
		'''compute derivative of polynomial
		
		   >>> p = UniVarPoly([0, 0, 1])
		   >>> pd = p.der()
		   >>> pd.coeffs
		   [0, 2]
		'''
		# derivative of constant polynomial is the zero polynomial
		if len(self.coeffs) == 1: return UniVarPoly()
		
		coeffsDer = [(i+1)*c for i,c in enumerate(self.coeffs[1:])]
		return UniVarPoly(coeffsDer)


	def int(self, interval=None):
		'''compute indefinite or definite integral of polynomial
		
		   >>> p = UniVarPoly([0, 1])
		   >>> p.int().coeffs
		   [0, 0, 0.5]
		   >>> p.int([0,1])
		   0.5
		'''
		if interval is None:
			return self.intIndef()
		return self.intDef(interval)

		
	def intDef(self, interval):
		'''definite integral.

		   >>> p = UniVarPoly([0, 1])
		   >>> p.intDef([0,1])
		   0.5
		'''
		pIntIndef = self.intIndef()
		return pIntIndef.eval(interval[1]) - pIntIndef.eval(interval[0])


	def intIndef(self):
		'''indefinite integral

		   >>> p1 = UniVarPoly([0, 1])
		   >>> p1.intIndef().coeffs
		   [0, 0, 0.5]
		'''
		c0 = self.coeffs[0]
		coeffsInt = [c0-c0] # make new coefficient the same type as existing ones
		coeffsInt.append(c0) # special case: avoid division by 1 as it would change type 'int' to type 'float'
		for i in range(1, len(self.coeffs)):
			coeffsInt.append(self.coeffs[i]/(i+1))
		return UniVarPoly(coeffsInt)


	@staticmethod
	def _coeffRepr(c, prec=None, signedZero=False):
		'''minimal string representation of coefficient with given number of (max.) decimals.
		   Trailing zero decimals and a trailing decimal separator '.' are removed.
		   default precision: full precision
		   
		   >>> UniVarPoly._coeffRepr(1.0)
		   '1'
		   >>> UniVarPoly._coeffRepr(0.999)
		   '0.999'
		   >>> UniVarPoly._coeffRepr(0.999, 2)
		   '1'
		'''
		if isinstance(c, Fraction): return str(c)
		cFormat = '%f' if prec is None else ('%%.%df' % prec)
		cRepr = cFormat % c
		if '.' in cRepr:
			while cRepr[-1] == '0':
				cRepr = cRepr[:-1]
			if cRepr[-1] == '.':
				cRepr = cRepr[:-1]
		if cRepr == '-0': cRepr = '0'
		if signedZero and c != 0 and cRepr == '0':
			cRepr = '0.' if c > 0 else '-0.' # signal a non-zero number with small absolute value
		return cRepr

		
	def __str__(self, varName='x', parenthesizeCoeffs=False, coeffPrec=None, opMul='', opPow='^', termOrderAsc=False, termSep=' '):
		'''generate string representation of polymial

		   >>> str(UniVarPoly())
		   '0'
		   >>> str(UniVarPoly(-1)) 
		   '-1'
		   >>> str(UniVarPoly([0,1]))
		   'x'
		   >>> str(UniVarPoly([0,-1]))
		   '-x'
		   >>> str(UniVarPoly([0,2]))
		   '2x'
		   >>> str(UniVarPoly([1,2]))
		   '2x + 1'
		   >>> str(UniVarPoly([1,0,1]))
		   'x^2 + 1'
		   >>> str(UniVarPoly([-1,-1,-1]))
		   '-x^2 - x - 1'
		   >>> str(UniVarPoly([1.0]))
		   '1'
		   >>> str(UniVarPoly([0.0, -1.0]))
		   '-x'
		   >>> UniVarPoly([2,0,-2]).__str__(varName='y')
		   '-2y^2 + 2'
		   >>> UniVarPoly([2,0,-2]).__str__(parenthesizeCoeffs=True)
		   '(-2)x^2 + 2'
		   >>> UniVarPoly([0.0001,0.9999]).__str__(coeffPrec=3)
		   'x'
		   >>> UniVarPoly([2,2,-1]).__str__(opMul='*')
		   '-x^2 + 2*x + 2'
		   >>> UniVarPoly([2,0,-1]).__str__(opPow='**')
		   '-x**2 + 2'
		   >>> UniVarPoly([-1,0,-1]).__str__(termOrderAsc=True)
		   '-1 - x^2'
		   >>> UniVarPoly([2,0,-2]).__str__(termSep='')
		   '-2x^2+2'
		'''
		idxStart,idxEnd,idxIncr = (0,len(self.coeffs),1) if termOrderAsc else (len(self.coeffs)-1,-1,-1)
		strRepr = ''
		for i in range(idxStart, idxEnd, idxIncr):
			ci = self.coeffs[i]
			isHighestPower = i == self.deg()
			ciRepr = UniVarPoly._coeffRepr(ci, coeffPrec, signedZero=isHighestPower)
			if ciRepr == '0': continue
			coeffShown = False
			if strRepr:
				extractMinus = not parenthesizeCoeffs and isinstance(ci, numbers.Real) and ciRepr[0] == '-'
				if extractMinus: ciRepr = ciRepr[1:]
				termComb = '-' if extractMinus else '+'
				strRepr += '%s%s%s' % (termSep, termComb, termSep)
				if ciRepr != '1' or i == 0:
					if parenthesizeCoeffs and (not isinstance(ci, numbers.Real) or ci < 0):
						strRepr += '(%s)' % ciRepr
					else:
						strRepr += ciRepr
					coeffShown = True
			else:
				if ciRepr != '1' or i == 0:
					if parenthesizeCoeffs and ciRepr != '1':
						strRepr = '(%s)' % ciRepr
						coeffShown = True
					elif ciRepr == '-1' and i>0:
						strRepr = '-'
					elif ciRepr == '1' and i>0:
						strRepr = ''
					else:
						strRepr = ciRepr
						coeffShown = True
			if i>0:
				if coeffShown: strRepr += opMul;
				strRepr += '%s' % varName
				if i>1:
					strRepr += '%s%d' % (opPow, i)
		return strRepr if strRepr else '0'


	def __repr__(self):
		return "<poly '" + str(self) + "'>"


	def _eqCoeffs(self, coeffs, eps):
		if len(self.coeffs) != len(coeffs): return False
		for i,c in enumerate(self.coeffs):
			if abs(c-coeffs[i]) > eps: return False
		return True


	def __eq__(self, poly, eps=1e-10):
		if isinstance(poly, numbers.Number):
			return len(self.coeffs) == 1 and abs(self.coeffs[0] - poly) < eps
		if isinstance(poly, list):
			coeffs = poly
		elif isinstance(poly, UniVarPoly):
			coeffs = poly.coeffs
		else:
			raise ValueError("unexpected argument type " + type(poly))
		return self._eqCoeffs(coeffs, eps)


# predefined polynomials
p_0  = UniVarPoly()
p_1  = UniVarPoly(1)
p_x  = UniVarPoly([0,1])
p_x2 = UniVarPoly([0,0,1])
p_x3 = UniVarPoly([0,0,0,1])


if __name__ == "__main__":
	import doctest
	doctest.testmod()

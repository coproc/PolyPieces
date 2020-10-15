'''Basic arithmetic for univariate polynomials encoded as list of coefficients
'''
from __future__ import division
import copy
from fractions import Fraction
import numbers
import re


class UniVarPoly:
	def __init__(self, repr=0, varName='x'):
		'''create univariate polynomial.

		   A polynomial can be constructed from its list of coefficients.
		   The coefficients must be given in ascending order.
		   If a single number is given instead of a list the corresponding constant
		   polynomial is constructed.
		   If a polynomial is given its coefficents are (deeply) copied.
		   If a string is given it is evaluated as Python expression in the given
		   variable (default: 'x').
		   If no input is given the 0 polynomial is assumed.
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
		self.varName = varName
		if isinstance(repr, UniVarPoly):
			self.coeffs = copy.deepcopy(repr.coeffs)
			self.varName = repr.varName
		elif isinstance(repr, numbers.Number):
			self.coeffs = [repr]
		elif isinstance(repr, str):
			p = UniVarPoly.fromString(repr, varName)
			self.coeffs = p.coeffs
		else:
			try:
				iter(repr)
				self.coeffs = list(copy.deepcopy(repr))
				if len(self.coeffs) == 0: self.coeffs.append(0)
				self._normalize()
			except TypeError:
				raise TypeError('unexpected type "%s" when constructing polynomial' % type(coeffs))
			

	@staticmethod
	def fromString(exprStr, varNames=None):
		'''create univariate polynomial from expression string
		
		   >>> p = poly('(y-1)**3')
		   >>> p.coeffs
		   [-1, 3, -3, 1]
		   >>> p.varName
		   'y'
		   >>> poly('x^2')
		   <UniVarPoly 'x^2'>
		   >>> poly('2xy')
		   <UniVarPoly '2xy'>
		   >>> poly('(x+y)(x-y)')
		   <UniVarPoly '-y^2 + x^2'>
		   >>> poly('x-1/2')
		   <UniVarPoly 'x - 1/2'>
		'''
		if varNames is None:
			varNames = set(re.findall('[a-zA-Z][0-9]*', exprStr))
		exprStr = exprStr.replace('^', '**')
		for _ in range(2): # regular expressions for implicit multiplication may overlap
			exprStr = re.sub(r'([a-zA-Z0-9)])[ \t]*([(a-zA-Z])', r'\1*\2', exprStr)
		# assume exact arithmetic: division of integers is taken as Fraction;
		exprStr = re.sub(r'([1-9][0-9]*)\s*/\s*([1-9][0-9]*)', r'Fraction(\1,\2)', exprStr)
		return eval(exprStr, None, {v: symbol(v) for v in varNames})


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


	# removing leading zero coefficents
	def _normalize(self):
		while len(self.coeffs) > 1 and self.coeffs[-1] == 0:
			self.coeffs = self.coeffs[:-1]
		for idx,c in enumerate(self.coeffs):
			if isinstance(c, UniVarPoly):
				c._normalize()
				if c == 0:
					self.coeffs[idx] = 0
		if len(self.coeffs) == 1 and isinstance(self.coeffs[0], UniVarPoly):
			self.varName = self.coeffs[0].varName
			self.coeffs = self.coeffs[0].coeffs


	def _iaddCoeffs(self, coeffs):
		for i in range(min(len(self.coeffs), len(coeffs))):
			self.coeffs[i] += coeffs[i]
		if len(coeffs) > len(self.coeffs):
			self.coeffs += coeffs[len(self.coeffs):]
		self._normalize()


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
			if self.varName == poly.varName:
				self._iaddCoeffs(poly.coeffs)
			elif self.varName > poly.varName:
				self.coeffs[0] += poly
				self._normalize()
			else:
				tmp = UniVarPoly(self)
				self.coeffs = copy.deepcopy(poly.coeffs)
				self.varName = poly.varName
				self.coeffs[0] += tmp			
				self._normalize()
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
			if self.varName == poly.varName:
				self._isubCoeffs(poly.coeffs)
			elif self.varName > poly.varName:
				self.coeffs[0] -= poly
				self._normalize()
			else:
				tmp = UniVarPoly(self)
				self.coeffs = copy.deepcopy(poly.coeffs)
				self.varName = poly.varName
				self.scale(-1)
				self.coeffs[0] += tmp				
				self._normalize()
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
			pSum = UniVarPoly(self)
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
			pDiff = UniVarPoly(self.coeffs, varName=self.varName)
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
		p = UniVarPoly(poly, varName=self.varName)
		return p.__sub__(self)


	def scale(self, s):
		'''multiply each coefficient with given scale s
		
		   >>> p = UniVarPoly([2,1])
		   >>> p.scale(2)
		   >>> p.coeffs
		   [4, 2]
		   >>> p.scale(0)
		   >>> p.coeffs
		   [0]
		'''
		if s == 0:
			self.coeffs = [0]
		for i in range(len(self.coeffs)):
			self.coeffs[i] *= s


	def scaled(self, s):
		'''return polynomial scaled by given scale s
		
		   >>> p1 = UniVarPoly([2,1])
		   >>> p2 = p1.scaled(2)
		   >>> p2.coeffs
		   [4, 2]
		   >>> p3 = p1.scaled(0)
		   >>> p3.coeffs
		   [0]
		'''
		if s == 0:
			return UniVarPoly(0, varName=self.varName)
		polyScaled = UniVarPoly(self)
		polyScaled.scale(s)
		return polyScaled


	def _mulCoeffs(self, coeffs):
		if self.coeffs == [0] or coeffs == [0]:
			return [0]
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
		   >>> p0 = p1 * UniVarPoly(0)
		   >>> p0.coeffs
		   [0]
		'''
		if isinstance(poly, numbers.Number):
			return self.scaled(poly)
		if isinstance(poly, list):
			coeffs = poly
		elif isinstance(poly, UniVarPoly):
			if self.varName == poly.varName:
				coeffs = poly.coeffs
			elif self.varName > poly.varName:
				return self.scaled(poly)
			else:
				return poly.scaled(self)
		else:
			return NotImplemented
		return UniVarPoly(self._mulCoeffs(coeffs), varName=self.varName)


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
		self.varName = polyMul.varName

		
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


	def _termQuot(self, div):
		if isinstance(div, numbers.Number):
			return self/div
		assert isinstance(div, UniVarPoly), "internal error: unexpected div type %s" % type(div)
		if div.deg() == 0:
			assert isinstance(div.coeffs[0], numbers.Number), "internal error: unexpected div poly '%s' of var '%s'" % (div.coeffs[0], div.varName)
			return self/div.coeffs[0]
		if div.varName > self.varName:
			raise ValueError("cannot divide '%s' by '%s'" % (self, div))
		deg1 = self.deg()
		deg2,div_rec = (div.deg(),div.coeffs[-1]) if div.varName == self.varName else (0,div)
		for exp in range(deg1,deg2-1,-1):
			ci = self.coeffs[exp]
			if isinstance(ci, UniVarPoly):
				return UniVarPoly((exp-deg2)*[0] + [ci._termQuot(div_rec)], self.varName)
			assert isinstance(ci, numbers.Number), "internal error: unexpected coefficient %s (type %s)" % (ci, type(ci))
			if isinstance(div_rec, numbers.Number):
				if isinstance(ci, int): ci = Fraction(ci)
				return UniVarPoly((exp-deg2)*[0] + [ci/div_rec], self.varName)
		raise ValueError("cannot divide '%s' by '%s'" % (self, div))


	def __truediv__(self, d):
		'''overload operators /, /=
		
		   >>> p1 = UniVarPoly('2x-1')
		   >>> p = p1 / 5
		   >>> p.coeffs
		   [Fraction(-1, 5), Fraction(2, 5)]
		   >>> p /= 2
		   >>> p.coeffs
		   [Fraction(-1, 10), Fraction(1, 5)]
		   >>> q,r = poly('x^3-1') / poly('x-1'); print(f'{q}, {r}')
		   x^2 + x + 1, 0
		   >>> q,r = poly('x^3-1') / poly('x+1'); print(f'{q}, {r}')
		   x^2 - x + 1, -2
		   >>> q,r = poly('xy') / poly('2x'); print(f'{q}, {r}')
		   1/2y, 0
		'''
		if isinstance(d, numbers.Number):
			try:
				scaleFac = Fraction(1, d)
			except TypeError:
				scaleFac = 1/d
			return self.scaled(scaleFac)
		if not isinstance(d, UniVarPoly):
			raise TypeError("divisor of invalid type %s" % type(d))
		quot,rem = 0,UniVarPoly(self)
		try:
			while True:
				q = rem._termQuot(d)
				quot += q
				rem -= q*d
		except ValueError:
			pass
		return quot,rem


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
		res = UniVarPoly(1, varName=self.varName)
		p_2 = UniVarPoly(self, varName=self.varName)
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
		polyComp = UniVarPoly([self.coeffs[0]], varName=poly_k.varName)
		for k in range(1, len(self.coeffs)):
			if k > 1: poly_k *= poly
			polyComp += self.coeffs[k] * poly_k

		polyComp._normalize()
		return polyComp

	def __call__(self, poly):
		'''overload call operator (composition/substitution/evaluation)
		
		   >>> p1 = UniVarPoly('x**2+x-1')
		   >>> p1(0)
		   -1
		   >>> p2 = UniVarPoly('1-x')
		   >>> p1(p2).coeffs
		   [1, -3, 1]
		   >>> p1(p2)(p2).coeffs
		   [-1, 1, 1]
		'''
		return self.comp(poly)


	def der(self):
		'''compute derivative of polynomial
		
		   >>> p = UniVarPoly([0, 0, 1])
		   >>> pd = p.der()
		   >>> pd.coeffs
		   [0, 2]
		'''
		# derivative of constant polynomial is the zero polynomial
		if len(self.coeffs) == 1: return UniVarPoly(varName=self.varName)
		
		coeffsDer = [(i+1)*c for i,c in enumerate(self.coeffs[1:])]
		return UniVarPoly(coeffsDer, varName=self.varName)


	def int(self, interval=None):
		'''compute indefinite or definite integral of polynomial
		
		   >>> p = UniVarPoly([0, 1])
		   >>> p.int().coeffs
		   [0, 0, Fraction(1, 2)]
		   >>> p.int([0,1])
		   Fraction(1, 2)
		'''
		if interval is None:
			return self.intIndef()
		return self.intDef(interval)

		
	def intDef(self, interval):
		'''definite integral.

		   >>> p = UniVarPoly([0, 1])
		   >>> p.intDef([0,1])
		   Fraction(1, 2)
		'''
		pIntIndef = self.intIndef()
		return pIntIndef.eval(interval[1]) - pIntIndef.eval(interval[0])


	def intIndef(self):
		'''indefinite integral

		   >>> p1 = UniVarPoly([1, 1])
		   >>> p1.intIndef().coeffs
		   [0, 1, Fraction(1, 2)]
		'''
		c0 = self.coeffs[0]
		# make new coefficient (0) the same type as existing ones
		# save division by 1
		coeffsInt = [c0-c0, c0] + [self.coeffs[i]*Fraction(1,i+1) for i in range(1, len(self.coeffs))]
		return UniVarPoly(coeffsInt, varName=self.varName)


	@staticmethod
	def _coeffRepr(c, prec=None, signedZero=False, parenthesizeCoeffs=False, opMul='', opPow='^', termOrderAsc=False, termSep=' '):
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
		if isinstance(c, UniVarPoly): return c.format(parenthesizeCoeffs=parenthesizeCoeffs, coeffPrec=prec, opMul=opMul, opPow=opPow, termOrderAsc=termOrderAsc, termSep=termSep)
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


	def format(self, parenthesizeCoeffs=False, coeffPrec=None, opMul='', opPow='^', termOrderAsc=False, termSep=' '):
		'''generate string representation of polynomial

		   >>> UniVarPoly().format()
		   '0'
		   >>> UniVarPoly(-1).format()
		   '-1'
		   >>> UniVarPoly([0,1]).format()
		   'x'
		   >>> UniVarPoly([0,-1]).format()
		   '-x'
		   >>> UniVarPoly([0,2]).format()
		   '2x'
		   >>> UniVarPoly([1,2]).format()
		   '2x + 1'
		   >>> UniVarPoly([1,0,1]).format()
		   'x^2 + 1'
		   >>> UniVarPoly([-1,-1,-1]).format()
		   '-x^2 - x - 1'
		   >>> UniVarPoly([1.0]).format()
		   '1'
		   >>> UniVarPoly([0.0, -1.0]).format()
		   '-x'
		   >>> UniVarPoly([2,0,-2], 'y').format()
		   '-2y^2 + 2'
		   >>> UniVarPoly([2,0,-2]).format(parenthesizeCoeffs=True)
		   '(-2)x^2 + 2'
		   >>> UniVarPoly([0.0001,0.9999]).format(coeffPrec=3)
		   'x'
		   >>> UniVarPoly([2,2,-1]).format(opMul='*')
		   '-x^2 + 2*x + 2'
		   >>> UniVarPoly([2,0,-1]).format(opPow='**')
		   '-x**2 + 2'
		   >>> UniVarPoly([-1,0,-1]).format(termOrderAsc=True)
		   '-1 - x^2'
		   >>> UniVarPoly([2,0,-2]).format(termSep='')
		   '-2x^2+2'
		'''
		idxStart,idxEnd,idxIncr = (0,len(self.coeffs),1) if termOrderAsc else (len(self.coeffs)-1,-1,-1)
		strRepr = ''
		for i in range(idxStart, idxEnd, idxIncr):
			ci = self.coeffs[i]
			isHighestPower = i == self.deg()
			ciRepr = UniVarPoly._coeffRepr(ci, coeffPrec, signedZero=isHighestPower, parenthesizeCoeffs=parenthesizeCoeffs, opMul=opMul, opPow=opPow, termOrderAsc=termOrderAsc, termSep=termSep)
			if ciRepr == '0': continue
			coeffShown = False
			if strRepr:
				extractMinus = not parenthesizeCoeffs and isinstance(ci, numbers.Real) and ciRepr[0] == '-'
				if extractMinus: ciRepr = ciRepr[1:]
				termComb = '-' if extractMinus else '+'
				strRepr += '%s%s%s' % (termSep, termComb, termSep)
				if ciRepr != '1' or i == 0:
					if (parenthesizeCoeffs and (not isinstance(ci, numbers.Real) or ci < 0)) or (isinstance(ci, UniVarPoly) and ('+' in ciRepr or '-' in ciRepr) and (i>0 or ciRepr.startswith('-'))):
						strRepr += '(%s)' % ciRepr
					else:
						strRepr += ciRepr
					coeffShown = True
			else:
				if ciRepr != '1' or i == 0:
					if (parenthesizeCoeffs and ciRepr != '1') or (isinstance(ci, UniVarPoly) and ('+' in ciRepr or '-' in ciRepr) and i > 0):
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
				strRepr += '%s' % self.varName
				if i>1:
					strRepr += '%s%d' % (opPow, i)
		return strRepr if strRepr else '0'


	def __str__(self):
		'''overload conversion to string
		
		   >>> str(UniVarPoly([-1, 1]))
		   'x - 1'
		'''
		return self.format(parenthesizeCoeffs=False, coeffPrec=None, opMul='', opPow='^', termOrderAsc=False, termSep=' ')


	def __repr__(self):
		return "<UniVarPoly '%s'>" % self


	@staticmethod
	def _eqCoeffs(coeffs1, coeffs2, eps):
		if len(coeffs1) != len(coeffs2): return False
		for c1,c2 in zip(coeffs1, coeffs2):
			if isinstance(c1, numbers.Number):
				if isinstance(c2, numbers.Number):
					if eps is None and (isinstance(c1, float) or isinstance(c2, float)):
						eps = 1e-10
					ceq = c1 == c2 if eps is None or eps == 0 else abs(c1 - c2) < eps
					if not ceq: return False
				elif isinstance(c2, UniVarPoly):
					if not c2.__eq__(c1, eps): return False
				else:
					raise ValueError("_eqCoeffs: unexpected coefficient type " + type(c2))
			elif isinstance(c1, UniVarPoly):
				if not c1.__eq__(c2, eps): return False
			else:
				raise ValueError("_eqCoeffs: unexpected coefficient type " + type(c1))
		return True


	def __eq__(self, poly, eps=None):
		'''overload operator ==
		unset eps defaults to 1e-10 if floats are involved, exact comparison otherwise
		
		>>> UniVarPoly(0) == 0
		True
		>>> UniVarPoly(1) == 1
		True
		>>> UniVarPoly('x') == 0
		False
		>>> UniVarPoly('x') == symbol('x')
		True
		>>> symbol('x') == symbol('y')
		False
		'''
		if isinstance(poly, numbers.Number):
			return UniVarPoly._eqCoeffs(self.coeffs, [poly], eps)
		if isinstance(poly, list):
			coeffs = poly
		elif isinstance(poly, UniVarPoly):
			if self.varName != poly.varName and max(len(self.coeffs), len(poly.coeffs)) > 1:
				return False
			coeffs = poly.coeffs
		else:
			raise ValueError("__eq__: unexpected argument type " + type(poly))
		return UniVarPoly._eqCoeffs(self.coeffs, coeffs, eps)


# create identity polynomials for given variable name (e.g. polynomial x for variable name 'x')
def symbol(varName='x'):
	'''generate simplest polynomials given a variable name
	
	>>> symbol()
	<UniVarPoly 'x'>
	>>> symbol('y')
	<UniVarPoly 'y'>
	'''
	return UniVarPoly([0,1], varName=varName.strip())

def symbols(varNames):
	'''generate several symbols in one call
	
	>>> x,y = symbols('x,y')
	>>> x+y
	<UniVarPoly 'y + x'>
	'''
	return [symbol(v) for v in re.split('[, \t]+', varNames)]


def poly(polyStr):
	'''generate polynomial from string
	
	>>> poly('x')
	<UniVarPoly 'x'>
	>>> poly('(x+y)^2')
	<UniVarPoly 'y^2 + 2xy + x^2'>
	'''
	return UniVarPoly.fromString(polyStr)


def _selfTest():
	import doctest
	print('running doc tests ...')
	doctest.testmod()

if __name__ == "__main__":
	_selfTest()

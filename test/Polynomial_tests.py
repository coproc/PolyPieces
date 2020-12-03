import unittest

from src.Polynomial import Polynomial as Poly

TEST_CASES_CREATION = [
	('1',	([1], 'x')),
	(('1',['y']),	([1], 'y')),
	('x',	([0, 1], 'x')),
	('y',	([0, 1], 'y')),
	('1-x',	([1, -1], 'x')),
	('1-y',	([1, -1], 'y')),
	('1-xy',	([1, ([0, -1], 'x')], 'y')),
	(('1-xy',['xy']),	([1, -1], 'xy')),
	('(1-x)(1-y)',	([([1, -1], 'x'), ([-1, 1], 'x')], 'y')),
	('(x+y+z)^2',	([([([0,0,1], 'x'), ([0,2], 'x'), 1], 'y'), ([([0,2], 'x'), 2], 'y'), 1], 'z'))
]

TEST_CASES_NULLARY = {
	Poly.deg: [
		(-1, []),
		(-1, [0]),
		( 0, [1]),
		( 1, [-1,2]),
		( 2, [0,0,-1])
	],
	Poly._normalize: [
		# univariate polys
		([],	[]),
		([],	[0]),
		([1],	[1,0]),
		([0,-1],	[0,-1,0,0]),
		# multivariate polys: remove zero leading terms in all layers
		(([0, ([0,2], 'x')], 'y'), '(x^2+2xy+y^2)-x^2-y^2'), # = 2xy
		# multivariate polys: remove (layers with) variables with only constant terms
		(([([0,1], 'x'), 1], 'z'), '(x+y+z) - y') # = x + z
	],
	Poly.der: [
		# univariate polys
		([],	[]),
		([],	[0]),
		([],	[1]),
		([1],	[0,1]),
		([0,2],	[0,0,1]),
		# multivariate polys
		(([0, ([0,2], 'y')], 'z'), '1+yz^2') # d(1+yz^2)/dz = 2yz
	],
	Poly.intIndef: [
		# univariate polys
		([],	[]),
		([],	[0]),
		([0,1],	[1]),
		([0,0,1],	[0,2]),
		# multivariate polys
		(([0, 1, ([0,1], 'y')], 'z'), '1+2yz') # int(1+2yz)dz = z+yz^2
	]
}


TEST_CASES_UNARY = {
	Poly.deg: [
		(1,	('x', 'x')),
		(0,	('x', 'y')),
		(0,	('y', 'x'))
	],
	Poly.eval: [
		(0,	('x', 0)),
		(1,	('x', 1)),
		(-1,	('x', -1)),
		(1,	('x^2', -1)),
		(0,	('x^2+x', -1)),
		([0,1],	('x+y', 0)),
		([2,1],	('x+y', 2)),
	],
	Poly.comp: [
		(([], 'x'),	('x+y', {'x':0, 'y':0})),
		(([5], 'y'),	('x+y', {'x':2, 'y':3})),
		(([0,3], 'x'),	('x+y', {'y': Poly.fromString('2x')})), # 3x = (x+y)|(y=2x)
	],
	Poly.der: [
		([1],	('x', 'x')),
		(([], 'y'),	('x', 'y')),
		([],	('y', 'x'))
	],
	Poly.intIndef: [
		([0,1],	('1', 'x')),
		(([0,1], 'y'),	('1', 'y')),
		(([0, ([0,1], 'x')], 'y'),	('y', 'x')),
		(([0, ([0,1], 'x')], 'y'),	('x', 'y')),
		(([0, ([0,0,1], 'x')], 'y'),	('2xy', 'x')), # int(2xy)dx = x^2y
		(([0, 0, ([0,1], 'x')], 'y'),	('2xy', 'y')), # int(2xy)dy = xy^2
	]
}


TEST_CASES_BINARY = {
	Poly.iadd: [
		([1,0,1],	('x-1', 'x^2-x+2')), # x^2+1 = (x-1) + (x^2-x+2)
		(([([0,1], 'x'), 1],'y'),	('x', 'y')),
	],
	Poly.isub: [
		([-3,2,-1],	('x-1', 'x^2-x+2')), # -x^2+2x-3 = (x-1) - (x^2-x+2)
		(([([0,1], 'x'), -1],'y'),	('x', 'y')),
	],
	Poly.imul: [
		([],	('x', '0')),
		([],	('0', 'x')),
		([-1,0,1],	('x-1', 'x+1')),
		(([0, ([0,1], 'x')],'y'),	('x', 'y')),
	],
	Poly.comp: [
		([],	('0', 'x')),
		([],	('x', '0')),
		(([0,1], 'x'),	('y', 'x')),
		(([0,1], 'y'),	('x', 'y')),
		([-1,3,-3,1],	('x^3', 'x-1')),
	]
}

def _createPoly(repr):
	if isinstance(repr, Poly): return repr
	if isinstance(repr, str): return Poly.fromString(repr)
	if isinstance(repr, tuple): return Poly(*repr) if isinstance(repr[0], list) else Poly.fromString(*repr)
	if isinstance(repr, list): return Poly(repr)
	raise TypeError('cannot create polynomial from type %s (%s)' % (type(repr), repr))


class PolynomialTests(unittest.TestCase):

	def _assertPolyStruct(self, polyStruct, p, depthPath=None, rootStruct=None, rootPoly=None):
		if depthPath	is None: depthPath = []
		if rootStruct	is None: rootStruct = polyStruct
		if rootPoly	is None: rootPoly = p
		whileMsg = (' while checking coeff %s of %s ~ %s' % 
				(' of coeff '.join([str(d) for d in depthPath]), rootStruct, rootPoly))\
			if depthPath else ''
		coeffsExp,varNameExp = polyStruct
		self.assertEqual(varNameExp, p.varName,
			'testing variable in %s ~ %s%s' % (polyStruct, p, whileMsg))
		self.assertEqual(len(coeffsExp), len(p.coeffs) if p.coeffs != [0] else 0,
			'testing coeff count in %s ~ %s%s' % (polyStruct, p, whileMsg))
		for idx,(cExp,cPoly) in enumerate(zip(coeffsExp, p.coeffs)):
			if isinstance(cExp, tuple) and isinstance(cPoly, Poly):
				self._assertPolyStruct(cExp, cPoly, [idx]+depthPath, rootStruct, rootPoly)
			else:
				self.assertEqual(cExp, cPoly,
					'testing coeff %d in %s ~ %s%s' % (idx, polyStruct, p, whileMsg))
		
	def test_creation(self):
		print('testing Polynomial creation: ', end='')
		for expr, polyStruct in TEST_CASES_CREATION:
			try:
				p = _createPoly(expr)
				self._assertPolyStruct(polyStruct, p)
				print('.', end='')
			except AssertionError:
				print('F\n', end='')
				raise
			except:
				print('E\n', end='')
				raise
		print()


	def test_nullaryMethods(self):
		for func,inOutData in TEST_CASES_NULLARY.items():
			print('testing Polynomial.%s (nullary): ' % func.__name__, end='')
			for resultExp,polyRepr in inOutData:
				try:
					p = _createPoly(polyRepr)
					f_p = func(p)
					# if there is no return value, method has changed polynomial
					result = p if f_p is None else f_p
					if isinstance(result, Poly):
						if isinstance(resultExp, list): resultExp = (resultExp, 'x')
						self._assertPolyStruct(resultExp, result)
					else:
						self.assertEqual(resultExp, result, 'testing %s = %s.%s()' % (resultExp, p, func.__name__))
					print('.', end='')
				except AssertionError:
					print('F\n', end='')
					raise
				except:
					print('E\n', end='')
					raise
			print()


	def test_unaryMethods(self):
		for func,inOutData in TEST_CASES_UNARY.items():
			print('testing Polynomial.%s (unary): ' % func.__name__, end='')
			for resultExp,(polyRepr,arg) in inOutData:
				try:
					p = _createPoly(polyRepr)
					f_p = func(p, arg)
					# if there is no return value, method has changed polynomial
					result = p if f_p is None else f_p
					if isinstance(result, Poly):
						if isinstance(resultExp, list): resultExp = (resultExp, 'x')
						self._assertPolyStruct(resultExp, result)
					else:
						self.assertEqual(resultExp, result, 'testing %s = %s.%s(%s)' % (resultExp, p, func.__name__, arg))
					print('.', end='')
				except AssertionError:
					print('F\n', end='')
					raise
				except:
					print('E\n', end='')
					raise
			print()

	def test_binaryMethods(self):
		for func,inOutData in TEST_CASES_BINARY.items():
			print('testing Polynomial.%s (binary): ' % func.__name__, end='')
			for resultExp,(polyRepr,argPolyRepr) in inOutData:
				try:
					p = _createPoly(polyRepr)
					pa = _createPoly(argPolyRepr)
					f_p = func(p, pa)
					# if there is no return value, method has changed polynomial
					result = p if f_p is None else f_p
					if isinstance(result, Poly):
						if isinstance(resultExp, list): resultExp = (resultExp, 'x')
						self._assertPolyStruct(resultExp, result)
					else:
						self.assertEqual(resultExp, result, 'testing %s = %s.%s(%s)' % (resultExp, p, func.__name__, pa))
					print('.', end='')
				except AssertionError:
					print('F\n', end='')
					raise
				except:
					print('E\n', end='')
					raise
			print()

#	def test_special(self):
#		print('testing special: ', end='')
#		p = _createPoly('y')
#		result = p.der('x')
#		print(result)
#		self._assertPolyStruct(([],'x'), result)
#		print()

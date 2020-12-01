import unittest

from src.Polynomial import Polynomial as Poly

TEST_CASES_CREATION = [
	('1', ([1], 'x')),
	(('1', ['y']), ([1], 'y')),
	('x', ([0, 1], 'x')),
	('y', ([0, 1], 'y')),
	('1-x', ([1, -1], 'x')),
	('1-y', ([1, -1], 'y')),
	('1-xy', ([1, ([0, -1], 'x')], 'y')),
	(('1-xy', ['xy']), ([1, -1], 'xy')),
	('(1-x)(1-y)', ([([1, -1], 'x'), ([-1, 1], 'x')], 'y'))
]
	

class MultivarTests(unittest.TestCase):

	def assertPolyStruct(self, polyStruct, p, depthPath=None, rootStruct=None, rootPoly=None):
		if depthPath	is None: depthPath = []
		if rootStruct	is None: rootStruct = polyStruct
		if rootPoly	is None: rootPoly = p
		whileMsg = ('while checking coeff %s of %s ~ %s' % 
				(' of coeff '.join([str(d) for d in depthPath]), rootStruct, rootPoly))\
			if depthPath else ''
		coeffsExp,varNameExp = polyStruct
		self.assertEqual(varNameExp, p.varName,
			'testing variable in %s ~ %s%s' % (polyStruct, p, whileMsg))
		for idx,(cExp,cPoly) in enumerate(zip(coeffsExp, p.coeffs)):
			if isinstance(cExp, tuple) and isinstance(cPoly, Poly):
				self.assertPolyStruct(cExp, cPoly, [idx]+depthPath, rootStruct, rootPoly)
			else:
				self.assertEqual(cExp, cPoly,
					'testing coeff %d in %s ~ %s%s' % (idx, polyStruct, p, whileMsg))
		
	def test_creation(self):
		print('testing creation: ', end='')
		for expr, polyStruct in TEST_CASES_CREATION:
			try:
				p = Poly.fromString(expr) if isinstance(expr, str) else Poly.fromString(*expr)
				self.assertPolyStruct(polyStruct, p)
				print('.', end='')
			except AssertionError:
				print('F\n', end='')
				raise
			except:
				print('E\n', end='')
				raise
		print()

from numpy import array as na, array_equal as na_eq
import unittest

from src import univar_polyops as upo

TEST_CASES_UNARY = {
	upo.degree: [
		(-1, []),
		(-1, [0]),
		( 0, [1]),
		( 1, [1,1]),
		( 2, [0,0,-1])
	],
	upo.normalize: [
		([],	[]),
		([],	[0]),
		([1],	[1,0]),
		([0,-1],	[0,-1,0,0])
	]
}

TEST_CASES_BINARY = {
	upo.evaluate: [
		( 0, ([], 1)),
		(-1, ([-1], 0)),
		( 2, ([0,1], 2)),
		( 4, ([0,0,1], 2)), #  4 = 1*2^2
		(11, ([3,-2,1], 4)) # 11 = 1*4^2 - 2*4^1 + 3
	],
	upo.add: [
		([],	([], [])),
		([],	([], [0])),
		([5,7,3],	([1,2,3], [4,5])), # 3x^2 + 7x + 5 = (3x^2 + 2x + 1) + (5x + 4)
		([2],	([1,1], [1,-1]))
	],
	upo.subtract: [
		([],	([], [])),
		([-1],	([], [1])),
		([-3,-3, 3],	([1,2,3], [4,5])), #  3x^2 - 3x - 3 = (3x^2 + 2x + 1) - (5x + 4)
		([ 3, 3,-3],	([4,5], [1,2,3])), # -3x^2 + 3x + 3 = (5x + 4) - (3x^2 + 2x + 1)
		([2],	([1,1], [-1,1]))
	],
	upo.multiply: [
		([], ([], [])),
		([], ([], [1])),
		([6], ([2], [3])),
		([3,6], ([1,2], [3])),
		([3,6], ([3], [1,2])),
		([-1,0,1], ([1,1], [-1,1])),     # x^2 - 1 = (x + 1)*(x - 1)
		([-1,0,0,1], ([-1,1], [1,1,1])), # x^3 - 1 = (x - 1)*(x^2 + x + 1)
		([-1,3,0,-3,-5,6], ([1,-3,2], [-1,0,2,3])) # 6x^5 - 5x^4 - 3x^3 + 3x - 1 = (2x^2 - 3x + 1)*(3x^3 + 2x^2 - 1)
	],
	upo.scale: [
		([],	(0, [])),
		([],	(0, [1])),
		([2,1],	(1, [2,1])),
		([1,-1],	(-1, [-1,1])),
		([4,2,6],	(2, [2,1,3]))
	]
}

class Univar_PolyOps(unittest.TestCase):

	def test_unaryFunctions(self):
		for func,inOutData in TEST_CASES_UNARY.items():
			print('testing %s: ' % func.__name__, end='')
			for output,input in inOutData:
				self.assertEqual(output, func(input), 'testing %s = %s(%s)' % (output,func.__name__,input))
				print('.', end='')
			print()

	def test_binaryFunctions(self):
		for func,inOutData in TEST_CASES_BINARY.items():
			print('testing %s: ' % func.__name__, end='')
			for output,input in inOutData:
				self.assertEqual(output, func(*input), 'testing %s = %s(%s, %s)' % (output,func.__name__,*input))
				print('.', end='')
			print()


# feed numpy array into functions and compare results with numpy arrays
# (currently not very useful since the poly operations are not aware of numpy)
class Univar_PolyOps_numpy(unittest.TestCase):

	def test_unaryFunctions(self):
		for func,inOutData in TEST_CASES_UNARY.items():
			print('testing %s with numpy: ' % func.__name__, end='')
			for output,input in inOutData:
				self.assertTrue(na_eq(na(output), func(na(input))), 'testing %s = %s(%s)' % (output,func.__name__,input))
				print('.', end='')
			print()

	def test_binaryFunctions(self):
		for func,inOutData in TEST_CASES_BINARY.items():
			print('testing %s with numpy: ' % func.__name__, end='')
			for output,input in inOutData:
				self.assertTrue(na_eq(na(output), func(*list(map(na,input)))), 'testing %s = %s(%s, %s)' % (output,func.__name__,*input))
				print('.', end='')
			print()


import unittest

from src import univar_polyops as upo

class Univar_PolyOps(unittest.TestCase):

	def test_degree(self):
		self.assertEqual(-1, upo.degree([]))
		self.assertEqual(-1, upo.degree([0]))
		self.assertEqual( 0, upo.degree([1]))
		self.assertEqual( 1, upo.degree([1,1]))
		self.assertEqual( 2, upo.degree([0,0,-1]))

	def test_normalize(self):
		self.assertEqual([], upo.normalize([]))
		self.assertEqual([], upo.normalize([0]))
		self.assertEqual([1], upo.normalize([1,0]))
		self.assertEqual([0,-1], upo.normalize([0,-1,0,0]))
		
	def test_evaluate(self):
		self.assertEqual( 0, upo.evaluate([], 1))
		self.assertEqual(-1, upo.evaluate([-1], 0))
		self.assertEqual( 2, upo.evaluate([0,1], 2))
		self.assertEqual( 4, upo.evaluate([0,0,1], 2))
		self.assertEqual( 9, upo.evaluate([1,2,1], 2))
	
	def test_add(self):
		self.assertEqual([], upo.add([], []))
		self.assertEqual([], upo.add([], [0]))
		self.assertEqual([5,7,3], upo.add([1,2,3], [4,5]))
		self.assertEqual([2], upo.add([1,1], [1,-1]))

	def test_subtract(self):
		self.assertEqual([], upo.subtract([], []))
		self.assertEqual([-1], upo.subtract([], [1]))
		self.assertEqual([-3,-3, 3], upo.subtract([1,2,3], [4,5]))
		self.assertEqual([ 3, 3,-3], upo.subtract([4,5], [1,2,3]))
		self.assertEqual([2], upo.subtract([1,1], [-1,1]))

	def test_multiply(self):
		self.assertEqual([], upo.multiply([], []))
		self.assertEqual([], upo.multiply([], [1]))
		self.assertEqual([6], upo.multiply([2], [3]))
		self.assertEqual([3,6], upo.multiply([1,2], [3]))
		self.assertEqual([3,6], upo.multiply([3], [1,2]))
		self.assertEqual([-1,0,1], upo.multiply([1,1], [-1,1])) # x^2 - 1 = (x + 1)*(x - 1)
		self.assertEqual([-1,0,0,1], upo.multiply([-1,1], [1,1,1])) # x^3 - 1 = (x - 1)*(x^2 + x + 1)
		self.assertEqual([-1,3,0,-3,-5,6], upo.multiply([1,-3,2], [-1,0,2,3])) # 6x^5 - 5x^4 - 3x^3 + 3x - 1 = (2x^2 - 3x + 1)*(3x^3 + 2x^2 - 1)


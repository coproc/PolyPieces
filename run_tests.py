#! /usr/bin/env python3.8
# -*- coding: utf-8 -*-
"""Run all tests below the containing directory and display the result.

The subdirectories will be searched for *test*.py files.

If an argument is given (e.g. "autorun"), the script terminates itself after
running tests.
"""

import os
import sys
import unittest

assert sys.version_info[:2] == (3, 8)


TEST_FILE_PATTERN = '*test*.py'


def discoverAndRunTests(path):
	"""Return all test results from the discovered tests.
	
	Start test discovery and runs all tests which are found in test classes.
	
	Args:
		path (str): Parameter for test discovery, which requires an
			absolute path.
	
	Returns:
		A test result summary object on all test runs.
	"""
	testSuite = unittest.defaultTestLoader.discover(path, TEST_FILE_PATTERN)
	testRunner = unittest.TextTestRunner(resultclass=unittest.TextTestResult, verbosity=0)
	result = testRunner.run(testSuite)
	return result


def printResult(result):
	print()
	print(result)
	if result.wasSuccessful():
		print()
		print("All tests successful!")


if __name__ == '__main__':
	thisDir = os.path.dirname(__file__)
	
	testResult = discoverAndRunTests(thisDir)
	printResult(testResult)
	
	# For automation, an arbitrary argument (e.g. "autorun") can be given to
	# quit without user interaction:
	if len(sys.argv) < 2:
		input("\nPress ENTER to exit.")
	
	if testResult.wasSuccessful():
		sys.exit(0)
	else:
		sys.exit(1)

#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run all unit tests and display the result.
The test folder and subdirectories will be searched for *test*.py files.

If an argument is given (e.g. "autorun"), the script terminates immediately after running tests.
"""

import os
import sys
import unittest

TEST_FILE_PATTERN = '*test*.py'


def discover_and_run_tests(rootPath):
	"""Return test summary of discovered tests.
	Start test discovery and run all tests found.
	
	args:
		rootPath (str): path to root of tests
	
	returns:
		test result summary object on all tests run.
	"""
	testSuite = unittest.defaultTestLoader.discover(rootPath, TEST_FILE_PATTERN)
	testRunner = unittest.TextTestRunner(resultclass=unittest.TextTestResult, verbosity=0)
	result = testRunner.run(testSuite)
	return result


if __name__ == '__main__':
	thisDir = os.path.dirname(__file__)
	testDir = os.path.join(thisDir, 'test')
	testResult = discover_and_run_tests(testDir)
	print('\n', testResult)
	
	# To keep an automatically opened shell window open, pressing 'ENTER' is required to terminate
	# the script if no arguments have been given. Any argument will quit without user interaction.
	if len(sys.argv) == 1:
		input("\nPress ENTER to exit.")

	sys.exit(0 if testResult.wasSuccessful() else 1)

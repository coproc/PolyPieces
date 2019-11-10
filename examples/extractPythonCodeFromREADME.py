import os, re

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
README_PATH = os.path.join(FILE_DIR, os.pardir, 'README.md')
README_CODE_PATH = os.path.join(FILE_DIR, 'README_commands.py')

CODE_INIT = '''
#------------ CODE INIT ------------
# make sure imports from ../src work
import os, sys
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(FILE_DIR, os.pardir, 'src'))
# simulate console output of expressions
_p_ = None
# print result of last expression
def _p():
	global _p_
	if _p_ is not None:
		print(_p_.__repr__())
		_p_ = None
#------------ CODE INIT ------------

'''

insideCode = False
codeType = None
linePrev = None


def _isExpression(line):
	STATEMENT_STARTS = ['def ', 'import ', 'from ', 'print(']
	line = line.strip()
	for start in STATEMENT_STARTS:
		if line.startswith(start): return False
	# assignment?
	if re.match(r'^[A-Za-z0-9_]+[ \t]*=.*', line): return False
	return len(line) > 0

	
with open(README_PATH) as fileIn:
	with open(README_CODE_PATH, 'w') as fileOut:
		fileOut.write(CODE_INIT)
		for line in fileIn:
			if line.startswith('```'):
				insideCode = not insideCode
				if insideCode:
					codeType = line[3:].strip()
				else:
					if linePrev and linePrev.startswith('>>> ') and _isExpression(linePrev[4:]):
						#print("linePrev='%s'" % linePrev)
						fileOut.write('_p()\n')
					codeType = None
					linePrev = None
				continue
			if insideCode and codeType == 'python':
				if line.startswith('>>> '):
					command = line[4:]
					if _isExpression(command):
						command = '_p_= ' + command
					fileOut.write(command)
				elif line.startswith('#'):
					fileOut.write(line)
				elif len(line.strip()) > 0 and linePrev and _isExpression(linePrev[4:]):
					fileOut.write('_p()\n')
				linePrev = line

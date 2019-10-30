import os

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
README_PATH = os.path.join(FILE_DIR, os.pardir, 'README.md')
README_CODE_PATH = os.path.join(FILE_DIR, 'README_commands.py')

insideCode = False
codeType = None
linePrev = None

with open(README_PATH) as fileIn:
	with open(README_CODE_PATH, 'w') as fileOut:
		fileOut.write('import sys\n')
		fileOut.write('sys.path.append("../src")\n')
		fileOut.write('_ = None\n')
		for line in fileIn:
			if line.startswith('```'):
				insideCode = not insideCode
				if insideCode:
					codeType = line[3:].strip()
				else:
					codeType = None
				continue
			if insideCode and codeType == 'python':
				if line.startswith('>>> '):
					command = line[4:]
					SPECIAL_STARTS = ['def ', 'import ', 'from ']
					for start in SPECIAL_STARTS:
						if command.strip().startswith(start):
							command += '_ = None\n'
							break
					else: command = '_ = ' + command
					fileOut.write(command)
				elif line.startswith('#'):
					fileOut.write(line)
				elif linePrev and not linePrev[4:].startswith('print(') and not ' = ' in linePrev:
					fileOut.write('if _ is not None: print(_.__repr__())\n')
				linePrev = line

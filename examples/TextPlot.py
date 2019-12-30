import os
import unicodedata


# dot characters in ascending heights
PLOT_DOTS = ('\N{COMBINING DOT BELOW}', '.', '\N{MIDDLE DOT}', '\N{COMBINING DOT ABOVE}')


# generate a string representing an ASCII plot
# @param f function to plot
# @param xRange interval of range over which to plot as iterable (xMin, xMax)
# @param yRange y-range for plot (default: range of f over given x-range)
# @param xRes resolution in x-direction in number of characters
# @param yRes resolution in y-direction in number of lines
# @param unicodeOutput if set to False, only the decimal point '.' will be used
# @param insertSpacesBeforeCombiningChars in windows terminals combining characters are printed separately by default,
#                                         on linux systems those characters are handled correctly, so a space must be
#                                         inserted before to avoid combining with the previous dot
#                                         default: None (choose value dependent on operating system)
# @return string with (yRes+1) lines, each (xRes+1) characters long
def plot(f, xRange, yRange=None, xRes=80, yRes=20, unicodeOutput=True, insertSpacesBeforeCombiningChars=None):
	if insertSpacesBeforeCombiningChars is None:
		insertSpacesBeforeCombiningChars = os.name != 'nt'
	dx = (xRange[1]-xRange[0])/xRes
	xVals = [xRange[0]+i*dx for i in range(xRes+1)]
	yVals = [f(x) for x in xVals]
	yMin,yMax = (min(yVals),max(yVals)) if yRange is None else yRange
	dy = (yMax-yMin)/(yRes-1)
	plotArea = [len(xVals)*' ' for _ in range(yRes+1)]
	for xIdx,y in enumerate(yVals):
		yScaled = (yMax-y)/dy+0.4
		yIdx = int(yScaled)
		line = plotArea[yIdx]
		dotChar = PLOT_DOTS[3-int(3.98*(yScaled-yIdx)+0.01)] if unicodeOutput else '.'
		plotArea[yIdx] = line[0:xIdx] + dotChar + line[xIdx+1:]
	plotString = '\n'.join(plotArea)
	if insertSpacesBeforeCombiningChars:
		for c in PLOT_DOTS:
			if unicodedata.category(c) == 'Mn':
				plotString = plotString.replace(c, '\u2000'+c) # insert 'en quad' space to make dot centered horizontally
	return plotString


# generate ascii plot (as string) for piecewise polynomial function.
# @param fpp piecewise polynomial function (type PolyPieceFunc)
# other parameters have same meaning as in function plot
def plotFpp(fpp, xRange=None, yRange=None, xRes=80, yRes=20, unicodeOutput=True):
	polyPieces = fpp.polyPieces
	if xRange is None: xRange = [polyPieces[0].interval[0],polyPieces[-1].interval[1]]
	return plot(lambda x: fpp.eval(x), xRange, yRange, xRes, yRes, unicodeOutput)

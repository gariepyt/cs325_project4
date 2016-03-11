# Nearing Neighbour Implementation of TSP
# Author: Tom Gariepy
# Last Updated: 3/7/2016
# Description: Nearest Neighbour implementation of TSP

#Imports
import math
import sys
import os # I don't think I need this
import time


def calcDistance(start, target):
	# x val
	x = abs(target[1] - start[1])

	# y val
	y = abs(target[2] - start[2])

	# triangle calc
	distance = round(math.sqrt((x**2) + (y**2)))

	#return result
	return distance



def minNext(start, unmarked, n):
	minDist = None
	minVal = None
	items = []

	# This is just to append distance where we are at so far into items, from start to n - 1
	for y in range(0, n):
		selectVal = unmarked[y]
		selectDist = calcDistance(start, selectVal)
		item = []
		item.append(selectVal[0])
		item.append(selectDist)
		items.append(item)

	# Does the actual calculation of and decision of what is minimum distance from n to end of graph
	for x in range(n, len(unmarked)):
		selectVal = unmarked[x]
		selectDist = calcDistance(start, selectVal)
		item = []
		item.append(selectVal[0])
		item.append(selectDist)
		items.append(item)

		if (minDist == None):
			minDist = selectDist
			minVal = selectVal
		# change here to decide if current min is still less than the calculated minimum
		elif(selectDist < minDist):
			minDist = selectDist
			minVal = selectVal

	return minDist, minVal, items



def calcMin(start, graph):
	path = []
	currentV = start
	distance = 0

	graphLength = len(graph)
	for n in range(0, len(graph)):
		nextD, nextV, items = minNext(currentV, graph, n)
		distance = distance + nextD
		path.append(nextV)
		currentV = graph[n]

	distance = distance + calcDistance(start, path[len(path) - 1])

	return distance, path, items



def calcPath(graph):
	minDist = None
	path = None
	curItems = []

	graphLength = len(graph)

	for x in range(0,len(graph)):
		resMin, resPath, items = calcMin(graph[x], graph)

		if (minDist == None):
			minDist = resMin
			path = resPath
			curItems = items
		elif (resMin < minDist):
			minDist = resMin
			path = resPath
			curItems = items

	# With the path decided, sort the array from least distance to greatest
	curItems = sorted(curItems, key= lambda x: (x[1]))

	return minDist, curItems


def main():
	totMinDist = 0
	curPath = []
	if (len(sys.argv) == 2):
		inName = sys.argv[1]
		outName = inName + ".tour"

		if (os.path.isfile(inName) == False):
			print("ERROR: " + inName + " not found.")
			return 1

		with open(outName, 'wt') as resultFile:

			with open(inName, 'rt') as inputFile:
				inData = inputFile.read().splitlines()

				for x in range(0, len(inData)):
					inData[x] = inData[x].split()

					inData[x][1] = int(inData[x][1])
					inData[x][2] = int(inData[x][2])

				# If length of in Data < 300, do normal nearest neighbor
				if(len(inData) < 300):
					tStart = time.time()
					totMinDist, curPath = calcPath(inData)
					tEnd = time.time()

				else:
					inData.sort(key= lambda a: (a[1]))
					start = 0
					stop = 300
					mInData = []
					sectionCount = (len(inData)/300)
					if ((len(inData)%300)!= 0):
						sectionCount += 1
					tStart = time.time()
					for y in range(0, sectionCount):
						#if (y == sectionCount - 1):
						#	stop = len(inData) - 1
						mInData = inData[start:stop]
						mInData.sort(key=lambda b: (b[2]))
						mStart = 0
						mStop = 50
						mSectionCount = (len(inData[start:stop])/50)
						if ((len(inData[start:stop])%50)!= 0):
							mSectionCount += 1
						for m in range(0, mSectionCount):
							#if (m == mSectionCount - 1):
							#	mStop = len(inData[start:stop]) - 1
							minDist, path = calcPath(mInData[mStart:mStop])
							totMinDist = totMinDist + minDist
							curPath.append(path)
							mStart = mStart + 50
							mStop = mStop + 50
						start = start + 300
						stop = stop + 300

					tEnd = time.time()

				runTime = tEnd - tStart

				totMinDist = int(totMinDist)

				print("Time elapsed: ", runTime)
				print("Minimal Distance: ", totMinDist)
				resultFile.write(str(totMinDist) + "\n")

				printLeng = len(curPath)

				if(len(inData) < 300):
					for n in range(0,len(curPath)):
						resultFile.write(str(curPath[n][0]) + "\n")
				else:
					for k in range(0,len(curPath)):
						for j in range(0, len(curPath[k])):
							resultFile.write(str(curPath[k][j][0]) + "\n")

		inputFile.close()
		resultFile.close()
	else:
		print("ERROR: Not enough variables!")

main()
# print("Running some code!")
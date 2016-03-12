# Nearing Neighbour Implementation of TSP
# Author: Tom Gariepy
# Last Updated: 3/7/2016
# Description: Nearest Neighbour implementation of TSP

# Note to self: still fails when dealing with larger number of cities

#Imports
import math
import sys
import os # I don't think I need this
import time

divMark = 85

def calcDistance(start, target):
	# x val
	x = abs(target[1] - start[1])

	# y val
	y = abs(target[2] - start[2])

	# triangle calc
	distance = round(math.sqrt((x**2) + (y**2)))

	#return result
	return int(distance)

def minNext(start, unmarked):
	minDist = 0
	minVal = None

	endPoint = len(unmarked)
	# if (endPoint > 300):
		# endPoint = 300

	interval = int(endPoint / divMark) + 1

	# print "endPoint: " + str(endPoint) + " graph: " + str(len(unmarked))

	for x in range(0, endPoint, interval):
		selectVal = list(unmarked[x])
		selectDist = calcDistance(start, selectVal)
		# print "Checking: " + str(selectVal)
		# print "   x: " + str(x)

		if (minDist == 0):
			minDist = selectDist
			minVal = list(selectVal)
		elif(selectDist < minDist):
			minDist = selectDist
			minVal = list(selectVal)

	return minDist, minVal

def calcMin(start, graph):
	unmarked = list(graph)
	unmarked.remove(start)

	path = [start]
	currentV = start
	distance = 0

	while (len(unmarked) > 0):
		nextD, nextV = minNext(currentV, unmarked)

		distance = distance + nextD

		path.append(nextV)
		# print "Selected:(" + str(len(unmarked)) + ") " + str(nextV)
		unmarked.remove(nextV)

		currentV = nextV

	distance = distance + calcDistance(start, path[len(path) - 1])

	return distance, path

def calcPath(graph, sTime):
	# nextG = list(graph)
	# nextS = nextG[0]

	minDist = None
	path = None

	endPoint = len(graph)
	
	interval = int(endPoint / divMark) + 1

	for x in range(0,endPoint, interval):
		resMin, resPath = calcMin(graph[x], graph)
		# graph = resPath
		
		if (minDist == None):
			minDist = resMin
			path = list(resPath)
		elif (resMin < minDist):
			minDist = resMin
			path = list(resPath)

		# cEnd = time.time()
		# cTime = cEnd - sTime
		# print "Interval: " + str(x) 
		# print "Result min: " +str(resMin)
		# print "Current min: " + str(minDist)
		# print "Current Start: " + str(path[0])
		# print "Current time: " + str(cTime)

		# nextG = list(resPath)
		# nextS = resPath[len(nextG)/2]

	return minDist, path

def main():
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
					inData[x].append(calcDistance(['start', 0, 0], inData[x]))

				inData = sorted(inData, key=lambda line: line[3])

				if (len(inData) < 450):
					divMark = 5000

				inData = sorted(inData, key=lambda line: line[1])

				tStart = time.time()
				minDist, path = calcPath(inData, tStart)
				tEnd = time.time()

				runTime = tEnd - tStart

				minDist = int(minDist)

				print "Time elapsed: " + str(runTime) 
				print "Minimal Distance: " + str(minDist)

				resultFile.write(str(minDist) + "\n")

				for x in range(0,len(path)):
					resultFile.write(str(path[x][0]) + "\n")

		inputFile.close()
		resultFile.close()
	else:
		print("ERROR: Not enough variables!")

main()
# print("Running some code!")

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

	for x in range(n, len(unmarked)):
		selectVal = unmarked[x]
		selectDist = calcDistance(start, selectVal)

		if (minDist == None):
			minDist = selectDist
			minVal = selectVal
		elif(minVal < minDist):
			minDist = selectDist
			minVal = selectVal

	return minDist, minVal

def calcMin(start, graph):
	#unmarked = graph
	#unmarked.remove(start)
	path = []

	#path = [start]
	#path.append(start)
	currentV = start
	distance = 0

	#while (len(unmarked) > 0):
		#nextD, nextV = minNext(currentV, unmarked)
	#while (len(graph) > 0):
	for n in range(0, len(graph)):
		nextD, nextV = minNext(currentV, graph, n)

		distance = distance + nextD
		
		path.append(nextV)
		#unmarked.remove(nextV)

		currentV = graph[n]

	distance = distance + calcDistance(start, path[len(path) - 1])

	return distance, path

def calcPath(graph):
	minDist = None
	path = None

	for x in range(0,len(graph)):
		resMin, resPath = calcMin(graph[x], graph)
		#graph = resPath
		
		if (minDist == None):
			minDist = resMin
			path = resPath
		elif (resMin < minDist):
			minDist = resMin
			path = resPath

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

				tStart = time.time()
				minDist, path = calcPath(inData)
				tEnd = time.time()

				runTime = tEnd - tStart

				minDist = int(minDist)

				print("Time elapsed: ", runTime)
				print("Minimal Distance: ", minDist)

				resultFile.write(str(minDist) + "\n")

				for x in range(0,len(path)):
					resultFile.write(str(path[x][0]) + "\n")

		inputFile.close()
		resultFile.close()
	else:
		print("ERROR: Not enough variables!")

main()
# print("Running some code!")
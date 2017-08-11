"""
Written by Michelle Sit

Used to analyze different combinations of unique license plate characters
Program can analyze 3 minibus taxi lines or across all the lines

"""

def analyzeRoutesClusterOnSingleLine(inputRoute):

	routePlates = []
	for x in range(len(allRouteVals)):
		for busNum in inputRoute:
			if allRouteVals[x] == str(busNum):
				routePlates.append(allFullPlates[x])

	# print "All Route License Plates: ", routePlates
	print "Number of License Plates: ", len(routePlates)

	print "========================================================="

	uniqueID = set([plate for plate in routePlates 
					if routePlates.count(plate) >= 1])

	print "Unique License Plates: ", uniqueID
	print "Number of unique plates: ", len(uniqueID)

	print "========================================================="

	shortened_Plate = [short[-4:] for short in uniqueID]
	print "Option 1 last 4 digits: ", shortened_Plate

	# shortened_Plate = [short[-3:] for short in uniqueID]
	# print "Option 2 last 3 digits: ", shortened_Plate

	# shortened_Plate = [short[2:6] for short in uniqueID]
	# print "Option 3 Middle 4 digits: ", shortened_Plate

	# shortened_Plate = [short[2:5] for short in uniqueID]
	# print "Option 4 Middle 3 digits: ", shortened_Plate

	# shortened_Plate = [short[:6] for short in uniqueID]
	# print "Option 5 First 6 digits: ", shortened_Plate

	# shortened_Plate = [short[:5] for short in uniqueID]
	# print "Option 6 First 5 digits: ", shortened_Plate

	print "Num of unique plates: ", len(shortened_Plate)
	print "----------"

	for each in shortened_Plate:
		if shortened_Plate.count(each) > 1:
			print "Number of shortID overlap: ", shortened_Plate.count(each)
			print "ShortID value: ", each
			print "----------"
			shortened_Plate.remove(each)

	# print "-------------------------"

def analyzeRoutesClusterAcrossAllLines():

	print "Length of all plates: ", len(allFullPlates)

	allPlatesCrop = [short[-4:] for short in allFullPlates]
	print "Option 1 last 4 digits: "

	# allPlatesCrop = [short[-3:] for short in allFullPlates]
	# print "Option 2 last 3 digits: "

	# allPlatesCrop = [short[2:6] for short in allFullPlates]
	# print "Option 3 Middle 4 digits: "

	# allPlatesCrop = [short[2:5] for short in allFullPlates]
	# print "Option 4 Middle 3 digits: "

	# allPlatesCrop = [short[:6] for short in allFullPlates]
	# print "Option 5 First 6 digits: "

	# allPlatesCrop = [short[:5] for short in allFullPlates]
	# print "Option 6 First 5 digits: "

	# allPlatesCrop = allFullPlates
	# print "All plates: "

	uniquePlateMatchRoute = dict()
	for x in range(len(allPlatesCrop)):
		try:
			if int(allRouteVals[x]) in K2CP:
				route = "K2CP"
			elif allRouteVals[x] in MP2W:
				route = "MP2W"
			elif int(allRouteVals[x]) in MP2CP:
				route = "MP2CP"
		except:
			route = "MP2W"

		if allPlatesCrop[x] not in uniquePlateMatchRoute:
			uniquePlateMatchRoute[allPlatesCrop[x]] = [route]
		elif allPlatesCrop[x] in uniquePlateMatchRoute:
			uniquePlateMatchRoute[allPlatesCrop[x]].append(route)

	print uniquePlateMatchRoute.keys()
	print "uniquePlateMatchRoute len: ", len(uniquePlateMatchRoute)

	print "=============================================="

	print "Plates on multiple routes"

	multiplePlatesCount = 0
	for plate in uniquePlateMatchRoute:
		if (len(uniquePlateMatchRoute[plate]) > 1) & (len(set(uniquePlateMatchRoute[plate]))>1):
			print  str(plate) + " : " + str(uniquePlateMatchRoute[plate])
			multiplePlatesCount += 1
	print "Number of plates with the same code across all lines: ", multiplePlatesCount


if __name__ == '__main__':
	file = open("plates.txt", 'rw')
	allFullPlates = []
	allRouteVals = []

	for line in file:
		parse = line.rstrip()
		parts = parse.split()

		allRouteVals.append(parts[0])
		allFullPlates.append(parts[1])
	file.close()

	K2CP = [607]
	MP2CP = [99, 116, 117, 118, 119, 258, 259, 260, 261, 452]
	MP2W = ["8", "234", "F81", "F82"]

	# print "LINE: Khayelitsha to Cape Town"
	# print "LINE: Mitchells Plain to Cape Town"
	# print "LINE: Mitchells Plain to Wynberg"

	# analyzeRoutesClusterOnSingleLine(MP2W)

	print "All lines"
	analyzeRoutesClusterAcrossAllLines()

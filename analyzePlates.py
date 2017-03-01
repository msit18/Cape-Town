file = open("plates.txt", 'rw')
massiveArray = []
massiveBus = []

for line in file:
	parse = line.rstrip()
	parts = parse.split()
	# currentVal = parts[1][len(parts[1])-7:]
	currentVal = parts[1]
	massiveBus.append(parts[0])
	massiveArray.append(currentVal)
# print massiveArray
# print massiveBus

def analyzeRoutesCluster():
	K2CP = [607]
	MP2CP = [99, 116, 117, 118, 119, 258, 259, 260, 261, 452]
	MP2W = ["8", "234", "F81", "F82"]

	maBin = []
	routeLen = 0
	for x in range(len(massiveBus)):
		for busNum in MP2CP:
			if massiveBus[x] == str(busNum):
				routeLen += 1
				maBin.append(massiveArray[x])
	# print "LINE: Khayelitsha to Cape Town"
	# print "LINE: Mitchells Plain to Wynberg"
	print "LINE: Mitchells Plain to Cape Town"
	print "All License Plates: ", maBin
	print "Number of License Plates: ", len(maBin)

	ID = 0
	for each in range(len(maBin)):
		count = maBin.count(maBin[each])
		if count > 1:
			# print "SAME: ", maBin.count(maBin[each])
			# print "SAME EACH: ", each
			# print "SAME VAL: ", maBin[each]
			ID += 1
		else:
			ID += 1
	# print "ID = ", ID

	uniqueID = [maBin[0]]

	print "========================================================="

	# for each in range(len(maBin)):
	# 	for allVals in range(len(uniqueID)):
	# 		if maBin[each] == uniqueID[allVals]:
	# 			continue
	# 		elif allVals == len(uniqueID):
	# 			print "len(uniqueID) old: ", len(uniqueID)
	# 			print "allVals: ", allVals
	# 			uniqueID.append(maBin[each])

	each = 0
	allVals = 0
	while each < len(maBin):
		allVals = 0
		while allVals < len(uniqueID):
			# print "EACH: ", each
			# print "ALL: ", allVals
			# print "each: ", maBin[each]
			# print "allVals: ", uniqueID[allVals]
			# # print "len(maBin): ", len(maBin)
			# # if int(each) != int(allVals):
			if (maBin[each] == uniqueID[allVals]):
					# print "each: ", maBin[each]
					# print "allVals: ", uniqueID[allVals]
					# print "MATCH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
					break
			elif int(allVals) == (len(uniqueID)-1):
				# print "this is the end!"
				# print "also each: ", each
				# print "allVals: ", allVals
				if (maBin[each] == uniqueID[allVals]):
					break
				else:
					uniqueID.append(maBin[each])
					# print "uniqueID: ", uniqueID
				# if maBin[each] == maBin[allVals]:
				# 	print "TF: ", (maBin[each] != maBin[allVals])
				# 	print "THE SAME"
				# 	print "each: ", maBin[each]
				# 	print "allVals: ", maBin[allVals]
				# if str(maBin[each]) == str(maBin[allVals]):
				# 	print "EACH: ", each
				# 	print "each val: ", maBin[each]
				# 	print "ALL: ", allVals
				# 	print "all val: ", maBin[allVals]
				# 	maBin.remove(maBin[allVals])
					# print "new LEN: ", len(maBin)
			allVals += 1
		# print "NEXT EACH VALUE ==================="
		each += 1

	# print "routeNum: ", str(busNum)
	# print "routeLen: ", routeLen
	print "Unique License Plates: ", uniqueID
	print "Number of unique plates: ", len(uniqueID)

	shortBin = []
	for short in range(len(uniqueID)):
		# shortBin.append(uniqueID[short][len(parts[1])-3:])
		shortBin.append(uniqueID[short][2:5])
		# shortBin.append(uniqueID[short])

	print "========================================================="

	print "4 Digits after first two letters: ", shortBin

	print "----------"

	for each in range(len(shortBin)):
		count = shortBin.count(shortBin[each])
		if count > 1:
			print "Number of shortID overlap: ", shortBin.count(shortBin[each])
			# print "SAME EACH: ", each
			print "ShortID value: ", shortBin[each]
			print "----------"

analyzeRoutesCluster()


def analyzeAllRoutesIndividually():
	route = massiveBus[0]
	routeLen = 0
	maBin = []
	print "route: ", route
	for x in range(len(massiveBus)):
		if route == massiveBus[x]:
			routeLen += 1
			maBin.append(massiveArray[x])
		else:
			print "routeLen: ", routeLen
			routeLen = 1
			print "BIN: ", maBin
			for each in range(len(maBin)):
				count = maBin.count(maBin[each])
				if count > 1:
					print "SAME: ", maBin.count(maBin[each])
					print "SAME EACH: ", each
					print "SAME VAL: ", maBin[each]

			maBin = [massiveArray[x]]
			print "_______________________________"
			route = massiveBus[x]
			print "route: ", route

# print "routeLen: ", routeLen
# routeLen = 1
# print "BIN: ", maBin
# for each in range(len(maBin)):
# 	count = maBin.count(maBin[each])
# 	if count > 1:
# 		print "SAME: ", maBin.count(maBin[each])
# 		print "SAME EACH: ", each
# 		print "SAME VAL: ", maBin[each]

# numCopies = 0
# for val in range(len(massiveArray)):
# 	# print "counts: ", massiveArray.count(val)
# 	if massiveArray.count(massiveArray[val]) > 1:
# 		numCopies+=1
# 		# print "SAME"
# print "Copies: ", numCopies


file.close()
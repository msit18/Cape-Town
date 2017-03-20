from __future__ import division
from cloudant.client import Cloudant
from cloudant.result import Result, ResultByKey
from time import gmtime, strftime

#remove thank you for your responses if rate sent
#check need to use "people" tag in testSample
#check need to use so many tags (people, bus)

class Server:
	def __init__(self):
		cloudantUsername = "citivan"
		cloudantPassword = "CityVan1"
		serviceURL = "https://citivan.cloudant.com"
		client = Cloudant(cloudantUsername, cloudantPassword, url=serviceURL,\
						connect=True, auto_renew=True)

class CitivanSMS:
	def __init__(self, callerID, client):
		self.callerID = str(callerID)
		self.client = client

		self.database = client['citivan']
		self.json = self.getDataFile("testSample2")
		self.busJson = self.getDataFile("busData")
		# self.callerHashInfo = self.json["people"][self.callerID]
		print "END OF INITIALIZED-----"

	def getDataFile(self, dataFile):
		end_point = "{0}/citivan/{1}/".format(serviceURL, dataFile)
		params = {'include_docs': 'true'}
		response = self.client.r_session.get(end_point, params=params)
		jsonFile = response.json()
		return jsonFile

	def calculateAverage(self, inputBusName, questionNum, decimalPlace):
		print "CalculateAverage method"
		avg = float()
		if decimalPlace == "percent":
			avg = (self.busJson[str(inputBusName)][str(questionNum)])/ \
					(self.busJson[str(inputBusName)][str(questionNum+5)])*100
		elif decimalPlace == "fiveScale":
			avg = (self.busJson[str(inputBusName)][str(questionNum)])/ \
					(self.busJson[str(inputBusName)][str(questionNum+5)])
		print "avg: ", avg
		return round(avg, 1)

	def rateBus(self, rateBusName, currentConvoNum):
		print "RateBus method"
		print "rateBusName Type: ", type(rateBusName)
		print "rateBusName:", rateBusName
		if rateBusName in self.busJson == False:
			print "BUS HAS NOT BEEN RATED YET"
			return "The bus {0} has not been rated yet. @@{1}".format(rateBusName, questions[currentConvoNum-1])
		elif self.busJson[rateBusName]["12"] == 0:
			print "12 value is 0. Surveyors have not finished survey."
			return "The bus {0} has not been rated yet. @@{1}".format(rateBusName, questions[currentConvoNum-1])
		else:
			try:
				#if currentConvoNum-1 >6 don't send thank you msg
				print "BUS RATING IS THE FOLLOWING"
				question2Answer = self.calculateAverage(rateBusName, 2, "fiveScale")
				question3Answer = self.calculateAverage(rateBusName, 3, "fiveScale")
				question4Answer = self.calculateAverage(rateBusName, 4, "percent")
				question5Answer = self.calculateAverage(rateBusName, 5, "percent")
				question6Answer = self.calculateAverage(rateBusName, 6, "percent")
				overrideReturnValue = "Minibus {0}: {1} ratings\n"\
									"Avg ride quality {2}/5\n"\
									"Avg comfort {3}/5\n"\
									"{4}% think the driver drives safely\n"\
									"{5}% think the driver is courteous\n"\
									"{6}% feel safe\n"\
									"@@{7}".\
				format(rateBusName, self.busJson[rateBusName]["12"], question2Answer,\
				question3Answer, question4Answer, question5Answer, question6Answer,\
				questions[currentConvoNum-1])
				return overrideReturnValue
			except:
				print "There was an error in bus data"
				return "The bus {0} has not been rated yet.\n{1}".format(rateBusName, questions[currentConvoNum-1])

	#check the userText format is okay
	def getBusName(self, userText, surveyNum):
		print "getBusName Method"
		busName = self.json["people"][self.callerID][str(surveyNum)]["1"]
		print "BUSNAME VALUE: ", busName
		if busName == 0:
			print "BUS NAME IS NOT ENTERED"
			busName = userText
			print str(busName) not in self.busJson
			if (str(busName) not in self.busJson) & (str(userText) != "rate"):
				print "CREATING NEW BUS DATA"
				# print "BEFORE: ", self.busJson
				self.busJson[str(busName)] = {"1":"{0}".format(userText), "2":0, "3":0, "4":0, "5":0, "6":0,
										"7":0, "8":0, "9":0, "10":0, "11":0, "12":0}
				# print "AFTER : ", self.busJson
		return busName

	def inputDataToCloudant(self, currentConvoNum, callerID, userText, surveyNum):
		print "InputDataToCloudant method"
		print "CurrentConvoNum for Input: ", currentConvoNum
		_busName = self.getBusName(userText, surveyNum)
		print "userText: ", userText
		print isinstance(userText, int)
		try:
			intUserText = int(userText)
		except:
			intUserText = 0
		print "intUserText: ", intUserText
		strCurrentConvoNum = str(currentConvoNum)
		if currentConvoNum == 1:
			print "FIRST QUESTION. PUTTING BUS NAME INTO THE SYSTEM"
			self.json["people"][self.callerID][str(surveyNum)][strCurrentConvoNum] = userText
			self.busJson[_busName][str(currentConvoNum+6)] += 1
			self.json["people"][self.callerID]["convoNum"] += 1
			self.json["people"][self.callerID][str(surveyNum)]["LastSubmitTime"] = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
		elif (2<=currentConvoNum<=3) & (1<=intUserText<=5):
			print  "QUESTION TWO OR QUESTION 3. PUTTING IN INFO"
			self.json["people"][self.callerID][str(surveyNum)][strCurrentConvoNum] = intUserText
			self.busJson[_busName][strCurrentConvoNum] += intUserText
			self.busJson[_busName][str(currentConvoNum+6)] += 1
			self.json["people"][self.callerID]["convoNum"] += 1
			self.json["people"][self.callerID][str(surveyNum)]["LastSubmitTime"] = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
		elif (currentConvoNum > 3) & ((userText == "yes") | (userText == "no") | (1<=intUserText<=2)):
			print "QUESTIONS FOUR THROUGH SIX. PUTTING IN INFO"
			if (userText == "yes")  | (intUserText == 1):
				self.json["people"][self.callerID][str(surveyNum)][strCurrentConvoNum] = "yes"
				self.busJson[_busName][strCurrentConvoNum] += 1
			elif (userText == "no") | (intUserText == 2):
				self.json["people"][callerID][str(surveyNum)][strCurrentConvoNum] = "no"
				#Does not add to busJson question number if the answer is no
			self.busJson[_busName][str(currentConvoNum+6)] += 1
			self.json["people"][self.callerID]["convoNum"] += 1
			self.json["people"][self.callerID][str(surveyNum)]["LastSubmitTime"] = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
		else:
			pass


	###MAIN METHOD
	def runNew(self, userText):
		#Connects to database server in initialized
		print "RUNNEW Method"
		print "callerID from runnew: ", self.callerID
		print "input text: ", userText
		overrideReturnValue = ""
		print "self.json: ", self.json
		userTextSplit = userText.split()
		try:
			###DOES USER EXIST? If so, then all the other functions are allowed.
      		#If this is a new user, disregard the input text and just create a new profile
			if self.callerID in self.json["people"]:
				print "VERIFY USER EXISTS: USER ALREADY EXISTS"
				print "self.jsonPeopleCallerIDConvoNum", self.json["people"][self.callerID]["convoNum"]
				newUser = False
				callerHashInfo = self.json["people"][self.callerID]

				#Creates new survey hash if last is full
				if (callerHashInfo["convoNum"]>6) & (userTextSplit[0] != "rate"):
					print "CREATING NEW SURVEY HASH. LAST SURVEY IS FULL"
					self.json["people"][self.callerID]["convoNum"] = 1
					self.json["people"][self.callerID][len(callerHashInfo)] = {"LastSubmitTime":0, "1":0, "2":0, "3":0, "4":0, "5":0, "6":0}
					# putText = {"LastSubmitTime":0, "1":0, "2":0, "3":0, "4":0, "5":0, "6":0}
				else:
					print "NOT CREATING NEW SURVEY HASH"
					currentConvoNum = callerHashInfo["convoNum"]
					print "NUM ITEMS IN CALLERID: ", str(len(callerHashInfo))
					surveyNum = len(callerHashInfo)-1 #Note: convoNum item is removed from length
					overrideReturnValue = ""

					###RATE CMD
					if userTextSplit[0] == "rate":
						print "running rate function"
						overrideReturnValue = self.rateBus(userTextSplit[1], currentConvoNum)

					###INPUT TEXT INTO SURVEY
					else:
						print "ELSE STATEMENT"
						self.inputDataToCloudant(currentConvoNum, self.callerID, userText, surveyNum)

			###NEW USER. Create new account. Disregarded input text.
			else:
				print "VERIFY USER EXISTS: CREATE NEW PROFILE"
				newCaller = {"1": {"LastSubmitTime":0, "1":0, "2":0, "3":0, "4":0, "5":0, "6":0}, "convoNum":1}
				self.json["people"][self.callerID] = newCaller
				newUser = True

				if userTextSplit[0] == "rate":
					print "Running rate function"
					overrideReturnValue = self.rateBus(userTextSplit[1], 1) #verify that this 1 value works

		finally:
			print "OverrideReturnValue :", overrideReturnValue
			print "OverrideTrueTest: ", overrideReturnValue == ""
			###Note: store information into user databases
			if overrideReturnValue == "":
				print "overrideReturnValue is null"
				print "self.jsonPeopleCallerIDConvoNum", self.json["people"][self.callerID]["convoNum"]
				returnValue = self.json["people"][self.callerID]["convoNum"]
				jsonFormat = self.json
				print "self.json: ", self.json
				end_point = "{0}/citivan/{1}/".format(serviceURL, "testSample2")
				r = client.r_session.put(end_point, json=jsonFormat)
				print "ENDPT {0}\n".format(r.json())

				if newUser == False:
					print "newUser is False"
					busJsonFormat = self.busJson
					end_point_bus = "{0}/citivan/{1}/".format(serviceURL, "busData")
					r_bus = client.r_session.put(end_point_bus, json=busJsonFormat)
					print "BUS: {0}\n".format(r_bus.json())
			else:
				returnValue = overrideReturnValue
			
			print "RETURNVALUE :", returnValue

		return returnValue

if __name__ == '__main__':
	# s = Server()

	questions = ["What are the last four digits of the minibus license plate? (Example: for CA34578, enter 4578).", 
				"Pick a number from 1 to 5 to rate the quality of your ride. 1) Very poor. 2) Poor. 3) Average. 4) Good. 5) Excellent.",
				"Rate from 1 to 5, how comfortable you are in the vehicle? 1) Very Uncomfortable 2) Uncomfortable 3) Average 4) Good 5) Very Comfortable",
				"Does the driver drive safely? Enter 1 for yes or 2 for no.",
				"Was your driver courteous? Enter 1 for yes or 2 for no.", 
				"Do you feel safe in this vehicle? Enter 1 for yes or 2 for no.", 
				"Thank you for your responses! Have a great day."]

	cloudantUsername = "citivan"
	cloudantPassword = "CityVan1"
	serviceURL = "https://citivan.cloudant.com"
	client = Cloudant(cloudantUsername, cloudantPassword, url=serviceURL,\
					connect=True, auto_renew=True)

	caller = 123456
	text = raw_input("What is your message? ")
	c = CitivanSMS(caller, client)
	status = c.runNew(text.lower())
	print "STATUS TYPE: ", type(status)
	print isinstance(status, int)
	print "\n\nCELLPHONE TEXT: "
	if status <= 1:
		print "Welcome to CitiVan! Please answer the following questions. To see the ratings of a van, send \"rate VanNumber\" \n"
		print questions[0]
	elif isinstance(status, int)==False:
		splitMsg = status.split("@@")
		print splitMsg[0]
		print "\nsplit here \n"
		print splitMsg[1]
	else:
		print questions[status-1]
	print "END OF CELLPHONE TEXT"
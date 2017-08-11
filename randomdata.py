"""

Written by Michelle Sit

Used to generate the fake data points for the early Flocktracker visualizations.
The headers are based off of the Flocktracker questionnaire. To see the file,
please refer to the Cape Town dropbox folder.

"""

import random
import datetime

route = [random.randrange(1, 3) for y in range(500)]
passengers = [random.randrange(1, 11) for y in range(500)]
gender = [random.randrange(1, 3) for y in range(500)]
safeVehicle = [random.randrange(1, 6) for y in range(500)]
comfort = [random.randrange(1, 6) for y in range(500)]
clean = [random.randrange(1, 3) for y in range(500)]
driverDrive = [random.randrange(1, 3) for y in range(500)]
driverRespect = [random.randrange(1, 6) for y in range(500)]
modeTransport = [random.randrange(1, 8) for y in range(500)]
tripPurpose = [random.randrange(1, 6) for y in range(500)]
waitVehicle = [random.randrange(1, 4) for y in range(500)]
age = [random.randrange(1, 8) for y in range(500)]
waitTime = [random.randrange(1, 31) for y in range(500)]

######################################
#time
ranDate = [random.randrange(1, 8) for y in range(500)]
ranHour = [random.randrange(6, 24) for y in range(500)]
ranMin = [random.randrange(0, 60) for y in range(500)]

time = []
for x in range(500):
	timex = "09/{0}/17 {1}:{2}".format(ranDate[x], ranHour[x], ranMin[x])
	time.append(timex)

######################################

for s in range (500):
	row = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\t{12}\t{13}\t{14}"\
		.format(s, route[s], passengers[s], gender[s], safeVehicle[s], comfort[s], \
		clean[s], driverDrive[s], driverRespect[s], modeTransport[s], tripPurpose[s], waitVehicle[s], age[s], time[s], waitTime[s])
	print row
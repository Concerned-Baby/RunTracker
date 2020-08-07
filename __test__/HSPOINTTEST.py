

def getPointsHSEvent(event, time):

	EQUALCONSTANT = 150
	#time = self.getPREvent(event)
	if event == "100m": 
		THRES = 11.59
		pr = time
		if pr < THRES:
			return 5.1 * pow((THRES - time + 7.2) / 1.1, 1.8)
		elif (pr > THRES):
			return 3 * pow((THRES - time + 14) / 1.1, 1.4) + 44
		return EQUALCONSTANT
	return -1

#rewrite with a new function
#graph on desmos

values = [23, 23.5, 23.7, 23.79, 23.8, 23.81, 23.9, 25, 27, 30, 32]
for value in values:
	print(getPointsHSEvent("200m", value))
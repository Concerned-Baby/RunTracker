

def getPointsHSEvent(event, time):

	EQUALCONSTANT = 150
	#time = self.getPREvent(event)
	if event == "100m":
		THRES = 11.59
		pr = time
		if pr < THRES:
			return pow((THRES - pr + 3) / 1.1, 2) * 20.25
		elif (pr > THRES):
			return pow((10 - pr + THRES) / 1.1, 2) * 1.8
		return EQUALCONSTANT
	elif event == "200m":
		THRES = 23.8
		pr = time
		if pr < THRES:
			return pow((THRES - pr + 3.3) / 1.2, 2) * 19.82
		elif (pr > THRES):
			return pow((11 - pr + THRES) / 1.2, 2) * 1.78
		return EQUALCONSTANT
	return -1


values = [23, 23.5, 23.7, 23.79, 23.8, 23.81, 23.9, 25, 27, 30, 32]
for value in values:
	print(getPointsHSEvent("200m", value))
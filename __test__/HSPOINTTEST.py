import math
"""
def getPointsHSEvent(event, time):

	EQUALCONSTANT = 150
	#time = self.getPREvent(event)
	score = -1
	if event == "100m": 
		THRES = 11.59
		pr = time
		if pr < THRES:
			score = 5.1 * pow((THRES - time + 7.2) / 1.1, 1.8)
		elif (pr > THRES):
			score =  3 * pow((THRES - time + 14) / 1.1, 1.4) + 44
		else:
			score = EQUALCONSTANT
	if event == "200m": 
		THRES = 23.8
		pr = time
		if pr < THRES:
			score = (5.1 / 0.9) * pow((THRES - time + 7.2) / 1.2, 1.8) + 7.441
		elif (pr > THRES):
			score = (3 / 0.9)* pow((THRES - time + 14) / 1.2, 1.4) + 46.1
		else:
			score = EQUALCONSTANT
	if event == "400m": 
		THRES = 53.75
		pr = time
		if pr < THRES:
			score =  (5.1 / 5) * pow((THRES - time + 7.2) / 0.9, 1.8) + 106.932
		elif (pr > THRES):
			score =  (3 / 5)* pow((THRES - time + 14) / 0.9, 1.4) + 122.023
		else:
			score = EQUALCONSTANT
	try:
		score = float(score)
	except TypeError:
		score = float(str(score)[1:9]) - math.sqrt(float(str(score)[str(score).index("-") + 1: -2]))

	string = str(score)[0:8]
	score = float(string)


	return score

#rewrite with a new function
#graph on desmos

values100 = [11.3, 11.5, 11.58, 11.59, 11.6, 11.7, 12, 12.6, 13, 15, 18]
values200 = [23, 23.5, 23.7, 23.79, 23.8, 23.81, 23.9, 25, 27, 30, 32]
values400 = [50, 52, 53, 53.5, 53.74, 53.75, 53.76, 53.8, 55, 60, 70, 80]
for value in values400:
	print(getPointsHSEvent("400m", value))
"""

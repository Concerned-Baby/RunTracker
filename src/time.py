class myTime(object):
	def __init__(self, _seconds):
		self.seconds = _seconds
	def toString(self):
		if self.seconds < 60:
			return "%d" % self.seconds
		return "%d:%d" % (self.seconds / 60, self.seconds % 60)
	def compareTo(self, fles):
		if self.seconds > fles.getSeconds():
			return 1
		elif self.seconds < fles.getSeconds():
			return -1
		return 0
	def getSeconds(self):
		return self.seconds
class frameStack(object):

	def __init__ (self):
		self.stack = []

	def push (self, frame):
		self.stack.append(frame)
		return frame

	def pop (self):
		if (not self.isEmpty()):
			return self.stack.pop()
		else:
			return null

	def getTop(self):
		return self.stack[len(self.stack) - 1]

	def isEmpty(self):
		return (len(self.stack) == 0)

	def toString(self):
		text = ""
		for frame in self.stack:
			text += frame.toString() + " - "
		return text

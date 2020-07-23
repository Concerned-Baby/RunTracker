class frameStack(object):

	def __init__ (self):
		self.stack = []

	def push (frame):
		self.stack.append(frame)

	def pop (self):
		if (not self.isEmpty()):
			return self.stack.pop()
		else:
			return null

	def isEmpty(self):
		return (len(self.stack) == 0)
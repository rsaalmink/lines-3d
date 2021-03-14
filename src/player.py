class Player:
	def __init__(self, uid, color):
		self.uid = uid
		self.color = color

	def __repr__(self):
		return "Player {} with color {}".format(self.uid, self.color)
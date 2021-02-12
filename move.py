class Move:
	def __init__(self, coords, specialMove=False, thirdParty=False):
		self.coords = coords
		self.specialMove = specialMove
		self.thirdParty = thirdParty